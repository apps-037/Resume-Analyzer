from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

from datetime import datetime

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert", page_icon="📄", layout="wide") 

st.markdown("""
    <h1 style='text-align: center; color: orange;'>📄 ATS Resume Expert</h1>
    <p style='text-align: center;'>An AI-powered assistant to analyze and improve your resume based on job descriptions.</p>
""", unsafe_allow_html=True)

input_text = st.text_area("📝 Paste the Job Description:", key="input")
uploaded_file = st.file_uploader("📎 Upload your Resume (PDF format)...", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ PDF Uploaded Successfully")

col1, col2, col3 = st.columns(3)

with col1:
    submit1 = st.button("🧠 Resume Evaluation")

with col2:
    submit2 = st.button("✨ Generate Summary")

with col3:
    submit3 = st.button("📊 Percentage Match + Skill Gap Analysis")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a professional resume writer. Based on the given resume, write 3 compelling and concise professional summaries,
each suitable for a LinkedIn "About Me" section. Separate each summary clearly.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
Your task is to evaluate the resume against the provided job description.

1. Give the match percentage.
2. List any missing keywords or skills.
3. Provide final thoughts on alignment.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("📋 Evaluation Result:")
        st.write(response)
    else:
        st.warning("⚠️ Please upload your resume.")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("💡 LinkedIn Summary:")
        st.write(response)
    else:
        st.warning("⚠️ Please upload your resume.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("📊 Match Analysis Report:")
        st.write(response)
    else:
        st.warning("⚠️ Please upload your resume.")
