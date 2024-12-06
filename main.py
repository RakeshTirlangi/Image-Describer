import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
from dotenv import load_dotenv
import os
import base64
import time

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

def compress_and_encode_image(image_bytes, max_size=(800, 800)):
    img = Image.open(io.BytesIO(image_bytes))
    img.thumbnail(max_size, Image.LANCZOS)
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def describe_image(encoded_image, prompt):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        response = model.generate_content([{
            "mime_type": "image/jpeg",
            "data": encoded_image
        }, prompt])
        return response.text.strip()
    except Exception as e:
        st.error(f"Error describing image: {e}")
        return None

def animated_text(text):
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(f'<p style="color: #333333; font-size: 16px; text-align: center; font-weight: 300;">{full_text}</p>', unsafe_allow_html=True)
        time.sleep(0.05)
    return placeholder

def main():
    st.set_page_config(
        page_title="Image Describer AI", 
        page_icon="🖼️",  
        layout="centered"
    )
    
    st.markdown(""" 
    <style>
    .stApp {
        background: linear-gradient(135deg, #e0eafc 0%, #f5f9fc 100%);
        font-family: 'Inter', sans-serif;
    }
    header, footer {
        display: none !important;
    }
    .main-container {
        background: #ffffff;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1), 0 6px 10px rgba(0,0,0,0.05);
        padding: 30px;
        max-width: 600px;
        margin: 20px auto;
        transition: all 0.3s ease;
    }
    .title {
        background: linear-gradient(45deg, #4f8bf9, #2152e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-bottom: 15px;
        font-size: 2.5em;
    }
    .stFileUploader {
        background: #f5f8fa;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stFileUploader:hover {
        background: #e5e9ee;
        transform: scale(1.02);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .description-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1), 0 3px 8px rgba(0,0,0,0.05);
    }
    .stMarkdown, .stText {
        color: #333333;
        font-weight: 400;
    }
    .stImage {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    .stFileUploader label, .stFileUploader > div > div > label {
        color: #333333 !important;
    }
    .stImage label {
        color: #333333 !important;
    }
    /* Adjust styling for visibility */
    .stFileUploader {
        color: #333333 !important;
    }
    .stFileUploader > div > div > label {
        font-size: 16px;
        font-weight: 600;
        color: #333333 !important;
    }
    .stMarkdown, .stText {
        color: #333333;
        font-weight: 400;
    }
    .stSpinner {
        color: #333333;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="title">Image Describer</h1>', unsafe_allow_html=True)
    animated_text("Unveil the stories in your images")
    
    uploaded_file = st.file_uploader(
        "Upload Image", 
        type=['jpg', 'jpeg', 'png'],
        help="Upload an image for an AI-powered description"
    )
    
    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        encoded_image = compress_and_encode_image(image_bytes)
        st.image(image_bytes, caption="Uploaded Image", width=400)
        prompt = "Describe the contents of this image in a detailed and engaging manner."
        with st.spinner('AI is analyzing the image...'):
            description_result = describe_image(encoded_image, prompt)
        if description_result:
            st.markdown(f'<div class="description-container"><p style="color: #333333; font-size: 18px; line-height: 1.6;">{description_result}</p></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
