import streamlit as st
from utils import *


# Navegación Principal
def main():
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None

    st.sidebar.title("Navegación")
    pages = ["Inicio", "Rankings"]

    if st.session_state["user_role"] == "Mentor":
        pages += ["Asignación Manual", "Asignación Automática", "Estadísticas Mentores", "Admin"]
    

    page = st.sidebar.radio("Selecciona una página:", pages)

    # Menú para login/logout siempre disponible
    with st.sidebar:
        if st.session_state["user_role"] != "Mentor":
            login()
                # Si es mentor, agregar opciones extra
        else:
            if st.button("Cerrar Sesión"):
                st.session_state["user_role"] = None
                

    
    
    # Cargar páginas
    if page == "Inicio":
        homepage()
    elif page == "Asignación Manual":
        assign_points_ui()
    elif page == "Asignación Automática":
        assign_points_auto_ui()
    elif page == "Rankings":
        show_rankings()
    elif page == "Estadísticas Mentores":
        mentor_stats_ui()
    elif page == "Admin":
        admin_ui()

if __name__ == "__main__":
    main()
