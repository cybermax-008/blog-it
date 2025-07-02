# BlogGen 📝

Convert your podcast to a professional blog post with iterative editing capabilities.

## Features

### 🎙️ Multiple Input Options
- **Upload Transcript**: Upload a `.txt` file containing your podcast transcript
- **YouTube Link**: Automatically extract transcripts from YouTube videos

### 🤖 AI-Powered Blog Generation
- Automatic podcast analysis and section identification
- SEO-optimized content generation
- Professional blog formatting with proper markdown structure
- Content validation and improvement

### ✏️ Section-wise Editing
- **Custom Prompt Editing**: Modify individual sections using natural language instructions
- **Real-time Preview**: See changes immediately in the preview tab
- **Revert Functionality**: Easily revert any section back to its original content
- **Section Statistics**: Track word count and section metrics

### 🚀 Publishing & Export
- **Copy to Clipboard**: Easy content copying for publishing
- **Download as Markdown**: Export your blog post as a `.md` file
- **Real-time Preview**: See exactly how your blog will look

## How to Use

### 1. Input Your Podcast Content
Choose between uploading a transcript file or providing a YouTube URL:

```
📁 Upload Transcript File: Upload a .txt file with your podcast content
🌐 YouTube Link: Enter a YouTube URL to automatically extract the transcript
```

### 2. Generate Your Blog Post
Click "🚀 Generate Blog Post" and watch as the AI:
- Analyzes your podcast content
- Identifies key sections and topics
- Generates SEO-optimized content
- Validates and improves the output

### 3. Edit Individual Sections
Use the "✏️ Edit Sections" tab to refine your content:

#### Effective Modification Prompts:

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

### 4. Publish Your Blog
When you're satisfied with your content:
- Use "📋 Copy Blog Content" to copy the content to your clipboard
- Or "💾 Download as .md" to save it as a markdown file
- Share it on your blog, website, or publishing platform

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bloggen
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
Create a `.env` file with your Google Gemini API key:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## Requirements

- Python 3.7+
- Google Gemini API key
- Internet connection for AI processing and YouTube transcript extraction

## File Structure

```
bloggen/
├── app.py                          # Main Streamlit application
├── blogit/                         # Core blog generation package
│   ├── __init__.py
│   ├── agentic_content_gen.py      # Content generation and modification
│   ├── gemini_config.py            # AI model configuration
│   ├── podcast_analyzer.py         # Podcast analysis and transcription
│   └── qa_validator.py             # Content validation and improvement
├── requirements.txt                # Python dependencies
├── sample_transcript.txt           # Sample podcast transcript for testing
└── README.md                       # This file
```

## Key Features Explained

### Session State Management
The application maintains your blog content and editing history throughout your session, allowing you to:
- Switch between preview and editing modes
- Make multiple iterations on different sections
- Revert changes when needed

### AI-Powered Section Modification
Each section can be independently modified using natural language instructions. The AI understands context and maintains consistency while applying your requested changes.

### Progressive Enhancement
The blog generation process includes multiple stages:
1. **Analysis**: Identifies key themes and structure
2. **Generation**: Creates initial content for each section
3. **Validation**: Improves coherence and SEO optimization
4. **Modification**: User-directed refinements

## Tips for Best Results

1. **Provide Clear Transcripts**: Clean, well-formatted transcripts produce better results
2. **Be Specific with Edit Requests**: The more specific your modification prompts, the better the results
3. **Use the Preview**: Always check the preview tab to see how your changes look
4. **Iterate Gradually**: Make small, focused changes rather than major overhauls
5. **Save Your Work**: Use the download feature to save versions you like

## Troubleshooting

- **Long Generation Times**: Large transcripts may take longer to process
- **API Errors**: Ensure your Google Gemini API key is valid and has sufficient quota
- **YouTube Extraction Issues**: Some videos may not have transcripts available

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve BlogGen.

## License

This project is open source and available under the MIT License.

