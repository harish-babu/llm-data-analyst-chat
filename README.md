
# LLM Based Data Analyst Chatbot
We are building a data analyst chat bot that can analyze data using an LLM.  Data is loaded from a csv file to a Pandas dataframe.  The user enters requests as natural language questions / statements and the LLM is able to perform calculations and provide the output.

## Table of Contents
* [Getting Started](#getting-started)
* [Technologies Used](#technologies-used)
* [Conclusions](#conclusions)
* [Acknowledgements](#acknowledgements)

<!-- You can include any other section that is pertinent to your problem -->

## Getting Started
### 1. Install Packages
Package requirements are provided in the `requirements.txt` file.  Open a terminal and change directory to the location where the code is checked out from git.  Install packages with the `pip install` command

	pip3 install -r requirements.txt

### 2. Setup OpenAI Key
Get an OpenAI key from your account.  If you don't have a key, you can create one from [your OpenAI account page](https://platform.openai.com/api-keys).
Once you have the key, there are a few ways in which you can use it.  Choose the variant that suits you.
#### 2.1 Using the environment file
Create an `.env` file inside the `src` directory.  Inside that file, place the following line.  Replace <YOUR_KEY> with your API key.

	OPENAI_API_KEY = "<YOUR_KEY>"

#### 2.2 Exporting the key through the command line
Alternatively, you could export you key on the command line using:

	export OPENAI_API_KEY=<YOUR_KEY>
Don't forget to replace <YOUR_KEY> with the actual key.

### 3. Running the chatbot
To run the chat bot use the following command

	streamlit run src/data_analyst_chat.py
This should open a browser window and show the main screen.



## Conclusions
- Conclusion 1 from the analysis
- Conclusion 2 from the analysis
- Conclusion 3 from the analysis
- Conclusion 4 from the analysis

<!-- You don't have to answer all the questions - just the ones relevant to your project. -->


## Technologies Used
- library - version 1.0
- library - version 2.0
- library - version 3.0

<!-- As the libraries versions keep on changing, it is recommended to mention the version of library used in this project -->

## Acknowledgements
Give credit here.
- This project was inspired by...
- References if any...
- This project was based on [this tutorial](https://www.example.com).


## Contact
Created by [@githubusername] - feel free to contact me!


<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->