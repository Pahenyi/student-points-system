import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
import pandas as pd
from utils import *

# Conectar a la base de datos
def connect_db():
    return sqlite3.connect('database/points_system.db')

# Función de Inicio
def homepage():
    st.markdown("""
    <div style="background-color:#FFECB3; padding:20px; border-radius:10px; text-align:center;">
        <h1 style="color:#FF5722;">🏆 ¡Bienvenidos al Sistema de Puntos! 🏆</h1>
        <p style="color:#37474F; font-size:18px;">Participa, aprende y gana premios increíbles.</p>
    </div>
    """, unsafe_allow_html=True)

# Asignar puntos
def assign_points_ui():
    if st.session_state.get("user_role") != "Mentor":
        st.error("Acceso denegado. Esta sección es solo para mentores.")
        return

    st.markdown("""
    <div style="background-color:#FFF3E0; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;">
        <h2 style="color:#FF5722;">Asigna puntos fácilmente</h2>
        <p style="color:#37474F;">Selecciona a los estudiantes y asigna puntos por su desempeño.</p>
    </div>
    """, unsafe_allow_html=True)

    conn = connect_db()
    cursor = conn.cursor()

    # Paso 1: Seleccionar el Mentor
    st.subheader("1. Selecciona el Mentor")
    cursor.execute("SELECT mentor_id, mentor_name FROM mentors;")
    mentors = cursor.fetchall()
    mentor_selection = st.selectbox("Mentores", mentors, format_func=lambda x: x[1])

    # Paso 2: Seleccionar el Curso
    st.subheader("2. Selecciona el Curso")
    cursor.execute("SELECT course_id, course_name FROM courses;")
    courses = cursor.fetchall()
    course_selection = st.selectbox("Cursos", courses, format_func=lambda x: x[1])

    # Paso 3: Seleccionar Estudiantes
    st.subheader("3. Selecciona Estudiantes")
    selected_students = []
    if course_selection:
        cursor.execute("""
            SELECT student_id, first_name, last_name
            FROM students
            WHERE current_course = ?;
        """, (course_selection[0],))
        students = cursor.fetchall()

        # Mostrar lista de estudiantes con opción de seleccionar todos
        select_all = st.checkbox("Seleccionar Todos")
        selected_students = st.multiselect(
            "Estudiantes",
            students,
            default=students if select_all else [],
            format_func=lambda x: f"{x[1]} {x[2]}"
        )

    # Paso 4: Seleccionar el Motivo
    st.subheader("4. Selecciona el Motivo")
    if course_selection:
        cursor.execute("""
            SELECT reason_id, reason_description, image_url, point_value, category
            FROM reasons
            WHERE course_id_exclusive IS NULL OR course_id_exclusive = ?
            ORDER BY category, point_value DESC;
        """, (course_selection[0],))
        reasons = cursor.fetchall()

        if "selected_reason" not in st.session_state:
            st.session_state["selected_reason"] = None

        # Categorías de motivos
        categories = {
            1: "Premios",
            2: "Penalizaciones",
            3: "Canjeos"
        }

        for category, title in categories.items():
            st.write(f"**{title}**")
            for reason in [r for r in reasons if r[4] == category]:
                if st.button(f"{reason[1]} ({reason[3]} puntos)", key=f"reason_{reason[0]}"):
                    st.session_state["selected_reason"] = reason

    # Paso 5: Confirmar y Enviar
    st.subheader("5. Confirmar y Enviar")
    if st.button("Asignar Puntos", key="assign_points_button"):
        if st.session_state.get("selected_reason") and mentor_selection and selected_students:
            for student in selected_students:
                cursor.execute("""
                    INSERT INTO points_log (mentor_id, student_id, reason_id, points)
                    VALUES (?, ?, ?, ?);
                """, (mentor_selection[0], student[0], st.session_state["selected_reason"][0], st.session_state["selected_reason"][3]))

                cursor.execute("""
                    INSERT INTO students_scores (student_id, total_points)
                    VALUES (?, ?)
                    ON CONFLICT(student_id) DO UPDATE SET total_points = total_points + excluded.total_points;
                """, (student[0], st.session_state["selected_reason"][3]))

            conn.commit()
            st.success("¡Puntos asignados correctamente!")
        else:
            st.error("Por favor, completa todos los pasos antes de asignar puntos.")

    conn.close()



def mentor_stats_ui():
    if st.session_state.get("user_role") != "Mentor":
        st.error("Acceso denegado. Esta sección es solo para mentores.")
        return

    st.markdown("""
    <div style="background-color:#E3F2FD; padding:20px; border-radius:10px; text-align:center;">
        <h2 style="color:#0D47A1;">📊 Estadísticas de Mentores</h2>
    </div>
    """, unsafe_allow_html=True)

    conn = connect_db()
    cursor = conn.cursor()

    # Ranking de mentores
    st.subheader("🏆 Ranking de Mentores por Uso")
    cursor.execute("""
        SELECT mentor_name, COUNT(*) as total_assignments
        FROM points_log
        JOIN mentors ON points_log.mentor_id = mentors.mentor_id
        GROUP BY mentor_name
        ORDER BY total_assignments DESC;
    """)
    mentor_rankings = cursor.fetchall()

    if mentor_rankings:
        st.write("Ranking de mentores por número de asignaciones:")
        for i, (mentor, count) in enumerate(mentor_rankings, start=1):
            st.markdown(f"**{i}. {mentor}** - {count} asignaciones")
    else:
        st.write("No hay datos para mostrar en el ranking de mentores.")


    # Log por curso
    st.subheader("📚 Log de Actividades por Curso")
    cursor.execute("SELECT course_id, course_name FROM courses;")
    courses = cursor.fetchall()

    tabs = st.tabs([course[1] for course in courses])
    for i, course in enumerate(courses):
        with tabs[i]:
            st.subheader(f"Actividades para el curso: {course[1]}")
            cursor.execute("""
                SELECT 
                    DATE(date_time) as log_date, 
                    mentors.mentor_name, 
                    students.first_name || ' ' || students.last_name AS student_name, 
                    reasons.reason_description, 
                    points_log.points
                FROM points_log
                JOIN mentors ON points_log.mentor_id = mentors.mentor_id
                JOIN students ON points_log.student_id = students.student_id
                JOIN reasons ON points_log.reason_id = reasons.reason_id
                WHERE students.current_course = ?
                ORDER BY log_date DESC;
            """, (course[0],))
            course_logs = cursor.fetchall()

            if course_logs:
                st.write(f"Historial de asignaciones en {course[1]}:")
                st.table(pd.DataFrame(course_logs, columns=["Fecha", "Mentor", "Estudiante", "Motivo", "Puntos"]))
            else:
                st.write(f"No hay datos disponibles para el curso {course[1]}.")

    

    conn.close()



# Mostrar rankings
def show_rankings(limit=10):
    st.markdown("""
    <div style="background-color:#FFF3E0; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;">
        <h2 style="color:#FF5722;">Consulta el ranking de los mejores estudiantes 🏅</h2>
    </div>
    """, unsafe_allow_html=True)

    conn = connect_db()
    cursor = conn.cursor()

    tabs = st.tabs(["Ranking por Curso", "Ranking General", "Ranking por Total de Puntos por Curso"])

    with tabs[0]:
        st.subheader(f"Ranking por Curso (Top {limit})")
        cursor.execute("SELECT course_id, course_name FROM courses;")
        courses = cursor.fetchall()

        course_selection = st.selectbox("Selecciona un Curso", courses, format_func=lambda x: x[1])

        if course_selection:
            cursor.execute(f"""
                SELECT s.first_name || ' ' || s.last_name AS full_name, sc.total_points
                FROM students_scores sc
                JOIN students s ON sc.student_id = s.student_id
                WHERE s.current_course = ?
                ORDER BY sc.total_points DESC
                LIMIT {limit};
            """, (course_selection[0],))
            rankings = cursor.fetchall()

            if rankings:
                st.markdown("""
                <style>
                .ranking-podium {
                    display: flex;
                    justify-content: center;
                    align-items: flex-end;
                    gap: 20px;
                    margin-bottom: 20px;
                }
                .podium-item {
                    text-align: center;
                    background-color: #FFF8E1;
                    border-radius: 8px;
                    padding: 10px;
                    width: 100px;
                    color: #FF5722;
                }
                .podium-item.gold {
                    font-size: 20px;
                    font-weight: bold;
                }
                .podium-item.silver {
                    font-size: 18px;
                }
                .podium-item.bronze {
                    font-size: 16px;
                }
                .ranking-row {
                    background-color: #FFF8E1;
                    border-radius: 8px;
                    padding: 10px;
                    margin-bottom: 5px;
                    font-size: 16px;
                    color: #FF5722;
                }
                </style>
                """, unsafe_allow_html=True)

                # Mostrar podio
                st.markdown("<div class='ranking-podium'>" +
                    (f"<div class='podium-item gold'>🥇<br>{rankings[0][0]}<br>{rankings[0][1]} pts</div>" if len(rankings) > 0 else "") +
                    (f"<div class='podium-item silver'>🥈<br>{rankings[1][0]}<br>{rankings[1][1]} pts</div>" if len(rankings) > 1 else "") +
                    (f"<div class='podium-item bronze'>🥉<br>{rankings[2][0]}<br>{rankings[2][1]} pts</div>" if len(rankings) > 2 else "") +
                    "</div>", unsafe_allow_html=True)

                # Mostrar resto del ranking
                for i, (name, points) in enumerate(rankings[3:], start=4):
                    st.markdown(f"<div class='ranking-row'>{i}. {name} - {points} puntos</div>", unsafe_allow_html=True)
            else:
                st.write("No hay estudiantes en este curso.")

    with tabs[1]:
        st.subheader(f"Ranking General (Top {limit})")
        cursor.execute(f"""
            SELECT s.first_name || ' ' || s.last_name AS full_name, sc.total_points, c.course_name
            FROM students_scores sc
            JOIN students s ON sc.student_id = s.student_id
            JOIN courses c ON s.current_course = c.course_id
            ORDER BY sc.total_points DESC
            LIMIT {limit};
        """)
        rankings = cursor.fetchall()

        if rankings:
            st.markdown("""
            <style>
            .general-ranking-podium {
                display: flex;
                justify-content: center;
                align-items: flex-end;
                gap: 20px;
                margin-bottom: 20px;
            }
            .general-podium-item {
                text-align: center;
                background-color: #FFE0B2;
                border-radius: 8px;
                padding: 10px;
                width: 100px;
                color: #BF360C;
            }
            .general-podium-item.gold {
                font-size: 20px;
                font-weight: bold;
            }
            .general-podium-item.silver {
                font-size: 18px;
            }
            .general-podium-item.bronze {
                font-size: 16px;
            }
            .general-ranking-row {
                background-color: #FFE0B2;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 5px;
                font-size: 16px;
                color: #BF360C;
            }
            </style>
            """, unsafe_allow_html=True)

            # Mostrar podio
            st.markdown("<div class='general-ranking-podium'>" +
                (f"<div class='general-podium-item gold'>🥇<br>{rankings[0][0]} ({rankings[0][2]})<br>{rankings[0][1]} pts</div>" if len(rankings) > 0 else "") +
                (f"<div class='general-podium-item silver'>🥈<br>{rankings[1][0]} ({rankings[1][2]})<br>{rankings[1][1]} pts</div>" if len(rankings) > 1 else "") +
                (f"<div class='general-podium-item bronze'>🥉<br>{rankings[2][0]} ({rankings[2][2]})<br>{rankings[2][1]} pts</div>" if len(rankings) > 2 else "") +
                "</div>", unsafe_allow_html=True)

            # Mostrar resto del ranking
            for i, (name, points, course) in enumerate(rankings[3:], start=4):
                st.markdown(f"<div class='general-ranking-row'>{i}. {name} ({course}) - {points} puntos</div>", unsafe_allow_html=True)
        else:
            st.write("No hay estudiantes registrados.")

    with tabs[2]:
        st.subheader("Ranking por Total de Puntos por Curso")
        cursor.execute("""
            SELECT c.course_name, SUM(sc.total_points) as total_points
            FROM students_scores sc
            JOIN students s ON sc.student_id = s.student_id
            JOIN courses c ON s.current_course = c.course_id
            GROUP BY c.course_name
            ORDER BY total_points DESC;
        """)
        course_rankings = cursor.fetchall()

        if course_rankings:
            st.markdown("""
            <style>
            .course-ranking-row {
                background-color: #FFF3E0;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 5px;
                font-size: 16px;
                color: #37474F;
            }
            </style>
            """, unsafe_allow_html=True)

            st.write("Ranking de Cursos:")
            for i, (course_name, total_points) in enumerate(course_rankings, start=1):
                st.markdown(f"<div class='course-ranking-row'>{i}. {course_name} - {total_points} puntos</div>", unsafe_allow_html=True)
        else:
            st.write("No hay datos disponibles.")

    conn.close()

# Función de inicio de sesión
def login():
    st.sidebar.markdown("""
    <div style="background-color:#FFECB3; padding:20px; border-radius:10px; text-align:center;">
        <h3 style="color:#FF5722;">🔒 Inicio de Sesión</h3>
    </div>
    """, unsafe_allow_html=True)

    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None

    with st.sidebar.form("login_form"):
        user_role = st.radio("Selecciona tu rol:", ["Estudiante", "Mentor"])
        if user_role == "Mentor":
            password = st.text_input("Contraseña (solo para Mentores)", type="password")
        submit = st.form_submit_button("Iniciar Sesión")

        if submit:
            if user_role == "Estudiante":
                st.session_state["user_role"] = "Estudiante"
            elif user_role == "Mentor" and password == "mentor123":
                st.session_state["user_role"] = "Mentor"
            elif user_role == "Mentor":
                st.error("Contraseña incorrecta. Intenta nuevamente.")
