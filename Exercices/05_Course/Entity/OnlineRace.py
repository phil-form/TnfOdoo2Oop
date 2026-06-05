import json
import threading
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

from Entity.Car import Car
from Entity.Driver import Driver
from Entity.Race import Race
from Entity.RaceTrack import RaceTrack
from utils.outputs import locked_print


class OnlineRace(Race):
    def __init__(self,
                 name: str,
                 circuit: RaceTrack,
                 nbLap: int,
                 reward: int,
                 available_cars: list[Car]) -> None:
        super().__init__(name, circuit, nbLap, reward)
        self.__available_cars = available_cars
        self.__connections = {}
        self.__conn_lock = threading.Lock()
        self.__race_started = False
        self.__race_started_lock = threading.Lock()
        self.__race_complete = threading.Event()

        self.add_race_end_callback(self.__on_race_end)

        srv = socket(AF_INET, SOCK_STREAM)
        srv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        locked_print("Listening on 56523")
        srv.bind(("0.0.0.0", 56523))
        srv.listen()

        threading.Thread(target=self.__accept_loop, args=(srv,), daemon=True).start()

    def wait_for_completion(self):
        self.__race_complete.wait()

    def __accept_loop(self, srv):
        while True:
            conn, addr = srv.accept()
            locked_print("Connected by", addr)
            threading.Thread(target=self.__handle_client, args=(conn,), daemon=True).start()

    def __handle_client(self, conn):
        buf = b""
        try:
            while b"\n\r" not in buf:
                chunk = conn.recv(1024)
                if not chunk:
                    conn.close()
                    return
                buf += chunk
        except OSError:
            conn.close()
            return

        header, body = buf.decode().split("\n\r", 1)

        if "/add" not in header:
            conn.send(b'{"type":"error","message":"Unknown command"}\n')
            conn.close()
            return

        decoded = json.loads(body)
        driver = Driver(
            name=decoded["name"],
            number=decoded["number"],
            car=self.__available_cars[int(decoded["car"])],
        )
        index = self.addDriver(driver)
        is_host = (index == 0)

        conn_lock = threading.Lock()
        with self.__conn_lock:
            self.__connections[index] = (conn, conn_lock)

        driver.add_lap_callback(self.__broadcast_standings)
        driver.add_sector_callback(self.__broadcast_standings)

        conn.send((json.dumps({
            "type": "joined",
            "nb_lap": self.nbLap,
            "is_host": is_host,
            "n_sectors": max(1, self.circuit.length // 1000),
        }) + "\n").encode())

        self.__broadcast_lobby()

        # stay connected to receive START from the host
        cmd_buf = b""
        while True:
            try:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                cmd_buf += chunk
                while b"\n" in cmd_buf:
                    idx = cmd_buf.index(b"\n")
                    cmd = cmd_buf[:idx].decode().strip()
                    cmd_buf = cmd_buf[idx + 1:]
                    if cmd == "START" and is_host:
                        self.__start_race()
            except OSError:
                break

    def __broadcast_lobby(self):
        players = [d.name for d in self._concurrents]
        self.__broadcast_all(json.dumps({"type": "lobby", "players": players}) + "\n")

    def __start_race(self):
        with self.__race_started_lock:
            if self.__race_started:
                return
            self.__race_started = True
        self.__broadcast_all(json.dumps({"type": "race_started"}) + "\n")
        threading.Thread(target=self.startCourse, daemon=False).start()

    def __broadcast_standings(self, _driver):
        standings = sorted(
            self._concurrents,
            key=lambda d: d.totalTime if d.lapTimes else float("inf"),
        )
        data = [
            {
                "name": d.name,
                "laps": len(d.lapTimes),
                "total": d.totalTime,
                "last_lap": d.get_last_lap_time if d.lapTimes else 0.0,
                "sector": d.current_sector,
                "sector_entry_time": d.sector_entry_time,
                "sector_duration": d.last_sector_duration,
            }
            for d in standings
        ]
        n_sectors = max(1, self.circuit.length // 1000)
        self.__broadcast_all(
            json.dumps({"type": "standings", "n_sectors": n_sectors, "data": data}) + "\n"
        )

    def __on_race_end(self, winner):
        msg = json.dumps({"type": "race_finished", "winner": winner.name}) + "\n"
        with self.__conn_lock:
            entries = list(self.__connections.items())
        for _, (conn, lock) in entries:
            with lock:
                try:
                    conn.send(msg.encode())
                    conn.close()
                except OSError:
                    pass
        self.__race_complete.set()

    def __broadcast_all(self, msg: str):
        with self.__conn_lock:
            entries = list(self.__connections.items())
        for _, (conn, lock) in entries:
            with lock:
                try:
                    conn.send(msg.encode())
                except OSError:
                    pass
