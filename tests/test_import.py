try:
    import google.generativeai as genai
    print("SUCCESS: google-generativeai imported.")
    print(f"Version: {genai.__version__}")
except Exception as e:
    print(f"FAILURE: {e}")
except ImportError as e:
    print(f"IMPORT FAILURE: {e}")
