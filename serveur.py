from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

alertes = []


@app.route('/')
def dashboard():
    chemin = os.path.join(os.path.dirname(__file__), 'dashboard.html')
    return open(chemin, encoding='utf-8').read()

@app.route('/alerte', methods=['POST'])
def recevoir_alerte():
    data = request.json
    data['heure'] = datetime.now().strftime("%H:%M:%S")
    alertes.append(data)
    print(f"ALERTE recue : {data}")
    return jsonify({"status": "ok"})

@app.route('/alertes', methods=['GET'])
def voir_alertes():
    return jsonify(alertes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)