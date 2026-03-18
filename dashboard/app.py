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
@st.cache_data
def cargar_datos():
    db = DB()
    df = db.query("SELECT * FROM licitaciones ORDER BY date_scraped DESC")
    return df

df = cargar_datos()

if df.empty:
    st.error("No hay datos en la base de datos. Ejecuta python pipeline.py primero.")
    st.stop()
st.subheader("Resumen general")

col1, col2, col3, col4 = st.columns(4)

df_con_monto = df[df["monto_estimado"].notna()]
monto_total  = df_con_monto["monto_estimado"].sum()

with col1:
    st.metric(
        label="Total licitaciones",
        value=len(df)
    )
with col2:
    st.metric(
        label="Con monto estimado",
        value=len(df_con_monto)
    )
with col3:
    st.metric(
        label="Monto total (CLP)",
        value=f"${monto_total:,.0f}"
    )
with col4:
    st.metric(
        label="Hospitales únicos",
        value=df["hospital"].nunique()
    )
st.divider()
st.subheader("Licitaciones hospitalarias")

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

def colorear_estado(val):
    if val == "Publicada":
        return "background-color: #cce5ff; color: #004085"
    elif val == "Cerrada":
        return "background-color: #fff3cd; color: #856404"
    elif val == "Adjudicada":
        return "background-color: #d4edda; color: #155724"
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
st.divider()
st.subheader("Análisis por región")

col_g1, col_g2 = st.columns(2)

with col_g1:
    df_region = df.groupby("region").agg(
        total=("codigo", "count"),
        monto=("monto_estimado", "sum")
    ).reset_index().sort_values("total", ascending=True)

    fig1 = px.bar(
        df_region,
        x="total",
        y="region",
        orientation="h",
        title="Licitaciones por región",
        labels={"total": "Total licitaciones", "region": ""},
        color="total",
        color_continuous_scale="Blues"
    )
    fig1.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        coloraxis_showscale=False
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    df_monto = df[df["monto_estimado"].notna()].groupby("region").agg(
        monto_total=("monto_estimado", "sum")
    ).reset_index().sort_values("monto_total", ascending=True)

    fig2 = px.bar(
        df_monto,
        x="monto_total",
        y="region",
        orientation="h",
        title="Monto total estimado por región (CLP)",
        labels={"monto_total": "Monto total", "region": ""},
        color="monto_total",
        color_continuous_scale="Greens"
    )
    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        coloraxis_showscale=False
    )
    st.plotly_chart(fig2, use_container_width=True)
st.divider()
st.subheader("Top 10 hospitales por monto estimado")

df_top = df[df["monto_estimado"].notna()].groupby(
    ["hospital", "region"]
).agg(
    total_licitaciones=("codigo", "count"),
    monto_total=("monto_estimado", "sum")
).reset_index().sort_values("monto_total", ascending=False).head(10)

fig3 = px.bar(
    df_top,
    x="monto_total",
    y="hospital",
    orientation="h",
    color="region",
    title="Top 10 hospitales por monto total licitado",
    labels={
        "monto_total": "Monto total (CLP)",
        "hospital":    "",
        "region":      "Región"
    }
)
fig3.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    height=450
)
st.plotly_chart(fig3, use_container_width=True)
st.divider()
st.subheader("Resumen por región")

df_resumen = df.groupby("region").agg(
    licitaciones      =("codigo",          "count"),
    con_monto         =("monto_estimado",  "count"),
    monto_total       =("monto_estimado",  "sum"),
    monto_promedio    =("monto_estimado",  "mean"),
    hospitales_unicos =("hospital",        "nunique")
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
