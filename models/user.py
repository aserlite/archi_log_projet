class User:
    def __init__(self, id_user, nom, prénom, email, password, âge, poids, genre, create_dt, session_token):
        self.id_user = id_user
        self.nom = nom
        self.prénom = prénom
        self.email = email
        self.password = password
        self.âge = âge
        self.poids = poids
        self.genre = genre
        self.create_dt = create_dt
        self.session_token = session_token

    def __repr__(self):
        return (f"User(id_user={self.id_user}, nom={self.nom}, prénom={self.prénom}, "
                f"email={self.email}, password=****, âge={self.âge}, poids={self.poids}, "
                f"genre={self.genre}, create_dt={self.create_dt}, session_token=****)")

    @staticmethod
    def get_all(cursor):
        cursor.execute("SELECT * FROM utilisateur")
        rows = cursor.fetchall()
        return [User(*row) for row in rows]

    @staticmethod
    def create(cursor, nom, prénom, email, password, âge, poids, genre):
        cursor.execute(
            "INSERT INTO utilisateur (nom, prénom, email, password, âge, poids, genre) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (nom, prénom, email, password, âge, poids, genre)
        )

    @staticmethod
    def delete(cursor, id_user):
        cursor.execute("DELETE FROM utilisateur WHERE id_user = %s", (id_user,))