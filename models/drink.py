class Drink:
    def __init__(self, id_boisson, nom, ingredients, alcool=True, degre=None, description=None):
        self.id_boisson = id_boisson
        self.nom = nom
        self.ingredients = ingredients
        self.alcool = alcool
        self.degre = degre
        self.description = description

    def __repr__(self):
        return (f"Drink(id_boisson={self.id_boisson}, nom={self.nom}, ingredients={self.ingredients}, "
                f"alcool={self.alcool}, degre={self.degre}, description={self.description})")

    @staticmethod
    def get_all(cursor):
        cursor.execute("SELECT * FROM boisson")
        rows = cursor.fetchall()
        return [Drink(*row) for row in rows]

    @staticmethod
    def get_by_id(cursor, drink_id):
        cursor.execute("SELECT * FROM boisson WHERE id_boisson = %s", (drink_id,))
        row = cursor.fetchone()
        if row:
            return Drink(*row)
        return None

    @staticmethod
    def create(cursor, nom, ingredients, alcool=True, degre=None, description=None):
        cursor.execute(
            "INSERT INTO boisson (nom, ingrédients, alcool, degré, description) VALUES (%s, %s, %s, %s, %s)",
            (nom, ingredients, alcool, degre, description)
        )
        return cursor.lastrowid

    @staticmethod
    def delete(cursor, id_boisson):
        cursor.execute("DELETE FROM boisson WHERE id_boisson = %s", (id_boisson,))

    @staticmethod
    def search_by_name(cursor, query):
        cursor.execute("SELECT id_boisson, nom FROM boisson WHERE nom LIKE %s LIMIT 10", (f"%{query}%",))
        return [{'id': row[0], 'nom': row[1]} for row in cursor.fetchall()]

    @staticmethod
    def get_random(cursor):
        cursor.execute("SELECT id_boisson, nom FROM boisson ORDER BY RAND() LIMIT 1")
        row = cursor.fetchone()
        return [{'id': row[0], 'nom': row[1]}] if row else []

    @staticmethod
    def is_alcoholic(cursor, id_boisson):
        cursor.execute("SELECT alcool FROM boisson WHERE id_boisson = %s", (id_boisson,))
        res = cursor.fetchone()
        return res and res[0] == 1