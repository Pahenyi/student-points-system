-- Crear tabla de cursos
CREATE TABLE courses (
    course_id TEXT PRIMARY KEY,
    course_name TEXT NOT NULL
);

-- Crear tabla de estudiantes
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT CHECK(gender IN ('M', 'F', 'Otro')),
    rut TEXT UNIQUE NOT NULL,
    current_course TEXT NOT NULL,
    FOREIGN KEY (current_course) REFERENCES courses(course_id)
);

-- Crear tabla de mentores
CREATE TABLE mentors (
    mentor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mentor_name TEXT NOT NULL,
    image_url TEXT
);

-- Crear tabla de motivos
CREATE TABLE reasons (
    reason_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reason_description TEXT NOT NULL,
    point_value INTEGER NOT NULL,
    image_url TEXT,
    course_id_exclusive TEXT,
    FOREIGN KEY (course_id_exclusive) REFERENCES courses(course_id)
);

-- Crear tabla de registro de puntos
CREATE TABLE points_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    mentor_id INTEGER NOT NULL,
    reason_id INTEGER NOT NULL,
    points INTEGER NOT NULL,
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (mentor_id) REFERENCES mentors(mentor_id),
    FOREIGN KEY (reason_id) REFERENCES reasons(reason_id)
);

-- Crear tabla de puntajes acumulados
CREATE TABLE students_scores (
    student_id INTEGER PRIMARY KEY,
    total_points INTEGER DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);


-- CAMBIOS EN LA BASE DE DATOS!!!!!!!
-- Agregar la columna 'category' en la tabla 'reasons'
ALTER TABLE reasons ADD COLUMN category INTEGER DEFAULT 1;

-- Actualizar las categorías existentes
-- 1: Suma de puntos por buen comportamiento
-- 2: Resta de puntos por penalización
-- 3: Resta de puntos por canjeo

-- Asignar categorías a los motivos existentes
UPDATE reasons SET category = 1 WHERE point_value > 0;
UPDATE reasons SET category = 2 WHERE point_value < 0;

-- Agregar nuevos motivos para la categoría de canjeo
INSERT INTO reasons (reason_description, image_url, point_value, category)
VALUES 
('Más tiempo en el desafío', 'time_icon.png', -10, 3),
('Elegir la música', 'music_icon.png', -20, 3);

-- Verificar los cambios
SELECT * FROM reasons;

