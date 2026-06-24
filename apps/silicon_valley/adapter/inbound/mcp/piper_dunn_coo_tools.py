from mcp.server.fastmcp import FastMCP

mcp = FastMCP("piper_dunn_coo")


@mcp.tool("/myself")
async def introduce_myself() -> str:
    return "파이퍼 COO 던 입니다"
