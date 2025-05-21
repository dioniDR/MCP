from server.tools.write_file import write_file
from server.tools.rename_file import rename_file
from server.tools.delete_file import delete_file
from server.tools.search_in_file import search_in_file

@mcp.tool()
def write_file_tool(filepath: str, content: str) -> str:
    return write_file(filepath, content)

@mcp.tool()
def rename_file_tool(src: str, dst: str) -> str:
    return rename_file(src, dst)

@mcp.tool()
def delete_file_tool(filepath: str) -> str:
    return delete_file(filepath)

@mcp.tool()
def search_in_file_tool(filepath: str, pattern: str) -> str:
    return search_in_file(filepath, pattern)