import socket
import json

HOST = '127.0.0.1'
PORT = 9009

class client_logic:
    """Lớp xử lý kết nối mạng với server"""
    
    def __init__(self):
        self.sock = None
        self.connected = False
    
    def connect(self, host=HOST, port=PORT):
        """Kết nối tới server"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            self.connected = True
            return True
        except Exception as e:
            self.connected = False
            raise e
    
    def send_json(self, obj):
        """Gửi dữ liệu JSON tới server"""
        if self.sock and self.connected:
            try:
                self.sock.sendall((json.dumps(obj) + "\n").encode())
                return True
            except Exception as e:
                self.connected = False
                raise e
        return False
    
    def recv_json(self):
        """Nhận dữ liệu JSON từ server"""
        if not self.sock or not self.connected:
            return None
        
        try:
            data = b""
            while b"\n" not in data:
                part = self.sock.recv(4096)
                if not part:
                    self.connected = False
                    return None
                data += part
            line, _, _ = data.partition(b"\n")
            return json.loads(line.decode())
        except Exception as e:
            self.connected = False
            raise e
    
    def disconnect(self):
        """Ngắt kết nối"""
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
        self.connected = False
        self.sock = None
    
    def is_connected(self):
        """Kiểm tra trạng thái kết nối"""
        return self.connected