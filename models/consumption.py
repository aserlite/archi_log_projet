class Consumption:
    def __init__(self, id_user, id_soiree, id_boisson, quantité, commentaire, timestamp):
        self.id_user = id_user
        self.id_soiree = id_soiree
        self.id_boisson = id_boisson
        self.quantité = quantité
        self.commentaire = commentaire
        self.timestamp = timestamp

    def __repr__(self):
        return (f"Consumption(id_user={self.id_user}, id_soiree={self.id_soiree}, "
                f"id_boisson={self.id_boisson}, quantité={self.quantité}, "
                f"commentaire={self.commentaire}, timestamp={self.timestamp})")

    @staticmethod
    def get_all(cursor):
        cursor.execute("SELECT * FROM consommation")
        rows = cursor.fetchall()
        return [Consumption(*row) for row in rows]

    @staticmethod
    def create(cursor, id_user, id_soiree, id_boisson, quantité, commentaire):
        cursor.execute(
            "INSERT INTO consommation (id_user, id_soiree, id_boisson, quantité, commentaire) VALUES (%s, %s, %s, %s, %s)",
            (id_user, id_soiree, id_boisson, quantité, commentaire)
        )