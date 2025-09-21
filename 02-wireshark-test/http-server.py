import http.server
import socketserver
import signal
import threading

HOST = "0.0.0.0"
PORT = 8000
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

    server_thread = threading.Thread(target=server.serve_forever)
    # Allows the main program to exit even if threads are running
    server_thread.daemon = True
    server_thread.start()
    print(f"Serving at port {HOST}:{PORT}")

    # Keep the main thread alive until the server thread finishes
    server_thread.join()
    print("Bye!")
