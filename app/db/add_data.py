import sqlite3

def connect_db():
    """Conectar a la base de datos SQLite."""
    return sqlite3.connect('database/points_system.db')

def add_courses():
    """Agregar cursos iniciales."""
    courses = [
        ('ROB001', 'Robótica Básica'),
        ('ROB002', 'Robótica Intermedio'),
        ('VG001', 'Videojuegos Básico - Scratch'),
        ('VG002', 'Videojuegos Básico - Roblox'),
        ('ClubComun', 'Club de Robótica'),
        ('ClubArte', 'Club de Robótica - Arte'),
        ('ClubVel', 'Club de Robótica - Velocistas'),
        ('ClubMusta', 'Club de Robótica - Mustabot')
    ]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO courses (course_id, course_name) VALUES (?, ?);", courses)
    conn.commit()
    conn.close()
    print("Cursos agregados exitosamente.")

def add_mentors():
    """Agregar mentores iniciales."""
    mentors = [
        ('Seba', '/img/seba.png'),
        ('Pau', '/img/pau.png'),
        ('Lukas', '/img/lukas.png'),
        ('Maty', '/img/maty.png'),
        ('Sofi', '/img/sofi.png'),
        ('Emilio', '/img/emilio.png')
    ]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO mentors (mentor_name, image_url) VALUES (?, ?);", mentors)
    conn.commit()
    conn.close()
    print("Mentores agregados exitosamente.")

def add_students():
    """Agregar estudiantes iniciales."""
    students = [
        ('Ana', 'García', 'F', '123678-9', 'ROB001'),
        ('Pedro', 'Soto', 'M', '8765421-0', 'ROB001'),
        ('Luis', 'Martínez', 'M', '9875432-1', 'VG001'),
        ('María', 'López', 'F', '2345679-2', 'VG001'),
        ('Sofía', 'Hernández', 'F', '112344-5', 'ROB002'),
        ('Diego', 'Gómez', 'M', '5544322-1', 'ROB002'),
        ('Juan', 'Pérez', 'M', '5432178-9', 'VG002'),
        ('Carla', 'Torres', 'F', '87521-0', 'VG002'),
        ('Javiera', 'González', 'F', '1234678-9', 'ClubComun'),
        ('Pedro', 'Soto', 'M', '876541-0', 'ClubComun'),
        ('Luis', 'Martínez', 'M', '9765432-1', 'ClubArte'),
        ('María', 'López', 'F', '3456789-2', 'ClubArte'),
        ('Sofía', 'Hernández', 'F', '1123344-5', 'ClubVel'),
        ('Diego', 'Gómez', 'M', '55443322-1', 'ClubVel'),
        ('Juan', 'Pérez', 'M', '5432678-9', 'ClubMusta'),
        ('Carla', 'Torres', 'F', '876521-0', 'ClubMusta')
    ]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO students (first_name, last_name, gender, rut, current_course)
        VALUES (?, ?, ?, ?, ?);
    """, students)
    conn.commit()
    conn.close()
    print("Estudiantes agregados exitosamente.")

def add_reasons():
    """Agregar razones iniciales."""
    reasons = [
        ('Llega temprano', 10, '', None),
        ('Deja desordenado', -5, '', None),
        ('Realiza tarea en Gatito Labs', 15, '', 'ROB001'),
        ('Gana Kahoot', 15, '', 'ROB002'),
        ('Realiza tarea en Scratch', 15, '', 'VG001'),
        ('Realiza tarea en Roblox', 15, '', 'VG002'),
        ('Buen trabajo en equipo', 30, '', 'ClubComun'),
        ('Participa en torneo de velocidad', 30, '', 'ClubVel'),
        ('Gana torneo de Mustabot', 50, '', 'ClubMusta'),
        ('Participa en taller de arte', 15, '', 'ClubArte')
    ]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO reasons (reason_description, point_value, image_url, course_id_exclusive)
        VALUES (?, ?, ?, ?);
    """, reasons)
    conn.commit()
    conn.close()
    print("Razones agregadas exitosamente.")

if __name__ == "__main__":
    #add_courses()
    #add_mentors()
    #add_students()
    add_reasons()
