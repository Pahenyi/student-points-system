import streamlit as st
import psycopg2

def test_connection():
    try:
        # Conectar usando st.secrets
        conn = psycopg2.connect(
            host=st.secrets["database"]["host"],
            dbname=st.secrets["database"]["name"],
            user=st.secrets["database"]["user"],
            password=st.secrets["database"]["password"],
            port=st.secrets["database"]["port"]
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result and result[0] == 1:
            st.success("✅ Conexión a la base de datos exitosa!")
        else:
            st.error("❌ Error inesperado en la conexión.")
    except Exception as e:
        st.error(f"❌ Error al conectar: {e}")

def main():
    st.title("Test de Conexión a Supabase")
    if st.button("Probar Conexión"):
        test_connection()

if __name__ == "__main__":
    main()
