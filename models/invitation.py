class Invitation:
    def __init__(self, id_user, id_soiree, statut):
        self.id_user = id_user
        self.id_soiree = id_soiree
        self.statut = statut

    def __repr__(self):
        return (f"Invitation(id_user={self.id_user}, id_soiree={self.id_soiree}, statut={self.statut})")

    @staticmethod
    def get_all(cursor):
        cursor.execute("SELECT * FROM invitation")
        rows = cursor.fetchall()
        return [Invitation(*row) for row in rows]

    @staticmethod
    def create(cursor, id_user, id_soiree, statut):
        cursor.execute(
            "INSERT INTO invitation (id_user, id_soiree, statut) VALUES (%s, %s, %s)",
            (id_user, id_soiree, statut)
        )