from flask import Flask, render_template, jsonify
from flask_cors import CORS
import os
import consul

app = Flask(__name__)
app.secret_key = 'secret123'
CORS(app, supports_credentials=True)
app.config.from_object('config.Config')


# Ruta para renderizar el template index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Ruta para renderizar el template users.html
@app.route('/users')
def users():
    return render_template('users.html')

# Ruta para renderizar el template products.html
@app.route('/products')
def products():
    return render_template('products.html')

# Ruta para renderizar el template orders.html
@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/editUser/<string:id>')
def edit_user(id):
    print("id recibido",id)
    return render_template('editUser.html', id=id)

@app.route('/editProduct/<string:id>')
def edit_product(id):
    print("id recibido",id)
    return render_template('editProduct.html', id=id)

@app.route('/editOrder/<string:id>')
def edit_order(id):
    print("id recibido",id)
    return render_template('editOrder.html', id=id)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

# Register with Consul
def register_frontend():
    """Register frontend service with Consul"""
    consul_host = os.environ.get('CONSUL_HOST', 'consul')
    consul_port = int(os.environ.get('CONSUL_PORT', 8500))

    try:
        c = consul.Consul(host=consul_host, port=consul_port)
        c.agent.service.register(
            'frontend',
            service_id='frontend-5001',
            port=5001,
            check={
                'http': 'http://frontend:5001/health',
                'interval': '10s',
                'timeout': '5s',
                'deregister_critical_service_after': '30s'
            }
        )
        print("Frontend registered with Consul")
    except Exception as e:
        print(f"Could not register with Consul: {e}")

if __name__ == '__main__':
    try:
        register_frontend()
    except Exception as e:
        print(f"Consul registration failed: {e}")
    app.run(host='0.0.0.0', port=5001)
