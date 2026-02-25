import json
import os
from typing import Dict, Set, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SensorMetadata:
    name: str
    label: str
    unit: str
    min_value: float
    max_value: float
    optimal_min: float
    optimal_max: float
    
    @classmethod
    def from_dict(cls, name: str, data: Dict[str, Any]) -> 'SensorMetadata':
        return cls(
            name=name,
            label=data.get("label", name),
            unit=data.get("unit", ""),
            min_value=float(data.get("min", 0.0)),
            max_value=float(data.get("max", 100.0)),
            optimal_min=float(data.get("optimal_min", 0.0)),
            optimal_max=float(data.get("optimal_max", 100.0))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "unit": self.unit,
            "min": self.min_value,
            "max": self.max_value,
            "optimal_min": self.optimal_min,
            "optimal_max": self.optimal_max
        }


class SensorRegistry:
    
    _defaults: Dict[str, SensorMetadata] = {}
    _loaded: bool = False
    
    @classmethod
    def _load_defaults(cls):
        if cls._loaded:
            return

        try:
            # Ubicar el archivo de configuración relativo a este módulo o raíz del proyecto
            base_dir = Path(__file__).resolve().parent.parent
            config_path = base_dir / "config" / "sensor_defaults.json"
            
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for name, meta in data.items():
                        cls._defaults[name] = SensorMetadata.from_dict(name, meta)
            else:
                # Fallback genérico si falta el archivo (no debería pasar en prod)
                pass
                
            cls._loaded = True
        except Exception as e:
            print(f"Error cargando defaults de sensores: {e}")
            # Mantener defaults vacíos o parciales
            cls._loaded = True

    @staticmethod
    def _ensure_loaded():
        if not SensorRegistry._loaded:
            SensorRegistry._load_defaults()
    
    @staticmethod
    def discover_sensors_from_dataframe(df) -> Set[str]:
        if df.empty:
            return set()
        
        excluded_columns = {'timestamp', 'device_id', 'location', '_id', 'alerts'}
        potential_sensors = set(df.columns) - excluded_columns
        
        discovered = set()
        
        # 1. Chequear si alguna columna es un contenedor de sensores (diccionario)
        # Conocidos: 'sensors', 'sensor_data'
        container_cols = {'sensors', 'sensor_data'}.intersection(potential_sensors)
        
        if container_cols:
            for col in container_cols:
                # Inspeccionar el primer registro no nulo
                first_valid = df[col].dropna().iloc[0] if not df[col].dropna().empty else {}
                if isinstance(first_valid, dict):
                    discovered.update(first_valid.keys())
                    
        # 2. Las columnas que NO son contenedores, son sensores planos (Legacy)
        flat_sensors = potential_sensors - container_cols
        discovered.update(flat_sensors)
        
        return discovered
    
    @staticmethod
    def get_default_metadata(sensor_name: str) -> SensorMetadata:
        SensorRegistry._ensure_loaded()
        
        if sensor_name in SensorRegistry._defaults:
            return SensorRegistry._defaults[sensor_name]
        
        return SensorMetadata(
            name=sensor_name,
            label=sensor_name.replace('_', ' ').title(),
            unit="",
            min_value=0.0,
            max_value=100.0,
            optimal_min=20.0,
            optimal_max=80.0
        )
    
    @staticmethod
    def create_default_config(detected_sensors: Set[str]) -> Dict[str, Dict[str, Any]]:
        config = {}
        
        for sensor_name in detected_sensors:
            metadata = SensorRegistry.get_default_metadata(sensor_name)
            config[sensor_name] = metadata.to_dict()
        
        return config
    
    @staticmethod
    def merge_configs(existing_config: Dict[str, Any], detected_sensors: Set[str]) -> Dict[str, Any]:
        existing_sensors = existing_config.get("sensors", {})
        
        for sensor_name in detected_sensors:
            if sensor_name not in existing_sensors:
                metadata = SensorRegistry.get_default_metadata(sensor_name)
                existing_sensors[sensor_name] = metadata.to_dict()
        
        existing_config["sensors"] = existing_sensors
        
        return existing_config
    
    @staticmethod
    def validate_sensor_config(sensor_config: Dict[str, Any]) -> bool:
        """
        Acepta dos formatos de clave:
          - Formato JSON defaults: min / max / optimal_min / optimal_max
          - Formato UI settings:   critical_min / critical_max / min_value / max_value
        Cualquiera de los dos es válido.
        """
        # Mapear ambos formatos a valores comunes
        try:
            # Formato UI (settings.py): critical_min/min_value/max_value/critical_max
            has_ui_format = any(k in sensor_config for k in ["critical_min", "min_value", "max_value", "critical_max"])
            # Formato JSON (sensor_defaults.json): min/max/optimal_min/optimal_max
            has_json_format = any(k in sensor_config for k in ["min", "max", "optimal_min", "optimal_max"])

            if not has_ui_format and not has_json_format:
                return False  # No tiene ningún formato reconocido

            # Extraer valores usando ambos formatos como fallback
            c_min = float(sensor_config.get("critical_min", sensor_config.get("min", -9999)))
            o_min = float(sensor_config.get("min_value",   sensor_config.get("optimal_min", c_min)))
            o_max = float(sensor_config.get("max_value",   sensor_config.get("optimal_max", o_min + 1)))
            c_max = float(sensor_config.get("critical_max", sensor_config.get("max", o_max + 1)))

            # Validar orden lógico
            if not (c_min <= o_min <= o_max <= c_max):
                return False
        except (ValueError, TypeError):
            return False

        return True