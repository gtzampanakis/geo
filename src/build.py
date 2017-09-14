import os
import shutil
import zipfile

BASE_DIR = os.path.dirname(__file__)
BUILD_DIR = os.path.join(BASE_DIR, 'build')
LIB_DIR = os.path.join(BUILD_DIR, 'lib')

if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)

os.mkdir(BUILD_DIR)
os.mkdir(LIB_DIR)

for filename in [
    'datamerge.py',
    'error.py',
    'favicon.ico',
    'fileio.py.',
    'geomath.py',
    'gui.py',
    'geotypes.py',
]:
    shutil.copy(os.path.join(BASE_DIR, filename), LIB_DIR)

shutil.copyfile(
    os.path.join(BASE_DIR, 'geotools.py'),
    os.path.join(BUILD_DIR, 'geotools.pyw'))
