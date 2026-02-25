# 🦐 Monitor Biofloc

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-red?logo=streamlit&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?logo=mongodb&logoColor=white)
![Version](https://img.shields.io/badge/Versión-4.1.0-informational)

**Plataforma de monitoreo IoT para parámetros fisicoquímicos en sistemas Biofloc.**

[📖 Manual de Usuario](docs/MANUAL_USUARIO.md) · [🐛 Reportar Issue](https://github.com/Marton1123/UCN-Lab-IoT-Monitor/issues) · [👤 Autor](https://github.com/Marton1123)

</div>


---

## 📋 Descripción

**Monitor Biofloc** es una aplicación web construida con Streamlit que consolida datos de telemetría provenientes de dispositivos IoT (nodos ESP32/Micro-ROS) hacia una base de datos MongoDB Atlas. Permite supervisar en tiempo real los parámetros fisicoquímicos críticos (temperatura, pH, oxígeno disuelto, etc.) dentro de sistemas Biofloc.

---

## ✨ Funcionalidades

| Módulo | Funcionalidad |
|--------|---------------|
| **🔐 Autenticación** | Login obligatorio con bcrypt, sesión persistente, botón de cierre de sesión |
| **📊 Dashboard** | Tarjetas de dispositivo con estado en tiempo real, KPIs resumen, filtros avanzados |
| **🚦 Sistema de Alertas** | Semaforización automática Normal / Alerta / Crítico con umbrales configurables por dispositivo |
| **📈 Gráficas** | Análisis de tendencias multi-sensor, filtrado de outliers, SMA, rango temporal configurable |
| **📥 Historial** | Consulta histórica con filtros, exportación a Excel (.xlsx) y CSV |
| **⚙️ Configuración** | Alias, ubicación y umbrales de alerta editables por dispositivo desde la UI |

---

## 🏗️ Arquitectura

```
┌────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│  Dispositivos IoT  │─────▶│    MongoDB Atlas      │◀─────│   Monitor Biofloc    │
│  (ESP32 / ROS 2)   │      │  BioFloc_Monitoring   │      │     (Streamlit)      │
└────────────────────┘      └──────────────────────┘      └──────────────────────┘
```

**Stack tecnológico:**
- **Framework**: Streamlit 1.36+
- **Lenguaje**: Python 3.10+
- **Base de datos**: MongoDB Atlas (PyMongo)
- **Visualización**: Plotly
- **Seguridad**: bcrypt

---

## 📁 Estructura del Proyecto

```
UCN-Lab-IoT-Monitor/
│
├── Home.py                          # Punto de entrada: autenticación, navegación y routing
├── requirements.txt                 # Dependencias Python
├── .env                             # Variables de entorno locales (NO en git)
├── .env.example                     # Plantilla de configuración
├── .gitignore
├── README.md
├── CHANGELOG.md                     # Historial de versiones
│
├── .streamlit/
│   ├── config.toml                  # Configuración de tema Streamlit
│   ├── secrets.toml                 # Secretos para deploy en Streamlit Cloud (NO en git)
│   └── secrets.toml.example         # Plantilla de secretos para deploy
│
├── modules/                         # Lógica de negocio
│   ├── auth.py                      # Login / logout con bcrypt
│   ├── database.py                  # Conexión MongoDB, normalización multi-esquema
│   ├── device_manager.py            # Evaluación de estado y salud de dispositivos
│   ├── config_manager.py            # Gestión de umbrales y metadatos de dispositivos
│   ├── sensor_registry.py           # Registro dinámico de sensores desde sensor_defaults.json
│   └── styles.py                    # CSS global y componente header
│
├── views/                           # Vistas de la aplicación (una por página)
│   ├── __init__.py
│   ├── dashboard.py                 # Vista principal con tarjetas de dispositivo
│   ├── graphs.py                    # Gráficas históricas con Plotly
│   ├── history.py                   # Tabla de datos históricos y exportación
│   └── settings.py                  # Configuración de alias, ubicación y umbrales
│
├── config/
│   └── sensor_defaults.json         # Rangos y metadatos por defecto para cada tipo de sensor
│
├── scripts/                         # Utilidades de desarrollo y mantenimiento
│   ├── generate_password_hash.py    # Generador de hash bcrypt para APP_PASSWORD_HASH
│   ├── mock_data_generator.py       # Generador de datos de prueba para desarrollo
│   ├── debug_db.py                  # Herramienta de inspección de MongoDB
│   ├── test_normalization.py        # Tests de normalización multi-esquema
│   └── export_to_excel.py           # Exportación directa a Excel sin la UI
│
├── assets/
│   └── Logo-Acuicultura.png         # Logo del Depto. de Acuicultura UCN
│
└── docs/
    └── MANUAL_USUARIO.md            # Manual de uso para el personal del laboratorio
```

---

## 🗄️ Esquema de Base de Datos

El sistema trabaja con dos colecciones en MongoDB Atlas:

### `sensor_data` — Telemetría de sensores
```json
{
  "timestamp": { "$date": "2026-02-25T15:51:09.557Z" },
  "dispositivo_id": "34865D46A848",
  "datos": {
    "temperatura": 23.21,
    "ph": 4.08
  }
}
```

### `devices_data` — Registro y configuración de dispositivos
```json
{
  "_id": "34865D46A848",
  "nombre": "Dispositivo 5D46A848",
  "estado": "pendiente",
  "ubicacion": null,
  "configuracion": { "intervalo_lectura_seg": 60, "sensores_habilitados": ["ph", "temperatura"] },
  "calibracion": { "ph_offset": 0, "temp_offset": 0 },
  "conexion": { "primera": "...", "ultima": "...", "total_lecturas": 2 }
}
```

> El normalizador multi-esquema en `database.py` soporta ambos formatos (campos en español e inglés) de forma transparente.

---

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Python 3.10+ — se recomienda [Anaconda](https://www.anaconda.com/download)
- Acceso a un cluster de [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

### 1. Clonar el repositorio

```bash
git clone https://github.com/Marton1123/UCN-Lab-IoT-Monitor.git
cd UCN-Lab-IoT-Monitor
```

### 2. Crear y activar el entorno

```bash
conda create --name biofloc_monitor python=3.10 -y
conda activate biofloc_monitor
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia `.env.example` a `.env` y rellena con tus credenciales:

```ini
MONGO_URI=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/
MONGO_DB=BioFloc_Monitoring
MONGO_COLLECTION=sensor_data
MONGO_DEVICES_COLLECTION=devices_data

APP_PASSWORD_HASH=$2b$12$...  # ver paso 4
```

### 4. Generar hash de contraseña

```bash
python -m scripts.generate_password_hash "TuContraseñaSegura"
```

Copia el hash resultante a `APP_PASSWORD_HASH` en el `.env`.

### 5. Ejecutar

```bash
streamlit run Home.py
```

Accede en `http://localhost:8501`

---

## ☁️ Deploy en Streamlit Cloud

1. Sube el repositorio a GitHub (`.env` y `secrets.toml` están en `.gitignore`)
2. Ve a [share.streamlit.io](https://share.streamlit.io) → conecta el repo → selecciona `Home.py`
3. En **Settings → Secrets**, añade el equivalente de tu `.env`:

```toml
MONGO_URI = "mongodb+srv://..."
MONGO_DB = "BioFloc_Monitoring"
MONGO_COLLECTION = "sensor_data"
MONGO_DEVICES_COLLECTION = "devices_data"
APP_PASSWORD_HASH = "$2b$12$..."
```

---

## 📊 Vistas de la Aplicación

### 🏠 Dashboard
- Tarjetas por dispositivo: estado, última lectura, hora de actualización
- KPIs globales: Total · En Línea · Offline · Normal · Alerta · Crítico
- Filtros: por estado, ubicación, alias/ID, checkbox offline
- Actualización parcial por tarjeta (`@st.fragment`) o global

### 📈 Gráficas
- Carga completa del historial cacheada (1 hora de TTL)
- Selector de rango temporal: 5 min → 1 semana
- Media móvil (SMA) superpuesta a datos crudos
- Estadísticas por dispositivo: mín, máx, promedio, mediana

### 📥 Historial
- Búsqueda por rango de fechas y dispositivos
- Filtro de texto en resultados
- Descarga en **CSV** y **Excel (.xlsx)**
- Opción de backup histórico completo

### ⚙️ Configuración
- **Identidad**: editar alias y ubicación visible de cada dispositivo
- **Umbrales**: definir rangos óptimos y críticos por sensor y por dispositivo
- Los cambios se persisten directamente en `devices_data` en MongoDB

---

## 📝 Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para el historial completo de versiones.

---

<div align="center">

Desarrollado por [@Marton1123](https://github.com/Marton1123)

**Laboratorio de Máquinas Inteligentes · Escuela de Ingeniería · UCN Coquimbo**

**Laboratorio de Cultivos de Crustáceos · Departamento de Acuicultura · UCN**

</div>
