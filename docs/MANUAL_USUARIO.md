# Monitor Biofloc - Manual de Usuario

**Sistema de monitoreo IoT para el Laboratorio de Cultivos de Crustáceos (UCN)**

---

## Acceso al Sistema

### Login
1. Ingresa la contraseña configurada
2. Presiona **Enter** o haz clic en **"Iniciar Sesión"**

### Cerrar Sesión
- Haz clic en el botón **"Salir"** en la barra de navegación (esquina derecha)

---

## 1. Panel de Control (Dashboard)

El Dashboard es la interfaz principal para la supervisión en tiempo real.

### 1.1 Estados de Operación

| Estado | Color | Descripción |
|--------|-------|-------------|
| **Normal** | 🟢 Verde | Parámetros dentro de rangos óptimos |
| **Alerta** | 🟡 Amarillo | Parámetros fuera del rango óptimo pero dentro de límites seguros |
| **Crítico** | 🔴 Rojo | Valores fuera de límites de seguridad biológica |
| **Offline** | ⚫ Gris | Sin transmisión de datos por más de 5 minutos |

### 1.2 Tarjetas de Dispositivo

Cada tarjeta muestra:
- **Encabezado**: Nombre del dispositivo, ubicación y estado
- **Sensores**: Hasta 4 lecturas con sus valores actuales
- **Metadata**: ID técnico y hora de última actualización
- **Botón de Gráficas**: Acceso directo (📊)

### 1.3 Actualización de Datos

- **Botón "Actualizar"**: Refresca solo ese dispositivo
- **Botón "Actualizar Todo"**: Recarga todos los dispositivos

### 1.4 Filtrado y Búsqueda

- **Por Estado**: Normal, Alerta, Crítico, Offline
- **Por Ubicación**: Sector físico
- **Por Texto**: Búsqueda por ID o alias
- **Checkbox Offline**: Mostrar/ocultar dispositivos sin conexión

---

## 2. Análisis de Tendencias (Gráficas)

Visualización del comportamiento de parámetros en el tiempo.

### 2.1 Funcionalidades

- Rango temporal seleccionable
- Comparativa multi-dispositivo
- Estadísticas: Min, Max, Promedio, Mediana
- Zoom, pan y exportación de imágenes

### 2.2 Uso

1. Selecciona dispositivo(s)
2. Define rango de fechas
3. Elige sensores a visualizar
4. La gráfica se actualiza automáticamente

---

## 3. Gestión de Datos (Historial)

Acceso al registro completo de mediciones.

### 3.1 Consulta

- Filtrado por fechas y dispositivos
- Tabla con paginación
- Ordenamiento por columnas

### 3.2 Exportación

| Formato | Uso Recomendado |
|---------|-----------------|
| **Excel (.xlsx)** | Reportes, análisis (<50,000 registros) |
| **CSV** | Backups masivos, procesamiento externo |

---

## 4. Configuración

### 4.1 Identidad de Dispositivos

| Campo | Descripción |
|-------|-------------|
| **ID Técnico** | Identificador único del hardware |
| **Alias** | Nombre visible en Dashboard |
| **Ubicación** | Sector físico |

### 4.2 Umbrales de Alerta

```
[CRÍTICO] ← Mín Crítico ← [ALERTA] ← Mín Óptimo ← [NORMAL] → Máx Óptimo → [ALERTA] → Máx Crítico → [CRÍTICO]
```

- **Mínimo Crítico**: Límite inferior de seguridad
- **Mínimo Óptimo**: Inicio del rango ideal
- **Máximo Óptimo**: Fin del rango ideal
- **Máximo Crítico**: Límite superior de seguridad

---

## 5. Solución de Problemas

### Dispositivo "Offline"

1. Verificar alimentación del nodo sensor
2. Comprobar conectividad WiFi
3. Revisar estado de la antena

### Datos no se actualizan

1. Clic en "Actualizar" en la tarjeta
2. Si persiste, usar "Actualizar Todo"
3. Verificar conexión a base de datos

### Error de conexión MongoDB

1. Verificar credenciales en `.env`
2. Comprobar whitelist de IPs en Atlas
3. Revisar estado del cluster

---

**Laboratorio de Cultivos de Crustáceos**  
**Departamento de Acuicultura - Universidad Católica del Norte (UCN)**
