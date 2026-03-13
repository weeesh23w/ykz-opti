"""
Script para crear icono a partir del símbolo rojo que el usuario compartió
"""

from PIL import Image, ImageDraw
import os

def create_symbol_image(output_path="resources/ykz_symbol.png"):
    """
    Crea una imagen PNG del símbolo rojo en fondo negro
    (el kanji/símbolo que el usuario compartió)
    """
    
    # Crear imagen base (800x800 para buena calidad)
    width, height = 800, 800
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Dibujar fondo negro
    draw.rectangle([(0, 0), (width, height)], fill=(0, 0, 0, 255))
    
    # Definir el color rojo brillante (como en la imagen)
    red_color = (255, 50, 50, 255)  # Rojo vivo
    
    # Dibujar un símbolo similar al de la imagen (kanji estilizado)
    # Esto simula la forma del símbolo rojo que vimos
    center_x, center_y = width // 2, height // 2
    
    # Dibujar strokes del símbolo
    stroke_width = 35
    
    # Stroke principal horizontal
    draw.line([(center_x - 150, center_y - 120), (center_x + 150, center_y - 80)], 
              fill=red_color, width=stroke_width)
    
    # Strokes diagonales (forma característica)
    draw.line([(center_x - 100, center_y - 50), (center_x + 100, center_y + 80)], 
              fill=red_color, width=stroke_width)
    draw.line([(center_x + 80, center_y - 100), (center_x - 80, center_y + 80)], 
              fill=red_color, width=stroke_width)
    
    # Stroke inferior
    draw.line([(center_x - 120, center_y + 100), (center_x + 120, center_y + 100)], 
              fill=red_color, width=stroke_width)
    
    # Guardar
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    img.save(output_path, 'PNG')
    print(f"✅ Imagen símbolo creada: {output_path}")
    return output_path

if __name__ == "__main__":
    create_symbol_image()
