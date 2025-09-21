import http.server
import ssl
import signal
import threading
import socketserver

HOST = "0.0.0.0"
PORT = 8443
CERTFILE = "cert.pem"
KEYFILE = "key.pem"
HTTP_STATUS_200_OK = 200


class BasicHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTP_STATUS_200_OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello from Basic Http Request Handler\n")


with socketserver.TCPServer((HOST, PORT), BasicHttpRequestHandler) as server:

    def signal_handler(signum, frame):
        print(f"Received signal {signum}, shutting down server gracefully...")
        server.shutdown()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Wrap the socket with SSL
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
    server.socket = context.wrap_socket(server.socket, server_side=True)

    server_thread = threading.Thread(target=server.serve_forever)
    # Allows the main program to exit even if threads are running
    server_thread.daemon = True
    server_thread.start()
    print(f"Serving at port {HOST}:{PORT}")

    # Keep the main thread alive until the server thread finishes
    server_thread.join()
    print("Bye!")
