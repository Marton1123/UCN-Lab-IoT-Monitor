# Monitor Biofloc — Manual de Usuario

---


## Acceso al Sistema

### Iniciar sesión
1. Ingresa la contraseña de acceso
2. Presiona **Enter** o haz clic en **"Iniciar Sesión"**

### Cerrar sesión
- Haz clic en **"Salir"** en la barra de navegación (esquina derecha)

---

## 1. Dashboard (Inicio)

Vista principal con el estado en tiempo real de todos los dispositivos registrados.

### 1.1 Estados de operación

| Estado | Color | Condición |
|--------|-------|-----------|
| **Normal** | 🟢 Verde | Todos los parámetros dentro del rango óptimo |
| **Alerta** | 🟡 Amarillo | Algún parámetro fuera del óptimo, pero dentro del límite seguro |
| **Crítico** | 🔴 Rojo | Algún parámetro fuera del límite de seguridad biológica |
| **Offline** | ⚫ Gris | Sin datos recibidos en los últimos 5 minutos |

### 1.2 Tarjetas de dispositivo

Cada tarjeta muestra:
- **Nombre / Alias** del dispositivo y su ubicación
- **Etiqueta de estado** (Normal / Alerta / Crítico / Offline)
- **Lecturas actuales** de cada sensor con su unidad
- **ID técnico** y hora de la última lectura recibida
- **Atajo a Gráficas** (ícono 📊) que abre el historial de ese dispositivo

### 1.3 Actualización de datos

| Control | Acción |
|---------|--------|
| **Actualizar Todo** | Recarga todos los dispositivos desde la base de datos |
| Auto-refresh | Cada tarjeta se refresca automáticamente cada 2 minutos |

### 1.4 Filtros

- **Búsqueda rápida**: por ID técnico o alias
- **Selección rápida**: por ubicación, estado o nombre
- **Checkbox Offline**: mostrar u ocultar dispositivos sin conexión (ocultos por defecto)

---

## 2. Gráficas

Análisis visual del comportamiento de parámetros en el tiempo.

### 2.1 Cómo usar

1. Selecciona uno o más **dispositivos**
2. Selecciona los **parámetros** a visualizar (temperatura, pH, etc.)
3. Elige el **rango de tiempo** (5 minutos → 1 semana)
4. Presiona **"VER GRÁFICAS"** — los cambios posteriores de rango se aplican solos

### 2.2 Elementos del gráfico

| Elemento | Descripción |
|----------|-------------|
| Línea fina (transparente) | Valores crudos del sensor |
| Línea gruesa | Media móvil (tendencia suavizada) |
| Métricas superiores | Promedio por dispositivo y promedio global |
| Panel "Estadísticas" | Mínimo, Máximo, Promedio, Mediana y cantidad de registros |

### 2.3 Botón "Actualizar"
Fuerza la recarga del historial completo desde la base de datos. La carga normal está cacheada por 1 hora para mayor velocidad.

---

## 3. Historial (Datos)

Acceso al registro completo de mediciones con opciones de exportación.

### 3.1 Consultar datos

1. Define el **rango de fechas** (inicio y fin)
2. Opcionalmente, filtra por uno o más **dispositivos**
3. Presiona **"BUSCAR REGISTROS"**
4. Usa el **filtro de texto** para refinar los resultados por ID, alias o ubicación

### 3.2 Exportar datos

| Formato | Recomendado para |
|---------|-----------------|
| **CSV** | Grandes volúmenes, procesamiento externo, backups |
| **Excel (.xlsx)** | Reportes, análisis con fórmulas (<50.000 registros) |

> La opción **"Backup Completo"** descarga todo el historial disponible desde el inicio del proyecto.

---

## 4. Configuración

Edición de metadatos y umbrales de alerta por dispositivo.

### 4.1 Identidad del dispositivo

| Campo | Descripción |
|-------|-------------|
| **ID Técnico** | Identificador único del hardware (solo lectura) |
| **Alias** | Nombre visible en el Dashboard y Gráficas |
| **Ubicación** | Sector físico donde está instalado el dispositivo |

Los cambios de alias y ubicación se guardan directamente en la base de datos y se reflejan en toda la aplicación.

### 4.2 Umbrales de alerta

Cada sensor tiene cuatro límites configurables:

```
[CRÍTICO] ←── Mín. Crítico ──[ALERTA]── Mín. Óptimo ──[NORMAL]── Máx. Óptimo ──[ALERTA]── Máx. Crítico ──→ [CRÍTICO]
```

| Límite | Descripción |
|--------|-------------|
| **Mín. Crítico** | Por debajo → estado Crítico (rojo) |
| **Mín. Óptimo** | Por debajo → estado Alerta (amarillo) |
| **Máx. Óptimo** | Por encima → estado Alerta (amarillo) |
| **Máx. Crítico** | Por encima → estado Crítico (rojo) |

> Los umbrales se guardan por dispositivo. Si un dispositivo no tiene umbrales propios, se usan los rangos por defecto definidos en `config/sensor_defaults.json`.

---

## 5. Solución de Problemas

### El dispositivo aparece como "Offline"

1. Verificar alimentación eléctrica del nodo sensor
2. Comprobar conectividad WiFi en el punto de instalación
3. Revisar que el dispositivo esté enviando datos (logs del firmware)

### Los datos no se actualizan en el Dashboard

1. Hacer clic en **"Actualizar Todo"** en la esquina superior derecha
2. Si persiste, recargar la página del navegador (F5)
3. Verificar que el cluster de MongoDB Atlas esté operativo

### Error de conexión a la base de datos

1. Revisar que las credenciales en el archivo `.env` sean correctas
2. Comprobar que la IP del servidor esté en la whitelist de MongoDB Atlas
3. Verificar el estado del cluster en [cloud.mongodb.com](https://cloud.mongodb.com)

### El umbral guardado no se refleja en la semaforización

1. Recargar la página (los fragmentos del Dashboard se actualizan automáticamente, pero un reload fuerza el recálculo inmediato)
2. Verificar que los valores sigan el orden lógico: Mín. Crítico ≤ Mín. Óptimo ≤ Máx. Óptimo ≤ Máx. Crítico

---

Desarrollado por [@Marton1123](https://github.com/Marton1123)

**Laboratorio de Máquinas Inteligentes · Escuela de Ingeniería · UCN Coquimbo**

**Laboratorio de Cultivos de Crustáceos · Departamento de Acuicultura · UCN**

