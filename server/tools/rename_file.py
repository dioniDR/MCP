import os

def rename_file(src: str, dst: str) -> str:
    try:
        os.rename(src, dst)
        return f"✅ Archivo renombrado de '{src}' a '{dst}'."
    except FileNotFoundError:
        return f"❌ El archivo '{src}' no fue encontrado."
    except Exception as e:
        return f"❌ Error al renombrar '{src}': {str(e)}"