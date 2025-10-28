# Fish Angle Crops & Notebook – Reproducible Setup (sin usar Label Studio)

Este repositorio **ya incluye** un archivo JSON con anotaciones **exportado previamente desde Label Studio**.  
➡️ **No necesitas instalar ni usar Label Studio** para replicar el proceso: solamente ejecutarás el script de recorte y, si quieres, el notebook de entrenamiento/clasificación.

Esto está hecho para ver el funcionamiento del script, recomendamos usar la carpeta "fish_angles_raw" que fue enviada por interno.

> ✅ Requisitos: **Python 3.10+** y **git** instalados.

---

## 1) Estructura sugerida del repo

```
.
├─ crop_fish.py
├─ project-3-at-2025-10-21-17-49-288e7bbb.json   # JSON ya incluido en el repo
├─ FishAngle_Local_Jupyter.ipynb                 # Notebook (opcional)
├─ requirements.txt
├─ pyproject.toml                                # (opcional)
├─ data/                                         # ← se llena al descargar el dataset desde Drive (ver §3.1)
│  └─ ...                                        # imágenes originales
├─ cropped_por_angulo/                           # se genera al ejecutar el script
├─ notebooks/                                    # (opcional)
│  └─ tu_notebook.ipynb
└─ README.md

```

> Si prefieres otro nombre/ubicación para el JSON, ajusta `json_path` dentro de `crop_fish.py`.

---

## 2) Instalar dependencias

```bash
# Clonar el repositorio
git clone <TU_URL_DEL_REPO>.git
cd <TU_REPO>

# (Opcional) Crear y activar un entorno virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependencias clave:**  
- `Pillow` para abrir y recortar imágenes.  
- `JupyterLab`/`ipykernel` para notebooks.  
- `ultralytics` (opcional, si tu notebook usa YOLO11 clasificación).  
- `opencv-python` y `matplotlib` (útiles para notebooks/visualizaciones).

---

## 3) Datos incluidos (sin Label Studio)


- El repositorio trae `project-labelstudio.json` con las anotaciones.  
- Este JSON contiene **checkboxes de ángulo** (clases) y **bounding boxes** por imagen.  
- El script **no requiere** conectarse a Label Studio; leerá directamente ese JSON.

### Supuestos sobre los ángulos
- Los ángulos esperados son: `0, 45, 90, 135, 180, 225, 270, 315` (sin símbolo `°`).  
- Si el JSON trae variantes (`45°`, `45 º`, `45Â°`, etc.), el script las **normaliza** y crea **carpetas sin `°`**.  
- Si alguna imagen no tiene selección de ángulo, se guardará en `sin_angulo`.

---

## 4) Preparar imágenes y ejecutar `crop_fish.py`

1. Coloca **tus imágenes originales** en una o varias carpetas (se recomienda usar `data/`).  
2. Abre `crop_fish.py` y verifica estas variables al inicio del archivo:

```python
json_path = "project-labelstudio.json"   # Ruta al JSON ya incluido
img_folders = [
    "data",                              # Carpeta(s) donde están tus imágenes originales
]
cropped_folder = "cropped_por_angulo"    # Carpeta de salida para los recortes por ángulo
```

3. Ejecuta el script:

```bash
python crop_fish.py
```

Si todo va bien verás un resumen y se crearán subcarpetas:

```
cropped_por_angulo/
├─ 0/
├─ 45/
├─ 90/
├─ 135/
├─ 180/
├─ 225/
├─ 270/
├─ 315/
└─ sin_angulo/
```

Cada recorte se nombra como: `NOMBREIMG_x0_y0_x1_y1.png`.

---

## 5) Ejecutar el notebook (opcional)

Si tienes tu notebook en `notebooks/tu_notebook.ipynb`, lanza Jupyter y ábrelo:

```bash
jupyter lab
```

En el notebook, ya tendrás disponibles las dependencias instaladas desde `requirements.txt`.  
Si tu notebook usa **YOLO11 clasificación** (p. ej. `yolo11n-cls`), confirma que `ultralytics` está instalado (incluido en `requirements.txt`).

> **Sugerencia de organización para clasificación:**  
> - Mueve o copia `cropped_por_angulo/` a una estructura de `train/`, `val/`, `test/` con las mismas subcarpetas de ángulos.  
> - Por ejemplo:
>   ```
>   dataset/
>   ├─ train/
>   │  ├─ 0/ ... 
>   │  ├─ 45/ ...
>   │  └─ ...
>   ├─ val/
>   │  ├─ 0/ ...
>   │  └─ ...
>   └─ test/
>      ├─ 0/ ...
>      └─ ...
>   ```

---

## 6) Resolución de problemas

- **No encuentra imágenes**: revisa `img_folders` y que los nombres en el JSON coincidan con los archivos.  
- **Rutas con espacios/backslashes**: el script decodifica `%20` y normaliza barras.  
- **Cajas vacías o invertidas**: el script ajusta a los límites de la imagen y evita dimensiones negativas.  
- **Ángulo no detectado**: las muestras sin *choice* de ángulo van a `sin_angulo`.

---

## 7) Comandos rápidos (copiar/pegar)

**Windows (PowerShell):**
```powershell
git clone https://github.com/DalexQ/Salmon-Angle.git
cd <TU_REPO>
python -m venv .venv
.venv\Scripts\Activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python crop_fish.py
jupyter lab
```
