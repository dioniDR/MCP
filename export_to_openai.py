import json

# Definición manual de las tools en formato OpenAI-compatible

functions = [
    {
        "name": "read_file_tool",
        "description": "Lee hasta 1000 caracteres del contenido de un archivo de texto.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Ruta completa o relativa del archivo a leer."
                }
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "list_files_tool",
        "description": "Lista archivos y carpetas en un directorio dado.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Ruta del directorio a listar (puede ser '.')."
                }
            },
            "required": ["path"]
        }
    }
]

print(json.dumps(functions, indent=2))
