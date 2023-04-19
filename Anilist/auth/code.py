import socket
import re
import webbrowser

pat = re.compile(r'\?code=(.*?)(\&|\r| |\n)')

def get_code(client_id):
    webbrowser.open(f"https://anilist.co/api/v2/oauth/authorize?client_id={client_id}&redirect_uri=http://127.0.0.1:8000/&response_type=code", autoraise=True)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 8000))
    s.listen()
    conn, addr = s.accept()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        
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

        try:
            return pat.findall(data.decode('utf-8'))[0][0]
        except:
            break
