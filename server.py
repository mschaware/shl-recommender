import os
from streamlit.web import cli as stcli
import sys

if __name__ == '__main__':
    # Adjust the path for assessments_with_embeddings.pkl if needed
    os.environ["STREAMLIT_SERVER_PORT"] = "3000"
    sys.argv = ["streamlit", "run", "app.py", "--server.port=3000"]
    sys.exit(stcli.main())