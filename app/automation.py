import pandas as pd
import re

def leer_sheet_publico(sheet_id, hoja="Hoja1", header=0):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={hoja}"
    df = pd.read_csv(url, header=header)
    return df


sheet_id_ROB = "1k0_mgJxRxMM-S652QbIUJZKVtgim5ezW" 
sheet_id_VG = "1kN5T2MTSM_z9oqS69OG2ba1WvsMlfz1p"
sheet_id_clubes = "1nQ2EIPSY6mRyZf1NJTBeK4C1aV5fRfpg"

Asistencia = "Asistencia"
Puntajes = {
    "ROB": "ROB+001",
    "VG": "VG+001",
}


def getColumnsOfSesions(df):

    # Obtener las columnas
    columnas = df.columns.tolist()

    # Preparar estructuras
    sesiones = {}  # Guardará {"Sesion 1": [columnas], "Sesion 2": [columnas], etc.}
    col_actuales = [] 
    nombre_sesion_actual = None

    # Regex para detectar "Sesión X" en el nombre
    patron_sesion = re.compile(r"Sesión\s+\d+")

    for col in columnas:
        if patron_sesion.search(col):
            nombre_sesion_actual = patron_sesion.search(col).group()
            sesiones[nombre_sesion_actual] = []

            # Limpiar el nombre
            nombre_limpio = col.replace(nombre_sesion_actual, "").strip()
            if nombre_limpio == "":
                nombre_limpio = "Puntaje principal"

            # Verificar si ya existe en el DataFrame
            nombre_final = nombre_limpio
            contador = 1
            while nombre_final in df.columns:
                nombre_final = f"{nombre_limpio}.{contador}"
                contador += 1

            # Renombrar
            df = df.rename(columns={col: nombre_final})
            sesiones[nombre_sesion_actual].append(nombre_final)
        else:
            # Sigue perteneciendo a la misma sesión
            if nombre_sesion_actual is not None:
                sesiones[nombre_sesion_actual].append(col)
    
    return df, sesiones
    
    
    



# Puntajes por sesión
# Crear un nuevo DataFrame vacío para almacenar puntajes por sesión
def getPuntajesPorSesion(df, sesionNum):

    dff, sesiones = getColumnsOfSesions(df)
    print(sesiones)

    s = sesiones[f"Sesión {sesionNum}"]


    puntajes_por_sesion = pd.DataFrame()

    puntajes_por_sesion["Nombre"] = dff["Nombre"]
    puntajes_por_sesion["Apellido"] = dff["Apellido"]
    puntajes_por_sesion["Puntaje final"] = None
    

    # Sumamos SOLO las columnas que corresponden a esa sesión
    puntajes_por_sesion["Puntaje final"] = dff[s].sum(axis=1)

    # Mostrar el DataFrame final
    return puntajes_por_sesion

def getAsistencia(df, sesionNum):
    asistencia = pd.DataFrame()

    asistencia["Nombre"] = df["Nombre"]
    asistencia["Apellido"] = df["Apellido"]
    asistencia["Asistio"] =  df[f"S{sesionNum}"]

    # Mostrar el DataFrame final
    return asistencia



def getInfoRob(sesion):
    # Obtener la información de la hoja de cálculo
    df_asistencia = leer_sheet_publico(sheet_id_ROB, Asistencia)
    df_puntajes = leer_sheet_publico(sheet_id_ROB, Puntajes["ROB"])

    df_puntajes_sx = getPuntajesPorSesion(df_puntajes, sesion)
    df_asistencia_sx = getAsistencia(df_asistencia, sesion)

    return df_asistencia_sx, df_puntajes_sx 


def getInfoVg(sesion):
    # Obtener la información de la hoja de cálculo
    df_asistencia = leer_sheet_publico(sheet_id_VG, Asistencia)
    df_puntajes = leer_sheet_publico(sheet_id_VG, Puntajes["VG"])

    df_puntajes_sx = getPuntajesPorSesion(df_puntajes, sesion)
    df_asistencia_sx = getAsistencia(df_asistencia, sesion)

    return df_asistencia_sx, df_puntajes_sx



