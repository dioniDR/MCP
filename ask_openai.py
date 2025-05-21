import os
import json
import openai
from dotenv import load_dotenv
from server.tools.read_file import read_file
from server.tools.list_files import list_files
from server.tools.write_file import write_file
from server.tools.rename_file import rename_file
from server.tools.delete_file import delete_file
from server.tools.search_in_file import search_in_file

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
    },
    {
        "name": "write_file_tool",
        "description": "Escribe contenido en un archivo de texto.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Ruta del archivo a escribir."},
                "content": {"type": "string", "description": "Contenido a escribir en el archivo."}
            },
            "required": ["filepath", "content"]
        }
    },
    {
        "name": "rename_file_tool",
        "description": "Renombra un archivo.",
        "parameters": {
            "type": "object",
            "properties": {
                "src": {"type": "string", "description": "Ruta actual del archivo."},
                "dst": {"type": "string", "description": "Nueva ruta o nombre del archivo."}
            },
            "required": ["src", "dst"]
        }
    },
    {
        "name": "delete_file_tool",
        "description": "Elimina un archivo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Ruta del archivo a eliminar."}
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "search_in_file_tool",
        "description": "Busca un patrón (expresión regular) en un archivo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Ruta del archivo a buscar."},
                "pattern": {"type": "string", "description": "Patrón o expresión regular a buscar."}
            },
            "required": ["filepath", "pattern"]
        }
    }
]

# Map tool names to local Python functions
tool_functions = {
    "read_file_tool": read_file,
    "list_files_tool": list_files,
    "write_file_tool": write_file,
    "rename_file_tool": rename_file,
    "delete_file_tool": delete_file,
    "search_in_file_tool": search_in_file,
}

def print_history(messages):
    print("\n=== Historial del chat ===")
    for msg in messages:
        if msg["role"] == "user":
            print(f"👤 Usuario: {msg['content']}")
        elif msg["role"] == "assistant":
            print(f"🤖 Asistente: {msg['content']}")
        elif msg["role"] == "tool":
            print(f"🛠️ Tool: {msg['content']}")

def main():
    messages = []
    print("💬 Chat persistente con OpenAI + tools (Ctrl+C para salir)\n")
    while True:
        try:
            user_input = input("👤 Tú: ").strip()
            if not user_input:
                continue

            # Comando especial para imprimir historial
            if user_input.lower() in {"/hist", "/history"}:
                print_history(messages)
                continue
            if user_input.lower() == "/exit":
                print("👋 ¡Hasta luego!")
                break

            messages.append({"role": "user", "content": user_input})

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
                    tool_fn = tool_functions.get(name)
                    if tool_fn:
                        try:
                            result = tool_fn(**args)
                        except Exception as e:
                            result = f"❌ Error ejecutando tool: {str(e)}"
                    else:
                        result = "❌ Tool desconocida."

                    print(f"🤖 GPT quiere usar `{name}` con argumentos: {args}")
                    print("📦 Resultado de la tool:\n", result)
                    
                    # Añadir mensaje de tool-call al historial
                    messages.append(message)  # mensaje original del modelo
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })

                    # Responder a la tool
                    final_response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages
                    )
                    assistant_msg = final_response.choices[0].message
                    print("\n🧠 Respuesta del modelo:\n", assistant_msg.content)
                    messages.append({"role": "assistant", "content": assistant_msg.content})
            else:
                print("💬 Respuesta directa de GPT:\n", message.content)
                messages.append({"role": "assistant", "content": message.content})

        except KeyboardInterrupt:
            print("\n👋 Chat finalizado.")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()