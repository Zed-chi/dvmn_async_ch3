import asyncio
import datetime
import subprocess
from zipfile import ZipFile


def archivate():
    process = subprocess.Popen(["bash", "zip_files.sh"], stdout=subprocess.PIPE)
    return process.stdout.read()

async def async_archivate(cmd=None):
    if not cmd:
        cmd = ["bash", "zip_files.sh"]

    proc = await asyncio.create_subprocess_exec(
        "bash","zip_files.sh",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, _ = await proc.communicate()
    return stdout
    

if __name__ == "__main__":
    asyncio.run(async_archivate())