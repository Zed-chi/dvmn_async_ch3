import asyncio
import subprocess
import sys


def archivate(path):
    process = subprocess.Popen(
        ["bash", "zip_files.sh", path], stdout=subprocess.PIPE
    )
    sys.stdout.buffer.write(process.stdout.read())


async def async_archivate(path):
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
        sys.stdout.buffer.write(chunk)


if __name__ == "__main__":
    path = sys.argv[1]
    asyncio.run(async_archivate(path))
