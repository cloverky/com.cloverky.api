from mcp.server.fastmcp import FastMCP

mcp = FastMCP("piper_gilfoyle_sys")


@mcp.tool("/myself")
async def introduce_myself() -> str:
    return "파이퍼 시스템 엔지니어 길포일 입니다"
