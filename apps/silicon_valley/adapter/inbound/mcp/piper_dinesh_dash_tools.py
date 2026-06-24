from mcp.server.fastmcp import FastMCP

mcp = FastMCP("piper_dinesh_dash")


@mcp.tool("/myself")
async def introduce_myself() -> str:
    return "파이퍼 소프트웨어 개발자 디네시 입니다"
