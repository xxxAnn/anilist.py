import socket
import re
import webbrowser

pat = re.compile(r'\?code=(.*?)(\&|\r| |\n)')

def get_code(client_id):
    webbrowser.open(f"https://anilist.co/api/v2/oauth/authorize?client_id={client_id}&redirect_uri=http://127.0.0.1:8000/&response_type=code", autoraise=True)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 8000))
        s.listen()
        conn, _ = s.accept()
        code = None
        data = conn.recv(1024)
        if not data:
            return code
        
        conn.send("HTTP/1.1 200 OK\n".encode())
        conn.send("Content-Type: text/html\n\n".encode())
        conn.send("\n".encode())
        conn.send("""
            <html>
                <body>
                    <h1>Auth completed</h1>
                </body>
            </html>
        """.encode())
        conn.close()

        code = pat.findall(data.decode('utf-8'))[0][0]
        
    return code

        
