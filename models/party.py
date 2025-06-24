class Party:
    def __init__(self, id_soiree, nom, durée, date, id_organisateur):
        self.id_soiree = id_soiree
        self.nom = nom
        self.durée = durée
        self.date = date
        self.id_organisateur = id_organisateur

    def __repr__(self):
        return (f"Party(id_soiree={self.id_soiree}, nom={self.nom}, durée={self.durée}, "
                f"date={self.date}, id_organisateur={self.id_organisateur})")

    @staticmethod
    def get_all(cursor):
        cursor.execute("SELECT * FROM soiree")
        rows = cursor.fetchall()
        return [Party(*row) for row in rows]

    @staticmethod
    def create(cursor, nom, durée, date, id_organisateur):
        cursor.execute(
            "INSERT INTO soiree (nom, durée, date, id_organisateur) VALUES (%s, %s, %s, %s)",
            (nom, durée, date, id_organisateur)
        )