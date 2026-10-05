# src/datasets/dataset_manager.py
"""
Gestor de datasets crudos y procesados.
Soporta múltiples formatos de CSV (Facebook, Google Maps).
"""

import os
import glob
import json
import hashlib
import re
import random
import pandas as pd
from datetime import datetime, timedelta


class DatasetManager:
    """Gestor de archivos de datasets."""

    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            ))
        self.base_dir = base_dir
        self.raw_dir = os.path.join(base_dir, "data", "raw")
        self.processed_dir = os.path.join(base_dir, "data", "processed")
        self.history_file = os.path.join(base_dir, "data", "history.json")

        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)

    # =========================================================
    # HISTORIAL
    # =========================================================
    def _load_history(self):
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_history(self, history):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def agregar_historial(self, registro):
        history = self._load_history()
        history.insert(0, registro)
        self._save_history(history)

    def listar_historial(self):
        return self._load_history()

    def limpiar_historial(self):
        self._save_history([])

    # =========================================================
    # DETECCIÓN DE FUENTE
    # =========================================================
    @staticmethod
    def _detectar_fuente(archivo_path, df):
        """Detecta si es facebook o google_maps."""
        nombre = os.path.basename(archivo_path).lower()
        if "google" in nombre or "maps" in nombre or "resena" in nombre:
            return "google_maps"
        if "facebook" in nombre or "fb" in nombre or "confesion" in nombre:
            return "facebook"
        # Si no, revisar columnas
        if "metadata" in df.columns:
            return "google_maps"
        if "compartidos" in df.columns:
            return "facebook"
        return "facebook"

    # =========================================================
    # NORMALIZACIÓN DE FECHAS
    # =========================================================
    @staticmethod
    def _normalizar_fecha(valor, fuente):
        """
        Convierte diferentes formatos de fecha a datetime.
        - Facebook: "2026-06-20 11:59:08" (ya es fecha válida)
        - Google Maps: "Hace un año", "Hace 5 años" (relativo)
        """
        if pd.isna(valor) or valor is None:
            return None

        texto = str(valor).strip()

        # Caso 1: fecha ISO
        try:
            return pd.to_datetime(texto, errors='raise')
        except (ValueError, TypeError):
            pass

        # Caso 2: fecha relativa de Google Maps
        # "Hace un año", "Hace 2 años", "Hace 5 años", "Hace 3 meses", "Hace un mes"
        texto_lower = texto.lower()
        if "hace" in texto_lower or "ago" in texto_lower:
            ahora = datetime.now()

            # Detectar unidad
            if "año" in texto_lower or "year" in texto_lower:
                if "un año" in texto_lower or "1 año" in texto_lower:
                    return ahora - timedelta(days=365)
                # Extraer número
                match = re.search(r'(\d+)\s*año', texto_lower)
                if match:
                    return ahora - timedelta(days=365 * int(match.group(1)))
                return ahora - timedelta(days=365)

            if "mes" in texto_lower or "month" in texto_lower:
                if "un mes" in texto_lower or "1 mes" in texto_lower:
                    return ahora - timedelta(days=30)
                match = re.search(r'(\d+)\s*mes', texto_lower)
                if match:
                    return ahora - timedelta(days=30 * int(match.group(1)))
                return ahora - timedelta(days=30)

            if "semana" in texto_lower or "week" in texto_lower:
                match = re.search(r'(\d+)\s*semana', texto_lower)
                if match:
                    return ahora - timedelta(weeks=int(match.group(1)))
                return ahora - timedelta(weeks=1)

            if "día" in texto_lower or "day" in texto_lower:
                match = re.search(r'(\d+)\s*día', texto_lower)
                if match:
                    return ahora - timedelta(days=int(match.group(1)))
                return ahora - timedelta(days=1)

        # Caso 3: no se pudo parsear
        return None

    # =========================================================
    # NORMALIZACIÓN DE DATAFRAME
    # =========================================================
    def _normalizar_dataframe(self, df, archivo_path):
        """Normaliza el DataFrame a una estructura común."""
        nombre = os.path.basename(archivo_path).replace(".csv", "")
        fuente = self._detectar_fuente(archivo_path, df)

        # ==== Renombrar columnas ====
        rename_map = {
            "text": "texto",
            "content": "texto",
            "review": "texto",
            "texto_resena": "texto",
            "date": "fecha_original",
            "fecha": "fecha_original",
            "created_at": "fecha_original",
            "timestamp": "fecha_original",
            "fecha_creacion": "fecha_original",
            "author": "autor",
            "user": "autor",
            "rating": "calificacion",
            "estrellas": "calificacion",
            "id": "id_origen_raw",
        }
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

        # ==== id_origen ====
        if "id_origen" not in df.columns and "id_origen_raw" in df.columns:
            df["id_origen"] = df["id_origen_raw"]
        elif "id_origen" not in df.columns:
            df["id_origen"] = df.apply(
                lambda r: hashlib.md5(
                    str(r.get("texto", "")).encode()
                ).hexdigest()[:32],
                axis=1
            )

        # ==== texto ====
        if "texto" not in df.columns:
            df["texto"] = ""

        # ==== autor ====
        if "autor" not in df.columns:
            df["autor"] = "Anónimo"

        # ==== fuente ====
        df["fuente"] = fuente

        # ==== fecha ====
        if "fecha_original" in df.columns:
            df["fecha_creacion"] = df["fecha_original"].apply(
                lambda x: self._normalizar_fecha(x, fuente)
            )
        else:
            # Si no hay fecha, generar aleatoria en los últimos 4 años
            df["fecha_creacion"] = [
                datetime.now() - timedelta(days=random.randint(30, 1460))
                for _ in range(len(df))
            ]

        # Rellenar fechas nulas con la mediana o fecha actual
        if df["fecha_creacion"].isna().any():
            no_nulas = df["fecha_creacion"].dropna()
            if len(no_nulas) > 0:
                fecha_default = no_nulas.median()
            else:
                fecha_default = datetime.now() - timedelta(days=365)
            df["fecha_creacion"] = df["fecha_creacion"].fillna(fecha_default)

        # ==== Columnas derivadas ====
        df["fecha_dt"] = df["fecha_creacion"].dt.strftime("%Y-%m-%d %H:%M")
        df["fecha_dia"] = df["fecha_creacion"].dt.strftime("%Y-%m-%d")
        df["anio"] = df["fecha_creacion"].dt.year
        df["longitud_texto"] = df["texto"].astype(str).str.len()
        df["archivo_origen"] = nombre
        df["fecha_carga"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return df

    # =========================================================
    # CARGA
    # =========================================================
    def listar_archivos_raw(self):
        patron = os.path.join(self.raw_dir, "*.csv")
        archivos = glob.glob(patron)
        archivos.sort(key=os.path.getmtime, reverse=True)
        return archivos

    def cargar_dataset_raw(self, archivo_path):
        try:
            df = pd.read_csv(archivo_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(archivo_path, encoding='latin-1')

        return self._normalizar_dataframe(df, archivo_path)

    def cargar_todos_raw(self):
        """Carga y une todos los archivos crudos."""
        archivos = self.listar_archivos_raw()
        if not archivos:
            return pd.DataFrame(), []

        dataframes = []
        info_archivos = []

        for archivo in archivos:
            try:
                df = self.cargar_dataset_raw(archivo)
                dataframes.append(df)
                info_archivos.append({
                    "archivo": os.path.basename(archivo),
                    "registros": len(df),
                    "fuente": df["fuente"].iloc[0] if len(df) > 0 else "desconocida",
                    "fecha": datetime.fromtimestamp(
                        os.path.getmtime(archivo)
                    ).strftime("%Y-%m-%d %H:%M"),
                    "tamano_kb": round(os.path.getsize(archivo) / 1024, 1),
                })
            except Exception as e:
                info_archivos.append({
                    "archivo": os.path.basename(archivo),
                    "registros": 0, "fuente": "error",
                    "fecha": "—", "tamano_kb": 0, "error": str(e),
                })

        if not dataframes:
            return pd.DataFrame(), info_archivos

        df_total = pd.concat(dataframes, ignore_index=True)
        df_total = df_total.drop_duplicates(subset=["id_origen"], keep="first")
        df_total = df_total.reset_index(drop=True)

        return df_total, info_archivos

    # =========================================================
    # SIMULACIÓN DE SCRAPING (usa datasets reales)
    # =========================================================
    def simular_scraping(self, fuente, fecha_inicio, fecha_fin):
        """
        Simula un scraping usando los archivos reales.
        Ahora incluye filtro por fuente y rango de fechas.
        """
        df_total, _ = self.cargar_todos_raw()

        if len(df_total) == 0:
            return pd.DataFrame()

        df = df_total.copy()

        # Filtrar por fuente
        if fuente and fuente != "todas":
            df = df[df["fuente"] == fuente]

        # Filtrar por fechas
        if "fecha_creacion" in df.columns and len(df) > 0:
            fecha_inicio_dt = pd.to_datetime(fecha_inicio)
            fecha_fin_dt = pd.to_datetime(fecha_fin) + pd.Timedelta(days=1)
            df = df[
                (df["fecha_creacion"] >= fecha_inicio_dt) &
                (df["fecha_creacion"] < fecha_fin_dt)
            ]

        # Si no hay registros en el rango, tomar muestra aleatoria
        if len(df) == 0:
            df = df_total.copy()
            if fuente and fuente != "todas":
                df = df[df["fuente"] == fuente]
            if len(df) > 0:
                df = df.sample(n=min(len(df), 50), random_state=42)

        df = df.reset_index(drop=True)

        # Marcar "nuevos" (30% aleatorio)
        df["es_nuevo"] = False
        if len(df) > 0:
            n_nuevos = max(int(len(df) * 0.3), 1)
            nuevos_idx = df.sample(n=n_nuevos, random_state=42).index
            df.loc[nuevos_idx, "es_nuevo"] = True

        # Ordenar por fecha descendente
        df = df.sort_values("fecha_creacion", ascending=False).reset_index(drop=True)

        return df

    def estadisticas_por_fecha(self):
        """Devuelve el rango de fechas y estadísticas por año."""
        df, _ = self.cargar_todos_raw()
        if len(df) == 0 or "fecha_creacion" not in df.columns:
            return None, None, {}

        fechas = pd.to_datetime(df["fecha_creacion"], errors="coerce").dropna()
        if len(fechas) == 0:
            return None, None, {}

        # Estadísticas por año
        por_anio = df.groupby(df["fecha_creacion"].dt.year).size().to_dict()
        por_fuente = df.groupby("fuente").size().to_dict()

        return fechas.min().date(), fechas.max().date(), {
            "por_anio": por_anio,
            "por_fuente": por_fuente,
            "total": len(df),
        }

    # =========================================================
    # PROCESAMIENTO
    # =========================================================
    def procesar_corpus(self, df):
        df = df.copy()
        df["es_valido"] = True
        df["motivo_descarte"] = ""

        # F-01: texto muy corto
        mask_corto = df["longitud_texto"] < 5
        df.loc[mask_corto, "es_valido"] = False
        df.loc[mask_corto, "motivo_descarte"] = "Texto muy corto"

        # F-02: texto vacío
        mask_vacio = df["texto"].astype(str).str.strip() == ""
        df.loc[mask_vacio, "es_valido"] = False
        df.loc[mask_vacio, "motivo_descarte"] = "Texto vacío"

        # Limpieza básica
        df["texto_limpio"] = df["texto"].astype(str).apply(self._limpiar_texto)

        return df

    @staticmethod
    def _limpiar_texto(texto):
        import unicodedata
        if not texto or texto == "nan":
            return ""
        texto = unicodedata.normalize("NFC", str(texto))
        texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
        texto = re.sub(r'@\w+', '', texto)
        texto = re.sub(r'#\w+', '', texto)
        texto = re.sub(r'[^a-zA-ZáéíóúñÁÉÍÓÚÑ0-9\s\.,;:¿?¡!]', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto).strip()
        return texto

    def guardar_corpus_procesado(self, df, nombre=None):
        if nombre is None:
            nombre = f"corpus_{datetime.now():%Y%m%d_%H%M%S}"

        csv_path = os.path.join(self.processed_dir, f"{nombre}.csv")
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')

        parquet_path = os.path.join(self.processed_dir, f"{nombre}.parquet")
        try:
            df.to_parquet(parquet_path, index=False)
        except Exception:
            parquet_path = None

        return {
            "nombre": nombre,
            "csv": csv_path,
            "parquet": parquet_path,
            "registros": len(df),
        }