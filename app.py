from flask import Flask
from flask import render_template
from database import init_db
from config import Config

from routes.auth_routes import auth_bp
from routes.wallet_routes import wallet_bp
from routes.transaction_routes import transaction_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(wallet_bp)
app.register_blueprint(transaction_bp)


@app.route("/")
def home():
    return "Wallet Backend is Alive"
@app.route("/ui")
def ui():
    return render_template("index.html")


if __name__ == "__main__":
    init_db()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)