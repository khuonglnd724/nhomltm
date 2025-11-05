import socket
import random
import time
import threading
from logger import get_logger

HOST = '127.0.0.1'
PORT = 5555

moves = ["rock", "paper", "scissors"]
log = get_logger("TEST")

def client_simulator(id):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        log.info(f"[Client {id}] connected")

        time.sleep(2)

        for i in range(5):
            move = random.choice(moves)
            msg = f"CHOICE:{move}"
            s.send(msg.encode("utf-8"))
            log.info(f"[Client {id}] -> {msg}")

            response = s.recv(2048).decode('utf-8')
            log.info(f"[Client {id}] <- {response}")

            time.sleep(1)

        s.close()
        log.info(f"[Client {id}] closed")
    except Exception as e:
        log.error(f"[Client {id}] ERROR: {e}")

if __name__ == "__main__":
    threads = []
    for i in range(4):
        t = threading.Thread(target=client_simulator, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("TEST FINISHED")
