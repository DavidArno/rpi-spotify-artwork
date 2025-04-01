import os
import re
from socket import socket
from typing import Callable


class web_server:
    def __init__(self, web_socket: socket, validate_and_store_handler: Callable[[str, str], bool]):
        self._web_socket = web_socket
        self._validate_and_store_handler = validate_and_store_handler
        self._config_setup = False

    def setup_config(self) -> None:
        self._config_setup = False
        while not self._config_setup:
            client, _ = self._web_socket.accept()
            request = client.recv(800)
            response = self._response_to_request(request.decode("utf-8"))
            client.send(response)
            client.close()

    def _response_to_request(self, request: str) -> bytes:
        first_line = request.splitlines()[0]
        requested_item = first_line.split()[1]

        if requested_item.startswith("/web/"):
            return self._respond_with_file(requested_item)
        else:
            return self._respond_with_page(requested_item)

    def _respond_with_file(self, requested_item: str) -> bytes:
        if self._file_exists(requested_item):
            match os.path.splitext(requested_item)[1]:
                case "png":
                    document_type = "image/png"
                case "ico":
                    document_type = "image/x-icon"
                case "css":
                    document_type = "text/css"
                case "webmanifest":
                    document_type = "application/manifest+json"
                case _:
                    document_type = "text/plain"

            file = open(requested_item, "rb")
            data = file.read()
            file.close()
            return self._create_response(document_type, data)
        else:
            return self._not_found(requested_item)

    def _respond_with_page(self, requested_item: str) -> bytes:
        match re.split("[?&]", requested_item):
            case ["/"]:
                contents = self._create_home_page_data()
            case ["/configuration", field1, field2]:
                if self._validate_and_store_handler(field1, field2):
                    contents = self._create_restarting_data()
                    self._config_setup = True
                else:
                    contents = self._something_went_wrong_data()
            case _:
                return self._not_found(requested_item)

        return self._create_response("text/html", contents)

    def _file_exists(self, filename: str):
        try:
            return (os.stat(filename)[0] & 0x4000) == 0
        except OSError:
            return False

    def _create_response(self, document_type: str, content: bytes) -> bytes:
        return (
            f"HTTP/1.1 200 OK\r\nContent-Type: {document_type}\r\nContent-Length: "
            f"{len(content)}\r\n\r\n"
        ).encode('ascii') + content

    def _not_found(self, requested_item: str) -> bytes:
        content = self._create_page_data(f"""
<div class="configure">
  <h1>Resource not found</h1>
    <p>
        Requested item - {requested_item} - could not be found.
    </p>
    <p>
        <a href="http://192.168.4.1">Please return to the home page and try again.</a>
    </p>
</div>
        """)

        return (
            f"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: "
            f"{len(content)}\r\n\r\n{content}"
        ).encode('ascii')

    def _create_home_page_data(self) -> bytes:
        body = """
<div class="configure">
  <h1>Matrix Display WiFi Configuration</h1>
  <form method="get" action="/configuration">
    <p><input type="text" name="ssid" value="" placeholder="SSID (Router name)"></p>
    <p><input type="password" name="password" value="" placeholder="Password"></p>
    <p class="submit"><input type="submit" name="commit" value="Connect"></p>
    <p>
      <label>
        To get started, enter your wifi name (router name) and its password and hit connect. This display will then
        restart and attempt to connect to your wifi.
      </label>
    </p>
    <p>
      <label class="warning">
        If it fails to connect, the display will enable this configuration page once more so you can try again.
      </label>
    </p>
  </form>
</div>
"""
        return self._create_page_data(body).encode('ascii')

    def _something_went_wrong_data(self) -> bytes:
        body = """
<div class="configure">
  <h1>Matrix Display WiFi Configuration</h1>
    <p>
      <label class="error">
        Something went wrong. Please enter both the SSID and password and try again.
      </label>
    </p>
  <form method="get" action="/configuration">
    <p><input type="text" name="ssid" value="" placeholder="SSID (Router name)"></p>
    <p><input type="password" name="password" value="" placeholder="Password"></p>
    <p class="submit"><input type="submit" name="commit" value="Connect"></p>
    <p>
      <label>
        To get started, enter your wifi name (router name) and its password and hit connect. This display will then
        restart and attempt to connect to your wifi.
      </label>
    </p>
    <p>
      <label class="warning">
        If it fails to connect, the display will enable this configuration page once more so you can try again.
      </label>
    </p>
  </form>
</div>
"""
        return self._create_page_data(body).encode('ascii')

    def _create_restarting_data(self) -> bytes:
        body = """
<div class="configure">
  <h1>Matrix Display WiFi Configuration Completed</h1>
    <p>
        The Matrix Display will now restart to attempt to connect to your router.
        If it fails to connect, the display will enable this configuration page once more so you can try again.
    </p>
    <p>
        Please check the display for further information.
    </p>
</div>
"""
        return self._create_page_data(body).encode('ascii')

    def _create_page_data(self, body: str) -> str:
        return f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="styles.css">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="manifest" href="/site.webmanifest">
<style>
</style>
</head>
<body>
{body}
</body>
</html>
"""
