from flask import Flask, jsonify
from products.controllers.product_controller import product_controller
from db.db import db
from flask_cors import CORS
from consul_helper import register_service

app = Flask(__name__)
app.secret_key = 'secret123'
app.config.from_object('config.Config')
db.init_app(app)

app.register_blueprint(product_controller)
CORS(app, supports_credentials=True)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

# Register with Consul
with app.app_context():
    try:
        register_service(app, 'microProducts', 5003)
    except Exception as e:
        print(f"Could not register with Consul: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
