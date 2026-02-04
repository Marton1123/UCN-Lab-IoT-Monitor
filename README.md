# 🦐 Monitor Biofloc

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-red?logo=streamlit&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?logo=mongodb&logoColor=white)
![ROS 2](https://img.shields.io/badge/ROS_2-Jazzy-22314E?logo=ros&logoColor=white)

**Sistema de monitoreo IoT y telemetría para el Laboratorio de Cultivos de Crustáceos, Juveniles y Reproductores (UCN). Dashboard personalizado para control de parámetros en sistemas Biofloc.**

[Manual de Usuario](docs/MANUAL_USUARIO.md) · [Reportar Bug](https://github.com/Marton1123/UCN-Lab-IoT-Monitor/issues)

</div>

---

## 📋 Descripción

**Monitor Biofloc** es una plataforma de monitoreo IoT diseñada para el Laboratorio de Cultivos de Crustáceos del Departamento de Acuicultura de la Universidad Católica del Norte (UCN). 

Proporciona supervisión en tiempo real de parámetros fisicoquímicos críticos (pH, oxígeno disuelto, temperatura, salinidad, etc.) en sistemas Biofloc.

### ✨ Funcionalidades Principales

| Función | Descripción |
|---------|-------------|
| **🔐 Autenticación Segura** | Login obligatorio con bcrypt, botón de cerrar sesión en navbar |
| **📊 Dashboard en Tiempo Real** | Visualización de estado de dispositivos con actualización automática |
| **🚦 Sistema de Alertas** | Semaforización automática (Normal/Alerta/Crítico) con umbrales configurables |
| **📈 Gráficas Adaptativas** | Análisis de tendencias con filtrado de outliers |
| **📥 Exportación Universal** | Descarga de históricos en Excel (.xlsx) y CSV |
| **🔄 Registry-First Strategy** | Visualización de dispositivos inactivos con último estado conocido |

---

## 🏗️ Arquitectura

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Nodos ROS 2    │────▶│  MongoDB Atlas   │◀────│ Monitor Biofloc │
│  (Micro-ROS)    │     │   (Base Datos)   │     │   (Streamlit)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

**Stack Tecnológico:**
- **Frontend**: Streamlit 1.36+
- **Backend**: Python 3.10+, PyMongo
- **Base de Datos**: MongoDB Atlas
- **Visualización**: Plotly Express
- **Seguridad**: bcrypt (password hashing)

---

## 📁 Estructura del Proyecto

```
UCN-Lab-IoT-Monitor/
├── Home.py                      # Punto de entrada principal + navegación
├── requirements.txt             # Dependencias del proyecto
├── .env                         # Variables de entorno (NO en git)
├── .env.example                 # Plantilla de configuración
├── .gitignore                   # Archivos excluidos de git
├── README.md                    # Este archivo
├── COMMIT_SUMMARY.md            # Historial detallado de cambios
│
├── .streamlit/
│   ├── config.toml              # Configuración de Streamlit
│   ├── secrets.toml             # Secretos locales (NO en git)
│   └── secrets.toml.example     # Plantilla de secretos
│
├── modules/                     # Lógica de negocio
│   ├── auth.py                  # Sistema de autenticación (login/logout)
│   ├── database.py              # Conexión multi-fuente MongoDB
│   ├── device_manager.py        # Evaluación de estado de dispositivos
│   ├── config_manager.py        # Gestión de configuración y umbrales
│   ├── sensor_registry.py       # Registro dinámico de sensores
│   └── styles.py                # Estilos CSS y header del dashboard
│
├── views/                       # Vistas de la aplicación
│   ├── __init__.py              # Inicializador del paquete
│   ├── dashboard.py             # Dashboard principal con tarjetas
│   ├── graphs.py                # Gráficas interactivas con Plotly
│   ├── history.py               # Historial y exportación de datos
│   └── settings.py              # Configuración de sensores y umbrales
│
├── scripts/                     # Scripts de utilidad
│   ├── generate_password_hash.py  # Generador de hash bcrypt
│   ├── mock_data_generator.py     # Generador de datos de prueba
│   ├── debug_db.py                # Debugging de MongoDB
│   ├── test_normalization.py      # Test de normalización multi-esquema
│   └── export_to_excel.py         # Exportación a Excel
│
├── config/
│   └── sensor_defaults.json     # Valores por defecto de sensores
│
├── assets/
│   ├── Logo-Acuicultura.png     # Logo del Departamento de Acuicultura
│
└── docs/
    └── MANUAL_USUARIO.md        # Manual de usuario completo
```

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.10+ (recomendado: [Anaconda](https://www.anaconda.com/download))
- Cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Marton1123/UCN-Lab-IoT-Monitor.git
cd UCN-Lab-IoT-Monitor
```

### 2. Crear Entorno Virtual

```bash
conda create --name biofloc_monitor python=3.10 -y
conda activate biofloc_monitor
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

Copia `.env.example` a `.env` y configura:

```ini
# Base de Datos MongoDB
MONGO_URI=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/
MONGO_DB=BioflocDB
MONGO_COLLECTION=telemetria
MONGO_DEVICES_COLLECTION=devices

# Autenticación (OBLIGATORIO)
APP_PASSWORD_HASH=$2b$12$...hash_generado...
```

### 4. Configurar Contraseña de Acceso

```bash
python -m scripts.generate_password_hash "TuContraseñaSegura"
```

Copia el hash generado al archivo `.env`.

### 5. Ejecutar

```bash
streamlit run Home.py
```

Accede a `http://localhost:8501`

---

## 🔐 Sistema de Autenticación

| Característica | Descripción |
|---|---|
| **Login obligatorio** | Pantalla de acceso antes del dashboard |
| **Password hashing** | bcrypt con 12 rounds |
| **Botón Salir** | En el navbar, cierra sesión |
| **Enter para login** | Formulario con soporte de Enter |
| **Diseño unificado** | UI consistente con el dashboard |

---

## 📊 Vistas de la Aplicación

### 🏠 Dashboard (Inicio)
- Tarjetas de dispositivos con estado (Normal/Alerta/Crítico/Offline)
- Métricas resumen (Total, En Línea, Offline, OK, Alerta, Crítico)
- Filtros por estado, ubicación y alias
- Actualización parcial por tarjeta

### 📈 Gráficas
- Visualización histórica multi-sensor
- Filtrado automático de outliers
- Selector de rango de fechas
- Zoom, pan y exportación

### 📥 Datos (Historial)
- Tabla completa de lecturas
- Exportación Excel/CSV
- Filtros por dispositivo y fecha

### ⚙️ Configuración
- Alias y ubicaciones de dispositivos
- Umbrales de alerta personalizables
- Configuración por sensor

---

## ☁️ Deploy en Streamlit Cloud

### 1. Configurar Secretos

En Streamlit Cloud → Settings → Secrets:

```toml
MONGO_URI = "mongodb+srv://..."
MONGO_DB = "BioflocDB"
MONGO_COLLECTION = "telemetria"
MONGO_DEVICES_COLLECTION = "devices"
APP_PASSWORD_HASH = "$2b$12$..."
```

### 2. Desplegar

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu repositorio
3. Selecciona `Home.py` como archivo principal
4. ¡Deploy!

---

## 📝 Changelog

### v4.0.0 (Febrero 2026)
- ✅ **Sistema de Autenticación**: Login obligatorio con bcrypt
- ✅ **Botón Cerrar Sesión**: En navbar, discreto
- ✅ **Nuevo Branding**: "Monitor Biofloc - Lab. Cultivos Crustáceos UCN"
- ✅ **UI Login Unificada**: Diseño minimalista, Enter funcional
- ✅ **Documentación Actualizada**: README, estructura, ejemplos

### v3.1.0 (Febrero 2026)
- ✅ Dashboard: Filtro inteligente offline
- ✅ Gráficas: Auto-actualización
- ✅ UX mejorada en filtros

### v3.0.0 (Febrero 2026)
- ✅ Registry-First Strategy
- ✅ Filtrado de Outliers
- ✅ UI Mejorada en Settings

---

## 📄 Licencia

Este proyecto es de código abierto bajo licencia MIT.

---

<div align="center">

**Desarrollado para el Laboratorio de Cultivos de Crustáceos**

**Departamento de Acuicultura - Universidad Católica del Norte (UCN)**

</div>