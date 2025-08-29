from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
import os

HOST = "0.0.0.0"
PORT = 8000
# Directory to save uploaded files
UPLOAD_DIR = "uploaded_files"

HTTP_STATUS_200_OK = 200
HTTP_STATUS_400_BAS_REQUEST = 400
HTTP_STATUS_405_NOT_ALLOWED = 405
HTTP_STATUS_500_INTERNAL_SERVER_ERROR = 500


class HttpFormFileUploadRequestHandler(BaseHTTPRequestHandler):

    def _send_response(self, status: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        content_type = self.headers.get("Content-Type", "")

        if not content_type.startswith("multipart/form-data"):
            self._send_response(
                HTTP_STATUS_405_NOT_ALLOWED,
                b"Method Not Allowed or Invalid Content-Type",
            )
            return

        # Handle multipart/form-data for file uploads
        try:
            # Read the content length
            content_length = int(self.headers["Content-Length"])
            # Read the raw POST data
            post_data = self.rfile.read(content_length)

            # Find the boundary string
            boundary = content_type.split("boundary=")[1].encode()

            # Split the data by boundary
            parts = post_data.split(b"--" + boundary)

            # Iterate through parts to find the file
            for part in parts:
                if b"filename=" not in part:
                    continue

                # Extract filename and content
                headers_end_index = part.find(b"\r\n\r\n")
                if headers_end_index == -1:
                    continue

                headers = part[:headers_end_index].decode("utf-8")
                content = part[headers_end_index + 4 :]

                # Extract filename
                filename_start = headers.find('filename="') + len('filename="')
                filename_end = headers.find('"', filename_start)
                filename = headers[filename_start:filename_end]

                # Create the upload directory if it doesn't exist
                os.makedirs(UPLOAD_DIR, exist_ok=True)
                filepath = os.path.join(UPLOAD_DIR, filename)

                # Write the file content
                with open(filepath, "wb") as f:
                    f.write(
                        content.strip(b"\r\n--")
                    )  # Remove trailing boundary and newlines

                self._send_response(
                    HTTP_STATUS_200_OK,
                    f"File '{filename}' uploaded successfully.".encode(),
                )
                return

            self._send_response(
                HTTP_STATUS_400_BAS_REQUEST,
                b"No file found in the upload.",
            )

        except Exception as e:
            self._send_response(
                HTTP_STATUS_500_INTERNAL_SERVER_ERROR,
                f"Error processing upload: {e}".encode(),
            )

    def do_GET(self):
        self._send_response(
            HTTP_STATUS_200_OK,
            b"""
        <!DOCTYPE html>
        <html>
        <head><title>Upload File</title></head>
        <body>
            <h1>Upload a File</h1>
            <form action="/" method="post" enctype="multipart/form-data">
                <input type="file" name="uploaded_file">
                <input type="submit" value="Upload">
            </form>
        </body>
        </html>
        """,
        )


with TCPServer((HOST, PORT), HttpFormFileUploadRequestHandler) as httpd:
    print(f"Serving at port {HOST}:{PORT}")
    print(f"Uploaded files will be saved in: {os.path.abspath(UPLOAD_DIR)}")
    httpd.serve_forever()
