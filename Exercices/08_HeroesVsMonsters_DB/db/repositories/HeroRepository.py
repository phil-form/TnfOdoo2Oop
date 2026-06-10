from db.connection import Database


class HeroRepository:
    @staticmethod
    def find_all() -> list:
        conn = Database.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, description, stamina_bonus, strength_bonus "
                "FROM hero_races ORDER BY id"
            )
            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "stamina_bonus": row[3],
                    "strength_bonus": row[4],
                }
                for row in cur.fetchall()
            ]

    @staticmethod
    def find_by_id(hero_id: int) -> dict | None:
        conn = Database.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, description, stamina_bonus, strength_bonus "
                "FROM hero_races WHERE id = %s",
                (hero_id,),
            )
            row = cur.fetchone()
            if row is None:
                return None
            return {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "stamina_bonus": row[3],
                "strength_bonus": row[4],
            }
