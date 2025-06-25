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

    @staticmethod
    def get_id_for_user(cursor, user_id):
        cursor.execute("""
                       SELECT id_soiree
                       FROM soiree
                       WHERE (id_organisateur = %s OR id_soiree IN (SELECT id_soiree
                                                                    FROM invitation
                                                                    WHERE id_user = %s))
                         AND status = 'ongoing' LIMIT 1
                       """, (user_id, user_id))
        result = cursor.fetchone()
        return result[0] if result else None

    @staticmethod
    def is_user_invited(cursor, party_id, user_id):
        cursor.execute("""
                       SELECT 1
                       FROM invitation
                       WHERE id_soiree = %s
                         AND id_user = %s
                       """, (party_id, user_id))
        return cursor.fetchone() is not None

    @staticmethod
    def add_invitation(cursor, party_id, user_id):
        cursor.execute("""
                       INSERT INTO invitation (id_soiree, id_user)
                       VALUES (%s, %s)
                       """, (party_id, user_id))

    @staticmethod
    def remove_invitation(cursor, party_id, user_id):
        cursor.execute("""
                       DELETE FROM invitation
                       WHERE id_soiree = %s
                         AND id_user = %s
                       """, (party_id, user_id))

    @staticmethod
    def close(cursor, party_id):
        cursor.execute("""
                       UPDATE soiree
                       SET status = 'finished'
                       WHERE id_soiree = %s
                       """, (party_id,))

    @staticmethod
    def count_user_drinks(cursor, party_id, user_id):
        cursor.execute("""
                       SELECT SUM(quantité) AS total_consommations
                       FROM consommation
                       WHERE id_soiree = %s
                       AND id_user = %s;
                       """, (party_id, user_id))
        result = cursor.fetchone()
        return result[0] if result else 0

    @staticmethod
    def get_participants_in_party(cur, party_id):
        cur.execute("""
            SELECT utilisateur.id_user, utilisateur.pseudo
            FROM invitation
            JOIN utilisateur ON invitation.id_user = utilisateur.id_user
            WHERE invitation.id_soiree = %s
        """, (party_id,))
    
        results = cur.fetchall()
        return [{"id": row[0], "pseudo": row[1]} for row in results]

    @staticmethod
    def get_party_stats(cursor, party_id):
        cursor.execute("""
                       SELECT u.pseudo, COUNT(c.id_user) as count
                       FROM invitation i
                           JOIN utilisateur u
                       ON u.id_user = i.id_user
                           LEFT JOIN consommation c ON c.id_user = u.id_user AND c.id_soiree = %s
                       WHERE i.id_soiree = %s
                       GROUP BY u.id_user
                       UNION
                       SELECT u.pseudo, COUNT(c.id_user) as count
                       FROM soiree s
                           JOIN utilisateur u
                       ON u.id_user = s.id_organisateur
                           LEFT JOIN consommation c ON c.id_user = u.id_user AND c.id_soiree = %s
                       WHERE s.id_soiree = %s
                       GROUP BY u.id_user
                       """, (party_id, party_id, party_id, party_id))
        return [{"user": row[0], "count": row[1]} for row in cursor.fetchall()]
