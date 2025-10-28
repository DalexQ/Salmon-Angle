from PIL import Image
import json
import os

# Rutas
json_path = "project-3-at-2025-10-21-17-49-288e7bbb.json"
img_folders = [
    "fish original"
]
cropped_folder = "fish_angles_raw"

# 🔹 Crear carpetas para cada ángulo y una para sin ángulo
angles = ["0", "45", "90", "135", "180", "225", "270", "315", "sin_angulo"]
for angle in angles:
    angle_folder = os.path.join(cropped_folder, angle)
    os.makedirs(angle_folder, exist_ok=True)

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 🔹 Mapeo para normalizar los ángulos del JSON
# Convierte "0°" o "0Â°" del JSON a "0" (nombre simple de carpeta)
angle_mapping = {
    "0°": "0",
    "45°": "45",
    "90°": "90",
    "135°": "135",
    "180°": "180",
    "225°": "225",
    "270°": "270",
    "315°": "315"
}

for item in data:
    # 🔹 Extraer el nombre de la imagen desde el campo "data"
    if "data" in item and "image" in item["data"]:
        img_url = item["data"]["image"]
        # Extraer el nombre después de "?d=" y decodificar URL
        import urllib.parse
        img_path_encoded = img_url.split("?d=")[-1]
        img_relative_path = urllib.parse.unquote(img_path_encoded)
        img_name_clean = os.path.basename(img_relative_path)
    else:
        continue

    # 🔹 Buscar la imagen en todas las carpetas especificadas
    img_path = None
    for folder in img_folders:
        potential_path = os.path.join(folder, img_name_clean)
        # También buscar en subcarpetas (seq_0001, seq_0002, etc.)
        if os.path.exists(potential_path):
            img_path = potential_path
            break
        # Buscar recursivamente en subcarpetas
        for root, dirs, files in os.walk(folder):
            if img_name_clean in files:
                img_path = os.path.join(root, img_name_clean)
                break
        if img_path:
            break

    if not img_path or not os.path.exists(img_path):
        print(f"⚠️ No se encontró la imagen: {img_name_clean}")
        continue
    
    img = Image.open(img_path)
    
    # 🔹 Buscar el ángulo en las anotaciones
    angle_choice = None
    for ann in item["annotations"]:
        for result in ann["result"]:
            # Buscar el resultado con "choices" para obtener el ángulo
            if "value" in result and "choices" in result["value"]:
                angle_choice = result["value"]["choices"][0]
                break
        if angle_choice:
            break
    
    # Si no se encontró ángulo, usar carpeta "sin_angulo"
    if not angle_choice:
        angle_choice = "sin_angulo"
    else:
        # 🔹 Normalizar el ángulo usando el mapeo
        angle_choice = angle_mapping.get(angle_choice, angle_choice)
    
    # 🔹 Procesar cada anotación de rectángulo
    for ann in item["annotations"]:
        for result in ann["result"]:
            # Solo procesar rectanglelabels (las cajas de recorte)
            if result.get("type") == "rectanglelabels":
                val = result["value"]
                x_px = int(val["x"] / 100 * result["original_width"])
                y_px = int(val["y"] / 100 * result["original_height"])
                w_px = int(val["width"] / 100 * result["original_width"])
                h_px = int(val["height"] / 100 * result["original_height"])
                
                cropped = img.crop((x_px, y_px, x_px + w_px, y_px + h_px))
                save_name = f"{os.path.splitext(img_name_clean)[0]}_{x_px}_{y_px}.png"
                
                # Guardar en la carpeta del ángulo correspondiente
                angle_folder = os.path.join(cropped_folder, angle_choice)
                os.makedirs(angle_folder, exist_ok=True)
                cropped.save(os.path.join(angle_folder, save_name))

print("✅ Recortes completados. Imágenes guardadas en:", cropped_folder)
print(f"   Organizadas por ángulos: {', '.join(angles)}")
