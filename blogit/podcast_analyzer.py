import json
import re
from .gemini_config import get_model
from youtube_transcript_api import YouTubeTranscriptApi

# Function to extract transcript details from a YouTube video URL
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript
    except Exception as e:
        raise e

def analyze_podcast(podcast_text):

    # Using Gemini to analyze the transcript of the podcast and identify key sections for the blog post

    system_instruction = """
    You are expert content analyst. Your task is to analyze the podcast transcript and identify 4-5 main sections that would make a cohesive blog post. The sections should have
    a good flow and cover the main points of the podcast. You can also include an introduction and conclusion to tie the sections together.
    """

    model = get_model(model_type="analysis", system_instruction=system_instruction)

    prompt = f"""Analyze this podcast transcript and identify 4-5 main sections that would make a cohesive blog post. For each section, provide a title and a crief description of what that section
    should cover. Ensure the sections flow well togther and cover the main points of the podcast.

    Transcript:
    {podcast_text}

    Output the sections as a list of JSON objects with 'title' and 'description' keys for each section. Format your response as a valid JSON array.
    """

    # Generate the analysis
    response = model.generate_content(prompt)

    # Parse the response to extract the sections
    sections_text = response.text

    # Extract the sections from the response
    try:
        # Look for  JSON array pattern in the response
        json_match = re.search(r'\[\s*\{.*\}\s*\]', sections_text, re.DOTALL)
        if json_match:
            sections = json.loads(json_match.group())
        else:
            # try parsing the whole text as JSON
            sections = json.loads(sections_text)
    except Exception as e:
        print("Error parsing sections:", e)
        return None
    
    return sections

