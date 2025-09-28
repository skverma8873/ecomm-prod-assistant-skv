import subprocess
import sys
import time

# Define packages in small batches to avoid memory issues
batches = [
    ["beautifulsoup4==4.13.5", "html5lib==1.1", "lxml==6.0.1"],
    ["python-dotenv==1.1.1", "python-multipart==0.0.20", "jinja2==3.1.6"],
    ["fastapi==0.116.1", "uvicorn==0.35.0"],
    ["selenium==4.35.0", "undetected-chromedriver==3.5.5"],
    ["structlog==25.4.0", "ddgs==9.6.0"],
    ["langchain-core==0.3.75"],
    ["langchain==0.3.27"],
    ["langchain-astradb==0.6.1", "langchain-google-genai==2.1.8"],
    ["langchain-groq==0.3.6", "langchain-openai==0.3.32"],
    ["langchain-mcp-adapters==0.1.10", "mcp==1.14.0"],
    ["langgraph==0.6.7"],
    ["ragas==0.3.4"],
    ["streamlit==1.49.1"]
]

def install_batch(packages):
    """Install a batch of packages with memory-efficient options"""
    cmd = [
        sys.executable, "-m", "pip", "install", 
        "--no-cache-dir",  # Don't use cache to save memory
        "--no-build-isolation",  # Reduce memory usage
        "--disable-pip-version-check"  # Skip version check
    ] + packages
    
    print(f"Installing: {', '.join(packages)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✓ Successfully installed: {', '.join(packages)}")
            return True
        else:
            print(f"✗ Failed to install: {', '.join(packages)}")
            print(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ Timeout installing: {', '.join(packages)}")
        return False
    except Exception as e:
        print(f"✗ Exception installing {', '.join(packages)}: {e}")
        return False

def main():
    print("Starting batch installation of requirements...")
    failed_batches = []
    
    for i, batch in enumerate(batches, 1):
        print(f"\n--- Batch {i}/{len(batches)} ---")
        if not install_batch(batch):
            failed_batches.append(batch)
        
        # Small delay between batches to let system recover
        time.sleep(2)
    
    # Install the local package
    print(f"\n--- Installing local package ---")
    if not install_batch(["-e", "."]):
        failed_batches.append(["-e", "."])
    
    # Report results
    print(f"\n{'='*50}")
    print("INSTALLATION SUMMARY")
    print(f"{'='*50}")
    
    if not failed_batches:
        print("✅ All packages installed successfully!")
    else:
        print(f"❌ {len(failed_batches)} batch(es) failed:")
        for batch in failed_batches:
            print(f"  - {', '.join(batch)}")
        print("\nYou may need to install these manually or one at a time.")

if __name__ == "__main__":
    main()