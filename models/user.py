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
    def create(cursor, nom, prénom, email, password, âge, poids, genre, session_token):
        cursor.execute(
            "INSERT INTO utilisateur (nom, prénom, email, password, âge, poids, genre, session_token) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (nom, prénom, email, password, âge, poids, genre, session_token)
        )

    @staticmethod
    def get_id_by_email(cursor, email):
        cursor.execute("SELECT id_user FROM utilisateur WHERE email = %s", (email,))
        row = cursor.fetchone()
        return row[0] if row else None

    @staticmethod
    def get_by_email(cursor, email):
        cursor.execute("SELECT * FROM utilisateur WHERE email = %s", (email,))
        row = cursor.fetchone()
        return User(*row) if row else None

    @staticmethod
    def get_by_id(cursor, id_user):
        cursor.execute("SELECT * FROM utilisateur WHERE id_user = %s", (id_user,))
        row = cursor.fetchone()
        return User(*row) if row else None

    @staticmethod
    def update_session_token(cursor, id_user, session_token):
        cursor.execute("UPDATE utilisateur SET session_token = %s WHERE id_user = %s", (session_token, id_user))

    @staticmethod
    def get_session_token(cursor, id_user):
        cursor.execute("SELECT session_token FROM utilisateur WHERE id_user = %s", (id_user,))
        row = cursor.fetchone()
        return row[0] if row else None

    @staticmethod
    def delete(cursor, id_user):
        cursor.execute("DELETE FROM utilisateur WHERE id_user = %s", (id_user,))

    @staticmethod
    def update_profile(cursor, id_user, nom, prénom, email, âge, poids, genre, password):
        cursor.execute(
            "UPDATE utilisateur SET nom=%s, prénom=%s, email=%s, âge=%s, poids=%s, genre=%s, password=%s WHERE id_user=%s",
            (nom, prénom, email, âge, poids, genre, password, id_user)
        )
