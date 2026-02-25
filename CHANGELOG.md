# Changelog — Monitor Biofloc

Todos los cambios relevantes de cada versión están documentados aquí.

---


## [4.1.0] — 2026-02-25

### Corregido
- **Dashboard**: Color de tarjeta mostraba estado obsoleto (stale) en reruns — `show_view()` ahora propaga el `DeviceInfo` fresco al `session_state` antes de renderizar los fragmentos
- **Settings**: Umbrales de temperatura partían con valores de rango de pH — corregido el mapeo de claves `sensor_defaults.json` (`optimal_min/max`) a claves UI (`min_value/max_value`)
- **Settings**: El mensaje de confirmación al guardar nunca era visible — reemplazado `st.success()` + `st.rerun()` por `st.toast()` que persiste entre reruns
- **sensor_registry**: El validador de umbrales exigía formato JSON (`min/max/optimal_min/optimal_max`) y rechazaba silenciosamente todo lo guardado desde la UI (`critical_min/min_value/max_value/critical_max`) — ahora acepta ambos formatos
- **database**: `sort()` lanzaba `TypeError` al mezclar timestamps con y sin zona horaria — se normaliza a `naive` antes del sort
- **history**: Se creaba una segunda `DatabaseConnection` innecesaria para cargar metadatos — se reutiliza la conexión ya existente
- **history**: El backup completo evadía `@st.cache_data` porque `datetime.now()` generaba claves únicas en cada llamada — reemplazado por anchor fijo `datetime(2020, 1, 1)`

### Compatible
- Nuevo esquema de BD (`devices_data` / `sensor_data` con campos en español) — el normalizador multi-esquema de `database.py` ya era compatible sin cambios adicionales

---

## [4.0.0] — 2026-02-04

### Añadido
- Sistema de autenticación con bcrypt (login obligatorio, botón de cierre de sesión)
- Script `generate_password_hash.py` para generar hashes de contraseña
- Nuevo branding: **Monitor Biofloc** — Lab. Cultivos Crustáceos UCN

---

## [3.1.0] — 2026-02-02

### Añadido
- Dashboard: checkbox compacto para mostrar/ocultar dispositivos offline
- Gráficas: auto-actualización al cambiar filtros tras primera búsqueda
- Filtros de Dashboard: opciones dinámicas según dispositivos visibles

### Corregido
- Fix crítico: carga de umbrales personalizados (merge `umbrales` + `thresholds`)
- Filtro "Por Estado: Offline" funcionaba de forma contradictoria con el checkbox

---

## [3.0.0] — 2026-01-30

### Añadido
- Registry-First Strategy: dispositivos offline muestran último estado conocido
- Filtrado automático de outliers en Gráficas (rangos físicamente imposibles)
- Soporte multi-esquema de base de datos (normalización de nombres de campos)
- UI mejorada en Settings con tooltips y formato correcto de nombres técnicos

---

## [2.0.0] — 2026-01-24

### Añadido
- Soporte multi-base de datos (múltiples fuentes MongoDB en paralelo)
- Carga paralela de historial con `ThreadPoolExecutor`
- Manejo de zonas horarias UTC vs. local

---

Desarrollado por [@Marton1123](https://github.com/Marton1123)

**Laboratorio de Máquinas Inteligentes · Escuela de Ingeniería · UCN Coquimbo**

**Laboratorio de Cultivos de Crustáceos · Departamento de Acuicultura · UCN**
