import os
import wave
from google.genai import Client, types
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

load_dotenv()

# Initialize client. It's critical that the .env file is loaded before this line.
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment. Please ensure it is set in your .env file and the file is loaded before this module.")
genai_client = Client(api_key=api_key)


def display_gemini_response(response):
    """Extract text from Gemini response and display as markdown with references"""
    console = Console()
    
    # Extract main content
    text = response.candidates[0].content.parts[0].text
    md = Markdown(text)
    console.print(md)
    
    # Get candidate for grounding metadata
    candidate = response.candidates[0]
    
    # Build sources text block
    sources_text = ""
    
    # Display grounding metadata if available
    if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
        console.print("\n" + "="*50)
        console.print("[bold blue]References & Sources[/bold blue]")
        console.print("="*50)
        
        # Display and collect source URLs
        if candidate.grounding_metadata.grounding_chunks:
            console.print(f"\n[bold]Sources ({len(candidate.grounding_metadata.grounding_chunks)}):[/bold]")
            sources_list = []
            for i, chunk in enumerate(candidate.grounding_metadata.grounding_chunks, 1):
                if hasattr(chunk, 'web') and chunk.web:
                    title = getattr(chunk.web, 'title', 'No title') or "No title"
                    uri = getattr(chunk.web, 'uri', 'No URI') or "No URI"
                    console.print(f"{i}. {title}")
                    console.print(f"   [dim]{uri}[/dim]")
                    sources_list.append(f"{i}. {title}\n   {uri}")
            
            sources_text = "\n".join(sources_list)
        
        # Display grounding supports (which text is backed by which sources)
        if candidate.grounding_metadata.grounding_supports:
            console.print(f"\n[bold]Text segments with source backing:[/bold]")
            for support in candidate.grounding_metadata.grounding_supports[:5]:  # Show first 5
                if hasattr(support, 'segment') and support.segment:
                    snippet = support.segment.text[:100] + "..." if len(support.segment.text) > 100 else support.segment.text
                    source_nums = [str(i+1) for i in support.grounding_chunk_indices]
                    console.print(f"• \"{snippet}\" [dim](sources: {', '.join(source_nums)})[/dim]")
    
    return text, sources_text


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save PCM data to a wave file"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


def create_podcast_discussion(topic, search_text, video_text, search_sources_text, video_url, filename="research_podcast.wav", configuration=None):
    """Create a 2-speaker podcast discussion explaining the research topic in Bengali"""
    
    # Use default values if no configuration provided
    if configuration is None:
        from agent.configuration import Configuration
        configuration = Configuration()
    
    # Step 1: Generate podcast script
    script_prompt = f"""
    নিচের গবেষণা বিষয়বস্তু ব্যবহার করে, রাহুল (উপস্থাপক) এবং সাবিনা (বিশেষজ্ঞ)-এর মধ্যে "{topic}" বিষয়ক একটি স্বাভাবিক, আকর্ষণীয় পডকাস্ট আলোচনা বাংলায় তৈরি করুন।

    গবেষণা ফলাফল:
    {search_text}

    ভিডিও বিশ্লেষণ:
    {video_text}

    ডায়ালগ আকারে উপস্থাপন করুন:
    - রাহুল বিষয়টি উপস্থাপন করবে এবং প্রশ্ন করবে
    - সাবিনা মূল ধারণা ও বিশ্লেষণ ব্যাখ্যা করবে
    - স্বাভাবিক কথোপকথন (৫-৭ বার আদান-প্রদান)
    - রাহুল অনুসরণমূলক প্রশ্ন করবে
    - সাবিনা মূল বিষয়গুলো সংক্ষেপে তুলে ধরবে
    - কথোপকথনটি সহজবোধ্য ও আকর্ষণীয় রাখুন (৩-৪ মিনিটের মধ্যে)

    নিম্নরূপ ফরম্যাটে দিন:
    রাহুল: [প্রশ্ন]
    সাবিনা: [উত্তর]
    রাহুল: [অনুসরণমূলক প্রশ্ন]
    সাবিনা: [ব্যাখ্যা]
    [চলতে থাকুক...]
    """
    
    script_response = genai_client.models.generate_content(
        model=configuration.synthesis_model,
        contents=script_prompt,
        config={"temperature": configuration.podcast_script_temperature}
    )
    # Defensive: check for valid response
    if not script_response or not script_response.candidates or not script_response.candidates[0].content or not script_response.candidates[0].content.parts:
        raise RuntimeError("Gemini did not return a valid podcast script.")
    podcast_script = script_response.candidates[0].content.parts[0].text
    
    # Step 2: Generate TTS audio
    tts_prompt = f"TTS the following conversation in Bengali between রাহুল and সাবিনা:\n{podcast_script}"
    
    # Gemini TTS currently does not support multi-speaker config via public API.
    # Use a single Bengali voice for the whole podcast.
    response = genai_client.models.generate_content(
        model=configuration.tts_model,
        contents=tts_prompt,
        config={
            "response_modalities": ["AUDIO"],
            "speech_config": {
                "voice_config": {
                    "prebuilt_voice_config": {
                        "voice_name": configuration.mike_voice  # Set to a Bengali voice in configuration.py
                    }
                }
            }
        }
    )
    # Defensive: check for valid audio response
    if not response or not response.candidates or not response.candidates[0].content or not response.candidates[0].content.parts or not hasattr(response.candidates[0].content.parts[0], 'inline_data') or response.candidates[0].content.parts[0].inline_data is None or not hasattr(response.candidates[0].content.parts[0].inline_data, 'data'):
        raise RuntimeError("Gemini did not return valid TTS audio data.")
    audio_data = response.candidates[0].content.parts[0].inline_data.data
    wave_file(filename, audio_data, configuration.tts_channels, configuration.tts_rate, configuration.tts_sample_width)
    
    print(f"Podcast saved as: {filename}")
    return podcast_script, filename


def create_research_report(topic, search_text, video_text, search_sources_text, video_url, configuration=None):
    """Create a comprehensive research report by synthesizing search and video content in Bengali"""
    
    # Use default values if no configuration provided
    if configuration is None:
        from agent.configuration import Configuration
        configuration = Configuration()
    
    # Step 1: Create synthesis using Gemini
    synthesis_prompt = f"""
    আপনি একজন গবেষণা বিশ্লেষক। আমি "{topic}" বিষয়ক তথ্য দুটি উৎস থেকে সংগ্রহ করেছি:

    অনুসন্ধান ফলাফল:
    {search_text}

    ভিডিও বিষয়বস্তু:
    {video_text}

    দয়া করে বাংলায় একটি সংক্ষিপ্ত ও সমন্বিত প্রতিবেদন তৈরি করুন, যেখানে:
    ১. উভয় উৎস থেকে মূল বিষয় ও অন্তর্দৃষ্টি চিহ্নিত করা হবে
    ২. পরিপূরক বা বিপরীত দৃষ্টিভঙ্গি থাকলে তা তুলে ধরা হবে
    ৩. এই মাল্টিমোডাল গবেষণার ভিত্তিতে সামগ্রিক বিশ্লেষণ থাকবে
    ৪. প্রতিবেদনটি সংক্ষিপ্ত কিন্তু তথ্যবহুল (৩-৪ অনুচ্ছেদ)

    উভয় উৎসের সেরা অন্তর্দৃষ্টি একত্রিত করে একটি সুসংহত বিবরণ দিন। প্রতিবেদনটি সম্পূর্ণ বাংলায় লিখুন।
    """
    
    synthesis_response = genai_client.models.generate_content(
        model=configuration.synthesis_model,
        contents=synthesis_prompt,
        config={
            "temperature": configuration.synthesis_temperature,
        }
    )
    # Defensive: check for valid synthesis response
    if not synthesis_response or not synthesis_response.candidates or not synthesis_response.candidates[0].content or not synthesis_response.candidates[0].content.parts:
        raise RuntimeError("Gemini did not return a valid research synthesis.")
    synthesis_text = synthesis_response.candidates[0].content.parts[0].text
    
    # Step 2: Create markdown report in Bengali
    report = f"""# গবেষণা প্রতিবেদন: {topic}

## সারসংক্ষেপ

{synthesis_text}

## ভিডিও সূত্র
- **URL**: {video_url}

## অতিরিক্ত সূত্রসমূহ
{search_sources_text}

---
*ওয়েব অনুসন্ধান ও ভিডিও বিশ্লেষণ সমন্বিত মাল্টিমোডাল AI গবেষণার মাধ্যমে প্রতিবেদনটি তৈরি হয়েছে*
"""
    
    return report, synthesis_text