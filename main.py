import streamlit as st
import json
import pandas as pd
from bs4 import BeautifulSoup
import prompting
from PIL import Image
import streamlit.components.v1 as components

im = Image.open("./assets/images/RS-square-logo.jpeg")

st.set_page_config(
    layout="wide", page_title="RiskSpotlight - Process RCSA", page_icon=im
)

hide_streamlit_style = """
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                .embeddedAppMetaInfoBar_container__DxxL1 {visibility: hidden;}
                # img {position: absolute; top: 0; left: 0;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Process RCSA - Risk Identification")

col1, col2 = st.columns(2)

with col1:
    process = st.text_area("Please provide process details.", value="", height=200)
    clicked = st.button("Submit")

with col2:
    num_risks = st.number_input(
        "No. of risks", min_value=3, max_value=10
    )
    risk_category = st.multiselect(
        "Risk Categories",
        ["Business Process Execution Failures", 
        "Damage to Tangible and Intangible Assets",
        "Employment Practices and Workplace Safety",
        "External Theft & Fraud",
        "Improper Business Practices",
        "Internal Theft & Fraud",
        "Regulatory & Compliance",
        "Technology Failures & Damages",
        "Vendor Failures & Damages"],
    )

if clicked:
    if not process or not num_risks or not risk_category:
        st.warning("Please fill in all the information.")

    else:
        with st.spinner("Please wait..."):
            response = prompting.generate_risks(process, num_risks, risk_category)

            risks_output = response["choices"][0]["message"]["content"]
            # print(response)

            # Parse the JSON response
            data = json.loads(risks_output)
            # st.write(risks)
            # st.write(data)

            # Iterate through the extracted data
            risks = data["Risks"]

            risk_information_output = []

            for risk in risks:
                risk_title = risk["Risk Title"]
                risk_category_name = risk["Risk Category"]

                final_response = prompting.generate_risk_information(risk_title, risk_category_name)

                risk_info = final_response["choices"][0]["message"]["content"]
                risk_data = json.loads(risk_info)
                risk_information_output.append(risk_data)

            risk_info_data = {
                "Risk Information": risk_information_output
            }

            risk_row = risk_info_data["Risk Information"]

            table_rows = ""

            for item in risk_row:
                # Extract fields from the risk iteration
                risk_title = item["Risk Title"]
                description = item["Description"]
                # causes = ", ".join(item["Causes"])
                # financial_impacts = ", ".join(item["Financial Impacts"])
                # non_financial_impacts = ", ".join(item["Non-Financial Impacts"])
                banking_example = item["Banking Example"]
                risk_category = item["Risk Category"]

                causes = ""
                for cause in item["Causes"]:
                    causes += f"""<li>{cause}</li>"""
                
                financial_impacts = ""
                for financial_impact in item["Financial Impacts"]:
                    financial_impacts += f"""<li>{financial_impact}</li>"""

                non_financial_impacts = ""
                for non_financial_impact in item["Non-Financial Impacts"]:
                    non_financial_impacts += f"""<li>{non_financial_impact}</li>"""
                
                # Create an HTML table row for the current risk iteration
                table_row = f"""<tr><td>{risk_category}</td><td>{risk_title}</td><td>{description}</td><td><ul>{causes}</ul></td><td><ul>{financial_impacts}</ul></td><td><ul>{non_financial_impacts}</ul></td><td>{banking_example}</td></tr>"""

                # Append the current table row to the table_rows string
                table_rows += table_row

            # Complete HTML table with headers and table rows
            html_before = """
            <table>
                <thead>
                    <tr style="background-color: #000; color: #fff; text-align: center;">
                        <th>Risk Category</th>
                        <th>Risk Title</th>
                        <th>Description</th>
                        <th>Causes</th>
                        <th>Financial Impacts</th>
                        <th>Non-Financial Impacts</th>
                        <th>Banking Example</th>
                    </tr>
                </thead>
                <tbody>
            """

            html_after = """  
                </tbody>
            </table>
            """
            # print(table_rows)
            final_html = html_before + table_rows + html_after
            # print(final_html)
            # Display the HTML table
            st.write(final_html, unsafe_allow_html=True)