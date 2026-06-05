#!/usr/bin/env python3
import argparse
import json
import socket
import sys
import threading
import time

from utils.display import RaceDisplay

SERVER_PORT = 56523

CARS = [
    ("Ferrari",  "F1",   250, 350),
    ("Mercedes", "W12",  240, 340),
    ("Red Bull", "RB16", 245, 345),
]


class RaceClient:

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self.nb_lap = 10
        self.n_sectors = 1
        self.is_host = False
        self.my_name = ""
        self.phase = "lobby"
        self.players = []
        self.standings: list[dict] = []
        self.winner = None
        self._lock = threading.Lock()
        self._buf = b""
        self.sock: socket.socket | None = None

    def setup_and_connect(self):
        print("\n=== OnlineRace ===\n")

        name = ""
        while not name:
            name = input("Nom du pilote    : ").strip()
        self.my_name = name

        while True:
            try:
                number = int(input("Numéro de course : "))
                break
            except ValueError:
                print("  Entrez un entier.")

        print("\nVoitures disponibles :")
        for i, (brand, model, vmin, vmax) in enumerate(CARS):
            print(f"  {i}  {brand} {model:<10}  {vmin}–{vmax} km/h")

        car = -1
        while not 0 <= car < len(CARS):
            try:
                car = int(input(f"\nVotre voiture (0–{len(CARS) - 1}) : "))
            except ValueError:
                print("  Entrez un entier.")

        print(f"\nConnexion au serveur {self._host}:{self._port}...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self._host, self._port))

        payload = json.dumps({"name": name, "number": number, "car": car})
        self.sock.send(f"POST /add\n\r{payload}".encode())

        line = self._read_line()
        if line is None:
            raise ConnectionError("Connexion fermée par le serveur")
        msg = json.loads(line)
        if msg.get("type") != "joined":
            raise ConnectionError(f"Réponse inattendue : {line}")

        self.nb_lap = msg["nb_lap"]
        self.is_host = msg["is_host"]
        self.n_sectors = msg.get("n_sectors", 1)

        role = "hôte" if self.is_host else "pilote"
        print(f"Connecté en tant que {role} '{name}' — {self.nb_lap} tours")
        time.sleep(0.4)

    def _read_line(self) -> str | None:
        while b"\n" not in self._buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                return None
            self._buf += chunk
        idx = self._buf.index(b"\n")
        line = self._buf[:idx].decode().strip()
        self._buf = self._buf[idx + 1:]
        return line

    def start_recv(self):
        threading.Thread(target=self._recv_loop, daemon=True).start()

    def _recv_loop(self):
        while True:
            line = self._read_line()
            if line is None:
                with self._lock:
                    if self.phase != "finished":
                        self.phase = "finished"
                break
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue

            with self._lock:
                t = msg.get("type")
                if t == "lobby":
                    self.players = msg["players"]
                elif t == "race_started":
                    self.phase = "racing"
                elif t == "standings":
                    self.n_sectors = msg.get("n_sectors", self.n_sectors)
                    now = time.time()
                    prev = {d["name"]: d for d in self.standings}
                    color_index = {name: i for i, name in enumerate(self.players)}
                    for entry in msg["data"]:
                        # server sends game-time seconds; wall-clock duration is /60
                        entry["sector_duration"] = entry.get("sector_duration", 0) / 60
                        entry["color"] = color_index.get(entry["name"], 0)
                        n = entry["name"]
                        if n in prev and prev[n]["laps"] == entry["laps"]:
                            entry["update_time"] = prev[n].get("update_time", now)
                        else:
                            entry["update_time"] = now
                    self.standings = msg["data"]
                elif t == "race_finished":
                    self.phase = "finished"
                    self.winner = msg["winner"]

    def send_start(self):
        try:
            self.sock.send(b"START\n")
        except OSError:
            pass

    def get_state(self) -> dict:
        with self._lock:
            return {
                "nb_lap":    self.nb_lap,
                "n_sectors": self.n_sectors,
                "is_host":   self.is_host,
                "my_name":   self.my_name,
                "phase":     self.phase,
                "players":   list(self.players),
                "standings": list(self.standings),
                "winner":    self.winner,
            }


parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1")
parser.add_argument("--port", type=int, default=SERVER_PORT)
args = parser.parse_args()

client = RaceClient(args.host, args.port)
try:
    client.setup_and_connect()
except (ConnectionError, OSError) as e:
    print(f"\nErreur : {e}", file=sys.stderr)
    sys.exit(1)

RaceDisplay(client).start()
