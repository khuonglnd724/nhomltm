# server/leaderboard.py
import json
import os
from typing import Dict, List, Tuple

LEADERBOARD_FILE = os.path.join(os.path.dirname(__file__), "leaderboard.json")

def init_leaderboard():
    """Khởi tạo file leaderboard nếu chưa có."""
    if not os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)

def load_data() -> Dict[str, dict]:
    init_leaderboard()
    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: Dict[str, dict]):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def update_score(player_name: str, result: str):
    """
    Cập nhật điểm cho player_name.
    result: 'win' | 'lose' | 'draw'
    Quy ước điểm: win +3, draw +1, lose +0
    """
    data = load_data()
    if player_name not in data:
        data[player_name] = {"win": 0, "lose": 0, "draw": 0, "score": 0}

    if result == "win":
        data[player_name]["win"] += 1
        data[player_name]["score"] += 3
    elif result == "lose":
        data[player_name]["lose"] += 1
    elif result == "draw":
        data[player_name]["draw"] += 1
        data[player_name]["score"] += 1
    else:
        raise ValueError("result phải là 'win'|'lose'|'draw'")

    save_data(data)

def get_leaderboard() -> List[Tuple[str, dict]]:
    """Trả về danh sách (player, stats) đã sort theo score giảm dần."""
    data = load_data()
    sorted_board = sorted(data.items(), key=lambda x: x[1].get("score", 0), reverse=True)
    return sorted_board

# server/leaderboard.py

def save_leaderboard_file(filename="leaderboard.txt"):
    """Lưu bảng xếp hạng ra file dạng text giống khi in console"""
    board = get_leaderboard()
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n🏆 BẢNG XẾP HẠNG 🏆\n")
        f.write("-" * 48 + "\n")
        f.write(f"{'Hạng':4} {'Tên':20} {'Điểm':6} {'Thắng':6} {'Hòa':6} {'Thua':6}\n")
        f.write("-" * 48 + "\n")
        for i, (player, stats) in enumerate(board, start=1):
            f.write(f"{i:4} {player:20} {stats['score']:6} {stats['win']:6} {stats['draw']:6} {stats['lose']:6}\n")
        f.write("-" * 48 + "\n")


if __name__ == "__main__":
    # Demo test
    init_leaderboard()
    data = load_data()
    if not data:
        update_score("Alice", "win")
        update_score("Bob", "lose")
        update_score("Alice", "draw")
    print_leaderboard()