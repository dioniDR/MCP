def read_file(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read(1000)  # Limita la lectura a 1000 caracteres
    except FileNotFoundError:
        return f"❌ El archivo '{filepath}' no fue encontrado."
    except Exception as e:
        return f"❌ Error al leer '{filepath}': {str(e)}"
