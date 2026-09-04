"""
Vision Digital - Dashboard de ejemplo
Estructura base: login simple, sidebar de navegacion, tarjetas de metricas,
grafico de barras y tabla con tabs (Lista / Calendario / Registro).

Correr con:
    pip install streamlit pandas plotly
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# ---------------------------------------------------------------------------
# CONFIGURACION GENERAL
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Vision Digital",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Usuarios de ejemplo. En un proyecto real esto vendria de una base de datos
# o de un servicio como streamlit-authenticator.
USUARIOS = {
    "jonathan": {"password": "1234", "nombre": "Jonathan Sanchez", "rol": "Jefe de capacitacion"},
    "admin": {"password": "admin", "nombre": "Administrador", "rol": "Admin"},
}

# ---------------------------------------------------------------------------
# ESTILOS (tema oscuro simple con CSS embebido)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 18px 20px;
    }
    .metric-label {
        color: #9ca3af;
        font-size: 12px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #f9fafb;
    }
    .metric-sub {
        color: #6b7280;
        font-size: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------------------
def pantalla_login():
    st.title("Vision Digital")
    st.caption("Tu punto de impresion")
    st.divider()

    with st.form("login_form"):
        usuario = st.text_input("Usuario")
        password = st.text_input("Contrasena", type="password")
        enviado = st.form_submit_button("Iniciar sesion")

    if enviado:
        datos = USUARIOS.get(usuario)
        if datos and datos["password"] == password:
            st.session_state["logueado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["nombre"] = datos["nombre"]
            st.session_state["rol"] = datos["rol"]
            st.rerun()
        else:
            st.error("Usuario o contrasena incorrectos")


# ---------------------------------------------------------------------------
# DATOS DE EJEMPLO
# ---------------------------------------------------------------------------
@st.cache_data
def cargar_visitas():
    # En un proyecto real esto vendria de un CSV, Google Sheets o una base de datos.
    data = [
        {"fecha": "2026-09-02", "sucursal": "Escuintla", "supervisor": "Jhonatan Capacitacion", "estado": "Visitada"},
        {"fecha": "2026-09-03", "sucursal": "Montserrat", "supervisor": "Jhonatan Capacitacion", "estado": "Visitada"},
        {"fecha": "2026-09-03", "sucursal": "Coban", "supervisor": "Jhonatan Capacitacion", "estado": "Visitada"},
        {"fecha": "2026-09-04", "sucursal": "Barrios", "supervisor": "Jhonatan Capacitacion", "estado": "Visitada"},
        {"fecha": "2026-09-04", "sucursal": "Norte", "supervisor": "Jhonatan Capacitacion", "estado": "Visitada"},
    ]
    return pd.DataFrame(data)


def capacitaciones_iniciales():
    # En un proyecto real esto vendria de un CSV, Google Sheets o una base de datos.
    # horas_hombre = duracion_horas x participantes (se calcula al crear el curso).
    data = [
        {"fecha": "2026-09-02", "modulo": "LIDERAZGO", "submodulo": "LIDERAZGO ORGANIZACIONAL", "modalidad": "Virtual", "tienda": "Todas", "responsable": "Jonathan Sanchez", "duracion_horas": 2.0, "participantes": 12, "horas_hombre": 24.0},
        {"fecha": "2026-09-16", "modulo": "LIDERAZGO", "submodulo": "ESCUELA DE LIDERAZGO JEFE DE TIENDA", "modalidad": "Presencial", "tienda": "Todas", "responsable": "Jonathan Sanchez", "duracion_horas": 4.0, "participantes": 8, "horas_hombre": 32.0},
        {"fecha": "2026-09-17", "modulo": "LIDERAZGO", "submodulo": "ESCUELA DE LIDERAZGO JEFE DE TIENDA", "modalidad": "Presencial", "tienda": "Todas", "responsable": "Jonathan Sanchez", "duracion_horas": 4.0, "participantes": 8, "horas_hombre": 32.0},
        {"fecha": "2026-09-28", "modulo": "VENTAS", "submodulo": "INTRODUCCION A VENTAS", "modalidad": "Presencial", "tienda": "Todas", "responsable": "Jonathan Sanchez", "duracion_horas": 3.0, "participantes": 15, "horas_hombre": 45.0},
    ]
    return data


def cargar_capacitaciones():
    # Se guarda en session_state para que los cursos que el usuario cree
    # durante la sesion se mantengan visibles mientras usa la app.
    if "capacitaciones" not in st.session_state:
        st.session_state["capacitaciones"] = capacitaciones_iniciales()
    return pd.DataFrame(st.session_state["capacitaciones"])


# ---------------------------------------------------------------------------
# TARJETA DE METRICA REUTILIZABLE
# ---------------------------------------------------------------------------
def tarjeta_metrica(label, value, sub, columna):
    with columna:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-sub">{sub}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# PAGINA: DASHBOARD DE VISITAS
# ---------------------------------------------------------------------------
def pagina_visitas():
    st.title("Visitas a Sucursales")
    st.caption("Registro y seguimiento de supervisores en campo")

    if st.button("+ Registrar Visita", type="primary"):
        st.info("Aqui iria un formulario (st.form) para registrar una nueva visita.")

    visitas = cargar_visitas()

    c1, c2, c3, c4 = st.columns(4)
    tarjeta_metrica("Visitas esta semana", len(visitas), "de 18 sucursales", c1)
    tarjeta_metrica("Visitas - Septiembre 2026", len(visitas), "del mes seleccionado", c2)
    tarjeta_metrica("Sucursales visitadas", visitas["sucursal"].nunique(), "de 18 en el mes", c3)
    tarjeta_metrica("Supervisores activos", visitas["supervisor"].nunique(), "en campo", c4)

    st.write("")
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("📊 Visitas por Supervisor")
        conteo = visitas.groupby("supervisor").size().reset_index(name="visitas")
        fig = px.bar(conteo, x="visitas", y="supervisor", orientation="h", text="visitas")
        fig.update_layout(
            yaxis_title="", xaxis_title="",
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e5e7eb", height=350,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_der:
        st.subheader("🏬 Cobertura de Sucursales")
        todas_sucursales = ["Escuintla", "Mazatenango", "Santa Lucia", "San Cristobal",
                             "Obelisco", "Hincapie", "Norte", "Coban", "Barrios", "Montserrat"]
        for suc in todas_sucursales:
            visitas_suc = visitas[visitas["sucursal"] == suc]
            n = len(visitas_suc)
            estado = f"{n} visita" + ("s" if n != 1 else "") if n > 0 else "Sin visita"
            color = "🟢" if n > 0 else "🔴"
            st.write(f"{color} **{suc}** — {estado}")


# ---------------------------------------------------------------------------
# PAGINA: CAPACITACION
# ---------------------------------------------------------------------------
def pagina_capacitacion():
    st.title("🎓 Capacitacion")
    st.caption("Modulos y submodulos de capacitacion por tienda, con material de apoyo y calificacion del personal.")

    capacitaciones = cargar_capacitaciones()

    # --- Metricas de horas hombre ---------------------------------------
    c1, c2, c3 = st.columns(3)
    tarjeta_metrica("Cursos creados", len(capacitaciones), "en total", c1)
    tarjeta_metrica("Horas hombre totales", f"{capacitaciones['horas_hombre'].sum():.0f}", "acumuladas", c2)
    tarjeta_metrica("Participantes totales", int(capacitaciones["participantes"].sum()), "en todos los cursos", c3)

    st.write("")

    # --- Formulario para crear un nuevo curso ----------------------------
    with st.expander("➕ Crear nuevo curso"):
        with st.form("nuevo_curso_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                fecha_curso = st.date_input("Fecha del curso", value=date(2026, 9, 4))
                modulo = st.text_input("Modulo", placeholder="Ej. VENTAS")
                submodulo = st.text_input("Submodulo", placeholder="Ej. TECNICAS DE CIERRE")
                modalidad = st.selectbox("Modalidad", ["Presencial", "Virtual"])
            with col_b:
                tienda = st.text_input("Tienda", value="Todas")
                responsable = st.text_input("Responsable", value=st.session_state.get("nombre", ""))
                duracion_horas = st.number_input("Duracion del curso (horas)", min_value=0.5, step=0.5, value=2.0)
                participantes = st.number_input("Numero de participantes", min_value=1, step=1, value=10)

            horas_hombre = duracion_horas * participantes
            st.metric("Horas hombre de este curso", f"{horas_hombre:.1f}")
            st.caption("Se calcula automaticamente: duracion del curso × numero de participantes.")

            crear = st.form_submit_button("Crear curso", type="primary")

            if crear:
                if not modulo or not submodulo:
                    st.error("Modulo y submodulo son obligatorios.")
                else:
                    st.session_state["capacitaciones"].append({
                        "fecha": fecha_curso.strftime("%Y-%m-%d"),
                        "modulo": modulo.upper(),
                        "submodulo": submodulo.upper(),
                        "modalidad": modalidad,
                        "tienda": tienda,
                        "responsable": responsable,
                        "duracion_horas": duracion_horas,
                        "participantes": participantes,
                        "horas_hombre": horas_hombre,
                    })
                    st.success(f"Curso '{submodulo}' creado con {horas_hombre:.1f} horas hombre.")
                    st.rerun()

    st.subheader("📅 Cronograma de capacitaciones")
    mes = st.date_input("Mes a consultar (elige cualquier dia de ese mes)", value=date(2026, 9, 4))

    tab_lista, tab_calendario, tab_qr = st.tabs(["📋 Lista", "🗓️ Calendario", "🔗 Registro (QR)"])

    with tab_lista:
        st.dataframe(
            capacitaciones,
            use_container_width=True,
            hide_index=True,
            column_config={
                "duracion_horas": st.column_config.NumberColumn("Duracion (h)", format="%.1f"),
                "participantes": st.column_config.NumberColumn("Participantes"),
                "horas_hombre": st.column_config.NumberColumn("Horas hombre", format="%.1f"),
            },
        )

    with tab_calendario:
        st.info("Aqui se podria usar streamlit-calendar o una tabla agrupada por fecha.")

    with tab_qr:
        st.info("Aqui iria la generacion o lectura de codigos QR (libreria 'qrcode').")


# ---------------------------------------------------------------------------
# APP PRINCIPAL
# ---------------------------------------------------------------------------
def app_principal():
    with st.sidebar:
        st.markdown("### Vision Digital")
        st.caption("Tu punto de impresion")
        st.divider()
        st.write(f"**Sesion:** {st.session_state['nombre']}")
        st.caption(f"Rol: {st.session_state['rol']}")
        if st.button("Cerrar sesion"):
            st.session_state.clear()
            st.rerun()
        st.divider()

        pagina = st.radio(
            "Navegacion",
            ["Visitas Sucursales", "Capacitacion"],
            label_visibility="collapsed",
        )

    if pagina == "Visitas Sucursales":
        pagina_visitas()
    elif pagina == "Capacitacion":
        pagina_capacitacion()


# ---------------------------------------------------------------------------
# PUNTO DE ENTRADA
# ---------------------------------------------------------------------------
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

if st.session_state["logueado"]:
    app_principal()
else:
    pantalla_login()
