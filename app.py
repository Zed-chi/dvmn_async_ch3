from zipfile import ZipFile
import subprocess
import datetime

def archivate():
    program = "zip_file.sh"
    process = subprocess.call(program)
    return process.stdout
 
print(process.stdout) # 0

import asyncio

async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')

asyncio.run(main())