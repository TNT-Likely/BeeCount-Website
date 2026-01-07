import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.main import mcp

if __name__ == "__main__":
    try:
        mcp.run()
    except KeyboardInterrupt:
        try:
            print("\nServer shutdown requested by user")
        except (ValueError, OSError):
            pass
    except Exception as e:
        try:
            print(f"Error: {e}")
        except (ValueError, OSError):
            pass
        sys.exit(1)
