import os
import re
from openai import OpenAI as openai

import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.schema.output_parser import OutputParserException
from langchain.callbacks import StreamlitCallbackHandler


if os.environ.get('OPENAI_API_KEY') is not None:
    openai.api_key = os.environ['OPENAI_API_KEY']
else:
    _ = load_dotenv(find_dotenv())  # read local .env file
    openai.api_key = os.environ['OPENAI_API_KEY']


def chat_api(
    messages, model="gpt-4o", temperature=0.0, max_tokens=4096, top_p=0.5
):
    """
    The chat API endpoint of the ChatGPT

    Args:
        messages (str): The input messages to the chat API
        model (str): The model, i.e. the LLM
        temperature (float): The temperature parameter
        max_tokens (int): Max number of tokens parameters
        top_p (float): Top P parameter

    Returns:
        str: The LLM response
    """
    plot_flag = False

    if any(keyword in st.session_state.messages[-1]["content"].lower() for keyword in ["plot", "graph", "draw", "chart"]):
        plot_flag = True
        code_prompt = """
                    Generate the code <code> for plotting the previous data in plotly, in the format requested. The solution should be given using plotly and only plotly. Do NOT use matplotlib.  Usage of matplotlib, matplotlib.pyplot are forbidden. Return the code <code> in the following format ```python <code>```
                    """        
        messages.append({
            "role": "assistant",
            "content": code_prompt
        })

    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )

    if plot_flag:
        code = extract_python_code(
            response["choices"][0]["message"]["content"])
        if code is None:
            st.warning(
                "Couldn't find data to plot in the chat. "
                "Check if the number of tokens is too low for the data at hand. "
                "I.e. if the generated code is cut off, this might be the case.",
                icon="🚨"
            )
        else:
            code = code.replace("fig.show()", "")
            code += """st.plotly_chart(fig, theme='streamlit', use_container_width=True)"""  # noqa: E501
            st.write(f"```{code}")
            exec(code)

    return response["choices"][0]["message"]


def extract_python_code(text):
    pattern = r'```python\s(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    if not matches:
        return None
    else:
        return matches[0]


def chat_with_data_api(df, model="gpt-4o", temperature=0.0, max_tokens=4096, top_p=0.5):
    """
    A function that answers data questions from a dataframe.
    """

    client = openai()
    if any(keyword in st.session_state.messages[-1]["content"].lower() for keyword in ["plot", "graph", "draw", "chart"]):
        code_prompt = """
                    Generate the code <code> for plotting the previous data in plotly, in the format requested. The solution should be given using plotly and only plotly. Do NOT use matplotlib.  Usage of matplotlib, matplotlib.pyplot are forbidden. Return the code <code> in the following format ```python <code>```
                    """     
        # Do not add the above code_prompt to the session state.  It affects the future code generation steps also.  Hence avoid adding it.   
        step_prompts = st.session_state.messages.copy()
        step_prompts.append({
            "role": "assistant",
            "content": code_prompt
        })
        response = client.chat.completions.create(
            model=model,
            messages=step_prompts,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        code = extract_python_code(response.choices[0].message.content)
        with st.chat_message('assistant'):
            if code is None:
                st.warning(
                    "Couldn't find data to plot in the chat. "
                    "Check if the number of tokens is too low for the data at hand. "
                    "I.e. if the generated code is cut off, this might be the case.",
                    icon="🚨"
                )
                return "Couldn't plot the data"
            else:
                code = code.replace("fig.show()", "")
                code += """st.plotly_chart(fig, theme='streamlit', use_container_width=True)"""  # noqa: E501
                st.write(f"```{code}")
                exec(code)
                return "Complete."
                # return response.choices[0].message.content
    else:
        llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )

        pandas_df_agent = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=True,
            return_intermediate_steps=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            handle_parsing_errors=False,
            allow_dangerous_code=True,
        )

        print(st.session_state.messages)
        try:
            stCBHandler = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            with st.chat_message('assistant'):
                answer = pandas_df_agent(st.session_state.messages, callbacks=[stCBHandler])
                if answer["intermediate_steps"]:
                    action = answer["intermediate_steps"][-1][0].tool_input["query"]
                    with st.status("Executed the code."):
                        st.write(f"```{action}```")
                st.write(answer['output'])
                return answer["output"]
        except OutputParserException:
            error_msg = """OutputParserException error occured in LangChain agent.
                Refine your query."""
            return error_msg
        except:  # noqa: E722
            error_msg = "Unknown error occured in LangChain agent. Refine your query"
            return error_msg
