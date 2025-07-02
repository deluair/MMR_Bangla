# 🇧🇩 Bengali Multi-Modal Researcher

AI research assistant that generates Bengali research reports, podcast scripts, and audio using Gemini AI.

## Quick Start

```bash
git clone https://github.com/deluair/MMR_Bangla.git
cd MMR_Bangla/multi-modal-researcher
pip install -e .
cp .env.example .env  # Add your GEMINI_API_KEY
python examples/run_example.py
```

**Outputs:** Bengali research report, podcast script, and audio file.

**Requirements:** Python 3.8+, Gemini API key

## 📚 Custom Usage

### Creating Your Own Research Topic

1. **Create a new example file:**
   ```bash
   cp examples/bengali_climate_change.py examples/my_research_topic.py
   ```

2. **Edit the topic in your new file:**
   ```python
   # In examples/my_research_topic.py
   BENGALI_TOPIC = "আপনার গবেষণার বিষয় এখানে লিখুন"
   ```

3. **Update the main runner:**
   ```python
   # In examples/run_example.py
   from my_research_topic import run_research
   ```

4. **Run your custom research:**
   ```bash
   python examples/run_example.py
   ```

### Programmatic Usage

```python
import asyncio
from langgraph.checkpoint.memory import MemorySaver
from agent.graph import create_compiled_graph

async def custom_research():
    # Initialize the research graph
    graph = create_compiled_graph()
    memory = MemorySaver()
    
    config = {
        "configurable": {
            "thread_id": "my-research-thread",
            "checkpoint": memory,
        }
    }
    
    # Define your research input
    inputs = {
        "topic": "বাংলাদেশে কৃত্রিম বুদ্ধিমত্তার ভবিষ্যৎ",  # AI future in Bangladesh
        "video_url": None,  # Optional YouTube URL
    }
    
    # Run the research
    result = await graph.ainvoke(inputs, config=config)
    
    return result["report"], result["podcast_script"]

# Run the research
report, script = asyncio.run(custom_research())
```

## 🏗️ Technical Architecture

### Core Components

- **LangGraph Workflow**: Advanced graph-based AI workflow management
- **Gemini 2.5 Flash**: Google's latest multimodal AI model for text generation
- **Web Search Integration**: Automated web scraping and information synthesis
- **Bengali Language Processing**: Specialized prompts and processing for Bengali content
- **Text-to-Speech**: Google's TTS service for audio generation

### Project Structure Deep Dive

```
multi-modal-researcher/
├── src/agent/
│   ├── configuration.py    # Model settings, TTS config, API keys
│   ├── graph.py           # LangGraph workflow definition
│   ├── state.py           # Agent state management
│   └── utils.py           # Core research and generation functions
├── examples/
│   ├── run_example.py     # Main execution script
│   └── bengali_climate_change.py  # Example research topic
├── output/                # Generated files appear here
│   ├── *.md              # Research reports
│   ├── *.txt             # Podcast scripts
│   └── *.wav             # Audio files
└── .env                   # API keys (create from .env.example)
```

### Workflow Process

1. **Input Processing**: Topic validation and preparation
2. **Web Search**: Multi-query search strategy for comprehensive coverage
3. **Content Synthesis**: AI-powered information aggregation with source tracking
4. **Report Generation**: Structured Bengali research report creation
5. **Script Writing**: Conversational podcast script development
6. **Audio Production**: Text-to-speech conversion
7. **Output Management**: File organization and saving

## ⚠️ Important Notes

### TTS Voice Limitation

The current Gemini 1.5 Flash model **does not have a native Bengali TTS voice**. The configuration (`src/agent/configuration.py`) uses an English voice (`"puck"`).

- **Result**: Generated `.wav` files have English speech reading Bengali text
- **Text Outputs**: Research reports and podcast scripts are entirely in Bengali
- **Future**: Will be updated when Google adds Bengali TTS support

### API Usage and Costs

- **Gemini API**: Pay-per-use model based on tokens processed
- **Rate Limits**: Respect Google's API rate limits
- **Optimization**: The system is designed to minimize API calls while maximizing quality

## 🔧 Troubleshooting

### Common Issues

**1. API Key Errors**
```bash
❌ Error: GEMINI_API_KEY not found
```
**Solution**: Ensure `.env` file exists with valid API key

**2. Import Errors**
```bash
❌ Error: Could not import 'run_research'
```
**Solution**: Check file paths and ensure you're in the correct directory

**3. Dependency Issues**
```bash
❌ ModuleNotFoundError: No module named 'langgraph'
```
**Solution**: Reinstall dependencies with `pip install -e .`

**4. Network Issues**
```bash
❌ Connection timeout during web search
```
**Solution**: Check internet connection and firewall settings

### Performance Tips

- **Virtual Environment**: Always use a virtual environment
- **Python Version**: Use Python 3.11+ for best compatibility
- **Memory**: Ensure sufficient RAM (4GB+ recommended)
- **Network**: Stable internet connection required for web searches

## 📄 Output Examples

### Research Report Structure
```markdown
# জলবায়ু পরিবর্তন এবং বাংলাদেশে এর প্রভাব

## নির্বাহী সারাংশ
[Executive summary in Bengali]

## মূল বিষয়সমূহ
[Key findings with source citations]

## বিস্তারিত বিশ্লেষণ
[Detailed analysis sections]

## সুপারিশসমূহ
[Recommendations]

## তথ্যসূত্র
[Source references]
```

### Podcast Script Format
```
স্পিকার ১: [Opening remarks in Bengali]
স্পিকার ২: [Response and discussion]
[Conversational flow continues...]
```

## 🤝 Contributing

We welcome contributions to improve MMR_Bangla! Here's how you can help:

### Ways to Contribute

- 🐛 **Bug Reports**: Report issues via GitHub Issues
- 💡 **Feature Requests**: Suggest new features or improvements
- 🔧 **Code Contributions**: Submit pull requests with improvements
- 📚 **Documentation**: Help improve documentation and examples
- 🌐 **Translations**: Improve Bengali language processing

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**:
   ```bash
   python examples/run_example.py
   ```
5. **Submit a pull request**

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings for new functions
- Include type hints where appropriate

## 📊 Performance Metrics

### Typical Processing Times

- **Web Search**: 30-60 seconds
- **Report Generation**: 2-5 minutes
- **Podcast Script**: 1-3 minutes
- **Audio Generation**: 1-2 minutes
- **Total Runtime**: 5-10 minutes (depending on topic complexity)

### Resource Usage

- **Memory**: 2-4 GB RAM during processing
- **Storage**: 10-50 MB per research session
- **Network**: 50-200 MB data transfer

## 🔮 Future Roadmap

### Planned Features

- [ ] **Native Bengali TTS**: When Google adds Bengali voice support
- [ ] **Multiple Output Formats**: PDF, DOCX, HTML export options
- [ ] **Advanced Search**: Domain-specific search capabilities
- [ ] **Interactive Mode**: Real-time research with user feedback
- [ ] **Batch Processing**: Multiple topics in one session
- [ ] **Custom Templates**: User-defined report and script templates
- [ ] **Integration APIs**: REST API for external applications

### Version History

- **v0.0.1**: Initial Bengali adaptation with basic functionality
- **v0.1.0**: Enhanced search capabilities and improved Bengali processing
- **v0.2.0**: Added comprehensive documentation and examples

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 MMR_Bangla Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 🙏 Acknowledgments

- **LangChain Team**: For the original Multi-Modal Researcher framework
- **Google**: For the Gemini AI model and TTS services
- **Bengali Language Community**: For inspiration and feedback
- **Open Source Contributors**: For various dependencies and tools

## 📞 Support

### Getting Help

- 📖 **Documentation**: Check this README and code comments
- 🐛 **Issues**: Report bugs via [GitHub Issues](https://github.com/deluair/MMR_Bangla/issues)
- 💬 **Discussions**: Join conversations in [GitHub Discussions](https://github.com/deluair/MMR_Bangla/discussions)
- 📧 **Contact**: Reach out to maintainers for specific questions

### Community

- **GitHub**: [https://github.com/deluair/MMR_Bangla](https://github.com/deluair/MMR_Bangla)
- **Original Project**: [LangChain Multi-Modal Researcher](https://github.com/langchain-ai/multi-modal-researcher)

---

**Made with ❤️ for the Bengali research community**

*"গবেষণার মাধ্যমে জ্ঞানের আলো ছড়িয়ে দিন" - "Spread the light of knowledge through research"*
