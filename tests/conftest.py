import os
import sys
import site

# Add the project root directory to Python path
# This allows the tests to import the project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Añadir el directorio de ComfyUI app para encontrar las dependencias
comfy_app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
sys.path.insert(0, comfy_app_dir)

# Cambiar el directorio de trabajo al directorio app de ComfyUI
print(f"Cambiando directorio de trabajo a: {comfy_app_dir}")
os.chdir(comfy_app_dir)
print(f"Directorio actual: {os.getcwd()}")

# Si ComfyUI usa un entorno virtual, añadir su site-packages
# Esto es crítico para encontrar paquetes como httpx
comfy_site_packages = os.path.join(comfy_app_dir, 'venv', 'Lib', 'site-packages')
if os.path.exists(comfy_site_packages):
    sys.path.insert(0, comfy_site_packages)
    # También podemos usar site.addsitedir que es más completo
    site.addsitedir(comfy_site_packages)

# Para depuración - mostrar paths y verificar httpx
print(f"Python executable: {sys.executable}")
print(f"Python paths:")
for p in sys.path:
    print(f"  - {p}")

try:
    import httpx
    print(f"✅ HTTPX encontrado: {httpx.__file__}")
except ImportError:
    print("❌ HTTPX no se pudo importar")