import asyncio
import os
import sys

# Add src to path, which is now one level up
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from langgraph.checkpoint.memory import MemorySaver
from agent.graph import create_compiled_graph


async def run_research():
    """
    Runs the Bengali multi-modal research and podcast generation workflow
    with a sample topic and saves the output.
    """
    # --- Configuration ---
    BENGALI_TOPIC = "জলবায়ু পরিবর্তন এবং বাংলাদেশে এর প্রভাব"
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')

    # --- Setup ---
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    graph = create_compiled_graph()
    memory = MemorySaver()
    config = {
        "configurable": {
            "thread_id": "bengali-research-thread-1",
            "checkpoint": memory,
        }
    }
    
    # --- Define Research Input ---
    inputs = {
        "topic": BENGALI_TOPIC,
        "video_url": None, # You can add a relevant Bengali YouTube video URL here
    }

    print(f"🔬 Starting research for topic: '{BENGALI_TOPIC}'")

    # --- Run the Graph ---
    try:
        # The graph is asynchronous, so we use 'ainvoke'
        final_state = await graph.ainvoke(inputs, config=config)

        # --- Process and Save Outputs ---
        report = final_state.get("report", "No report generated.")
        podcast_script = final_state.get("podcast_script", "No podcast script generated.")
        podcast_filename_in_memory = final_state.get("podcast_filename")

        # Define output paths
        report_path = os.path.join(OUTPUT_DIR, "bengali_research_report.md")
        script_path = os.path.join(OUTPUT_DIR, "bengali_podcast_script.txt")
        
        # Save the report and script
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"📄 Bengali research report saved to: {report_path}")
        
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(podcast_script)
        print(f"🎙️ Bengali podcast script saved to: {script_path}")

        # Move the generated podcast audio to the output directory
        if podcast_filename_in_memory and os.path.exists(podcast_filename_in_memory):
            # Correctly join paths for the destination
            podcast_dest_path = os.path.join(OUTPUT_DIR, os.path.basename(podcast_filename_in_memory))
            os.rename(podcast_filename_in_memory, podcast_dest_path)
            print(f"🎧 Bengali podcast audio saved to: {podcast_dest_path}")
        else:
            print("⚠️ Podcast audio file not found.")

    except Exception as e:
        print(f"An error occurred: {e}") 