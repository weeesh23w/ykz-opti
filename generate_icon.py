"""
Script para generar un archivo .ico con múltiples tamaños a partir de una imagen PNG.
Necesita: pip install Pillow

USO:
  python generate_icon.py                   # Usa ykz_logo_rendered.png
  python generate_icon.py exe_icon.png      # Usa exe_icon.png
  python generate_icon.py custom.png app.ico # Entrada y salida personalizadas
"""

from PIL import Image
import os
import sys

def generate_ico(source_path, output_path="resources/app_icon.ico", sizes=[16, 32, 48, 64, 128, 256]):
    """
    Genera un archivo .ico con múltiples tamaños.
    
    Args:
        source_path: Ruta de la imagen PNG de entrada
        output_path: Ruta del archivo .ico de salida
        sizes: Lista de tamaños en píxeles
    """
    
    if not os.path.exists(source_path):
        print(f"❌ Error: No se encontró {source_path}")
        print(f"   Rutas disponibles en 'resources/':")
        try:
            for file in os.listdir("resources"):
                if file.endswith(('.png', '.jpg', '.jpeg')):
                    print(f"     - resources/{file}")
        except:
            pass
        return False
    
    try:
        # Abrir imagen original
        img = Image.open(source_path).convert("RGBA")
        print(f"✅ Imagen original cargada: {source_path}")
        print(f"   Dimensiones: {img.size[0]}x{img.size[1]} px")
        
        # Si imagen es muy pequeña, advertir
        if img.size[0] < 256 or img.size[1] < 256:
            print(f"   ⚠️  ADVERTENCIA: La imagen es pequeña. Se escalará, pero puede perder calidad.")
        
        # Redimensionar a cada tamaño requerido
        print(f"\n🎨 Generando tamaños:")
        resized_images = []
        for size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            resized_images.append(resized)
            print(f"   ✓ {size:3d}x{size:<3d}px")
        
        # Guardar como .ico
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        resized_images[0].save(
            output_path,
            format="ICO",
            sizes=[(size, size) for size in sizes]
        )
        
        file_size = os.path.getsize(output_path) / 1024
        print(f"\n✅ Icono creado exitosamente!")
        print(f"   📁 Archivo: {output_path}")
        print(f"   📊 Tamaño: {file_size:.1f} KB")
        print(f"   📐 Resoluciones: {sizes}")
        return True
        
    except Exception as e:
        print(f"❌ Error al generar icono: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎨 Generador de Iconos para YKZ Optimizer")
    print("=" * 60)
    
    # Detectar parámetros
    if len(sys.argv) == 1:
        # Sin argumentos: usar valores por defecto
        source_image = "resources/ykz_logo_rendered.png"
        output_icon = "resources/app_icon.ico"
    elif len(sys.argv) == 2:
        # Un argumento: entrada personalizada
        source_image = sys.argv[1]
        # Si no tiene ruta, buscar en resources/
        if not os.path.exists(source_image):
            source_image = f"resources/{source_image}"
        output_icon = "resources/app_icon.ico"
    else:
        # Dos argumentos: entrada y salida personalizadas
        source_image = sys.argv[1]
        output_icon = sys.argv[2]
        if not os.path.exists(source_image):
            source_image = f"resources/{source_image}"
        if not "/" in output_icon:
            output_icon = f"resources/{output_icon}"
    
    print(f"📥 Entrada: {source_image}")
    print(f"📤 Salida:  {output_icon}")
    print("-" * 60)
    
    if generate_ico(source_image, output_icon):
        print("\n" + "=" * 60)
        print("📌 PRÓXIMOS PASOS:")
        print("   1. Ejecuta: pyinstaller YKZ_OPTI.spec")
        print("   2. Tu .exe estará en: dist/YKZ_OPTI.exe")
        print("   3. El icono aparecerá en:")
        print("      • Explorador Windows 📁")
        print("      • Barra de tareas ⚡")
        print("      • Ventana de la aplicación 🪟")
        print("=" * 60)
    else:
        print("\n❌ No se pudo generar el icono. Verifica la imagen de entrada.")
        sys.exit(1)

