import os

def list_files(path: str) -> str:
    try:
        items = os.listdir(path)
        if not items:
            return f"La carpeta '{path}' está vacía."
        return f"Contenido de '{path}':\n" + "\n".join(items)
    except FileNotFoundError:
        return f"❌ La carpeta '{path}' no fue encontrada."
    except NotADirectoryError:
        return f"❌ '{path}' no es una carpeta válida."
    except Exception as e:
        return f"❌ Error al listar '{path}': {str(e)}"
