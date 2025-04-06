import os
import sys
from streamlit.web import cli as stcli

if __name__ == '__main__':
    # Use Render's PORT env var, default to 8501 locally
    port = os.getenv("PORT", "8501")
    sys.argv = ["streamlit", "run", "app.py", "--server.port", port]
    sys.exit(stcli.main())