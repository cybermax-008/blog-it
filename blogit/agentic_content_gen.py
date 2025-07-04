import asyncio
from .gemini_config import get_model

async def generate_section_content(transcript, section):

    system_instruction = f"""
    You are an expert content writer specializing in creating SEO-optimized blog posts. You are tasked with writing a section of a blog post based on the provided trasncript.

    The section you need to write is : {section['title']}
    Description of this section: {section['description']}

    Your content should be:
    1. Be well-structured with appropriate headers ( user markdown ## for subsctions)
    2. Include relevant keywords naturally for SEO optimization
    3. Be informative and engaging for the reader
    4. Be approximately 300-500 words in length
    5. Maintain the original tone and style of the podcast
    6. Include only factual information from the podcast transcript (don't make up facts)
    7. Formar the content in Markdown format
    """

    model = get_model(model_type="content", system_instruction=system_instruction)

    prompt = f""" Write the {section['title']} section of the blog post based on the following transcript:

    {transcript}

    Remember to follow the guidelines and focus specifically on content related to this section. Start with the section title as mardown heading (# {section['title']}).
    """

    try:
        # Generate the content for the section
        response = model.generate_content(prompt)
        section_index = section.get('index', 0)
        return section_index, response.text
    except Exception as e:
        print("Error generating content for section {section['title']}:", e)
        section_index = section.get('index', 0)
        return section_index, f"Error generating content for section {section['title']}: {e}"

async def modify_section_content(transcript, section, custom_prompt):
    """
    Modify an existing section based on custom user instructions
    
    Args:
        transcript: The original podcast transcript
        section: Dictionary containing section info (title, content, etc.)
        custom_prompt: User's custom instructions for modification
    
    Returns:
        Modified section content as string
    """
    
    system_instruction = f"""
    You are an expert content editor specializing in refining blog post sections based on specific user instructions.
    
    Your task is to modify an existing blog section according to the user's custom instructions while:
    1. Maintaining the core factual information from the original podcast transcript
    2. Preserving the overall structure and markdown formatting
    3. Keeping the section title consistent (# {section['title']})
    4. Following the user's specific modification instructions precisely
    5. Ensuring the content remains SEO-optimized and engaging
    6. Maintaining appropriate length (not too short or excessively long unless specifically requested)
    """

    model = get_model(model_type="content", system_instruction=system_instruction)

    prompt = f"""
    Please modify the following blog section according to the user's specific instructions:

    ORIGINAL SECTION CONTENT:
    {section['content']}

    USER'S MODIFICATION INSTRUCTIONS:
    {custom_prompt}

    ORIGINAL PODCAST TRANSCRIPT (for reference):
    {transcript}

    Please provide the modified section content in Markdown format, ensuring it still accurately represents the podcast content while following the user's instructions.
    """

    try:
        # Generate the modified content
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error modifying section {section['title']}:", e)
        return f"Error modifying section {section['title']}: {e}"

async def generate_blog_content(transcript, sections):

    # Check for introduction and conclusion sections and add them if not present
    has_intro = any(section['title'].lower() == 'introduction' for section in sections)
    has_conclusion = any(section['title'].lower() == 'conclusion' for section in sections)

    if not has_intro:
        sections.insert(0, {'title': 'Introduction', 'description': 'Introduction to the podcast content and the main topics covered.', 'index': 0})
    if not has_conclusion:
        sections.append({'title': 'Conclusion', 'description': 'Summary of key points and final thoughts.', 'index': len(sections)})

    # Add index to each section for tracking
    for i, section in enumerate(sections):
        section['index'] = i

    # create tasks for async content generation
    tasks = []
    for section in sections:
        task = generate_section_content(transcript, section)
        tasks.append(task)

    # Gather the results of the async tasks
    results = await asyncio.gather(*tasks)

    # Sort the results based on the section index
    results.sort(key=lambda x: x[0])

    # return just the content
    return [content for index, content in results]
