import streamlit as st
import os
from blogit import generate_blog_content, analyze_podcast, validate_blog, extract_transcript_details
import asyncio

# Set page configuration
st.set_page_config(
    page_title="Podcast to Blog Post",
    page_icon="🎙️",
    layout="wide",
)

st.title("BlogGen")
st.markdown("Convert your podcast to a blog post")

# Input options
input_option = st.radio(
    "Choose input type:",
    ["Upload Transcript File", "YouTube Link"]
)

podcast_text = None

if input_option == "Upload Transcript File":
    # File upload
    uploaded_file = st.file_uploader("Upload your podcast file", type=["txt"])
    if uploaded_file:
        podcast_text = uploaded_file.getvalue().decode("utf-8")
else:
    # YouTube link input
    youtube_link = st.text_input("Enter YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)")
    if youtube_link:
        try:
            with st.spinner("Extracting transcript from YouTube..."):
                podcast_text = extract_transcript_details(youtube_link)
            st.success("Transcript extracted successfully!")
        except Exception as e:
            st.error(f"Error extracting transcript: {str(e)}")

col1, col2 = st.columns(2)

with col1:
    generate_button = st.button("Generate Blog Post", disabled=podcast_text is None)

with col2:
    output_format = st.selectbox(
        "Output format",
        ["Markdown", "HTML"]
    )

if podcast_text and generate_button:
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
