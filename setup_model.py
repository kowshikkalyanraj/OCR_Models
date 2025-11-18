#!/usr/bin/env python3
"""
Setup script to ensure model is downloaded and pre-loaded.
This script:
1. Checks if the model exists
2. Downloads it if not present
3. Pre-warms the model by making a test call
4. Sets up keep-alive for faster subsequent calls
"""

import subprocess
import sys
import time
import ollama
from ai_extractor import OLLAMA_MODEL, test_ollama_connection

def check_model_exists(model_name):
    """Check if the model is already downloaded."""
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=10)
        if model_name in result.stdout:
            return True
        return False
    except Exception as e:
        print(f"⚠️ Error checking models: {e}")
        return False

def pull_model(model_name):
    """Download the model using Ollama."""
    print(f"📥 Downloading model: {model_name}")
    print("⏳ This may take a few minutes depending on your internet speed...")
    
    try:
        # Run ollama pull command
        process = subprocess.Popen(
            ['ollama', 'pull', model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Stream output
        for line in process.stdout:
            print(line, end='')
        
        process.wait()
        
        if process.returncode == 0:
            print(f"\n✅ Model '{model_name}' downloaded successfully!")
            return True
        else:
            error = process.stderr.read()
            print(f"\n❌ Error downloading model: {error}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def prewarm_model(model_name):
    """Pre-warm the model by making a test call."""
    print(f"\n🔥 Pre-warming model: {model_name}")
    print("⏳ Making initial test call to load model into memory...")
    
    try:
        start_time = time.time()
        
        # Make a simple test call
        test_text = "test, 123 main st, new york, ny 10001, john doe"
        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    'role': 'system',
                    'content': 'Extract recipient name and address from OCR. Return JSON only.'
                },
                {
                    'role': 'user',
                    'content': f'Extract from: {test_text}'
                }
            ],
            options={
                'num_predict': 100,
                'temperature': 0.1,
            }
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Model pre-warmed in {elapsed:.2f} seconds")
        print(f"💡 Model is now loaded in memory and ready for fast inference")
        return True
    except Exception as e:
        print(f"⚠️ Pre-warming failed: {e}")
        print(f"💡 Model will load on first use (may take 3-5 seconds)")
        return False

def setup_keep_alive():
    """Provide instructions for setting up keep-alive."""
    print("\n" + "="*60)
    print("📝 SETUP INSTRUCTIONS FOR OPTIMAL PERFORMANCE")
    print("="*60)
    print("\n1. Set OLLAMA_KEEP_ALIVE environment variable:")
    print("   macOS/Linux:")
    print("   export OLLAMA_KEEP_ALIVE=5m")
    print("\n   To make it permanent, add to ~/.zshrc or ~/.bashrc:")
    print("   echo 'export OLLAMA_KEEP_ALIVE=5m' >> ~/.zshrc")
    print("   source ~/.zshrc")
    print("\n2. Or set it before running your script:")
    print("   OLLAMA_KEEP_ALIVE=5m python main.py")
    print("\n" + "="*60)

def main():
    """Main setup function."""
    print("🚀 OCR Label Extractor - Model Setup")
    print("="*60)
    print(f"Model: {OLLAMA_MODEL}\n")
    
    # Step 1: Check if Ollama is running
    print("📋 Step 1: Checking Ollama connection...")
    if not test_ollama_connection(OLLAMA_MODEL):
        print("❌ Ollama is not running. Please start it first:")
        print("   ollama serve")
        print("\n   Or if using Homebrew:")
        print("   brew services start ollama")
        sys.exit(1)
    print("✅ Ollama is running\n")
    
    # Step 2: Check if model exists
    print(f"📋 Step 2: Checking if model '{OLLAMA_MODEL}' is installed...")
    if check_model_exists(OLLAMA_MODEL):
        print(f"✅ Model '{OLLAMA_MODEL}' is already installed")
    else:
        print(f"❌ Model '{OLLAMA_MODEL}' is not installed")
        response = input(f"\n❓ Download model '{OLLAMA_MODEL}' now? (y/n): ").strip().lower()
        if response == 'y':
            if not pull_model(OLLAMA_MODEL):
                print("❌ Failed to download model")
                sys.exit(1)
        else:
            print("⏭️  Skipping model download")
            print("💡 You can download it later with: ollama pull " + OLLAMA_MODEL)
            sys.exit(0)
    
    # Step 3: Pre-warm the model
    print(f"\n📋 Step 3: Pre-warming model...")
    prewarm_model(OLLAMA_MODEL)
    
    # Step 4: Provide keep-alive instructions
    setup_keep_alive()
    
    print("\n✅ Setup complete!")
    print("\n🎯 Next steps:")
    print("   1. Set OLLAMA_KEEP_ALIVE=5m (see instructions above)")
    print("   2. Run: python main.py")
    print("   3. Model is ready for fast inference (<2 seconds)")

if __name__ == '__main__':
    main()

