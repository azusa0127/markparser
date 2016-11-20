# Automated Cleanup Script
# Author: Phoenix Song (c.song@alumni.ubc.ca)
# Version: 20161115
import os
import shutil

ROOTDIR = '.'

TARGET_DIRS = [
  '._.DS_Store',
  '_MACOSX'
  ]

TARGET_FILES = [
  '.DS_Store',
  '._.DS_Store',
  '.Spotlight-V100',
  '.Trashes',
  'ehthumbs.db',
  'Thumbs.db'
  ]

for subdir, dirs, files in os.walk(ROOTDIR):
  for d in dirs:
    if d in TARGET_DIRS:
      shutil.rmtree(os.path.join(subdir, d))
  for f in files:
    if f in TARGET_FILES:
      os.remove(os.path.join(subdir, f))

print('Folder Cleanup Done.')