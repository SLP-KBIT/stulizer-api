from flask import *
from cardinfo import CardInfo
from connect import Connection

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route("/")
def index():
    conn = Connection()
    try:
        conn.check_connect()
    except Exception as e:
        print(e)
    card = CardInfo()
    data = conn.get_data()
    card.update(data['id'], data['name'], data['balance'])
    return jsonify(card.get()), 200

if __name__ == "__main__":
    app.run(port=5000)
