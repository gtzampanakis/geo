import os
import shutil
import zipfile

BASE_DIR = os.path.dirname(__file__)
BUILD_DIR = os.path.join(BASE_DIR, 'build')
LIB_DIR = os.path.join(BUILD_DIR, 'lib')
ZIP_PATH = os.path.join(BASE_DIR, 'geotools.zip')

if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)

if os.path.exists(ZIP_PATH):
    os.remove(ZIP_PATH)

os.mkdir(BUILD_DIR)
os.mkdir(LIB_DIR)

LIB_FILENAMES = [
    'datamerge.py',
    'error.py',
    'favicon.ico',
    'fileio.py',
    'geomath.py',
    'gui.py',
    'geotypes.py',
]

for filename in LIB_FILENAMES:
    shutil.copy(os.path.join(BASE_DIR, filename), LIB_DIR)

shutil.copyfile(
    os.path.join(BASE_DIR, 'geotools.py'),
    os.path.join(BUILD_DIR, 'geotools.pyw'))

with zipfile.ZipFile(ZIP_PATH, 'w') as z:
    for filename in LIB_FILENAMES:
        z.write(os.path.join(LIB_DIR, filename), os.path.join('lib', filename))
    z.write(
        os.path.join(BUILD_DIR, 'geotools.pyw'),
        os.path.join('geotools.pyw'))
    

