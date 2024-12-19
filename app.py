import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
        border-radius: 10px;
    }
    .stTitle {
        color: #2E4057;
        font-size: 3rem !important;
        padding-bottom: 2rem;
        text-align: center;
    }
    .stSubheader {
        color: #048BA8;
        padding-top: 1rem;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #048BA8;
    }
    .stFileUploader {
        padding: 2rem 0;
    }
    .stButton>button {
        background-color: #048BA8;
        color: white;
        padding: 0.5rem 2rem;
        border-radius: 50px;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .results-container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
        box-shadow: 0 0 15px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    .keyword-chip {
        background-color: #f0f7ff;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.2rem;
        display: inline-block;
        color: #048BA8;
        border: 1px solid #048BA8;
    }
    .match-percentage {
        font-size: 3.5rem;
        color: #048BA8;
        text-align: center;
        font-weight: bold;
        margin: 0;
        padding: 0;
    }
    .match-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        border: 2px solid #048BA8;
    }
    .section-title {
        color: #2E4057;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #048BA8;
    }
    .profile-summary {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        color: #2E4057;
        line-height: 1.6;
    }
    .missing-keywords-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)


def get_gemini_repsonse(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

# App Layout
st.title("Smart Resume Scanner")
st.markdown("#### Optimize your resume for ATS with AI-powered analysis")

# Create two columns
col1, col2 = st.columns(2)

with col1:
    jd = st.text_area("Job Description", height=200,
                      placeholder="Paste the job description here...")

with col2:
    uploaded_file = st.file_uploader("Upload Resume (PDF)",
                                     type="pdf",
                                     help="Please upload your resume in PDF format")

# Center the analyze button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    submit = st.button("Analyze Resume 🔍")

if submit:
    if uploaded_file is not None and jd.strip() != "":
        with st.spinner('Analyzing your resume...'):
            text = input_pdf_text(uploaded_file)
            response = get_gemini_repsonse(input_prompt.format(text=text, jd=jd))
            response_dict = json.loads(response)

            # Results Container
            st.markdown("<div class='results-container'>", unsafe_allow_html=True)

            # Match Percentage with Container
            st.markdown("""
                <div class='match-container'>
                    <p class='match-percentage'>{}</p>
                    <p style='color: #2E4057; font-size: 1.2rem;'>Match Rate</p>
                </div>
            """.format(response_dict['JD Match']), unsafe_allow_html=True)

            # Missing Keywords
            st.markdown("<div class='section-title'>Missing Keywords</div>", unsafe_allow_html=True)
            st.markdown("<div class='missing-keywords-section'>", unsafe_allow_html=True)
            if response_dict['MissingKeywords']:
                for keyword in response_dict['MissingKeywords']:
                    st.markdown(f"<span class='keyword-chip'>{keyword}</span>",
                                unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: #2E4057;'>No missing keywords found!</p>",
                            unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Profile Summary
            st.markdown("<div class='section-title'>Profile Summary</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='profile-summary'>{response_dict['Profile Summary']}</div>",
                        unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    elif uploaded_file is None:
        st.error("Please upload your resume!")
    else:
        st.error("Please provide a job description!")

# Footer
st.markdown("""
<div style='text-align: center; padding: 2rem;'>
    <p style='color: #666;'>Made with Love for dev ❤️ </p>
</div>
""", unsafe_allow_html=True)