import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import WEB_HOST, WEB_PORT, WEB_DEBUG, C2_HOST, C2_PORT

C2_API_URL = f"http://{C2_HOST}:{C2_PORT}"

app = Flask(__name__)

if __name__ == '__main__':
    app.run(host=WEB_HOST, port=WEB_PORT, debug=WEB_DEBUG)