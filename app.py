import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()  ## load all our environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)


# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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

## streamlit app
st.title("Resume Scanner")
st.text("Check Resume ATS Match")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please uplaod the pdf")

submit = st.button("Analyze Resume")

# if submit:
#     if uploaded_file is not None:
#         text=input_pdf_text(uploaded_file)
#         response=get_gemini_repsonse(input_prompt)
#         st.subheader(response)
if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_repsonse(input_prompt.format(text=text, jd=jd))

        # Parse the JSON response
        response_dict = json.loads(response)

        # Display JD Match
        st.subheader(f"JD Match: {response_dict['JD Match']}")

        # Display Missing Keywords
        missing_keywords = response_dict['MissingKeywords']
        if missing_keywords:
            st.subheader("Missing Keywords:")
            st.write(missing_keywords)
        else:
            st.subheader("No Missing Keywords")

        # Display Profile Summary
        st.subheader("Profile Summary:")
        st.write(response_dict['Profile Summary'])

import streamlit as st

# # streamlit app
# st.title("Job Seekers")
#
# # Load an image from a file
# image_path = "img.png"
# image = st.image(image_path, caption="Job Seekers", width=300)
#
# # streamlit app
# st.title("Developer")

# # Load an image from a file
# image_path = "img1.png"
# image = st.image(image_path, caption="Danish Ammar", width=100)

# Alternatively, you can use an image URL
# image_url = "https://example.com/your-image.jpg"
# image = st.image(image_url, caption="Your Image Caption", use_column_width=True)

