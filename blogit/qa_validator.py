import json
import re
from .gemini_config import get_model

def validate_blog(blog_content, original_transcript):

    system_instruction = """You are an expert content editor and SEO specialist. Your task is to:
    
    1. Evalaute the quality of a blog post generated froma podcast trasncript
    2. Ensure the blog is cohesive, with smooth transitions between sections.
    3. Check that the blog accurately represents the content of the podcast.
    4. Verify SEO optimization with relevant keywords and appropriate formatting.
    5. Finally provide the improved version of the blog post.
    Your feedback should be detailed and provide constructive suggestions for enhancing the blog post.
    """

    model = get_model(model_type="validation", system_instruction=system_instruction)

    prompt = f"""Review this blog post that was generated from a podcast trasncript:

    BLOG CONTENT:
    {blog_content}

    ORIGINAL PODCAST TRANSCRIPT:
    {original_transcript}

    Evalaute the blog post for:
    1. Content quality and accuracy
    2. SEO optimization
    3. Section coherence and transitions
    4. Overall readability and engagement


    Output only the improved version of the blog post in Mardown format. Do not include the evaluation feedback in the final output.
    """

    # Generate the improved blog post
    response = model.generate_content(prompt)

    return response.text
    