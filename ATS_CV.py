import streamlit as st
import google.generativeai as genai
import os
import json
import PyPDF2 as pdf
import pandas as pd
from dotenv import load_dotenv

load_dotenv()  # Load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return str(response.text)

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
Act as a highly skilled and experienced Applicant Tracking System (ATS) with profound knowledge 
in the technology field, including IT Support, IT Project Management, Continuous Improvement, data science, data analysis, 
and big data engineering. Your task is to evaluate the resume against the provided job description. 
Given the highly competitive job market, provide the best possible assistance for enhancing the resume. 
Assign the percentage Matching based on Jd and Matching based on Jd and the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

## Streamlit Application
st.markdown("""
    <div style='background-color: #6CD2E9; padding: 20px; border-radius: 20px;border-style: solid; border-color: darkcyan; border-width: 4px;'>
        <h1 style='font-weight: bold; font-size: 30px; font-color: white; font-family: Verdana; text-align: center;'>Screen your CV</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="container" style='border: 4px solid #198F96; padding: 20px; border-radius: 10px;'>
    <div class='markdown-text-container'>
        <br>
        <p><b>Improve Your CV get higher ATS (Applicant Tracking System) ratings.</b></p>
        <p>Recruiters increasingly rely on Applicant Tracking 
        Systems (ATS) to evaluate and score applicants, enabling them to efficiently narrow the pool to a more 
        manageable group.</p>
        <p>Thus, it's crucial to incorporate the right keywords in your CV that align with the job 
        description. This strategic approach significantly enhances your chances of standing out in the competitive job market.</p>
    </div>
</div> 
""", unsafe_allow_html=True)

jd = st.text_area("Paste the Job Description for the job you are applying for", height=200)
uploaded_file = st.file_uploader("Upload Your CV here", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        prompt = input_prompt.format(text=text, jd=jd)
        response = get_gemini_response(prompt)

        response_dict = json.loads(response)

        # Convert the dictionary to a DataFrame
        df = pd.DataFrame([response_dict])

        # Display DataFrame
        st.table(df)


        
