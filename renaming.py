# Automated renaming Script
# Author: Phoenix Song (c.song@alumni.ubc.ca)
# Version: 20161115
import os

ROOTDIR = '.'

RENAME_DICT = {
  'marking-scheme.txt':'MARKING.txt',
  'readme.txt':'README.txt',
  'ReadMe.txt':'README.txt', 
  'README.txt.txt':'README.txt',
  'README.TXT':'README.txt',
  'readMe.txt':'README.txt',
  'ReadME.txt':'README.txt',
}

for subdir, dirs, files in os.walk(ROOTDIR):
  for file in files:
    if file in RENAME_DICT:
      os.rename(os.path.join(subdir, file),os.path.join(subdir, RENAME_DICT[file]))

print('File Renamings Done.')