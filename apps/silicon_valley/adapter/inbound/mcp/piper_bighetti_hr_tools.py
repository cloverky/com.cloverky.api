from mcp.server.fastmcp import FastMCP

mcp = FastMCP("piper_bighetti_hr")


@mcp.tool("/myself")
async def introduce_myself() -> str:
    return "파이퍼 HR 비게티 입니다"
