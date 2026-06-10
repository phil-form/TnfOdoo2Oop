from db.connection import Database


class MapRepository:
    @staticmethod
    def find_all() -> list:
        """Returns all maps (display data only, no weights — used for the menu)."""
        conn = Database.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, map_type, display_name, description, "
                "default_size, default_nb_monsters, empty_token "
                "FROM maps ORDER BY id"
            )
            return [
                {
                    "id": row[0],
                    "map_type": row[1],
                    "display_name": row[2],
                    "description": row[3],
                    "default_size": row[4],
                    "default_nb_monsters": row[5],
                    "empty_token": row[6],
                }
                for row in cur.fetchall()
            ]

    @staticmethod
    def find_by_type(map_type: str) -> dict | None:
        """Returns one map including its monster spawn weights."""
        conn = Database.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, map_type, display_name, description, "
                "default_size, default_nb_monsters, empty_token "
                "FROM maps WHERE map_type = %s",
                (map_type,),
            )
            row = cur.fetchone()
            if row is None:
                return None
            map_data = {
                "id": row[0],
                "map_type": row[1],
                "display_name": row[2],
                "description": row[3],
                "default_size": row[4],
                "default_nb_monsters": row[5],
                "empty_token": row[6],
            }
            cur.execute(
                "SELECT monster_type_id, weight "
                "FROM map_monster_weights "
                "WHERE map_id = %s ORDER BY monster_type_id",
                (map_data["id"],),
            )
            map_data["monster_weights"] = [
                {"monster_type_id": r[0], "weight": r[1]}
                for r in cur.fetchall()
            ]
            return map_data
