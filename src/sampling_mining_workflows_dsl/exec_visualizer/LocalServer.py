import http.server
import socketserver
import webbrowser


def serve_html_page(port: int = 8000, html_file: str = "workflow.html"):
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at http://localhost:{port}/{html_file}")
        webbrowser.open(f"http://localhost:{port}/{html_file}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down the server...")
            httpd.shutdown()
            httpd.server_close()


serve_html_page()
