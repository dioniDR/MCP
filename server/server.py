from mcp.server.fastmcp import FastMCP
from server.tools.read_file import read_file
from server.tools.list_files import list_files

mcp = FastMCP("MCPAgent")

@mcp.tool()
def read_file_tool(filepath: str) -> str:
    return read_file(filepath)

@mcp.tool()
def list_files_tool(path: str) -> str:
    return list_files(path)

if __name__ == "__main__":
    print("🧪 Prueba directa de read_file:")
    print(read_file_tool(filepath="README.md"))

    print("\n🧪 Prueba directa de list_files:")
    print(list_files_tool(path="."))
