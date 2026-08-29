# 🏥 Chile Hospital Procurement Intelligence

Monitor automatizado de licitaciones hospitalarias públicas — API MercadoPublico Chile

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automatizado-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Objetivo del proyecto

Chile destina miles de millones de pesos anuales en licitaciones hospitalarias públicas. Sin embargo, esa información está dispersa en cientos de registros en MercadoPublico y nunca ha sido analizada de forma sistemática.

Este proyecto construye un pipeline automatizado que extrae, procesa y visualiza las licitaciones hospitalarias públicas de Chile para responder preguntas críticas de supply chain y control de gestión:

- ¿Qué hospitales gastan más y en qué categorías de insumos?
- ¿cuánto demora el sistema en adjudicar una compra hospitalaria?
- ¿Qué regiones concentran el mayor volumen y presupuesto?
- ¿Qué insumos médicos y farmacéuticos se licitan con mayor frecuencia?

---

## 📊 Hallazgos principales

> Los insights se actualizan automáticamente con cada ejecución del pipeline.
> Los datos mostrados a continuación corresponden al análisis consolidado
> con las licitaciones registradas al **29 de agosto de 2026**.

### 🔴 Baja efectividad de adjudicación
Solo el **21,0% de las licitaciones fueron adjudicadas** en el período analizado (sobre un total de 195 procesos identificados), lo que evidencia desafíos en la participación de proveedores o en el diseño de las bases de licitación.

### ⚡ Ciclos de compra extendidos
El tiempo promedio de adjudicación alcanza los **60,3 días**, impactando directamente la oportunidad y continuidad en la disponibilidad de insumos hospitalarios.

### 🟠 Limitada visibilidad financiera
Solo el **45,1% de las licitaciones contó con un monto estimado informado**, lo que restringe el control presupuestario previo del sistema. Además, la tasa de licitaciones fallidas fue del **3,1%**.

### 🟡 Concentración territorial del presupuesto
El monto total analizado superó los **$9.633 millones CLP**, concentrado fuertemente en la Región Metropolitana de Santiago ($5.822 MM CLP; 65 licitaciones), seguida por la Región del Biobío ($903 MM CLP) y la Región de los Lagos ($892 MM CLP).

### 🔁 Compras reactivas y gestión hospitalaria
Hospitales como el **Hospital de Melipilla** y el **Servicio de Salud Hospital de Santa Cruz** encabezan la frecuencia de compras, mientras que el **Servicio de Salud Los Ríos** y la **Municipalidad de Pica** concentran los mayores montos licitados.

### 📦 Estructura de abastecimiento e insumos
Las **Farmacias** y las **Unidades dentales/médicas** lideran los productos más solicitados. En la distribución por categoría médica, el equipamiento representa un **27,6%** y los medicamentos un **26,6%** del total de ítems licitados.

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

El análisis revela que el sistema de compras hospitalarias públicas en Chile presenta desafíos relevantes en eficiencia, planificación y control financiero. Las principales oportunidades de mejora se centran en aumentar la tasa de adjudicación, reducir tiempos de proceso e implementar estrategias de compra más planificadas.

---

## 📌 Próximos pasos

- Modelo predictivo de demanda de insumos
- Segmentación de hospitales según eficiencia de compra
- Alertas automáticas de licitaciones críticas
- Integración con datos de escasez FDA para correlación de supply chain

---

## ⚖️ Fuente de datos

Datos obtenidos desde la **API pública de MercadoPublico** (ChileCompra — Dirección de Compras y Contratación Pública). Fuente: [api.mercadopublico.cl](https://api.mercadopublico.cl)

---

## 👤 Autor

**Ivan Arancibia** — [@Iarancibia98](https://github.com/Iarancibia98)
