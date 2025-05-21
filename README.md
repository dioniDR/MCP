# MCP Agent Project

Este proyecto implementa un agente MCP funcional en Python con herramientas reales que pueden ser utilizadas por modelos como Claude o OpenAI GPT-4o.

## 📁 Estructura del proyecto

```
MCP/
├── server/
│   ├── __init__.py
│   ├── server.py
│   └── tools/
│       ├── __init__.py
│       ├── read_file.py
│       └── list_files.py
├── ask_openai.py
├── export_to_openai.py
├── .env
├── README.md
└── venv/
```

## ⚙️ Comandos útiles

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar tools directamente
python -m server.server

# Simular ejecución con GPT-4o
python ask_openai.py

# Exportar funciones en formato OpenAI
python export_to_openai.py

# Ejecutar como servidor MCP
PYTHONPATH=. mcp dev server.server
```

## 🔐 .env

Crear un archivo `.env` con tu clave de OpenAI:

```
OPENAI_API_KEY=sk-xxxx
```

## 📦 Requisitos

- Python 3.10+
- Paquetes: `openai`, `python-dotenv`, `mcp[cli]`
- OpenAI API Key
