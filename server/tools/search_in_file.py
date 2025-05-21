import re

def search_in_file(filepath: str, pattern: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        matches = [line for line in content.splitlines() if re.search(pattern, line)]
        if matches:
            return "Coincidencias encontradas:\n" + "\n".join(matches)
        else:
            return "No se encontraron coincidencias."
    except FileNotFoundError:
        return f"❌ El archivo '{filepath}' no fue encontrado."
    except Exception as e:
        return f"❌ Error al buscar en '{filepath}': {str(e)}"