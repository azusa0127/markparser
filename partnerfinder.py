# Partner Finder Script
# Author: Phoenix Song (c.song@alumni.ubc.ca)
# Version: 20161205
import os

ROOTDIR = '.'

targetDict = {
  'k9k0b':{'sid':'30496153', 'name':'Jiayi Zhao'},
}

for subdir, dirs, files in os.walk(ROOTDIR):
  for file in files:
    if 'PARTNER' in file:
      partnerFile = open(os.path.join(subdir, file), 'r')
      partnerCSid = partnerFile.readline()
      partnerFile.close()
      if partnerCSid in targetDict:
        print(targetDict[partnerCSid]['sid'] + ' - ' + subdir)

print('Done.')