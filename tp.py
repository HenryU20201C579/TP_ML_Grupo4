import numpy as np
from PIL import Image

# Ruta de la imagen de entrada (debes proporcionar tu propia imagen)
input_image_path = "input.png"
# Escala de altura (ajústala según tus necesidades)
height_scale = 1.0

# Cargar la imagen y convertirla a escala de grises
image = Image.open(input_image_path).convert("L")

# Obtener los datos de la imagen como una matriz numpy
image_data = np.array(image)

# Obtener las dimensiones de la imagen
height, width = image_data.shape

# Función para generar un archivo STL a partir de una matriz de alturas
def generate_stl_from_heightmap(heightmap, scale):
    vertices = []
    faces = []

    for y in range(height):
        for x in range(width):
            z = heightmap[y, x] * scale
            vertices.append((x, y, z))

    for y in range(height - 1):
        for x in range(width - 1):
            v0 = y * width + x
            v1 = v0 + 1
            v2 = (y + 1) * width + x
            v3 = v2 + 1

            faces.append((v0, v2, v1))
            faces.append((v1, v2, v3))

    return vertices, faces

# Generar el archivo STL
vertices, faces = generate_stl_from_heightmap(image_data, height_scale)

# Escribir el archivo STL
output_stl_path = "salida.stl"
with open(output_stl_path, 'w') as stl_file:
    stl_file.write("solid my_model\n")
    for v in vertices:
        stl_file.write(f"  vertex {v[0]} {v[1]} {v[2]}\n")
    for f in faces:
        stl_file.write(f"  facet normal 0 0 0\n")
        stl_file.write(f"    outer loop\n")
        stl_file.write(f"      vertex {vertices[f[0]][0]} {vertices[f[0]][1]} {vertices[f[0]][2]}\n")
        stl_file.write(f"      vertex {vertices[f[1]][0]} {vertices[f[1]][1]} {vertices[f[1]][2]}\n")
        stl_file.write(f"      vertex {vertices[f[2]][0]} {vertices[f[2]][1]} {vertices[f[2]][2]}\n")
        stl_file.write(f"    endloop\n")
        stl_file.write(f"  endfacet\n")
    stl_file.write("endsolid my_model\n")

print(f"Archivo STL generado en {output_stl_path}")
