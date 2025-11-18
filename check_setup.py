#!/usr/bin/env python3
"""
Setup verification script for OCR Label Extractor with AI.
This script checks if all prerequisites are met.
"""

import sys
import subprocess

def check_ollama_installed():
    """Check if Ollama is installed."""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=1)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Ollama is installed: {version}")
            return True
        else:
            print("❌ Ollama is not installed or not accessible")
            return False
    except FileNotFoundError:
        print("❌ Ollama is not installed")
        print("   Install it with: brew install ollama")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False

def check_ollama_running():
    """Check if Ollama service is running."""
    try:
        result = subprocess.run(['curl', '-s', 'http://localhost:11434/api/tags'],
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Ollama service is running")
            return True
        else:
            print("❌ Ollama service is not running")
            print("   Start it with: brew services start ollama")
            print("   Or run: ollama serve")
            return False
    except FileNotFoundError:
        print("❌ curl is not available (needed for checking Ollama)")
        return False
    except Exception as e:
        print(f"❌ Ollama service is not running: {e}")
        print("   Start it with: brew services start ollama")
        print("   Or run: ollama serve")
        return False

def check_model_installed(model='llama3.2'):
    """Check if the specified model is installed."""
    try:
        result = subprocess.run(['ollama', 'list'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            output = result.stdout
            if model in output:
                print(f"✅ Model '{model}' is installed")
                return True
            else:
                print(f"❌ Model '{model}' is not installed")
                print(f"   Install it with: ollama pull {model}")
                return False
        else:
            print("❌ Could not list Ollama models")
            return False
    except Exception as e:
        print(f"❌ Error checking model: {e}")
        return False

def check_python_packages():
    """Check if required Python packages are installed."""
    try:
        import ollama
        print("✅ Python 'ollama' package is installed")
        return True
    except ImportError:
        print("❌ Python 'ollama' package is not installed")
        print("   Install it with: pip install -r requirements.txt")
        return False

def main():
    """Run all checks."""
    print("🔍 Checking OCR Label Extractor Setup...\n")
    
    checks = [
        ("Ollama Installation", check_ollama_installed),
        ("Ollama Service", check_ollama_running),
        ("Model Installation", lambda: check_model_installed('llama3.2')),
        ("Python Packages", check_python_packages),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        result = check_func()
        results.append(result)
    
    print("\n" + "="*50)
    print("📊 Setup Summary:")
    print("="*50)
    
    all_passed = all(results)
    if all_passed:
        print("✅ All prerequisites are met! You're ready to run the script.")
        print("\n🚀 Next steps:")
        print("   1. Activate virtual environment: source venv/bin/activate")
        print("   2. Run the script: python main.py")
        return 0
    else:
        print("❌ Some prerequisites are missing. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

