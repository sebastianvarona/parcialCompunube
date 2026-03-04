import os
import consul
from flask import Flask

def register_service(app: Flask, service_name: str, service_port: int):
    """Register service with Consul"""
    import socket
    consul_host = os.environ.get('CONSUL_HOST', 'consul')
    consul_port = int(os.environ.get('CONSUL_PORT', 8500))

    try:
        c = consul.Consul(host=consul_host, port=consul_port)

        # Get container's hostname/IP for Docker networking
        service_address = socket.gethostbyname(socket.gethostname())

        # Register service with address
        c.agent.service.register(
            service_name,
            service_id=f"{service_name}-{service_port}",
            port=service_port,
            address=service_address,
            check={
                'http': f'http://{service_address}:{service_port}/health',
                'interval': '10s',
                'timeout': '5s',
                'deregister_critical_service_after': '30s'
            }
        )
        print(f"Service {service_name} registered with Consul at {service_address}:{service_port}")
    except Exception as e:
        print(f"Failed to register service with Consul: {e}")

def get_service(service_name: str) -> str:
    """Discover service URL from Consul"""
    consul_host = os.environ.get('CONSUL_HOST', 'consul')
    consul_port = int(os.environ.get('CONSUL_PORT', 8500))

    try:
        c = consul.Consul(host=consul_host, port=consul_port)
        services = c.agent.services()
        for service_id, service in services.items():
            if service['Service'] == service_name:
                address = service.get('Address') or service['Service']
                return f"http://{address}:{service['Port']}"
        return None
    except Exception as e:
        print(f"Consul error: {e}")
        return None
