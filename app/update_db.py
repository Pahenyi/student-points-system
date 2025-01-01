import sqlite3

# Conectar a la base de datos
def connect_db():
    return sqlite3.connect('database/points_system.db')

def update_database():
    conn = connect_db()
    cursor = conn.cursor()

    # Agregar la columna 'category' si no existe
    try:
        cursor.execute("ALTER TABLE reasons ADD COLUMN category INTEGER DEFAULT 1;")
        print("Columna 'category' agregada exitosamente.")
    except sqlite3.OperationalError:
        print("La columna 'category' ya existe.")

    # Actualizar las categorías existentes
    cursor.execute("UPDATE reasons SET category = 1 WHERE point_value > 0;")
    cursor.execute("UPDATE reasons SET category = 2 WHERE point_value < 0;")

    # Insertar nuevos motivos de canje
    cursor.execute("""
        INSERT INTO reasons (reason_description, image_url, point_value, category)
        VALUES 
        ('Más tiempo en el desafío', 'time_icon.png', -10, 3),
        ('Elegir la música', 'music_icon.png', -20, 3)
        ON CONFLICT(reason_description) DO NOTHING;
    """)
    print("Motivos de canje agregados.")

    # Confirmar cambios y cerrar conexión
    conn.commit()
    conn.close()
    print("Base de datos actualizada correctamente.")

if __name__ == "__main__":
    update_database()
