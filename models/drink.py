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
    def create(cursor, nom, ingredients, alcool=True, degre=None, description=None):
        cursor.execute(
            "INSERT INTO boisson (nom, ingrédients, alcool, degré, description) VALUES (%s, %s, %s, %s, %s)",
            (nom, ingredients, alcool, degre, description)
        )

    @staticmethod
    def delete(cursor, id_boisson):
        cursor.execute("DELETE FROM boisson WHERE id_boisson = %s", (id_boisson,))