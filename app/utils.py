import streamlit as st
import psycopg2
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
import pandas as pd
from utils import *
from automation import *
import math
import matplotlib.pyplot as plt
import numpy as np

# Conectar a la base de datos
def connect_db():
    return psycopg2.connect(
        host=st.secrets["database"]["host"],
        database=st.secrets["database"]["name"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        port=st.secrets["database"]["port"]
    )


#homepage
def homepage():
    st.markdown("""
    <style>
        .section-title {
            font-size: 24px;
            font-weight: bold;
            color: #0D47A1;
            margin-top: 30px;
        }
        .highlight-box {
            background-color: #E3F2FD;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            color: #0D47A1;
        }
        .warning-box {
            background-color: #FFCDD2;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            color: #B71C1C;
        }
        .reward-box {
            background-color: #FFF9C4;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            color: #0D47A1;
        }
    </style>

    <div class="highlight-box" style="text-align:center;">
        <h1>🏆 ¡Bienvenidos a MustaPoint! 🏆</h1>
        <p style="font-size:18px;">Participa, aprende y gana premios increíbles acumulando MP🪙.</p>
    </div>

    <div class="highlight-box">
        <div class="section-title">¿Qué es MustaPoint?</div>
        <p>MustaPoint es nuestro sistema de puntos donde cada buena acción te recompensa con MP🪙. ¡Acumula MP🪙 para escalar posiciones en el ranking y canjear premios!</p>
    </div>

    <div class="highlight-box">
        <div class="section-title">💪 ¿Cómo ganas MP🪙?</div>
        <ul>
            <li><b>Participación y Comportamiento:</b>
                <ul>
                    <li>✅ Llegar antes de las 10:00 hrs – 3 MP🪙.</li>
                    <li>✅ Asistir o justificar ausencia – 1 MP🪙.</li>
                    <li>✅ Participación activa en clase – 1 MP🪙.</li>
                    <li>✅ Trabajo en equipo – 1 MP🪙.</li>
                </ul>
            </li>
            <li><b>Kahoot:</b>
                <ul>
                    <li>🥇 1º lugar – 3 MP🪙.</li>
                    <li>🥈 2º lugar – 2 MP🪙.</li>
                    <li>🥉 3º lugar – 1 MP🪙.</li>
                </ul>
            </li>
            <li><b>Desempeño Académico:</b>
                <ul>
                    <li>🏆 Desafío Final – Puntaje [0-10] (1 MP🪙 por cada 10% logrado).</li>
                    <li>📚 Tarea semanal perfecta – 3 MP🪙.</li>
                    <li>📖 Tarea parcial – 1 MP🪙.</li>
                    <li>📈 Superar tu puntaje de la sesión pasada – 3 MP🪙.</li>
                </ul>
            </li>
            <li><b>Actitudes y Valores:</b>
                <ul>
                    <li>🧹 Mantener limpio el espacio – 1 MP🪙.</li>
                </ul>
            </li>
            <li><b>Atención Plena:</b>
                <ul>
                    <li>🧠 Compartir tu estado de ánimo – 3 MP🪙.</li>
                    <li>🌬️ Participar en actividad de respiración consciente – 2 MP🪙.</li>
                </ul>
            </li>
        </ul>
    </div>

     <div class="reward-box">
        <div class="section-title">✨ ¡Bonos Especiales!</div>
        <ul>
            <li>⏰ <b>Racha de puntualidad:</b>
                <ul>
                    <li>x3 sesiones: 3 MP🪙</li>
                    <li>x5 sesiones: 5 MP🪙</li>
                    <li>Todo el taller: 20 MP🪙</li>
                </ul>
            </li>
            <li>🏫 <b>Racha de asistencia:</b>
                <ul>
                    <li>x3 sesiones: 3 MP🪙</li>
                    <li>x5 sesiones: 5 MP🪙</li>
                    <li>Completa: 20 MP🪙</li>
                </ul>
            </li>
            <li>🎯 <b>Puntaje perfecto:</b>
                <ul>
                    <li>x3: 10 MP🪙</li>
                    <li>x5: 20 MP🪙</li>
                    <li>Todo perfecto: 50 MP🪙</li>
                </ul>
            </li>
            <li>📈 <b>Racha de mejora:</b> (Sacar puntaje igual o mejor que la sesión anterior)
                <ul>
                    <li>x3: 3 MP🪙</li>
                    <li>x5: 5 MP🪙</li>
                    <li>Completa: 20 MP🪙</li>
                </ul>
            </li>
            <li>📝 <b>Racha de tareas entregadas:</b>
                <ul>
                    <li>x3: 10 MP🪙</li>
                    <li>x5: 20 MP🪙</li>
                    <li>Completa: 30 MP🪙</li>
                </ul>
            </li>
            <li>🧘‍♂️ <b>Racha de atención plena:</b> (participación en mindfulness)
                <ul>
                    <li>x3: 5 MP🪙</li>
                    <li>x5: 10 MP🪙</li>
                    <li>Completa: 50 MP🪙</li>
                </ul>
            </li>
        </ul>
        <p>¡Los bonos aceleran tu progreso hacia grandes premios! 🎉</p>
    </div>

    <div class="warning-box">
        <div class="section-title">🚨 Penalizaciones (¡casos muy extremos!)</div>
        <p>En MustaPoint, creemos en reforzar lo positivo. Estas penalizaciones solo se aplican si ocurre una situación muy grave y debe ser aprobado por TODOS los Mentores, ¡así que no te preocupes! 😄</p>
        <ul>
            <li>⚠️ Desobedecer o ignorar acuerdos grupales</li>
            <li>⚠️ Uso inapropiado de instrumentos o materiales</li>
            <li>⚠️ Reiteraciones:
                <ul>
                    <li>Interrumpir clases o mentores</li>
                    <li>Desorden persistente en el puesto </li>
                </ul>
            </li>
            <li>⚠️ Mala conducta:
                <ul>
                    <li>Peligrosa</li>
                    <li>Reprochable</li>
                </ul>
            </li>
        </ul>
        <p>La cantidad de descuento de MP🪙 queda a criterio del equipo :)</p>
        <p>¡Siempre apostamos por la buena convivencia! 🤝</p>
    </div>

   <div class="highlight-box">
        <div class="section-title">🎁 ¿En qué puedes canjear tus MP🪙?</div>
        <ul>
            <li>🥤 Juguito extra: 20 MP🪙</li>
            <li>🍪 Galleta extra: 20 MP🪙</li>
            <li>🍬 Un frugelé: 5 MP🪙</li>
            <li>🕔 5 minutos extra de recreo: 50 MP🪙</li>
            <li>💺 Silla VIP: 50 MP🪙</li>
            <li>🚶 Saltarse la fila en el break: 50 MP🪙</li>
            <li>🎵 Elegir música ambiente (1 canción): 30 MP🪙</li>
            <li>🏓 Ping pong en el break: 100 MP🪙</li>
            <li>⚽ Taka Taka en el break: 100 MP🪙</li>
            <li>🛋️ Break VIP (sillones de la Funda): 500 MP🪙</li>
            <li>👑 ¡Sé Mediador por un día!: 10,000 MP🪙</li>
            <li>🔜 Muchos más... (¡Muy pronto! 😉)</li>
        </ul>
        <p>¡Canjea tus MustaPoints con un Mentor por premios increíbles y vive una experiencia única! 🎉</p>
    </div>

     <div class="highlight-box">
        <div class="section-title">🚀 ¡Sube en el Ranking y Consigue un Premio Único!</div>
        <p>Compites en el ranking de tu curso y en el ranking general. 🏅</p>
        <p><strong>El o la estudiante con más MP🪙 de cada curso ganará un premio único y especial 🎁🎖️.</strong></p>
        <p>¡No te quedes atrás! Participa en todas las actividades, da lo mejor de ti, acumula MP🪙 y alcanza lo más alto del ranking MustaPoint. 🌟<strong> ¡Tú puedes ser nuestro gran campeón o campeona! 🏆</strong> </p>
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
            #4: "Bonos"  # <- CTIVAMOS BONOS
        }

        for category, title in categories.items():
            st.write(f"**{title}**")
            for reason in [r for r in reasons if r[3] == category]:
                if st.button(f"{reason[1]} ({reason[2]} puntos)", key=f"reason_{reason[0]}"):
                    st.session_state["selected_reason"] = reason
        
        # Si se seleccionó el Desafío Final (id=11), pedir puntaje manual
        if st.session_state.get("selected_reason") and st.session_state["selected_reason"][0] == 11:
            manual_point_value = st.number_input(
                "Ingresa el puntaje obtenido en el Desafío (0 a 20):",
                min_value=0, max_value=20, step=1
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
                st.dataframe(pd.DataFrame(course_logs, columns=["Fecha", "Mentor", "Estudiante", "Motivo", "Puntos"]))
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

    # Ranking por Curso
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
                    (f"<div class='podium-item gold'>🥇<br>{rankings[0][0]}<br>{rankings[0][1]} MP🪙</div>" if len(rankings) > 0 else "") +
                    (f"<div class='podium-item silver'>🥈<br>{rankings[1][0]}<br>{rankings[1][1]} MP🪙</div>" if len(rankings) > 1 else "") +
                    (f"<div class='podium-item bronze'>🥉<br>{rankings[2][0]}<br>{rankings[2][1]} MP🪙</div>" if len(rankings) > 2 else "") +
                    "</div>", unsafe_allow_html=True)

                # Mostrar resto del ranking
                for i, (name, points) in enumerate(rankings[3:], start=4):
                    st.markdown(f"<div class='ranking-row'>{i}. {name} - {points} MP🪙</div>", unsafe_allow_html=True)
            else:
                st.write("No hay estudiantes en este curso.")

    # Ranking General
    with tabs[1]:
        st.subheader(f"Ranking General (Top 50)")

        # 1. Obtener estudiantes y sus puntajes
        cursor.execute("""
            SELECT s.first_name || ' ' || s.last_name AS full_name, sc.total_points, c.course_name
            FROM students_scores sc
            JOIN students s ON sc.student_id = s.student_id
            JOIN courses c ON s.current_course = c.course_id;
        """)
        students_data = cursor.fetchall()

        if not students_data:
            st.write("No hay estudiantes registrados.")
        else:
            # 2. Preparar DataFrame para cálculo de z-score
            df_students = pd.DataFrame(students_data, columns=["full_name", "total_points", "course_name"])

            # 3. Calcular media y desviación estándar
            media = df_students["total_points"].mean()
            std = df_students["total_points"].std()

            if std == 0:  # Caso especial: todos tienen mismo puntaje
                df_students["z_score"] = 0
            else:
                df_students["z_score"] = (df_students["total_points"] - media) / std

            # 4. Ordenar y seleccionar Top 50
            df_students = df_students.sort_values(by="z_score", ascending=False).head(50)

            # 5. Mostrar
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

            # Podio
            st.markdown("<div class='general-ranking-podium'>" +
                (f"<div class='general-podium-item gold'>🥇<br>{df_students.iloc[0]['full_name']}<br>Z: {df_students.iloc[0]['z_score']:.2f}<br>{df_students.iloc[0]['total_points']} MP🪙</div>" if len(df_students) > 0 else "") +
                (f"<div class='general-podium-item silver'>🥈<br>{df_students.iloc[1]['full_name']}<br>Z: {df_students.iloc[1]['z_score']:.2f}<br>{df_students.iloc[1]['total_points']} MP🪙</div>" if len(df_students) > 1 else "") +
                (f"<div class='general-podium-item bronze'>🥉<br>{df_students.iloc[2]['full_name']}<br>Z: {df_students.iloc[2]['z_score']:.2f}<br>{df_students.iloc[2]['total_points']} MP🪙</div>" if len(df_students) > 2 else "") +
                "</div>", unsafe_allow_html=True)

            # El resto del ranking
            for i in range(3, len(df_students)):
                st.markdown(
                    f"<div class='general-ranking-row'>{i+1}. {df_students.iloc[i]['full_name']} ({df_students.iloc[i]['course_name']}) - Z: {df_students.iloc[i]['z_score']:.2f} ({df_students.iloc[i]['total_points']} MP🪙)</div>",
                    unsafe_allow_html=True
                )
    # ranking por total de puntos por curso
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
                st.markdown(f"<div class='course-ranking-row'>{i}. {course_name} - {total_points} MP🪙</div>", unsafe_allow_html=True)
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
        #print("pass: ", password)
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

    tabs = st.tabs(["Mentores", "Estudiantes", "Motivos", "Gestión de Logs"])

    # Gestión de Mentores
    with tabs[0]:
        st.subheader("Gestión de Mentores")

        """
        # Mostrar puntos_log actuales
        st.write("### Log de Asignaciones de Puntos")
        cursor.execute(
            SELECT p.log_id, s.first_name || ' ' || s.last_name AS estudiante, r.reason_description, p.points, p.date_time
            FROM points_log p
            JOIN students s ON p.student_id = s.student_id
            JOIN reasons r ON p.reason_id = r.reason_id
            ORDER BY p.date_time DESC;
        )
        logs = cursor.fetchall()
        df_logs = pd.DataFrame(logs, columns=["ID Log", "Estudiante", "Motivo", "Puntos", "Fecha"])
        st.dataframe(df_logs)

        st.divider()
        """

        # Mostrar mentores actuales
        st.write("### Lista de Mentores")
        cursor.execute("SELECT mentor_id, mentor_name FROM mentors;")
        mentors = cursor.fetchall()

        st.dataframe(pd.DataFrame(mentors, columns=["ID Mentor", "Nombre del Mentor"]))
        
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

            st.dataframe(pd.DataFrame(students, columns=["ID Estudiante", "Nombre", "Apellido"]))
            
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
            st.dataframe(pd.DataFrame(reasons, columns=["ID Motivo", "Descripción", "Valor (Puntos)", "Curso Exclusivo"]))
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

    # Gestión de Logs 
    with tabs[3]:
        st.subheader("🗑️ Gestión de Logs de Puntos y Logros")

        conn = connect_db()
        cursor = conn.cursor()

        # Mostrar puntos_log actuales
        st.write("### Log de Asignaciones de Puntos")
        cursor.execute("""
            SELECT p.log_id, s.first_name || ' ' || s.last_name AS estudiante, r.reason_description, p.points, p.date_time
            FROM points_log p
            JOIN students s ON p.student_id = s.student_id
            JOIN reasons r ON p.reason_id = r.reason_id
            ORDER BY p.date_time DESC;
        """)
        logs = cursor.fetchall()
        df_logs = pd.DataFrame(logs, columns=["ID Log", "Estudiante", "Motivo", "Puntos", "Fecha"])
        st.dataframe(df_logs)

        st.divider()

        st.subheader("🔎 Opciones de Eliminación")

        delete_option = st.radio("¿Qué deseas hacer?", ["Eliminar por ID individual"])

        if delete_option == "Eliminar por ID individual":
            log_id_to_delete = st.number_input("Ingresa el ID del Log a Eliminar:", min_value=1, step=1)
            if st.button("❌ Eliminar Log Individual"):
                eliminar_log_individual(log_id_to_delete)
                st.success(f"Registro con ID {log_id_to_delete} eliminado correctamente.")

        if delete_option == "Eliminar por Rango de Fechas":
            start_date = st.date_input("Fecha de Inicio")
            end_date = st.date_input("Fecha de Fin")
            if st.button("❌ Eliminar Logs en Rango de Fechas"):
                eliminar_logs_por_fecha(start_date, end_date)
                st.success(f"Registros entre {start_date} y {end_date} eliminados correctamente.")

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
        ("CLUB Nivelacion", "CLUB Nivelación"),
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
        elif (curso_selection[0].startswith("CLUB") or curso_selection[0].startswith("Rescue")  ) and sesion_input <= 10:
            df_asistencia = getInfoClubes(sesion_input)
            if curso_selection[0].startswith("Rescue"):
                df_asistencia = df_asistencia[df_asistencia["esRescue"] == 1]
            else:
                df_asistencia = df_asistencia[df_asistencia["esRescue"] == 0]
        else:
            st.error("Error: La sesión seleccionada no es válida para el curso seleccionado.")
            st.warning("Recuerda que la sesión máxima para ROB y VG es 8, y para Clubes y Rescue es 10.")
            return

        # filtramos segun el club elegido
        
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
                #st.error("Aun no implementado.")
                asignar_asistencia(df_asistencia, mentor_selection[0], curso_selection[0], sesion_input)

            if "Asignar Puntaje de Desafío según Sheet" in acciones:
                #st.error("Aun no implementado.")
                asignar_puntajes(df_puntajes, mentor_selection[0], curso_selection[0], sesion_input)

            conn.commit()
            st.success("¡Asignación automática completada! 🎉")

    conn.close()

def asignar_puntajes(df_puntajes, mentor_id, curso_id, sesion_numero):
    conn = connect_db()
    cursor = conn.cursor()

    # buscamos el id del curso
    cursor.execute("""
        SELECT course_id FROM courses WHERE course_name = %s
    """, (curso_id,))
    curso_id = cursor.fetchone()[0]


    reason_id = 11  # Desafío Final

    for idx, row in df_puntajes.iterrows():
        nombre = row['Nombre']
        apellido = row['Apellido']
        puntos = row['Puntaje final']
        # Normalizamos el puntaje a escala 0-10
        puntos = math.ceil(puntos / 10)

        # Buscar student_id
        cursor.execute("""
            SELECT student_id FROM students
            WHERE first_name = %s AND last_name = %s AND current_course = %s
        """, (nombre, apellido, curso_id))
        student = cursor.fetchone()

        if student:
            student_id = student[0]

            # Insertar en points_log
            cursor.execute("""
                INSERT INTO points_log (student_id, mentor_id, reason_id, points, auto)
                VALUES (%s, %s, %s, %s, %s);
            """, (student_id, mentor_id, reason_id, puntos, 1))

            # Actualizar students_scores
            cursor.execute("""
                INSERT INTO students_scores (student_id, total_points)
                VALUES (%s, %s)
                ON CONFLICT (student_id) DO UPDATE
                SET total_points = students_scores.total_points + EXCLUDED.total_points;
            """, (student_id, puntos))

            # Insertar logro (permite repeticiones)
            cursor.execute("""
                INSERT INTO student_achievements (student_id, reason_id)
                VALUES (%s, %s);
            """, (student_id, reason_id))

    conn.commit()
    conn.close()


def asignar_asistencia(df_asistencia, mentor_id, curso_id, sesion_numero):
    conn = connect_db()
    cursor = conn.cursor()

    # filtramos el df para el club seleccionado

    # buscamos el id del curso
    cursor.execute("""
        SELECT course_id FROM courses WHERE course_name = %s
    """, (curso_id,))

    if curso_id is None:
        st.error("Error: Curso no encontrado.")
        return
   # print("curso_id: ", curso_id)
    curso_id = cursor.fetchone()[0]

    reason_id = 5  # Asistencia

    for idx, row in df_asistencia.iterrows():
        nombre = row['Nombre']
        apellido = row['Apellido']
        asistencia = int(row['Asistio'])

        # Solo registramos si asistió (1)
        if asistencia == 1:

            # Buscar student_id
            cursor.execute("""
                SELECT student_id FROM students
                WHERE first_name = %s AND last_name = %s AND current_course = %s
            """, (nombre, apellido, curso_id))
            student = cursor.fetchone()

            if student:
                student_id = student[0]

                print("info previa al insert: ", student_id, mentor_id, reason_id)  
                # Insertar en points_log (1 punto)
                cursor.execute("""
                    INSERT INTO points_log (student_id, mentor_id, reason_id, points, auto)
                    VALUES (%s, %s, %s, %s, %s);
                """, (student_id, mentor_id, reason_id, 1, 1))

                # Actualizar students_scores
                cursor.execute("""
                    INSERT INTO students_scores (student_id, total_points)
                    VALUES (%s, 1)
                    ON CONFLICT (student_id) DO UPDATE
                    SET total_points = students_scores.total_points + 1;
                """, (student_id,))

                # Insertar logro (permite repeticiones)
                cursor.execute("""
                    INSERT INTO student_achievements (student_id, reason_id)
                    VALUES (%s, %s);
                """, (student_id, reason_id))

    conn.commit()
    conn.close()


def eliminar_log_individual(log_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Buscar el registro antes de eliminar
    cursor.execute("""
        SELECT student_id, mentor_id, reason_id, points
        FROM points_log
        WHERE log_id = %s;
    """, (log_id,))
    registro = cursor.fetchone()

    if registro:
        student_id, mentor_id, reason_id, points = registro
        print("student_id: ", student_id, "mentor_id: ", mentor_id, "reason_id: ", reason_id, "points: ", points)

        # Guardar el registro eliminado
        cursor.execute("""
            INSERT INTO deleted_records (student_id, mentor_id, reason_id, points, deletion_type)
            VALUES (%s, %s, %s, %s, 'individual');
        """, (student_id, mentor_id, reason_id, points))

        # Eliminar de student_achievements (solo si existe)
        cursor.execute("""
            DELETE FROM student_achievements
            WHERE student_id = %s AND reason_id = %s;
        """, (student_id, reason_id))

        #vamos a extraer la categoría del motivo
        cursor.execute("""
            SELECT category FROM reasons
            WHERE reason_id = %s;
        """, (reason_id,))
        category = cursor.fetchone()

        category = category[0] if category else None
        if category != 3: # si no es canjeo
            # Restar los puntos en students_scores
            cursor.execute("""
                UPDATE students_scores
                SET total_points = total_points - %s
                WHERE student_id = %s;
            """, (points, abs(student_id)))
        else: # re asignamos los puntos al estudiante
            cursor.execute("""
                UPDATE students_scores
                SET total_points = total_points + %s
                WHERE student_id = %s;
            """, (points, abs(student_id)))
            

        # Finalmente eliminar del log
        cursor.execute("""
            DELETE FROM points_log
            WHERE log_id = %s;
        """, (log_id,))

        conn.commit()

    conn.close()


def eliminar_logs_por_fecha(start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SET statement_timeout = 30000;")
    st.info("Iniciando eliminación de registros por fecha. Esto puede tomar algunos segundos...")

    # Paso 1: Borrar logs de student_achievements relacionados
    while True:
        cursor.execute("""
            SELECT DISTINCT s.student_id
            FROM students s
            JOIN points_log pl ON pl.student_id = s.student_id
            WHERE DATE(pl.date_time) BETWEEN %s AND %s
            LIMIT 100;
        """, (start_date, end_date))
        student_ids = cursor.fetchall()
        if not student_ids:
            break

        for sid in student_ids:
            cursor.execute("""
                DELETE FROM student_achievements
                WHERE student_id = %s;
            """, (sid[0],))
        conn.commit()

    # Paso 2: Borrar directamente de points_log (bloques)
    while True:
        cursor.execute("""
            DELETE FROM points_log
            WHERE DATE(date_time) BETWEEN %s AND %s
            LIMIT 100
            RETURNING *;
        """, (start_date, end_date))
        deleted = cursor.fetchall()
        if not deleted:
            break
        conn.commit()

    # Paso 3: Recalcular scores (esto puede tardar, pero es necesario)
    cursor.execute("""
        UPDATE students_scores SET total_points = COALESCE((
            SELECT SUM(points)
            FROM points_log
            WHERE points_log.student_id = students_scores.student_id
        ), 0);
    """)
    conn.commit()

    st.success("¡Registros eliminados correctamente por fecha!")
    conn.close()



def nnj_statistics_ui():
    st.title("👷 EN CONSTRUCCIÓN: \n📊 Estadísticas de NNJs")

    tabs = st.tabs(["Perfil de Estudiante", "Resumen General por Curso"])

    # --- Perfil de Estudiante
    with tabs[0]:
        st.header("🔎 Perfil Individual")

        # Inputs para seleccionar
        curso = st.selectbox("Selecciona el curso:", ["ROB001", "VG001", "Club Nivelación", "Rescue"])
        estudiante = st.selectbox("Selecciona el estudiante:", ["Estudiante 1", "Estudiante 2", "Estudiante 3"])

        st.subheader("Radar de Caracterización")
        # Valores de ejemplo
        labels = np.array(["Asistencia", "Promedio Puntajes", "Logros", "Participaciones"])
        valores = np.array([0.8, 0.7, 0.9, 0.6])

        # Radar chart
        fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
        valores = np.concatenate((valores, [valores[0]]))  # Cerrar el gráfico
        angles += angles[:1]

        ax.fill(angles, valores, color='skyblue', alpha=0.4)
        ax.plot(angles, valores, color='blue', linewidth=2)
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        st.pyplot(fig)

    # --- Resumen General
    with tabs[1]:
        st.header("📚 Resumen por Curso")

        curso_resumen = st.selectbox("Selecciona el curso para ver el resumen:", ["ROB001", "VG001", "Club Nivelación", "Rescue"], key="resumen")

        # Asistencia por sesión (datos de ejemplo)
        sesiones = [f"Sesión {i}" for i in range(1, 9)]
        asistencia = [25, 23, 22, 24, 21, 20, 23, 22]

        st.subheader("📅 Asistencia por Sesión")
        df_asistencia = pd.DataFrame({"Sesión": sesiones, "Asistencias": asistencia})
        st.bar_chart(df_asistencia.set_index("Sesión"))

        # Puntaje promedio por sesión (solo para ROB y VG)
        if curso_resumen in ["ROB001", "VG001"]:
            st.subheader("🎯 Puntaje Promedio por Sesión")
            puntajes_prom = [7.5, 8.0, 7.0, 8.5, 8.0, 7.8, 7.2, 8.3]
            df_puntajes = pd.DataFrame({"Sesión": sesiones, "Promedio Puntaje": puntajes_prom})
            st.bar_chart(df_puntajes.set_index("Sesión"))
