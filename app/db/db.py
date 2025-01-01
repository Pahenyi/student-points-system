import sqlite3
import os



# Crear conexión y base de datos
def create_database():
    
    os.makedirs('../database', exist_ok=True)
    conn = sqlite3.connect('../database/points_system.db')
    cursor = conn.cursor()

    # Leer y ejecutar el script SQL
    with open('sql/schema.sql', 'r') as f:
        cursor.executescript(f.read())
    
    print("Base de datos creada exitosamente.")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print(os.getcwd())
    create_database()
