import asyncio
import os
from dotenv import load_dotenv
import sys

# --- 1. Set up environment ---
print("🚀 Initializing...")

# Load .env file from the project root, which is one level up
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if not os.path.exists(dotenv_path):
    print("❌ Error: .env file not found. Please create one with your GEMINI_API_KEY.")
    sys.exit(1)
load_dotenv(dotenv_path=dotenv_path)

# Verify that the key is loaded
if not os.getenv("GEMINI_API_KEY"):
    print("❌ Error: GEMINI_API_KEY not found in .env file or environment.")
    sys.exit(1)

# --- 2. Import application logic AFTER loading the environment ---
try:
    from bengali_climate_change import run_research
except ImportError:
    print("❌ Error: Could not import 'run_research'. Make sure 'bengali_climate_change.py' exists in the examples folder.")
    sys.exit(1)


# --- 3. Run the application ---
if __name__ == "__main__":
    print("✅ Environment loaded. Starting Bengali research script...")
    asyncio.run(run_research())
    print("�� Script finished.") 