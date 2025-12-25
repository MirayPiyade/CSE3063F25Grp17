import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# Python adds the script's directory to sys.path[0]. Remove it.
if sys.path and sys.path[0] == script_dir:
    sys.path.pop(0)

# Also remove current working directory if present, just in case
if os.getcwd() in sys.path:
    sys.path.remove(os.getcwd())

# Add src/main/python to the beg1inning of sys.path
src_path = os.path.join(script_dir, 'src', 'main', 'python')
sys.path.insert(0, src_path)

try:
    import rag
except ImportError as e:
    print(f"Failed to import rag: {e}", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    from rag.app.rag_cli import main
    main()


