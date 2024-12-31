import streamlit as st
import sqlite3

# Función para conectar a la base de datos
def connect_db():
    return sqlite3.connect('database/points_system.db')

# Página principal
def main():
    st.title("Sistema de Puntos - Mustakis")

    # Conectar a la base de datos
    conn = connect_db()
    cursor = conn.cursor()

    # Mostrar cursos
    st.subheader("Cursos Disponibles")
    cursor.execute("SELECT course_id, course_name FROM courses;")
    courses = cursor.fetchall()
    for course in courses:
        st.write(f"{course[0]}: {course[1]}")

    conn.close()

if __name__ == "__main__":
    main()
