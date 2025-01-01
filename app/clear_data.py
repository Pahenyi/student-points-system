import sqlite3

def connect_db():
    """Conectar a la base de datos SQLite."""
    return sqlite3.connect('database/points_system.db')

def clear_table(table_name):
    """Vaciar una tabla específica."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name};")
    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")  # Reiniciar AUTOINCREMENT
    conn.commit()
    conn.close()
    print(f"Tabla '{table_name}' vaciada exitosamente.")

def clear_all_tables():
    """Vaciar todas las tablas en el orden correcto para mantener las claves foráneas."""
    tables = ['points_log', 'students_scores']#, 'reasons', 'students', 'mentors', 'courses']
    conn = connect_db()
    cursor = conn.cursor()

    # Deshabilitar claves foráneas temporalmente
    cursor.execute("PRAGMA foreign_keys = OFF;")

    for table in tables:
        cursor.execute(f"DELETE FROM {table};")
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")  # Reiniciar AUTOINCREMENT

    # Habilitar claves foráneas
    cursor.execute("PRAGMA foreign_keys = ON;")

    conn.commit()
    conn.close()
    print("Todas las tablas han sido vaciadas exitosamente.")

if __name__ == "__main__":
    # Llamar a la función que vacía todas las tablas
    clear_all_tables()
