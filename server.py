import argparse
import asyncio
import logging
import os

import aiofiles
from aiohttp import web


def get_args():
    parser = argparse.ArgumentParser(description="Image Archiver Service")
    parser.add_argument(
        "-l",
        action="store_true",
        dest="logging",
        help="turn log on/off",
    )
    parser.add_argument(
        "--delay",
        default=0,
        type=int,
        help="delay between response in seconds",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="host of the server",
    )
    parser.add_argument(
        "--port",
        default=10000,
        type=int,
        help="port of the server",
    )
    parser.add_argument(
        "--chunk_size",
        default=250000,
        type=int,
        help="chunk size to send in loop",
    )
    parser.add_argument(
        "--path",
        default="test_photos",
        help="path to photos dir",
    )
    args = parser.parse_args()
    return args


async def archivate(request):
    logging.info("zipper started")

    name = request.match_info.get("archive_hash", None)
    if not name:
        logging.error("can't get archive hash")
        raise web.HTTPBadRequest(text="Can't get archive hash")
    path = os.path.join(".", args.path, name)

    if not os.path.exists(path):
        logging.error("archive not found")
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
            chunk = await proc.stdout.read(args.chunk_size)
            if not chunk:
                break
            await response.write(chunk)
            await asyncio.sleep(args.delay)
        logging.info("archive sended")
    except (BaseException, asyncio.CancelledError) as e:
        logging.error(e)
        a, b = await proc.communicate()
        logging.error("process terminated")
    finally:
        logging.info("request finished")
    return response


async def handle_index_page(request):
    async with aiofiles.open(
        "index.html",
        mode="r",
        encoding="utf-8",
    ) as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type="text/html")


def init(path):
    path = os.path.join(".", path)
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    args = get_args()
    init(args.path)

    if args.logging:
        logging.basicConfig(filename="server.log", level=logging.INFO)
    else:
        logging.basicConfig(filename="server.log", level=logging.WARNING)

    app = web.Application()
    app.add_routes(
        [
            web.get("/", handle_index_page),
            web.get("/archive/{archive_hash}/", archivate),
        ],
    )

    web.run_app(app, host=args.host, port=args.port)
