import streamlit as st
import os
from blogit import generate_blog_content, analyze_podcast, validate_blog
import asyncio

# Set page configuration
st.set_page_config(
    page_title="Podcast to Blog Post",
    page_icon="🎙️",
    layout="wide",
)

st.title("BlogGen")
st.markdown("Convert your podcast to a blog post")

# Create API key input
api_key = st.sidebar.text_input(
    "Gemini API Key",
    type="password",
    help="Enter your Gemini API key",
)

if api_key:
    os.environ["GEMINI_API_KEY"] = api_key

# File upload
uploaded_file = st.file_uploader("Upload your podcast file", type=["txt"])

col1,col2 = st.columns(2)

with col1:
    generate_button = st.button("Generate Blog Post")

with col2:
    output_format = st.selectbox(
        "Output format",
        ["Markdown", "HTML"]
    
    )

if uploaded_file and generate_button:
    podcast_text = uploaded_file.getvalue().decode("utf-8")
    st.write("Analyzing podcast transcript...")
    sections = analyze_podcast(podcast_text)
    if sections:
        st.write("Generating blog content...")
        blog_content = asyncio.run(generate_blog_content(podcast_text, sections))
        st.write("Validating blog content...")
        improved_blog = validate_blog(blog_content, podcast_text)
        if output_format == "Markdown":
            st.markdown(improved_blog, unsafe_allow_html=True)
        else:
            st.write(improved_blog)
    else:
        st.write("Error analyzing podcast transcript")
