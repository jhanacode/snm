from flask import Flask, render_template
from notifypy import Notify
import socket


app = Flask(__name__)

hosts = [
    {"host": "jhanacode.com", "port": 80 },
    {"host": "jhanacode.com", "port": 443}
]

def ping(host, port=80, timeout=2):
    """
    Pings a given host and returns the status code.

    Args:
        host: The domain name or IP address to ping.

    Returns:
        The status code (0 for success, 1 for failure).
    """
    try:
        ip = socket.gethostbyname(host)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.close()
        return 0
    except socket.error:
        notification = Notify(default_application_name="Simple Network Monitor")
        notification.title = f'{host} Down'
        notification.message = f'Connection to {host}:{port} failed.'
        notification.send(block=False)
        return 1
    

@app.route("/")
def hello_world():
    notification = Notify(default_application_name="Simple Network Monitor")
    notification.title = f'Monitoring Enabled'
    notification.message = f'Leave the SNM page open to continue monitoring.'
    notification.send(block=False)
    return render_template('index.html', hosts=hosts)


@app.route("/ping/<host>/<port>")
def ping_host(host, port):
    result = ping(host, int(port), timeout=2)
    return render_template('sites.html', host=host, port=port, result=result)
