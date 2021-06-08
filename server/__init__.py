load_dotenv(find_dotenv())
BACKEND_URL = os.environ.get("BACKEND_URL")
JWT_SECRET = os.environ.get("JWT_SECRET")

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = JWT_SECRET
jwt = JWTManager(app)

client = MongoClient(BACKEND_URL)
db = client['videosum']
users = db['users']

from server import routes