import streamlit as st
import psycopg2
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
import pandas as pd
from utils import *
from automation import *

# Conectar a la base de datos
def connect_db():
    return psycopg2.connect(
        host=st.secrets["database"]["host"],
        database=st.secrets["database"]["name"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        port=st.secrets["database"]["port"]
    )

# Función de Inicio
def homepage():
    st.markdown("""
    <div style="background-color:#E3F2FD; padding:20px; border-radius:10px; text-align:center;">
        <h1 style="color:#0D47A1;">🏆 ¡Bienvenidos al Sistema de Puntos! 🏆</h1>
        <p style="color:#0D47A1; font-size:18px;">Participa, aprende y gana premios increíbles.</p>
    </div>
    """, unsafe_allow_html=True)

# Asignar puntos
def assign_points_ui():
    if st.session_state.get("user_role") != "Mentor":
        st.error("Acceso denegado. Esta sección es solo para mentores.")
        return

    st.markdown("""
    <div style="background-color:#E3F2FD; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;">
        <h2 style="color:#0D47A1;">Asigna puntos fácilmente</h2>
        <p style="color:#0D47A1;">Selecciona a los estudiantes y asigna puntos por su desempeño.</p>
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
            WHERE current_course = %s;
        """, (course_selection[0],))
        students = cursor.fetchall()

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
            SELECT reason_id, reason_description, point_value, category
            FROM reasons
            WHERE course_id_exclusive IS NULL OR course_id_exclusive = %s
            ORDER BY category, point_value DESC;
        """, (course_selection[0],))
        reasons = cursor.fetchall()

        if "selected_reason" not in st.session_state:
            st.session_state["selected_reason"] = None

        # Categorías de motivos
        categories = {
            1: "Premios",
            2: "Penalizaciones",
            3: "Canjeos",
            #4: "Bonos"  # <- ACTIVAMOS BONOS
        }

        for category, title in categories.items():
            st.write(f"**{title}**")
            for reason in [r for r in reasons if r[3] == category]:
                if st.button(f"{reason[1]} ({reason[2]} puntos)", key=f"reason_{reason[0]}"):
                    st.session_state["selected_reason"] = reason
        
        # Si se seleccionó el Desafío Final (id=11), pedir puntaje manual
        if st.session_state.get("selected_reason") and st.session_state["selected_reason"][0] == 11:
            manual_point_value = st.number_input(
                "Ingresa el puntaje obtenido en el Desafío Final (0 a 10):",
                min_value=0, max_value=10, step=1
            )

    # Paso 5: Confirmar y Enviar
    st.subheader("5. Confirmar y Enviar")
    if st.button("Enviar Asignación", key="assign_points_button"):
        if st.session_state.get("selected_reason") and mentor_selection and selected_students:
            for student in selected_students:
                reason_id = st.session_state["selected_reason"][0]
                category = st.session_state["selected_reason"][3]

                # Determinar el valor correcto de los puntos
                if reason_id == 11 and manual_point_value is not None:
                    point_value = manual_point_value
                else:
                    point_value = st.session_state["selected_reason"][2]

                # Validar si es un canjeo (category 3) y si tiene suficientes puntos
                if category == 3:  # Canjeo
                    cursor.execute("SELECT total_points FROM students_scores WHERE student_id = %s;", (student[0],))
                    current_points = cursor.fetchone()
                    if not current_points or current_points[0] < point_value:
                        st.error(f"El estudiante {student[1]} {student[2]} no tiene suficientes puntos para canjear.")
                        continue  # No aplicar el canjeo si no tiene puntos suficientes

                # Insertar en points_log
                cursor.execute("""
                    INSERT INTO points_log (mentor_id, student_id, reason_id, points)
                    VALUES (%s, %s, %s, %s);
                """, (mentor_selection[0], student[0], reason_id, point_value))

                # Actualizar el puntaje total del estudiante
                if category == 3:
                    # Canjeo: RESTAR puntos
                    cursor.execute("""
                        UPDATE students_scores
                        SET total_points = total_points - %s
                        WHERE student_id = %s;
                    """, (point_value, student[0]))
                else:
                    # Premio o penalización: SUMAR puntos
                    cursor.execute("""
                        INSERT INTO students_scores (student_id, total_points)
                        VALUES (%s, %s)
                        ON CONFLICT (student_id) DO UPDATE 
                        SET total_points = students_scores.total_points + EXCLUDED.total_points;
                    """, (student[0], point_value))

                # Insertar en student_achievements
                if category == 4:
                    # Es un BONUS → Verificar si ya existe antes de insertar
                    cursor.execute("""
                        SELECT 1 FROM student_achievements
                        WHERE student_id = %s AND reason_id = %s;
                    """, (student[0], reason_id))
                    already_exists = cursor.fetchone()

                    if not already_exists:
                        cursor.execute("""
                            INSERT INTO student_achievements (student_id, reason_id)
                            VALUES (%s, %s);
                        """, (student[0], reason_id))
                else:
                    # Es un PREMIO NORMAL → Insertar siempre
                    cursor.execute("""
                        INSERT INTO student_achievements (student_id, reason_id)
                        VALUES (%s, %s);
                    """, (student[0], reason_id))


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
                WHERE students.current_course = %s
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
    <div style="background-color:#E3F2FD; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;">
        <h2 style="color:#0D47A1;">Consulta el ranking de los mejores estudiantes 🏅</h2>
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
                WHERE s.current_course = %s
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
                    background-color: #B3CDE0;
                    border-radius: 8px;
                    padding: 10px;
                    width: 100px;
                    color: #003366;
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
                    background-color: #B3CDE0;
                    border-radius: 8px;
                    padding: 10px;
                    margin-bottom: 5px;
                    font-size: 16px;
                    color: #003366;
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
                background-color: #B3CDE0;
                border-radius: 8px;
                padding: 10px;
                width: 100px;
                color: #003366;
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
                background-color: #B3CDE0;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 5px;
                font-size: 16px;
                color: #003366;
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
                background-color: #B3CDE0;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 5px;
                font-size: 16px;
                color: #003366;;
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
    <div style="background-color:#E3F2FD; padding:20px; border-radius:10px; text-align:center;">
        <h3 style="color:#003366;">🔒 Inicio de Sesión</h3>
    </div>
    """, unsafe_allow_html=True)

    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None

    with st.sidebar.form("login_form"):
        user_role = st.session_state["user_role"]
        if user_role == None:
            password = st.text_input("Contraseña (solo para Mentores)", type="password")
        submit = st.form_submit_button("Iniciar Sesión")
        print("pass: ", password)
        if submit:
            if user_role == None and password == st.secrets["login"]["password"]:
                st.session_state["user_role"] = "Mentor"


def admin_ui():
    if st.session_state.get("user_role") != "Mentor":
        st.error("Acceso denegado. Esta sección es solo para mentores.")
        return

    st.title("Administración de MustaPoint")

    conn = connect_db()
    cursor = conn.cursor()

    tabs = st.tabs(["Mentores", "Estudiantes", "Motivos"])

    # Gestión de Mentores
    with tabs[0]:
        st.subheader("Gestión de Mentores")

        # Mostrar mentores actuales
        st.write("### Lista de Mentores")
        cursor.execute("SELECT mentor_id, mentor_name FROM mentors;")
        mentors = cursor.fetchall()
        for mentor in mentors:
            st.write(f"{mentor[1]} ({mentor[0]})")

        # Agregar nuevo mentor
        st.write("### Agregar Nuevo Mentor")
        new_mentor_name = st.text_input("Nombre del Mentor")
        if st.button("Agregar Mentor"):
            if new_mentor_name:
                cursor.execute("INSERT INTO mentors (mentor_name) VALUES (%s);", (new_mentor_name,))
                conn.commit()
                st.success("Mentor agregado exitosamente.")
            else:
                st.error("Por favor, ingresa un nombre.")

        # Eliminar mentor
        st.write("### Eliminar Mentor")
        mentor_to_delete = st.selectbox("Selecciona un Mentor para Eliminar", mentors, format_func=lambda x: x[1])
        if st.button("Eliminar Mentor"):
            cursor.execute("DELETE FROM mentors WHERE mentor_id = %s;", (mentor_to_delete[0],))
            conn.commit()
            st.success("Mentor eliminado exitosamente.")

      # Gestión de Estudiantes
    with tabs[1]:
        st.subheader("Gestión de Estudiantes")

        # Seleccionar curso
        st.write("### Seleccionar Curso")
        cursor.execute("SELECT course_id, course_name FROM courses;")
        courses = cursor.fetchall()
        course_selection = st.selectbox("Selecciona un Curso", courses, format_func=lambda x: x[1])

        if course_selection:
            # Mostrar estudiantes del curso seleccionado
            st.write("### Lista de Estudiantes en el Curso")
            cursor.execute("SELECT student_id, first_name, last_name FROM students WHERE current_course = %s;", (course_selection[0],))
            students = cursor.fetchall()
            for student in students:
                st.write(f"{student[1]} {student[2]} ({student[0]})")

            # Agregar nuevo estudiante
            st.write("### Agregar Nuevo Estudiante")
            new_student_first_name = st.text_input("Nombre del Estudiante")
            new_student_last_name = st.text_input("Apellido del Estudiante")
        
            if st.button("Agregar Estudiante"):
                if new_student_first_name and new_student_last_name:
                    cursor.execute("INSERT INTO students (first_name, last_name, current_course) VALUES (%s, %s, %s);", (new_student_first_name, new_student_last_name, course_selection[0]))
                    conn.commit()
                    st.success("Estudiante agregado exitosamente.")
                else:
                    st.error("Por favor, completa todos los campos.")

            # Eliminar estudiante
            st.write("### Eliminar Estudiantes")
            students_to_delete = st.multiselect("Selecciona uno o más Estudiantes para Eliminar", students, format_func=lambda x: f"{x[1]} {x[2]}")

            if st.button("Eliminar Estudiantes"):
                for student in students_to_delete:
                    # Primero eliminar en points_log
                    cursor.execute("DELETE FROM points_log WHERE student_id = %s;", (student[0],))
                    # Luego eliminar en students_scores
                    cursor.execute("DELETE FROM students_scores WHERE student_id = %s;", (student[0],))
                    # Finalmente eliminar en students
                    cursor.execute("DELETE FROM students WHERE student_id = %s;", (student[0],))
                conn.commit()
                st.success("Estudiantes eliminados exitosamente.")


 # Gestión de Motivos
    with tabs[2]:
        st.subheader("Gestión de Motivos")

        # Seleccionar categoría
        st.write("### Seleccionar Categoría de Motivo")
        categories = [(1, "Premios"), (2, "Penalizaciones"), (3, "Canjeos")]
        category_selection = st.selectbox("Selecciona una Categoría", categories, format_func=lambda x: x[1])

        if category_selection:
            # Mostrar motivos actuales de la categoría
            st.write("### Lista de Motivos en la Categoría")
            cursor.execute("SELECT reason_id, reason_description, point_value, course_id_exclusive FROM reasons WHERE category = %s;", (category_selection[0],))
            reasons = cursor.fetchall()
            for reason in reasons:
                if reason[3] is None:
                    course_name = "Transversal"
                else:
                    cursor.execute("SELECT course_name FROM courses WHERE course_id = %s;", (reason[3],))
                    course_name = cursor.fetchone()[0]
                st.write(f"{reason[1]} ({reason[2]} puntos, {course_name}, ID: {reason[0]})")

            # Agregar nuevo motivo
            st.write("### Agregar Nuevo Motivo")
            new_reason_description = st.text_input("Descripción del Motivo")
            new_reason_points = st.number_input("Valor del Motivo (Puntos)", step=1, format="%d")
            new_reason_course = st.selectbox("¿Motivo Exclusivo para un Curso?", [(None, "Transversal")] + [(course[0], course[1]) for course in courses], format_func=lambda x: x[1])
            if st.button("Agregar Motivo"):
                if new_reason_description:
                    cursor.execute("INSERT INTO reasons (reason_description, point_value, category, course_id_exclusive) VALUES (%s, %s, %s, %s);", (new_reason_description, new_reason_points, category_selection[0], new_reason_course[0]))
                    conn.commit()
                    st.success("Motivo agregado exitosamente.")
                else:
                    st.error("Por favor, ingresa una descripción.")

            # Eliminar motivo
            st.write("### Eliminar Motivo")
            reason_to_delete = st.selectbox("Selecciona un Motivo para Eliminar", reasons, format_func=lambda x: x[1])
            if st.button("Eliminar Motivo"):
                cursor.execute("DELETE FROM reasons WHERE reason_id = %s;", (reason_to_delete[0],))
                conn.commit()
                st.success("Motivo eliminado exitosamente.")

    conn.close()



def assign_points_auto_ui():
    if st.session_state.get("user_role") != "Mentor":
        st.error("Acceso denegado. Esta sección es solo para mentores.")
        return

    st.title("Asignación Automática de Puntos ✨")

    conn = connect_db()
    cursor = conn.cursor()

    # Seleccionar mentor
    cursor.execute("SELECT mentor_id, mentor_name FROM mentors;")
    mentors = cursor.fetchall()
    mentor_selection = st.selectbox("Selecciona el Mentor Asignador", mentors, format_func=lambda x: x[1])

    # Seleccionar curso
    cursos = [
        ("ROB001", "ROB001"),
        ("VG001", "VG001"),
        ("ClubNivelacion", "Club Nivelación"),
        ("Rescue", "Rescue")
    ]
    curso_selection = st.selectbox("Selecciona el Curso", cursos, format_func=lambda x: x[1])

    # Seleccionar acciones
    acciones = st.multiselect(
        "Acciones a realizar",
        ["Asignar Asistencia según Sheet", "Asignar Puntaje de Desafío según Sheet"]
    )

    # Indicar sesión
    sesion_input = st.number_input("Indica el número de la sesión: (Ej: 1, 2, 3...)", min_value=1, max_value=10, step=1)

    # Definir contenedores de DataFrames
    df_asistencia = None
    df_puntajes = None

    if mentor_selection and curso_selection and acciones and sesion_input:
        # Obtener data
        if curso_selection[0].startswith("ROB") and sesion_input <= 8:
            df_asistencia, df_puntajes = getInfoRob(sesion_input)
        elif curso_selection[0].startswith("VG") and sesion_input <= 8:
            df_asistencia, df_puntajes = getInfoVg(sesion_input)
        elif (curso_selection[0].startswith("Club") or curso_selection[0].startswith("Rescue")) and sesion_input <= 10:
            df_asistencia = getInfoClubes(sesion_input)
        else:
            st.error("Error: La sesión seleccionada no es válida para el curso seleccionado.")
            st.warning("Recuerda que la sesión máxima para ROB y VG es 8, y para Clubes y Rescue es 10.")
            return

        # Mostrar DataFrames antes de asignar
        if "Asignar Asistencia según Sheet" in acciones:
            st.subheader("📋 Asistencia detectada:")
            if df_asistencia is None:
                st.error("No se encontraron datos de asistencia para la sesión seleccionada.")
            else:   
                st.dataframe(df_asistencia)

        if "Asignar Puntaje de Desafío según Sheet" in acciones:
            st.subheader("📋 Puntajes detectados:")
            if df_puntajes is None:
                st.error("No se encontraron puntajes para la sesión seleccionada.")
            else:   
                st.dataframe(df_puntajes)

        if st.button("✅ Confirmar y Ejecutar Asignación"):
            if "Asignar Asistencia según Sheet" in acciones:
                st.error("Aun no implementado.")
                #asignar_asistencia(df_asistencia, mentor_selection[0], curso_selection[0], sesion_input)

            if "Asignar Puntaje de Desafío según Sheet" in acciones:
                st.error("Aun no implementado.")
                #asignar_puntajes(df_puntajes, mentor_selection[0], curso_selection[0], sesion_input)

            conn.commit()
            st.success("¡Asignación automática completada! 🎉")

    conn.close()

