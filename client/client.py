import socket, json

HOST = '127.0.0.1'
PORT = 9009

def send_json(sock, obj):
    sock.sendall((json.dumps(obj)+'\n').encode())

def recv_json(sock):
    data = b''
    while b'\n' not in data:
        part = sock.recv(4096)
        if not part: return None
        data += part
    line, _, _ = data.partition(b'\n')
    return json.loads(line.decode())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        name = input("Nhập tên của bạn: ")
        send_json(s, {"type":"join", "player": name})
        print(recv_json(s))

        send_json(s, {"type":"join_queue"})
        print("Đang chờ đối thủ...")

        while True:
            msg = recv_json(s)
            if not msg: break
            t = msg.get("type")
            if t == "match_found":
                print("Đã tìm thấy đối thủ:", msg["opponent"])
            elif t == "request_move":
                move = input("Chọn (rock/paper/scissors): ")
                send_json(s, {"type":"move", "move": move})
            elif t == "round_result":
                print(f"Kết quả: Bạn {msg['result']} (Bạn: {msg['your_move']} - Đối thủ: {msg['opponent_move']})")
            elif t == "game_over":
                print("Trò chơi kết thúc!", msg)
                break

if __name__ == "__main__":
    main()
