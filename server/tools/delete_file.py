import os

def delete_file(filepath: str) -> str:
    try:
        os.remove(filepath)
        return f"✅ Archivo '{filepath}' eliminado correctamente."
    except FileNotFoundError:
        return f"❌ El archivo '{filepath}' no fue encontrado."
    except Exception as e:
        return f"❌ Error al eliminar '{filepath}': {str(e)}"