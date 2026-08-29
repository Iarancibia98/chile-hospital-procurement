# 🏥 Chile Hospital Procurement Intelligence

Monitor automatizado de licitaciones hospitalarias públicas — API MercadoPublico Chile

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automatizado-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Objetivo del proyecto

Chile destina miles de millones de pesos anuales en licitaciones hospitalarias públicas. Sin embargo, esa información está dispersa en cientos de registros en MercadoPublico y requiere procesamiento para transformarse en información útil para la toma de decisiones.

Este proyecto construye un pipeline automatizado que extrae, procesa, almacena y visualiza licitaciones hospitalarias públicas de Chile para responder preguntas relevantes de **Supply Chain y Control de Gestión**:

- ¿Qué hospitales e instituciones concentran mayores montos licitados?
- ¿Cuánto demora el sistema en adjudicar una compra hospitalaria?
- ¿Qué regiones concentran el mayor volumen de licitaciones y presupuesto?
- ¿Qué productos e insumos se solicitan con mayor frecuencia?
- ¿Cómo se distribuyen los ítems licitados según categoría?

---

## 📊 Hallazgos principales

> Los insights se actualizan automáticamente con cada ejecución del pipeline.
>
> Los datos mostrados a continuación corresponden al análisis consolidado con las licitaciones registradas al **29 de agosto de 2026**.

### 🔴 Baja proporción de adjudicación

Solo el **21,0% de las licitaciones fueron adjudicadas** en el período analizado, sobre un total de **195 procesos identificados**.

Este indicador permite monitorear la efectividad del proceso de compra y constituye una métrica relevante para analizar posteriormente las causas de los procesos no adjudicados.

### ⚡ Ciclos de compra extendidos

El tiempo promedio de adjudicación alcanza los **60,3 días**, proporcionando una métrica relevante para evaluar la duración de los procesos de adquisición y su impacto potencial sobre la oportunidad de abastecimiento.

### 🟠 Limitada visibilidad financiera

Solo el **45,1% de las licitaciones contó con un monto estimado informado**, lo que limita la disponibilidad de información financiera para el análisis previo de los procesos.

El **gasto promedio por hospital fue de $82.335.689 CLP**, mientras que la tasa de licitaciones fallidas alcanzó el **3,1%**.

### 🟡 Concentración territorial del presupuesto

El monto total analizado alcanzó los **$9.633 millones CLP**.

La **Región Metropolitana de Santiago** concentró el mayor volumen, con **65 licitaciones** y aproximadamente **$5.822 millones CLP**, seguida por la **Región del Biobío**, con aproximadamente **$903 millones CLP**, y la **Región de Los Lagos**, con aproximadamente **$893 millones CLP**.

### 🔁 Concentración institucional de las compras

El análisis evidencia diferencias importantes en el comportamiento de compra entre instituciones.

Entre las instituciones con mayor frecuencia de licitaciones se encuentran el **Servicio de Salud Oriente — Hospital del Salvador**, el **Servicio de Salud Araucanía Sur — Hospital de Nueva Imperial** y el **Hospital Padre Alberto Hurtado**.

En términos de monto licitado, destacan instituciones como el **Hospital Padre Alberto Hurtado**, el **Servicio de Salud Oriente — Hospital del Salvador** y el **Hospital de Melipilla**.

### 📦 Estructura de abastecimiento e insumos

El análisis incorpora un ranking de los **15 productos más solicitados** y una distribución de los ítems por categoría.

Entre los productos con mayor frecuencia aparecen **Farmacias**, **Unidades dentales** y **Unidades médicas**, además de distintos insumos, equipamiento y servicios asociados al ámbito hospitalario.

En la distribución por categoría, **Equipamiento representa el 27,6%** y **Medicamentos el 26,6%** del total de ítems analizados.

---

## 🏗️ Arquitectura del sistema
```
API MercadoPublico (api.mercadopublico.cl)
         ↓
   Scraper Python
   requests + JSON
         ↓
   Filtro hospitalario
   212 de 1.456 licitaciones diarias
         ↓
   Limpieza de datos
   Pandas
         ↓
   Base de datos
   SQLite (licitaciones + items)
         ↓
   Dashboard interactivo
   Streamlit — 5 bloques analíticos
         ↓
   Automatización
   GitHub Actions — ejecución diaria
```

---

## 📁 Estructura del proyecto
```
chile-hospital-procurement/
├── .github/
│   └── workflows/
│       └── pipeline.yml       ← automatización en la nube
├── scraper/
│   ├── base_scraper.py        ← clase base con rate limiting y reintentos
│   └── mercadopublico_scraper.py ← scraper API MercadoPublico
├── database/
│   ├── schema.sql             ← diseño de tablas licitaciones e items
│   ├── db.py                  ← conexión y carga a SQLite
│   └── analysis.sql           ← queries de análisis supply chain
├── dashboard/
│   └── app.py                 ← dashboard Streamlit con 5 bloques
├── data/
│   └── *.csv                  ← respaldos históricos por fecha
├── pipeline.py                ← orquesta el flujo completo
├── .env                       ← ticket API (no se sube a GitHub)
└── requirements.txt
```

---

## 🛠️ Stack tecnológico

| Capa | Herramienta |
|------|-------------|
| Extracción | Python · requests · API REST |
| Limpieza | Pandas |
| Base de datos | SQLite |
| Automatización | GitHub Actions |
| Dashboard | Streamlit · Plotly |
| Análisis | SQL · Pandas |

---

## 📈 Dashboard — 5 bloques analíticos

**Bloque 1 — Resumen general**
Total licitaciones, monto total, ticket promedio y porcentaje adjudicadas.

**Bloque 2 — Eficiencia del proceso**
Tiempo promedio de adjudicación, tasa de licitaciones fallidas, porcentaje con monto informado y gasto promedio por hospital.

**Bloque 3 — Análisis territorial**
Licitaciones y monto por región con filtro interactivo.

**Bloque 4 — Gestión hospitalaria**
Top 10 hospitales por monto licitado y por frecuencia de compra.

**Bloque 5 — Análisis de abastecimiento**
Top 15 productos más solicitados y distribución por categoría médica.

---

## 🚀 Instalación y uso
```bash
# 1. Clonar el repositorio
git clone https://github.com/Iarancibia98/chile-hospital-procurement.git
cd chile-hospital-procurement

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar ticket API
echo MERCADOPUBLICO_TICKET=tu_ticket_aqui > .env

# 5. Ejecutar el pipeline
python pipeline.py

# 6. Lanzar el dashboard
streamlit run dashboard/app.py
```

> Para obtener tu ticket gratuito: [api.mercadopublico.cl](https://api.mercadopublico.cl)

---

## ⚙️ Automatización

El pipeline corre automáticamente todos los días vía **GitHub Actions** extrayendo las licitaciones hospitalarias del día y actualizando el historial.

---

## 🧠 Conclusión

El análisis permite observar diferencias relevantes en eficiencia, duración de los procesos, disponibilidad de información financiera, distribución territorial y comportamiento de compra dentro de las licitaciones hospitalarias analizadas.

Los principales indicadores obtenidos son:

- 195 licitaciones analizadas
- $9.633 millones CLP en monto total registrado
- 21,0% de procesos adjudicados
- 60,3 días de tiempo promedio de adjudicación
- 3,1% de tasa de licitaciones fallidas
- 45,1% de procesos con monto informado
- $82.335.689 CLP de gasto promedio por hospital

Estos indicadores establecen una línea base para desarrollar análisis posteriores sobre comportamiento de compra, eficiencia institucional, distribución territorial y gestión de abastecimiento.

---

## 📌 Próximos pasos

El proyecto puede evolucionar hacia análisis más avanzados de Data Analytics, Business Intelligence y Supply Chain, incluyendo:

- Modelo predictivo de demanda de insumos
- Segmentación de hospitales según comportamiento y eficiencia de compra
- Análisis temporal de frecuencia y montos de compra
- Detección de patrones anómalos de contratación
- Análisis de concentración de productos y proveedores
- Predicción de tiempos de adjudicación
- Alertas automáticas de licitaciones críticas
- Integración con fuentes externas de información de abastecimiento
- Correlación con datos de escasez de medicamentos e insumos

---

## ⚖️ Fuente de datos

Datos obtenidos desde la **API pública de MercadoPublico** (ChileCompra — Dirección de Compras y Contratación Pública). Fuente: [api.mercadopublico.cl](https://api.mercadopublico.cl)

---

## 👤 Autor

**Ivan Arancibia** — [@Iarancibia98](https://github.com/Iarancibia98)
