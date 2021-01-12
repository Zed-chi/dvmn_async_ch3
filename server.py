from aiohttp import web
import asyncio
import datetime
import aiofiles
import os


async def archivate(request):
    name = request.match_info.get("archive_hash", None)
    if not name:
        return
    path = os.path.join(".", "test_photos", name)

    if not os.path.exists(path):
        return
    response = web.StreamResponse(
        status=200,
        reason="OK",
        headers={
            "Content-Type": "application/zip",
            "Content-Disposition": f'attachment; filename="{name}.zip"',
        },
    )
    await response.prepare(request)

    proc = await asyncio.create_subprocess_exec(
        "bash",
        "zip_files.sh",
        path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    while True:
        chunk = await proc.stdout.read(100000)
        if not chunk:
            break
        await response.write(chunk)

    return response


async def handle_index_page(request):
    async with aiofiles.open(
        "index.html", mode="r", encoding="utf-8"
    ) as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type="text/html")


async def uptime_handler(request):

    response = web.StreamResponse(
        status=200,
        reason="OK",
        headers={
            "Content-Type": "text/html",
            "X-Content-Type-Options": "nosniff",
            "charset": "utf8",
        },
    )
    await response.prepare(request)

    for i in range(10):
        await response.write(f"text {i}\n".encode("utf-8"))
        await asyncio.sleep(1)


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(
        [
            web.get("/", handle_index_page),
            # web.get("/archive/7kna/", uptime_handler),
            web.get("/archive/{archive_hash}/", archivate),
        ]
    )
    web.run_app(app)
