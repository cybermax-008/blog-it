# Blog-it

Gemini AI powered SEO-optimized blog post generator from podcast transcripts.

## Project Overview
This is a streamlit based webUI tool that takes podcast transcript as input and uses multiple AI agentic fucntions to generate a cohesive , SEO-optimized blog post, The process works as follows:

1. The `podcast_analyzer.py` identifies 4-5 cohesive sections/headings from the trasncript.
2. We roll our individual section generation agents to create content for each of the sections in parallel using asyncio. Using fucntions inside `agentic_content_gen.py`
3. The sections are stitched together into a complete blog post.
4. The QA validation agent in `qa_validator.py` reviews the blog for quality, cohesiveness, and SEO optimizations.
5. The final blog post is delivered as markdonw or HTMl as output.

## Usage

```bash
# Clone the repo
git clone https://github.com/cybermax-008/blog-it.git
cd blog-it

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# create .env file from the example
cp .env.example .env

# Edit the .env file to add Gemini API key
GEMINI_API_KEY=your-gemini-api-key

# Install the dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

