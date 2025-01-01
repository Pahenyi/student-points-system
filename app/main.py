import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
import pandas as pd
from utils import *


# Navegación Principal
def main():
    if "user_role" not in st.session_state or st.session_state["user_role"] is None:
        login()
    else:
        st.sidebar.title("Navegación")
        if st.session_state["user_role"] == "Mentor":
            pages = ["Inicio", "Asignar Puntos", "Rankings", "Estadísticas"]
        else:
            pages = ["Inicio", "Rankings"]
        page = st.sidebar.radio("Selecciona una página:", pages)

        if page == "Inicio":
            homepage()
        elif page == "Asignar Puntos":
            assign_points_ui()
        elif page == "Rankings":
            show_rankings()
        elif page == "Estadísticas":
            mentor_stats_ui()

        if st.sidebar.button("Cerrar Sesión"):
            st.session_state["user_role"] = None

if __name__ == "__main__":
    main()
