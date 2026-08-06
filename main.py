import os
import sys
import subprocess

def main():
    """Entry point to run the Streamlit application."""
    # Resolve the absolute path to the app directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app", "app.py")

    if not os.path.exists(app_path):
        print(f"Error: Could not find {app_path}")
        sys.exit(1)

    print("🚀 Starting the Knowledge Graph Explorer...")
    
    # sys.executable ensures we use the Python interpreter from the active virtual environment
    cmd = [sys.executable, "-m", "streamlit", "run", app_path]
    
    try:
        # Run the Streamlit app and wait for it to finish
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()