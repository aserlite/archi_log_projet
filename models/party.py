import secrets

class Party:
    def __init__(self, id_soiree, nom, id_organisateur, date, code, status):
        self.id_soiree = id_soiree
        self.nom = nom
        self.id_organisateur = id_organisateur
        self.date = date
        self.code = code
        self.status = status

    def __repr__(self):
        return (f"Party(id_soiree={self.id_soiree}, nom={self.nom}, "
                f"id_organisateur={self.id_organisateur}, date={self.date}, "
                f"code={self.code}, status={self.status})")

    @staticmethod
    def create(cursor, nom, id_organisateur, date, status="ongoing"):
        code = secrets.token_urlsafe(6)
        cursor.execute(
            "INSERT INTO soiree (nom, id_organisateur, date, code, status) VALUES (%s, %s, %s, %s, %s)",
            (nom, id_organisateur, date, code, status)
        )
        return cursor.lastrowid, code

    @staticmethod
    def get_by_code(cursor, code):
        cursor.execute("SELECT * FROM soiree WHERE code = %s", (code,))
        row = cursor.fetchone()
        if row:
            return Party(*row)
        return None

    @staticmethod
    def get_by_id(cursor, party_id):
        cursor.execute("SELECT * FROM soiree WHERE id_soiree = %s", (party_id,))
        row = cursor.fetchone()
        if row:
            return Party(*row)
        return None

    @staticmethod
    def get_by_id_organisateur(cursor, id_organisateur):
        cursor.execute("SELECT * FROM soiree WHERE id_organisateur = %s", (id_organisateur,))
        rows = cursor.fetchall()
        if rows:
            return [Party(*row) for row in rows]
        return None