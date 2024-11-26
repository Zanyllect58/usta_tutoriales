import subprocess

# Función para ejecutar scripts
def ejecutar_script(script_name):
    try:
        print(f"Ejecutando {script_name}...")
        subprocess.run(["python", script_name], check=True)
        print(f"{script_name} ejecutado correctamente.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script_name}: {e}\n")

if __name__ == "__main__":
    # Lista de scripts a ejecutar en orden
    scripts = ["user_admin.py", "models.py", "app.py"]

    for script in scripts:
        ejecutar_script(script)
