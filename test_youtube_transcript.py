#!/usr/bin/env python3
"""
YouTube Transcript Extractor Test Script

This script extracts transcripts from YouTube videos and saves them to text files.
It uses the youtube-transcript-api library and includes comprehensive error handling.
"""

import os
import sys
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(youtube_url):
    """Extract video ID from various YouTube URL formats"""
    # Clean up the URL by removing escape characters
    youtube_url = youtube_url.replace("\\", "")
    
    if "watch?v=" in youtube_url:
        return youtube_url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_url:
        return youtube_url.split("youtu.be/")[1].split("?")[0]
    elif "embed/" in youtube_url:
        return youtube_url.split("embed/")[1].split("?")[0]
    else:
        # Try to extract from any URL with v= parameter
        if "v=" in youtube_url:
            return youtube_url.split("v=")[1].split("&")[0]
        else:
            raise ValueError(f"Unable to extract video ID from URL: {youtube_url}")


def get_video_info(video_id):
    """Get basic video information for the filename"""
    # For this test, we'll just use the video ID
    # In a real implementation, you might want to use the YouTube Data API
    # to get the actual video title
    return f"video_{video_id}"


def extract_and_save_transcript(youtube_url, output_dir="transcripts"):
    """
    Extract transcript from YouTube video and save to a text file
    
    Args:
        youtube_url (str): YouTube video URL
        output_dir (str): Directory to save the transcript file
    
    Returns:
        str: Path to the saved transcript file
    """
    
    try:
        # Extract video ID
        video_id = extract_video_id(youtube_url)
        print(f"📹 Video ID: {video_id}")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize the YouTube Transcript API
        ytt_api = YouTubeTranscriptApi()
        print(f"🔍 Searching for available transcripts...")
        
        # Try to get transcript with language preference
        fetched_transcript = None
        transcript_language = None
        
        try:
            # First try English
            fetched_transcript = ytt_api.fetch(video_id, languages=['en'])
            transcript_language = "English"
            print(f"✅ Found English transcript")
        except Exception as e:
            print(f"⚠️ English transcript not available: {e}")
            
            try:
                # Get list of available transcripts
                transcript_list = ytt_api.list(video_id)
                print(f"📋 Available transcripts:")
                
                # Show available transcripts
                available_languages = []
                for transcript in transcript_list:
                    lang_info = f"{transcript.language} ({transcript.language_code})"
                    if transcript.is_generated:
                        lang_info += " [Auto-generated]"
                    available_languages.append(lang_info)
                    print(f"   - {lang_info}")
                
                # Try to find any English variant
                try:
                    transcript = transcript_list.find_transcript(['en'])
                    fetched_transcript = transcript.fetch()
                    transcript_language = f"{transcript.language} ({transcript.language_code})"
                    print(f"✅ Using English transcript: {transcript_language}")
                except Exception:
                    # Try common languages
                    common_languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh']
                    for lang in common_languages:
                        try:
                            transcript = transcript_list.find_transcript([lang])
                            fetched_transcript = transcript.fetch()
                            transcript_language = f"{transcript.language} ({transcript.language_code})"
                            print(f"✅ Using transcript in: {transcript_language}")
                            break
                        except:
                            continue
                    
                    # If still no transcript found, use the first available
                    if fetched_transcript is None:
                        available_transcripts = list(transcript_list)
                        if available_transcripts:
                            transcript = available_transcripts[0]
                            fetched_transcript = transcript.fetch()
                            transcript_language = f"{transcript.language} ({transcript.language_code})"
                            print(f"✅ Using first available transcript: {transcript_language}")
                        else:
                            raise Exception("No transcripts available for this video")
                            
            except Exception as e2:
                raise Exception(f"Failed to get any transcript: {str(e2)}")
        
        if fetched_transcript is None:
            raise Exception("No transcript could be extracted")
        
        # Convert transcript to text
        transcript_text = ""
        word_count = 0
        
        print(f"📝 Processing transcript...")
        for snippet in fetched_transcript:
            transcript_text += snippet.text + " "
            word_count += len(snippet.text.split())
        
        transcript_text = transcript_text.strip()
        
        if not transcript_text:
            raise Exception("Transcript was extracted but appears to be empty")
        
        # Generate filename
        video_info = get_video_info(video_id)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{video_info}_{timestamp}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Save transcript to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"YouTube Transcript Extraction\n")
            f.write(f"{'=' * 40}\n\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"Video URL: {youtube_url}\n")
            f.write(f"Language: {transcript_language}\n")
            f.write(f"Word Count: {word_count:,}\n")
            f.write(f"Character Count: {len(transcript_text):,}\n")
            f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\n{'=' * 40}\n")
            f.write(f"TRANSCRIPT\n")
            f.write(f"{'=' * 40}\n\n")
            f.write(transcript_text)
        
        print(f"✅ Transcript saved successfully!")
        print(f"📁 File: {filepath}")
        print(f"📊 Stats: {word_count:,} words, {len(transcript_text):,} characters")
        print(f"🌐 Language: {transcript_language}")
        
        return filepath
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error: {error_msg}")
        
        # Provide helpful suggestions based on error type
        if "no transcripts available" in error_msg.lower():
            print("💡 Suggestions:")
            print("   - The video might not have captions enabled")
            print("   - Try a different video with captions")
            print("   - Check if the video is public and accessible")
        elif "video unavailable" in error_msg.lower():
            print("💡 Suggestions:")
            print("   - Check if the video URL is correct")
            print("   - Verify the video is not private or deleted")
            print("   - Try accessing the video in a browser first")
        
        raise


def main():
    """Main function to run the transcript extraction test"""
    
    print("🎬 YouTube Transcript Extractor Test")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # Use URL from command line argument
        youtube_url = sys.argv[1]
    else:
        # Ask user for URL
        youtube_url = input("Enter YouTube URL: ").strip()
    
    if not youtube_url:
        print("❌ No URL provided")
        return
    
    try:
        filepath = extract_and_save_transcript(youtube_url)
        print(f"\n🎉 Success! Transcript saved to: {filepath}")
        
        # Ask if user wants to view the file
        view_file = input("\nDo you want to view the transcript? (y/n): ").strip().lower()
        if view_file in ['y', 'yes']:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                print("\n" + "=" * 50)
                print("TRANSCRIPT CONTENT")
                print("=" * 50)
                print(content[:1000] + "..." if len(content) > 1000 else content)
                
    except Exception as e:
        print(f"\n💥 Failed to extract transcript: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 