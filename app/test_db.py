import sqlite3

def check_database():
    conn = sqlite3.connect('database/points_system.db')
    cursor = conn.cursor()

    # Verificar datos en la tabla 'students'
    cursor.execute("SELECT * FROM students;")
    students = cursor.fetchall()
    print("Estudiantes:", students)

    # Verificar datos en la tabla 'mentors'
    cursor.execute("SELECT * FROM mentors;")
    mentors = cursor.fetchall()
    print("Mentores:", mentors)

    # Verificar datos en la tabla 'reasons'
    cursor.execute("SELECT * FROM reasons;")
    reasons = cursor.fetchall()
    print("Razones:", reasons)

    conn.close()

if __name__ == "__main__":
    check_database()
