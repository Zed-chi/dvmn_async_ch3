import asyncio
import datetime
import subprocess
import sys
from zipfile import ZipFile


def archivate():
    process = subprocess.Popen(["bash", "zip_files.sh"], stdout=subprocess.PIPE)
    sys.stdout.write(process.stdout.read())

async def async_archivate(cmd=None):
    if not cmd:
        cmd = ["bash", "zip_files.sh"]

    proc = await asyncio.create_subprocess_exec(
        "bash","zip_files.sh",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    while True:        
        chunk = await proc.stdout.read(100000)
        if not chunk:
            break
        sys.stdout.buffer.write(chunk)        
    

if __name__ == "__main__":
    asyncio.run(async_archivate())