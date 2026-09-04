"""
Deseret Proyectos y Capacitaciones
Estructura base: login simple, tarjetas de metricas, formulario para crear
cursos con calculo de horas hombre, y tabla con tabs (Lista / Calendario / Registro).

Correr con:
    pip install streamlit pandas
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import calendar
from datetime import date

# ---------------------------------------------------------------------------
# CONFIGURACION GENERAL
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Deseret Proyectos y Capacitaciones",
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
    st.title("Deseret Proyectos y Capacitaciones")
    st.caption("Gestion de capacitacion")
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
        capacitaciones_mostrar = capacitaciones.reset_index().rename(columns={"index": "_idx"})

        evento = st.dataframe(
            capacitaciones_mostrar.drop(columns=["_idx"]),
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="multi-row",
            column_config={
                "duracion_horas": st.column_config.NumberColumn("Duracion (h)", format="%.1f"),
                "participantes": st.column_config.NumberColumn("Participantes"),
                "horas_hombre": st.column_config.NumberColumn("Horas hombre", format="%.1f"),
            },
        )

        filas_seleccionadas = evento.selection.rows if evento and evento.selection else []

        if filas_seleccionadas:
            st.warning(f"{len(filas_seleccionadas)} curso(s) seleccionado(s) para borrar.")
            if st.button("🗑️ Borrar curso(s) seleccionado(s)", type="primary"):
                indices_reales = capacitaciones_mostrar.iloc[filas_seleccionadas]["_idx"].tolist()
                for i in sorted(indices_reales, reverse=True):
                    st.session_state["capacitaciones"].pop(i)
                st.success("Curso(s) eliminado(s).")
                st.rerun()
        else:
            st.caption("Selecciona una o mas filas (marca la casilla a la izquierda) para poder borrarlas.")

    with tab_calendario:
        mostrar_calendario(capacitaciones, mes)

    with tab_qr:
        st.info("Aqui iria la generacion o lectura de codigos QR (libreria 'qrcode').")


# ---------------------------------------------------------------------------
# CALENDARIO INTERACTIVO
# ---------------------------------------------------------------------------
def mostrar_calendario(capacitaciones, mes_referencia):
    anio = mes_referencia.year
    mes_num = mes_referencia.month

    # Fechas con curso, agrupadas por dia (para saber cuantos hay cada dia)
    capacitaciones = capacitaciones.copy()
    capacitaciones["fecha_dt"] = pd.to_datetime(capacitaciones["fecha"]).dt.date
    cursos_por_dia = capacitaciones.groupby("fecha_dt").size().to_dict()

    if "dia_seleccionado" not in st.session_state:
        st.session_state["dia_seleccionado"] = None

    nombre_mes = calendar.month_name[mes_num].capitalize()
    st.markdown(f"**{nombre_mes} {anio}**")

    dias_semana = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]
    cols_header = st.columns(7)
    for c, d in zip(cols_header, dias_semana):
        c.markdown(f"<div style='text-align:center; color:#6b7280; font-size:12px;'>{d}</div>", unsafe_allow_html=True)

    semanas = calendar.monthcalendar(anio, mes_num)
    for semana in semanas:
        cols = st.columns(7)
        for col, dia in zip(cols, semana):
            if dia == 0:
                col.write("")
                continue
            fecha_actual = date(anio, mes_num, dia)
            n_cursos = cursos_por_dia.get(fecha_actual, 0)
            etiqueta = f"{dia} 🔵" if n_cursos > 0 else f"{dia}"
            tipo = "primary" if n_cursos > 0 else "secondary"
            if col.button(etiqueta, key=f"dia_{fecha_actual}", type=tipo, use_container_width=True):
                st.session_state["dia_seleccionado"] = fecha_actual

    st.divider()

    dia_sel = st.session_state["dia_seleccionado"]
    if dia_sel:
        cursos_del_dia = capacitaciones[capacitaciones["fecha_dt"] == dia_sel]
        st.markdown(f"#### Cursos el {dia_sel.strftime('%d/%m/%Y')}")
        if cursos_del_dia.empty:
            st.info("No hay cursos programados ese dia.")
        else:
            for _, curso in cursos_del_dia.iterrows():
                with st.container(border=True):
                    st.markdown(f"**{curso['submodulo']}** · {curso['modulo']}")
                    st.caption(
                        f"{curso['modalidad']} · Tienda: {curso['tienda']} · "
                        f"Responsable: {curso['responsable']}"
                    )
                    st.caption(
                        f"Duracion: {curso['duracion_horas']:.1f}h · "
                        f"Participantes: {int(curso['participantes'])} · "
                        f"Horas hombre: {curso['horas_hombre']:.1f}"
                    )
    else:
        st.caption("Toca un dia con 🔵 para ver los cursos programados.")


# ---------------------------------------------------------------------------
# APP PRINCIPAL
# ---------------------------------------------------------------------------
def app_principal():
    with st.sidebar:
        st.markdown("### Deseret Proyectos y Capacitaciones")
        st.caption("Gestion de capacitacion")
        st.divider()
        st.write(f"**Sesion:** {st.session_state['nombre']}")
        st.caption(f"Rol: {st.session_state['rol']}")
        if st.button("Cerrar sesion"):
            st.session_state.clear()
            st.rerun()

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
