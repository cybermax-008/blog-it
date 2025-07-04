import json
import re
from .gemini_config import get_model
from youtube_transcript_api import YouTubeTranscriptApi

# Function to extract transcript details from a YouTube video URL
def extract_transcript_details(youtube_video_url):
    try:
        # Extract video ID - handle different YouTube URL formats
        if "watch?v=" in youtube_video_url:
            video_id = youtube_video_url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in youtube_video_url:
            video_id = youtube_video_url.split("youtu.be/")[1].split("?")[0]
        elif "embed/" in youtube_video_url:
            video_id = youtube_video_url.split("embed/")[1].split("?")[0]
        else:
            # Fallback to original method
            video_id = youtube_video_url.split("=")[1]
        
        print(f"Attempting to extract transcript for video ID: {video_id}")
        
        # Initialize the API
        ytt_api = YouTubeTranscriptApi()
        
        # Try to get transcript - first attempt with default language (English)
        try:
            fetched_transcript = ytt_api.fetch(video_id, languages=['en'])
            print(f"Found English transcript")
        except Exception as e:
            print(f"Failed to get English transcript: {e}")
            # Try to get available transcripts and use the first available one
            try:
                transcript_list = ytt_api.list(video_id)
                # Try to find any English transcript first
                try:
                    transcript = transcript_list.find_transcript(['en'])
                    fetched_transcript = transcript.fetch()
                    print(f"Found English transcript: {transcript.language_code}")
                except Exception:
                    # If no English transcript, get any available transcript
                    try:
                        transcript = transcript_list.find_transcript(['de', 'es', 'fr', 'it', 'pt', 'ru', 'ja', 'ko', 'zh'])
                        fetched_transcript = transcript.fetch()
                        print(f"Using transcript in language: {transcript.language_code}")
                    except Exception:
                        # Get any available transcript
                        available_transcripts = list(transcript_list)
                        if available_transcripts:
                            transcript = available_transcripts[0]
                            fetched_transcript = transcript.fetch()
                            print(f"Using transcript in language: {transcript.language_code}")
                        else:
                            raise Exception("No transcripts found")
            except Exception as e2:
                raise Exception(f"No transcripts available for this video. This could be because: "
                              f"1) The video doesn't have any transcripts/captions, "
                              f"2) The video is private or restricted, "
                              f"3) The video ID is invalid. "
                              f"Original error: {str(e2)}")

        # Convert transcript to text using the new API structure
        transcript_text = ""
        for snippet in fetched_transcript:
            transcript_text += " " + snippet.text

        if not transcript_text.strip():
            raise Exception("Transcript was extracted but appears to be empty")

        print(f"Successfully extracted transcript with {len(transcript_text)} characters")
        return transcript_text.strip()
        
    except Exception as e:
        # Re-raise with more helpful error message
        error_msg = str(e)
        if "no element found" in error_msg.lower():
            raise Exception("Failed to extract transcript. This video may not have captions/transcripts available, or the video might be private/restricted.")
        elif "video unavailable" in error_msg.lower():
            raise Exception("The video is unavailable or private. Please check the URL and video privacy settings.")
        elif "transcript disabled" in error_msg.lower():
            raise Exception("Transcripts are disabled for this video.")
        else:
            raise Exception(f"Error extracting transcript: {error_msg}")

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

