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

Este proyecto construye un pipeline automatizado que extrae, procesa y visualiza las licitaciones hospitalarias públicas de Chile para responder preguntas críticas de supply chain:

- ¿Qué hospitales gastan más y en qué?
- ¿Cuánto demora el sistema en adjudicar una compra?
- ¿Qué regiones tienen procesos de compra más eficientes?
- ¿Qué insumos médicos se licitan con mayor frecuencia?

---

## 📊 Hallazgos principales

Los siguientes insights fueron extraídos del análisis de **195 licitaciones hospitalarias** y **1.828 items de productos** correspondientes al período analizado.

### 🔴 Baja efectividad del proceso de compra

Solo el **21% de las licitaciones son adjudicadas**, lo que indica una baja tasa de éxito en los procesos de compra pública hospitalaria. Esto sugiere problemas en el diseño de bases de licitación, baja participación de proveedores o desalineación con las condiciones reales del mercado.

### ⚡ Procesos de compra lentos

El tiempo promedio de adjudicación supera los **60 días**, lo que refleja una baja eficiencia operativa que impacta directamente en la disponibilidad de insumos y la continuidad operacional de los hospitales.

### 🟠 Falta de visibilidad financiera

Solo el **45% de las licitaciones cuenta con monto estimado informado**, lo que limita el control presupuestario y la transparencia del sistema. El monto total analizado supera los **$9.600 millones CLP**.

### 🟡 Alta concentración del gasto

El gasto se concentra en un grupo reducido de hospitales, liderado por el **Hospital Padre Alberto Hurtado** y el **Servicio de Salud Oriente Hospital del Salvador**, ambos de la Región Metropolitana. Esto indica centralización de compras y posible desigualdad en la asignación de recursos entre regiones.

### 🔁 Evidencia de compras reactivas

Algunos hospitales presentan alta frecuencia de licitaciones en períodos cortos, lo que sugiere una gestión de abastecimiento poco planificada y compras reactivas en vez de preventivas.

### 📦 Mezcla de compras clínicas y operativas

Las licitaciones incluyen tanto insumos médicos críticos como medicamentos, equipamiento quirúrgico y reactivos de laboratorio, junto con productos administrativos como útiles de oficina y arriendo de vehículos. Esto evidencia una oportunidad para segmentar estrategias de compra y optimizar los procesos de adquisición.

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
