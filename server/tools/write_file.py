def write_file(filepath: str, content: str) -> str:
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Archivo '{filepath}' escrito correctamente."
    except Exception as e:
        return f"❌ Error al escribir '{filepath}': {str(e)}"