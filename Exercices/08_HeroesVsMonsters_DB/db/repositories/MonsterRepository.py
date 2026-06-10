from db.connection import Database


class MonsterRepository:
    @staticmethod
    def find_all() -> list:
        conn = Database.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, stamina_bonus, strength_bonus, drops_gold, drops_leather, token "
                "FROM monster_types ORDER BY id"
            )
            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "stamina_bonus": row[2],
                    "strength_bonus": row[3],
                    "drops_gold": row[4],
                    "drops_leather": row[5],
                    "token": row[6],
                }
                for row in cur.fetchall()
            ]

    @staticmethod
    def find_by_id(monster_id: int) -> dict | None:
        conn = Database.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, stamina_bonus, strength_bonus, drops_gold, drops_leather, token "
                "FROM monster_types WHERE id = %s",
                (monster_id,),
            )
            row = cur.fetchone()
            if row is None:
                return None
            return {
                "id": row[0],
                "name": row[1],
                "stamina_bonus": row[2],
                "strength_bonus": row[3],
                "drops_gold": row[4],
                "drops_leather": row[5],
                "token": row[6],
            }
