import asyncio
import aiofiles
import logging
import os
import sys
from aiohttp import web
from config import get_args


ARGS = get_args()
if ARGS.logging:
    logging.basicConfig(filename="server.log", level=logging.INFO)
else:
    logging.basicConfig(filename="server.log", level=logging.WARNING)


async def archivate(request):
    logger.info("zipper started")
    name = request.match_info.get("archive_hash", None)
    if not name:
        logger.error("can't get archive hash")
        raise web.HTTPBadRequest(text="Can't get archive hash")
    path = os.path.join(".", ARGS.path, name)

    if not os.path.exists(path):
        logger.error("archive not found")
        raise web.HTTPNotFound(text="Archive not found")
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
    try:
        while True:
            chunk = await proc.stdout.read(100000)
            if not chunk:
                break            
            await response.write(chunk)
            await asyncio.sleep(ARGS.delay)
        logger.info("archive sended")
        return response
    except (BaseException, CancelledError) as e:
        logger.error(f"some {e.__class__.__name__} was done")                
        proc.terminate()
        a, b = await proc.communicate()
        logger.error("process terminated")
    finally:
        logger.info("request finished")        
    return response


async def handle_index_page(request):
    async with aiofiles.open(
        "index.html", mode="r", encoding="utf-8"
    ) as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type="text/html")


if __name__ == "__main__":            
    app = web.Application()
    app.add_routes(
        [
            web.get("/", handle_index_page),
            web.get("/archive/{archive_hash}/", archivate),
        ]
    )
    web.run_app(app)
