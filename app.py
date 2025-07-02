import streamlit as st
import os
from blogit import generate_blog_content, analyze_podcast, validate_blog, extract_transcript_details, modify_section_content
import asyncio
import re

# Set page configuration
st.set_page_config(
    page_title="Podcast to Blog Post",
    page_icon="🎙️",
    layout="wide",
)

# Custom CSS for better styling
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
    font-weight: bold;
}
.section-content {
    background-color: #f8f9fa;
    border-left: 4px solid #007bff;
    padding: 15px;
    margin: 10px 0;
    border-radius: 5px;
}
.publish-area {
    background-color: #e8f5e8;
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #28a745;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'blog_sections' not in st.session_state:
    st.session_state.blog_sections = []
if 'original_transcript' not in st.session_state:
    st.session_state.original_transcript = ""
if 'sections_metadata' not in st.session_state:
    st.session_state.sections_metadata = []
if 'generation_stage' not in st.session_state:
    st.session_state.generation_stage = 'input'  # input, generated, editing
if 'final_blog_content' not in st.session_state:
    st.session_state.final_blog_content = ""

st.title("BlogGen 📝")
st.markdown("Convert your podcast to a blog post with iterative editing")

def extract_sections_from_content(blog_content_list):
    """Extract individual sections from the generated blog content"""
    sections = []
    for i, content in enumerate(blog_content_list):
        # Extract title from the first line (assuming it starts with #)
        lines = content.strip().split('\n')
        title = lines[0].replace('#', '').strip() if lines else f"Section {i+1}"
        sections.append({
            'index': i,
            'title': title,
            'content': content
        })
    return sections

def combine_sections(sections):
    """Combine all sections into a single blog post"""
    return '\n\n'.join([section['content'] for section in sections])

# Stage 1: Input
if st.session_state.generation_stage == 'input':
    st.markdown("### 🎙️ Upload Your Podcast Content")
    
    # Input options
    input_option = st.radio(
        "Choose input type:",
        ["📁 Upload Transcript File", "🌐 YouTube Link"],
        horizontal=True
    )

    podcast_text = None

    if input_option == "📁 Upload Transcript File":
        # File upload
        uploaded_file = st.file_uploader(
            "Upload your podcast transcript file", 
            type=["txt"], 
            help="Upload a .txt file containing your podcast transcript"
        )
        if uploaded_file:
            podcast_text = uploaded_file.getvalue().decode("utf-8")
            st.success(f"✅ File uploaded successfully! ({len(podcast_text)} characters)")
    else:
        # YouTube link input
        youtube_link = st.text_input(
            "Enter YouTube video URL", 
            placeholder="https://www.youtube.com/watch?v=VIDEO_ID",
            help="Enter a valid YouTube URL to extract the transcript automatically"
        )
        if youtube_link:
            try:
                with st.spinner("🔄 Extracting transcript from YouTube..."):
                    podcast_text = extract_transcript_details(youtube_link)
                st.success(f"✅ Transcript extracted successfully! ({len(podcast_text)} characters)")
            except Exception as e:
                st.error(f"❌ Error extracting transcript: {str(e)}")

    if podcast_text:
        st.markdown("### 📊 Preview")
        with st.expander("View transcript preview"):
            st.text_area("Transcript content:", podcast_text[:500] + "..." if len(podcast_text) > 500 else podcast_text, height=150, disabled=True)

    col1, col2 = st.columns(2)

    with col1:
        generate_button = st.button(
            "🚀 Generate Blog Post", 
            disabled=podcast_text is None,
            type="primary",
            use_container_width=True
        )

    with col2:
        output_format = st.selectbox(
            "Output format",
            ["Markdown", "HTML"],
            help="Choose the format for your blog post"
        )

    if podcast_text and generate_button:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔍 Analyzing podcast transcript...")
        progress_bar.progress(25)
        sections = analyze_podcast(podcast_text)
        
        if sections:
            status_text.text("✍️ Generating blog content...")
            progress_bar.progress(50)
            blog_content = asyncio.run(generate_blog_content(podcast_text, sections))
            
            status_text.text("🔍 Validating and improving blog content...")
            progress_bar.progress(75)
            improved_blog = validate_blog(blog_content, podcast_text)
            
            status_text.text("✅ Blog post generated successfully!")
            progress_bar.progress(100)
            
            # Store in session state
            st.session_state.original_transcript = podcast_text
            st.session_state.blog_sections = extract_sections_from_content(blog_content)
            st.session_state.sections_metadata = sections
            st.session_state.final_blog_content = improved_blog
            st.session_state.generation_stage = 'generated'
            
            st.success("🎉 Your blog post is ready!")
            st.rerun()
        else:
            st.error("❌ Error analyzing podcast transcript")

# Stage 2: Generated blog with editing options
elif st.session_state.generation_stage in ['generated', 'editing']:
    
    # Show the current blog content
    st.header("📝 Generated Blog Post")
    
    # Tab layout for better organization
    tab1, tab2 = st.tabs(["📖 Preview & Publish", "✏️ Edit Sections"])
    
    with tab1:
        st.markdown("### Current Blog Content")
        if st.session_state.final_blog_content:
            st.markdown(st.session_state.final_blog_content)
        
        # Publish section with better styling
        st.markdown('<div class="publish-area">', unsafe_allow_html=True)
        st.markdown("### 🚀 Ready to Publish?")
        st.markdown("Your blog post is ready! Use the button below to copy the content to your clipboard.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("� Copy Blog Content", type="primary", use_container_width=True):
                # Create a text area with the content for easy copying
                st.markdown("**✅ Content ready for copying:**")
                st.text_area(
                    "Copy this content:", 
                    value=st.session_state.final_blog_content,
                    height=200,
                    help="Select all (Ctrl+A) and copy (Ctrl+C) the content above"
                )
                st.success("✅ Blog content is displayed above! Select all and copy it to your clipboard.")
                st.balloons()
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🔄 Generate New Blog", use_container_width=True):
                # Reset to input stage
                for key in ['blog_sections', 'original_transcript', 'sections_metadata', 'final_blog_content']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.generation_stage = 'input'
                st.rerun()
        
        with col3:
            # Download button
            st.download_button(
                label="💾 Download as .md",
                data=st.session_state.final_blog_content,
                file_name="blog_post.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### ✏️ Edit Individual Sections")
        st.markdown("Select a section below to modify it with a custom prompt.")
        
        if st.session_state.blog_sections:
            # Section selector
            section_titles = [f"{i+1}. {section['title']}" for i, section in enumerate(st.session_state.blog_sections)]
            selected_section_idx = st.selectbox(
                "Choose section to edit:",
                range(len(section_titles)),
                format_func=lambda x: section_titles[x],
                help="Select the section you want to modify"
            )
            
            selected_section = st.session_state.blog_sections[selected_section_idx]
            
            # Show current section content
            st.markdown("#### 📄 Current Section Content:")
            st.markdown('<div class="section-content">', unsafe_allow_html=True)
            st.markdown(selected_section['content'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Custom prompt input
            st.markdown("#### 💬 Modification Instructions:")
            custom_prompt = st.text_area(
                "Enter your instructions for modifying this section:",
                placeholder="Example prompts:\n• 'Make this section more technical and add specific examples'\n• 'Shorten this section and focus on key points'\n• 'Add more engaging language and storytelling elements'\n• 'Convert this to bullet points with subheadings'",
                height=120,
                help="Be specific about what changes you want to make"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔧 Apply Modifications", disabled=not custom_prompt, type="primary", use_container_width=True):
                    with st.spinner(f"🔄 Modifying section: {selected_section['title']}..."):
                        try:
                            modified_content = asyncio.run(modify_section_content(
                                st.session_state.original_transcript,
                                selected_section,
                                custom_prompt
                            ))
                            
                            # Update the section
                            st.session_state.blog_sections[selected_section_idx]['content'] = modified_content
                            
                            # Regenerate the final blog content
                            st.session_state.final_blog_content = combine_sections(st.session_state.blog_sections)
                            
                            st.session_state.generation_stage = 'editing'
                            st.success(f"✅ Section '{selected_section['title']}' has been modified!")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error modifying section: {str(e)}")
            
            with col2:
                if st.button("↩️ Revert to Original", use_container_width=True):
                    # Find the original section from sections_metadata
                    original_sections = st.session_state.sections_metadata
                    if selected_section_idx < len(original_sections):
                        with st.spinner("🔄 Regenerating original section..."):
                            try:
                                # Regenerate original content
                                from blogit.agentic_content_gen import generate_section_content
                                original_section = original_sections[selected_section_idx]
                                original_section['index'] = selected_section_idx
                                
                                _, original_content = asyncio.run(generate_section_content(
                                    st.session_state.original_transcript, 
                                    original_section
                                ))
                                
                                # Update the section
                                st.session_state.blog_sections[selected_section_idx]['content'] = original_content
                                
                                # Regenerate the final blog content
                                st.session_state.final_blog_content = combine_sections(st.session_state.blog_sections)
                                
                                st.success(f"✅ Section '{selected_section['title']}' has been reverted to original!")
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Error reverting section: {str(e)}")
        
        # Show editing history or tips
        with st.expander("💡 Editing Tips & Examples"):
            st.markdown("""
            **Effective modification prompts:**
            
            **Style Changes:**
            - "Make this more conversational and engaging"
            - "Write in a more formal, academic tone"
            - "Add humor and make it more entertaining"
            
            **Length Adjustments:**
            - "Expand this section with more details and examples"
            - "Condense this to the most important points"
            - "Make this section longer with additional insights"
            
            **Technical Level:**
            - "Simplify the technical language for general audience"
            - "Make this more technical with specific terminology"
            - "Add more beginner-friendly explanations"
            
            **Structure Changes:**
            - "Break this into bullet points and add subheadings"
            - "Convert to a numbered list format"
            - "Restructure with clear step-by-step instructions"
            
            **Content Focus:**
            - "Focus more on practical applications rather than theory"
            - "Add more specific examples and case studies"
            - "Include actionable takeaways for readers"
            """)
        
        # Section statistics
        if st.session_state.blog_sections:
            with st.expander("📊 Section Statistics"):
                total_words = sum(len(section['content'].split()) for section in st.session_state.blog_sections)
                st.metric("Total Word Count", total_words)
                
                for i, section in enumerate(st.session_state.blog_sections):
                    word_count = len(section['content'].split())
                    st.metric(f"Section {i+1}: {section['title']}", f"{word_count} words")
