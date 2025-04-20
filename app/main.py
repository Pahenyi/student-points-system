import streamlit as st
from utils import *

def footer():
    st.markdown("""
    <hr style="margin-top:50px;margin-bottom:10px;">
    <div style="text-align: center; color: #0D47A1; font-size: 14px;">
        Desarrollado con ❤️ por <b>Seba</b> para la Sede Recoleta de Fundación Mustakis 2025
    </div>
    """, unsafe_allow_html=True)



# Navegación Principal
def main():
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None

    st.sidebar.title("Navegación")
    pages = ["Inicio", "Rankings"]

    if st.session_state["user_role"] == "Mentor":
        pages += ["Asignación Manual", "Asignación Automática", "Estadísticas Mentores", "👷 Estadísticas NNJs","Admin"]
    

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
    elif page == "👷 Estadísticas NNJs":
        nnj_statistics_ui()
    elif page == "Admin":
        admin_ui()

if __name__ == "__main__":
    main()
    footer()
