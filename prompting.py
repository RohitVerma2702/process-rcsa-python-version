import os
import openai
import toml
import streamlit as st

openai.api_key = st.secrets["openai_api_key"]

def generate_risks(process, num_risks, risk_category):
    # Define your JSON format separately
    json_format = '''
    {
        "Risks": [
            {
                "Risk Title": "Title of Risk 1",
                "Risk Category": "Category of Risk 1"
            },
            {
                "Risk Title": "Title of Risk 2",
                "Risk Category": "Category of Risk 2"
            },
            {
                "Risk Title": "Title of Risk 3",
                "Risk Category": "Category of Risk 3"
            },
            {
                "Risk Title": "Title of Risk 4",
                "Risk Category": "Category of Risk 4"
            },
            {
                "Risk Title": "Title of Risk 5",
                "Risk Category": "Category of Risk 5"
            },
            {
                "Risk Title": "Title of Risk 6",
                "Risk Category": "Category of Risk 6"
            }
        ]
    }
    '''

    # Use the JSON format variable in your risk_titles string
    risk_titles = f"""As an Operational Risk expert, please provide "{num_risks}" risks associated with the process of "{process}". Categorize these risks into the following categories: "{risk_category}".
    Please use the below instructions to provide the output: 
    - Risk Title should at least have 8-12 words and provide a detailed understanding of the main event that may occur and it refers to a specific risk
    - Avoid mentioning risk in generic way such as "Geopolitical Risks", "Vendor Dependency"
    - Every title should have a verb which should highlight the main event that could occur
    - Use the words and terms from the Process context in the Risk Title where possible
    - Make sure to NOT use Financial Risks, I do not need any financial risk titles.

    Present the information in the following JSON format:
    {json_format}

    Ensure that each risk title contains 8 to 15 words and always includes a word associated with a threat or negative event. Take your time to consider and provide an appropriate response, and include only the risk titles and categories in your answer."""


    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": risk_titles}],
        temperature=0.6,
        max_tokens=7500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response

def generate_risk_information(risk_title, risk_category_name):

    json_format2 = '''
    {
        "Risk Title": "Title of the Risk from above.",
        "Description": "Provide a detailed description between 30 to 75 words. Description should contain details of how the risk can occur.",
        "Causes": ["List the key causes as bullet points."],
        "Financial Impacts": ["List the key financial impacts as bullet points."],
        "Non-Financial Impacts": ["List the key non-financial impacts as bullet points."],
        "Banking Example": "Provide 1 example of how this risk can occur in a bank.",
        "Risk Category": "Should be one or more from the values provided above."
    }
    '''

    text = f"""
    Imagine you are an Operational Risk expert.
    Generate risk information for the following risk title and risk category:
    Risk Title: {risk_title}
    Risk Category: {risk_category_name}

    Please generate this information in the following json format.

    {json_format2}

    Please take your time to generate the information and make sure to only provide the json format output with no additional information.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}],
        temperature=0.6,
        max_tokens=7500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response