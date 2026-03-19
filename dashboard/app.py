import sys
import os
import streamlit as st
import plotly.express as px
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import DB

st.set_page_config(
    page_title="Chile Hospital Procurement",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Chile Hospital Procurement Intelligence")
st.caption("Monitor de licitaciones hospitalarias públicas — MercadoPublico Chile")

# ── Cargar datos ──────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    db = DB()
    df = db.query("SELECT * FROM licitaciones ORDER BY date_scraped DESC")
    return df

@st.cache_data
def cargar_items():
    db = DB()
    df = db.query("""
        SELECT i.*, l.region, l.hospital
        FROM items i
        JOIN licitaciones l ON i.codigo_licitacion = l.codigo
    """)
    return df

def clasificar_categoria(cat):
    if pd.isna(cat):
        return "Otros"
    cat = cat.lower()
    if "medicamento" in cat or "farmacéutico" in cat or "farmac" in cat:
        return "Medicamentos"
    elif "equipamiento y suministros médicos" in cat:
        return "Equipamiento médico"
    elif "laboratorio" in cat:
        return "Laboratorio"
    elif "salud" in cat or "medicina" in cat or "sanitario" in cat:
        return "Servicios de salud"
    elif "construccion" in cat or "construcción" in cat or "estructura" in cat:
        return "Construcción"
    else:
        return "Otros"

df       = cargar_datos()
df_items = cargar_items()

if df.empty:
    st.error("No hay datos. Ejecuta python pipeline.py primero.")
    st.stop()

df_items["grupo"] = df_items["categoria"].apply(clasificar_categoria)

# ── Cálculos para KPIs ────────────────────────────────────────────────────────
total               = len(df)
df_con_monto        = df[df["monto_estimado"].notna()]
monto_total         = df_con_monto["monto_estimado"].sum()
ticket_promedio     = df_con_monto["monto_estimado"].mean()
pct_monto           = round(len(df_con_monto) / total * 100, 1)
total_adjudicadas   = len(df[df["estado"] == "Adjudicada"])
pct_adjudicadas     = round(total_adjudicadas / total * 100, 1)
total_fallidas      = len(df[df["estado"].isin(["Desierta", "Revocada"])])
tasa_fallidas       = round(total_fallidas / total * 100, 1)
gasto_por_hospital  = monto_total / df["hospital"].nunique() if df["hospital"].nunique() > 0 else 0

df["fecha_publicacion"]  = pd.to_datetime(df["fecha_publicacion"],  errors="coerce")
df["fecha_adjudicacion"] = pd.to_datetime(df["fecha_adjudicacion"], errors="coerce")
df_adj = df[df["fecha_adjudicacion"].notna() & df["fecha_publicacion"].notna()].copy()
df_adj["dias_licitacion"] = (df_adj["fecha_adjudicacion"] - df_adj["fecha_publicacion"]).dt.days
tiempo_promedio = round(df_adj["dias_licitacion"].mean(), 1) if not df_adj.empty else 0

# ── BLOQUE 1 — Resumen ────────────────────────────────────────────────────────
st.subheader("📊 Resumen general")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total licitaciones",     value=total)
with col2:
    st.metric(label="Monto total (CLP)",      value=f"${monto_total:,.0f}")
with col3:
    st.metric(label="Ticket promedio",        value=f"${ticket_promedio:,.0f}")
with col4:
    st.metric(label="% Adjudicadas",          value=f"{pct_adjudicadas}%")

# ── BLOQUE 2 — Eficiencia ─────────────────────────────────────────────────────
st.subheader("⚡ Eficiencia del proceso")

col5, col6, col7, col8 = st.columns(4)
with col5:
    st.metric(label="Tiempo promedio (días)", value=f"{tiempo_promedio}")
with col6:
    st.metric(label="Tasa de fallidas",       value=f"{tasa_fallidas}%",
              help="Licitaciones Desiertas + Revocadas")
with col7:
    st.metric(label="% con monto informado",  value=f"{pct_monto}%")
with col8:
    st.metric(label="Gasto promedio hospital",value=f"${gasto_por_hospital:,.0f}")

# ── Filtros ───────────────────────────────────────────────────────────────────
st.divider()
st.subheader("🔍 Licitaciones hospitalarias")

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    regiones = ["Todas"] + sorted(df["region"].dropna().unique().tolist())
    filtro_region = st.selectbox("Filtrar por región", regiones)

with col_f2:
    estados = ["Todos"] + sorted(df["estado"].dropna().unique().tolist())
    filtro_estado = st.selectbox("Filtrar por estado", estados)

with col_f3:
    busqueda = st.text_input("Buscar hospital", placeholder="Ej: Valdivia...")

df_filtrado = df.copy()

if filtro_region != "Todas":
    df_filtrado = df_filtrado[df_filtrado["region"] == filtro_region]
if filtro_estado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["estado"] == filtro_estado]
if busqueda:
    df_filtrado = df_filtrado[
        df_filtrado["hospital"].str.contains(busqueda, case=False, na=False)
    ]

df_items_filtrado = df_items.copy()
if filtro_region != "Todas":
    df_items_filtrado = df_items_filtrado[df_items_filtrado["region"] == filtro_region]

# ── Tabla dinámica ────────────────────────────────────────────────────────────
def colorear_estado(val):
    if val == "Publicada":
        return "background-color: #cce5ff; color: #004085"
    elif val == "Cerrada":
        return "background-color: #fff3cd; color: #856404"
    elif val == "Adjudicada":
        return "background-color: #d4edda; color: #155724"
    elif val in ["Desierta", "Revocada"]:
        return "background-color: #f8d7da; color: #721c24"
    return ""

st.dataframe(
    df_filtrado[[
        "codigo", "hospital", "region",
        "estado", "monto_estimado", "fecha_publicacion"
    ]].style.applymap(colorear_estado, subset=["estado"]),
    use_container_width=True,
    hide_index=True
)
st.caption(f"Mostrando {len(df_filtrado)} licitaciones")

# ── BLOQUE 3 — Análisis territorial ──────────────────────────────────────────
st.divider()
st.subheader("🗺️ Análisis territorial")

col_g1, col_g2 = st.columns(2)

with col_g1:
    df_region_bar = df_filtrado.groupby("region").agg(
        total=("codigo", "count")
    ).reset_index().sort_values("total", ascending=True)

    fig_r1 = px.bar(
        df_region_bar,
        x="total", y="region", orientation="h",
        title="Licitaciones por región",
        labels={"total": "Total", "region": ""},
        color="total", color_continuous_scale="Blues"
    )
    fig_r1.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False, height=420
    )
    st.plotly_chart(fig_r1, use_container_width=True)

with col_g2:
    df_region_monto = df_filtrado[df_filtrado["monto_estimado"].notna()].groupby("region").agg(
        monto_total=("monto_estimado", "sum")
    ).reset_index().sort_values("monto_total", ascending=True)

    fig_r2 = px.bar(
        df_region_monto,
        x="monto_total", y="region", orientation="h",
        title="Monto total por región (CLP)",
        labels={"monto_total": "Monto", "region": ""},
        color="monto_total", color_continuous_scale="Greens"
    )
    fig_r2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False, height=420
    )
    st.plotly_chart(fig_r2, use_container_width=True)

# ── BLOQUE 4 — Gestión hospitalaria ──────────────────────────────────────────
st.divider()
st.subheader("🏥 Gestión hospitalaria")

col_h1, col_h2 = st.columns(2)

with col_h1:
    df_top = df_filtrado[df_filtrado["monto_estimado"].notna()].groupby(
        ["hospital", "region"]
    ).agg(
        monto_total=("monto_estimado", "sum")
    ).reset_index().sort_values("monto_total", ascending=False).head(10)

    if not df_top.empty:
        fig_top = px.bar(
            df_top,
            x="monto_total", y="hospital", orientation="h",
            color="region",
            title="Top 10 hospitales por monto licitado",
            labels={"monto_total": "Monto (CLP)", "hospital": "", "region": "Región"}
        )
        fig_top.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=420
        )
        st.plotly_chart(fig_top, use_container_width=True)

with col_h2:
    df_freq = df_filtrado.groupby("hospital").agg(
        frecuencia=("codigo", "count")
    ).reset_index().sort_values("frecuencia", ascending=False).head(10)

    fig_freq = px.bar(
        df_freq,
        x="frecuencia", y="hospital", orientation="h",
        title="Top 10 hospitales por frecuencia de compra",
        labels={"frecuencia": "Nº licitaciones", "hospital": ""}
    )
    fig_freq.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=420
    )
    st.plotly_chart(fig_freq, use_container_width=True)

# ── BLOQUE 5 — Abastecimiento ─────────────────────────────────────────────────
st.divider()
st.subheader("📦 Análisis de abastecimiento")

col_p1, col_p2 = st.columns([1, 3])
with col_p1:
    grupos = ["Todos"] + sorted(df_items_filtrado["grupo"].unique().tolist())
    filtro_grupo = st.selectbox("Categoría de producto", grupos)

if filtro_grupo != "Todos":
    df_items_filtrado = df_items_filtrado[df_items_filtrado["grupo"] == filtro_grupo]

col_ab1, col_ab2 = st.columns(2)

with col_ab1:
    df_productos = df_items_filtrado.groupby("nombre_producto").size(
    ).reset_index(name="total").sort_values("total", ascending=True).tail(15)

    fig_prod = px.bar(
        df_productos,
        x="total", y="nombre_producto", orientation="h",
        title="Top 15 productos más solicitados",
        labels={"total": "Veces solicitado", "nombre_producto": ""}
    )
    fig_prod.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=500
    )
    st.plotly_chart(fig_prod, use_container_width=True)

with col_ab2:
    df_gasto_cat = df_items_filtrado.groupby("grupo").size(
    ).reset_index(name="total").sort_values("total", ascending=False)

    fig_cat = px.pie(
        df_gasto_cat,
        values="total", names="grupo",
        title="Distribución de items por categoría",
        hole=0.4
    )
    fig_cat.update_layout(height=500)
    st.plotly_chart(fig_cat, use_container_width=True)

# ── Resumen por región ────────────────────────────────────────────────────────
st.divider()
st.subheader("📋 Resumen por región")

df_resumen = df_filtrado.groupby("region").agg(
    licitaciones      =("codigo",         "count"),
    con_monto         =("monto_estimado", "count"),
    monto_total       =("monto_estimado", "sum"),
    monto_promedio    =("monto_estimado", "mean"),
    hospitales_unicos =("hospital",       "nunique")
).reset_index().sort_values("monto_total", ascending=False)

df_resumen["monto_total"]    = df_resumen["monto_total"].apply(
    lambda x: f"${x:,.0f}" if x > 0 else "N/A"
)
df_resumen["monto_promedio"] = df_resumen["monto_promedio"].apply(
    lambda x: f"${x:,.0f}" if pd.notna(x) else "N/A"
)

st.dataframe(
    df_resumen.rename(columns={
        "region":            "Región",
        "licitaciones":      "Total licitaciones",
        "con_monto":         "Con monto",
        "monto_total":       "Monto total",
        "monto_promedio":    "Monto promedio",
        "hospitales_unicos": "Hospitales únicos"
    }),
    use_container_width=True,
    hide_index=True
)
