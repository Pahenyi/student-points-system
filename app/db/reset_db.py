import sqlite3

def reset_database():
    conn = sqlite3.connect('database/points_system.db')
    cursor = conn.cursor()

    # Eliminar tablas existentes

    cursor.execute("DROP TABLE IF EXISTS reasons;")



    cursor.execute("""
        CREATE TABLE reasons (
            reason_id INTEGER PRIMARY KEY,
            reason_description TEXT NOT NULL,
            image_url TEXT,
            point_value INTEGER NOT NULL,
            course_id_exclusive INTEGER,
            category INTEGER DEFAULT 1,
            FOREIGN KEY (course_id_exclusive) REFERENCES courses(course_id)
        );
    """)


    cursor.executemany("""
        INSERT INTO reasons (reason_description, image_url, point_value, category) VALUES (?, ?, ?, ?);
    """, [
        ("Buen Comportamiento", "positive.png", 10, 1),
        ("Tarea Extra", "task.png", 15, 1),
        ("Interrumpir Clase", "interrupt.png", -5, 2),
        ("Llegar Tarde", "late.png", -10, 2),
        ("Más tiempo en el desafío", "time_icon.png", -10, 3),
        ("Elegir la música", "music_icon.png", -20, 3)
    ])

    conn.commit()
    conn.close()
    print("Base de datos reiniciada con éxito.")

if __name__ == "__main__":
    reset_database()
