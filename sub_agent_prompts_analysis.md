# Sub-Agent Prompts Analysis - BlogIt System

This document provides a comprehensive overview of the prompts used by different sub-agents in the BlogIt system, which converts podcast transcripts into SEO-optimized blog posts.

## System Architecture Overview

The BlogIt system uses a multi-agent approach with 3 specialized agents:

1. **Podcast Analyzer Agent** (`podcast_analyzer.py`) - Identifies cohesive sections from transcript
2. **Content Generation Agent** (`agentic_content_gen.py`) - Generates content for each section in parallel
3. **QA Validation Agent** (`qa_validator.py`) - Reviews and improves the final blog post

Each agent uses different Gemini model configurations optimized for their specific tasks.

## Model Configurations

The system uses `gemini-2.0-flash` with different temperature settings for each agent type:

- **Analysis Agent**: Temperature 0.1 (deterministic results)
- **Content Agent**: Temperature 0.7 (more creative variety)
- **Validation Agent**: Temperature 0.1 (deterministic improvements)

## 1. Podcast Analyzer Agent

### Purpose
Analyzes podcast transcripts and identifies 4-5 main sections that would create a cohesive blog post structure.

### System Instruction
```
You are expert content analyst. Your task is to analyze the podcast transcript and identify 4-5 main sections that would make a cohesive blog post. The sections should have a good flow and cover the main points of the podcast. You can also include an introduction and conclusion to tie the sections together.
```

### Main Prompt Template
```
Analyze this podcast transcript and identify 4-5 main sections that would make a cohesive blog post. For each section, provide a title and a brief description of what that section should cover. Ensure the sections flow well together and cover the main points of the podcast.

Transcript:
{podcast_text}

Output the sections as a list of JSON objects with 'title' and 'description' keys for each section. Format your response as a valid JSON array.
```

### Key Features
- Uses JSON output format for structured data
- Focuses on logical flow and cohesiveness
- Identifies 4-5 main sections automatically
- Provides both title and description for each section

## 2. Content Generation Agent

### Purpose
Generates detailed content for each identified section in parallel using asyncio for efficiency.

### System Instruction Template
```
You are an expert content writer specializing in creating SEO-optimized blog posts. You are tasked with writing a section of a blog post based on the provided transcript.

The section you need to write is: {section['title']}
Description of this section: {section['description']}

Your content should be:
1. Be well-structured with appropriate headers (use markdown ## for subsections)
2. Include relevant keywords naturally for SEO optimization
3. Be informative and engaging for the reader
4. Be approximately 300-500 words in length
5. Maintain the original tone and style of the podcast
6. Include only factual information from the podcast transcript (don't make up facts)
7. Format the content in Markdown format
```

### Section Generation Prompt Template
```
Write the {section['title']} section of the blog post based on the following transcript:

{transcript}

Remember to follow the guidelines and focus specifically on content related to this section. Start with the section title as markdown heading (# {section['title']}).
```

### Key Features
- **Parallel Processing**: Uses asyncio to generate all sections simultaneously
- **SEO Optimization**: Naturally incorporates relevant keywords
- **Length Control**: Targets 300-500 words per section
- **Factual Accuracy**: Emphasizes using only information from the transcript
- **Auto Section Management**: Automatically adds Introduction and Conclusion if missing
- **Markdown Formatting**: Outputs structured markdown content

### Section Management Logic
```python
# Automatically adds missing sections
has_intro = any(section['title'].lower() == 'introduction' for section in sections)
has_conclusion = any(section['title'].lower() == 'conclusion' for section in sections)

if not has_intro:
    sections.insert(0, {'title': 'Introduction', 'description': 'Introduction to the podcast content and the main topics covered.', 'index': 0})
if not has_conclusion:
    sections.append({'title': 'Conclusion', 'description': 'Summary of key points and final thoughts.', 'index': len(sections)})
```

## 3. QA Validation Agent

### Purpose
Reviews the generated blog post for quality, coherence, SEO optimization, and provides an improved version.

### System Instruction
```
You are an expert content editor and SEO specialist. Your task is to:

1. Evaluate the quality of a blog post generated from a podcast transcript
2. Ensure the blog is cohesive, with smooth transitions between sections.
3. Check that the blog accurately represents the content of the podcast.
4. Verify SEO optimization with relevant keywords and appropriate formatting.
5. Finally provide the improved version of the blog post.

Your feedback should be detailed and provide constructive suggestions for enhancing the blog post.
```

### Validation Prompt Template
```
Review this blog post that was generated from a podcast transcript:

BLOG CONTENT:
{blog_content}

ORIGINAL PODCAST TRANSCRIPT:
{original_transcript}

Evaluate the blog post for:
1. Content quality and accuracy
2. SEO optimization
3. Section coherence and transitions
4. Overall readability and engagement

Output only the improved version of the blog post in Markdown format. Do not include the evaluation feedback in the final output.
```

### Key Features
- **Comprehensive Review**: Evaluates quality, accuracy, SEO, and readability
- **Cross-Reference Validation**: Compares against original transcript
- **Improvement Focus**: Provides enhanced version rather than just feedback
- **Clean Output**: Returns only the improved blog post without evaluation notes

## Workflow Integration

### Main Application Flow (app.py)
```python
# 1. Extract/upload transcript
podcast_text = extract_transcript_details(youtube_link) or uploaded_file_content

# 2. Analyze and identify sections
sections = analyze_podcast(podcast_text)

# 3. Generate content for all sections in parallel
blog_content = asyncio.run(generate_blog_content(podcast_text, sections))

# 4. Validate and improve the blog
improved_blog = validate_blog(blog_content, podcast_text)
```

## Prompt Engineering Strategies Used

### 1. Role-Based Instructions
Each agent has a clear role definition:
- "expert content analyst"
- "expert content writer specializing in creating SEO-optimized blog posts"
- "expert content editor and SEO specialist"

### 2. Structured Output Requirements
- JSON format for section identification
- Markdown format for content generation
- Specific word counts and formatting guidelines

### 3. Quality Constraints
- Factual accuracy requirements
- SEO optimization guidelines
- Coherence and flow requirements
- Tone and style preservation

### 4. Multi-Stage Processing
- Analysis → Content Generation → Validation
- Each stage builds upon the previous stage's output
- Parallel processing for efficiency in content generation

### 5. Error Handling
- JSON parsing with regex fallbacks
- Exception handling for API calls
- Graceful degradation with error messages

## Key Insights

1. **Temperature Tuning**: Different agents use different creativity levels (0.1 for analysis/validation, 0.7 for content generation)

2. **Parallel Efficiency**: Content generation uses asyncio for simultaneous section creation

3. **Automatic Enhancement**: System automatically adds missing Introduction/Conclusion sections

4. **Multi-Format Support**: Outputs both Markdown and HTML formats

5. **Cross-Validation**: Final agent compares output against original transcript for accuracy

6. **SEO Focus**: All agents incorporate SEO best practices in their instructions

This multi-agent system demonstrates effective prompt engineering for complex content generation tasks, with each agent having specialized roles and optimized configurations for their specific functions.