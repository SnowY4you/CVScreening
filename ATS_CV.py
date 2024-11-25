import streamlit as st
import google.generativeai as genai
import os
import json
import PyPDF2 as pdf
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API key using st.secrets 
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

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
Act as a highly skilled and advanced Applicant Tracking System (ATS) with deep expertise in IT Support, IT Project Management, 
Continuous Improvement, IT Specialist roles, Process and Performance Improvement, Data Science, Data Analysis, and Service Desk Manager. 
Your task is to meticulously evaluate the resume against the provided job description in the current highly competitive job market. 
Provide the best possible assistance for enhancing the resume.  
Assign the percentage Matching based on JD and Matching based on JD and the missing keywords with high accuracy. Highlight and explain why 
this candidate is the best fit for the job, detailing their experience, skills, education, knowledge, or certifications.  
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

## Streamlit Application
st.markdown("""
    <div style='background-color: #6CD2E9; padding: 20px; border-radius: 20px; border-style: solid; border-color: darkcyan; border-width: 4px; width: 80%; margin: 0 auto;'>
        <h1 style='font-weight: bold; font-size: 30px; color: white; font-family: Verdana; text-align: center;'>Screen your CV</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="container" style='border: 4px solid #198F96; padding: 20px; border-radius: 10px; width: 100%; margin: 0 auto;'>
    <div class='markdown-text-container'>
        <br>
        <h4 style="text-align: center">Improve Your CV get higher ATS (Applicant Tracking System) ratings.</h4>
        <p><b>Nowadays, most companies, including 98.4% of Fortune 500 firms, use an applicant tracking system (ATS) to streamline their hiring process.
        If you’re unfamiliar with ATS, you’re not alone. Many job seekers don’t realize that their resume might be filtered out by an algorithm before a human ever sees it, even if they’re perfectly qualified for the job.</b></p>
        <p>In this guide, I'll explain what an ATS is, how it works, and how you can craft an ATS-friendly resume to boost your chances of landing more job interviews.</p>
        <p>For job seekers, the key thing to understand about ATS is that it allows employers to sift through resumes based on specific keywords. The most relevant resumes are then forwarded to hiring managers for a closer look.</p>
        <p>This is why it’s essential to tailor each resume with relevant keywords and to use a format that's ATS-friendly. Doing so increases the likelihood that your application will pass the initial screening and get into the hands of a hiring manager, potentially leading to an interview.</p>
        <b>How It Works</b>
        <p>Hiring managers use keywords to search for suitable candidates within the ATS database. Keywords can be single words or phrases, often related to job titles or skills.</p>
        <p>For instance, if a hiring manager is looking for an IT Specialist with experience in Citrix, they might enter "citrix" into the ATS search bar. 
        Hiring managers can also use combinations of terms. For example, “citrix” might be paired with “Netscaler” and “Azure Virtual Desktop”. 
        Resumes that include all the specified keywords will appear in the search results. Those that don’t contain all the keywords will remain hidden in the ATS database.</p>
        <p>To optimize your job search, tailor each resume to specifically target the job you’re applying for.</p>
        <p>While it takes more time and effort than sending out a generic resume, tailoring your resume will significantly increase your chances of getting more job interviews. That’s why I developed my own ATS system to check for keywords and ensure my resume is spot on.</p>
        <p>In this mini version of a ATS, paste in the job description you want to apply for (no limit character size), upload your CV in PDF form and Submit. It will show you a % of matching keywords, missing keywords and a profile summary why you would be fitting for the job.</p>
    </div>
</div> 
""", unsafe_allow_html=True)

# Define the text area for job description
jd = st.text_area("Paste the Job Description for the job you are applying for", height=400)

st.markdown("""
<style>
     .stTextArea textarea { 
        border-style: solid; 
        border-color: darkcyan; 
        border-width: 4px; 
        padding: 10px; 
        border-radius: 5px; 
        box-shadow: 2px 2px 2px lightgray; }
    .stFileUploader button {
        border: 2px solid #198F96;
        color: white;
        background-color: #6CD2E9;
    }
    div.stButton > button {
        border: 2px solid #198F96;
        color: white;
        background-color: #6CD2E9;
    }
</style>
""", unsafe_allow_html=True)

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

st.markdown("""
<div class="container"style='text-align: left; border: 4px solid #198F96; background-color: #3CA9AD; padding: 20px; border-radius: 10px; width: 100%; margin: 0 auto;'>
    <div class='markdown-text-container'>
        <br>
        <h4 style="text-align: center">Tips to create an ATS friendly resume</h4>
    <ul>
        <li><b>Clear Language:</b> Ensure your resume is written in straightforward, easy-to-understand language.</li>
        <li><b>Standard Headers:</b> Use conventional section headers like "Work Experience" and "Education" instead of creative ones like "My Professional Journey."</li>
        <li><b>Readable Fonts:</b> Opt for a common font like Arial, Helvetica, or Times New Roman.</li>
        <li><b>Proper Margins:</b> Keep one-inch margins on all sides to avoid overcrowding your resume.</li>
        <li><b>Simple Design:</b> Avoid fancy graphics or design elements that might confuse the ATS.</li>
        <li><b>No Special Characters:</b> Refrain from using special characters or symbols.</li>
        <li><b>Correct File Format:</b> Submit your resume in the preferred formats, usually .doc, .docx, or PDF.</li>
        <li><b>ATS Templates:</b> Consider using a resume builder or ATS-compatible templates to ensure readability.</li>
    </ul>
    </div>
</div> 

<div style='text-align: center; margin-top: 20px;'>
    <p><b>Thank you for using our service! @<a href="https://www.svanbuggenumanalytics.com">SnowY4you</a></b></p>
</div>
""", unsafe_allow_html=True)
