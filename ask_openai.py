import os
import json
import openai
from dotenv import load_dotenv
from server.tools.read_file import read_file
from server.tools.list_files import list_files

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

# Pregunta del usuario
messages = [
    {"role": "user", "content": "¿Qué archivos hay en esta carpeta?"}
]

# Primera llamada a GPT-4o con tools registradas
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=[{"type": "function", "function": f} for f in functions],
    tool_choice="auto"
)

message = response.choices[0].message

# ¿El modelo eligió usar una herramienta?
if message.tool_calls:
    for tool_call in message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        
        if name == "list_files_tool":
            result = list_files(**args)
        elif name == "read_file_tool":
            result = read_file(**args)
        else:
            result = "❌ Tool desconocida."

        print(f"🤖 GPT quiere usar `{name}` con argumentos: {args}")
        print("📦 Resultado de la tool:\n", result)

        # Enviamos la respuesta de la tool a GPT
        messages.append(message)  # el mensaje original del modelo
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        print("\n🧠 Respuesta final del modelo:\n", final_response.choices[0].message.content)
else:
    print("💬 Respuesta directa de GPT:\n", message.content)
