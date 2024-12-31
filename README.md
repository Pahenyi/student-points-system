# Sistema de Puntos para Estudiantes

## **Descripción del Proyecto**
Este proyecto es un sistema de gestión de puntos diseñado para fomentar el mérito, la colaboración y la participación en un entorno educativo. Los mentores (profesores) pueden asignar y restar puntos a los estudiantes (NNJs) en función de razones predefinidas, mientras que los estudiantes pueden visualizar su ranking y puntaje acumulado.

El sistema está construido con **Streamlit** para la interfaz de usuario y utiliza **SQLite** como base de datos.

---

## **Características Principales**
1. **Gestión de Puntos:**
   - Asignación/resta de puntos por razones predefinidas.
   - Registro detallado de cada acción, incluyendo el mentor responsable y la fecha.

2. **Visualización de Rankings:**
   - Ranking por curso.
   - Ranking general.

3. **Datos Almacenados:**
   - Cursos disponibles.
   - Mentores registrados.
   - Estudiantes y sus datos personales.
   - Razones predefinidas para asignar puntos.
   - Historial de puntos asignados.

4. **Interfaz Intuitiva:**
   - Fácil acceso para mentores y estudiantes.
   - Acceso rápido a información relevante.

---

## **Estructura del Proyecto**
```
student-points-system/
├── database/
│   └── points_system.db         # Archivo SQLite
├── app/
│   ├── main.py                  # Interfaz principal en Streamlit
│   ├── db.py                    # Conexión y configuración de SQLite
│   ├── add_data.py              # Script para agregar datos iniciales
│   ├── clear_data.py            # Script para vaciar las tablas
│   └── test_db.py               # Script para verificar la base de datos
├── sql/
│   └── schema.sql               # Esquema SQL para crear las tablas
├── .gitignore                   # Archivos ignorados por Git
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Documentación del proyecto
```

---

## **Requisitos Previos**
- **Python 3.6 o superior.**
- **Entorno Virtual (recomendado):**
  ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  .\venv\Scripts\activate  # Windows
  ```
- **Instalar Dependencias:**
  ```bash
  pip install -r requirements.txt
  ```

---

## **Cómo Usar el Proyecto**

### **1. Configuración Inicial**
1. Clona este repositorio:
   ```bash
   git clone https://github.com/tuusuario/student-points-system.git
   cd student-points-system
   ```
2. Activa el entorno virtual y asegura que las dependencias estén instaladas:
   ```bash
   pip install -r requirements.txt
   ```
3. Crea la base de datos:
   ```bash
   python app/db.py
   ```
4. Agrega datos iniciales:
   ```bash
   python app/add_data.py
   ```

### **2. Ejecutar la Aplicación**
1. Ejecuta Streamlit:
   ```bash
   streamlit run app/main.py
   ```
2. Abre el navegador en la URL proporcionada (generalmente `http://localhost:8501`).

---

## **Scripts Importantes**
- **Crear Base de Datos:**
  ```bash
  python app/db.py
  ```
  Crea el esquema inicial de la base de datos.

- **Agregar Datos Iniciales:**
  ```bash
  python app/add_data.py
  ```
  Agrega cursos, mentores, estudiantes y razones predefinidas.

- **Vaciar Tablas:**
  ```bash
  python app/clear_data.py
  ```
  Vacía todas las tablas de la base de datos.

- **Verificar Tablas y Datos:**
  ```bash
  python app/test_db.py
  ```
  Verifica las tablas creadas y los datos almacenados.

---

## **Licencia**
Este proyecto está bajo la Licencia MIT.

