# Automated marking parsing Script - module
#
# Author: Phoenix Song (c.song@alumni.ubc.ca)
# Version: 20161224-a6

import os
import re
import pprint

ROOTDIR = './a6/'

# Parse marks differently from MARKING.txt
def parseHelper(folderDir, markfile):
  mark = None

  if 'Frank' in folderDir:
    mark = 0
    for line in markfile.read().splitlines():
      if 'Part 1: Static Flow Control [' in line:
        mark += float(line.split('Part 1: Static Flow Control [')[1].split('/')[0])
      elif 'Part 2: The Stack [' in line:
        mark += float(line.split('Part 2: The Stack [')[1].split('/')[0])
      elif 'Part 3: Reading Assembly Code [' in line:
        mark += float(line.split('Part 3: Reading Assembly Code [')[1].split('/')[0])
      elif 'Part 4: Stack Smash Attack [' in line:
        mark += float(line.split('Part 4: Stack Smash Attack [')[1].split('/')[0])
  else:
    temp_str = (markfile.readline().split('['))[1].split('/')[0]
    # print(temp_str)
    if temp_str == '':
      print('[WARNING][a6]' + folderDir+ ' no marks given!')
    mark = float(temp_str) if temp_str != '' else 0
  return mark

# Returns a dictionary with folder csID as index
def parseMark(rootdir = ROOTDIR):
  ret_dict = {}

  for subdir, dirs, files in os.walk(rootdir):
    for file in files:
      if file == 'MARKING.txt':
        submitCSid = None
        partnerCSid = None
        mark = None
        sids = []

        # pprint.pprint((os.path.split(subdir)[-1],file))
        submitCSid = os.path.split(subdir)[-1]

        with open(os.path.join(subdir, file), 'r') as markfile:
          mark = parseHelper(subdir, markfile)

        # pprint.pprint(files)
        if 'README.txt' in files:
          with open(os.path.join(subdir, 'README.txt'), 'r') as rdmfile:
            sids = re.findall('[0-9]{8}', rdmfile.read())

        # pprint.pprint(subdir)

        if 'PARTNER.txt' in files:
          with open(os.path.join(subdir, 'PARTNER.txt'), 'r') as ptnfile:
            text = re.findall('[a-z][0-9][a-z][0-9][a-z]?', ptnfile.read().lower())
            if len(text) > 0 and text[0] != submitCSid:
              partnerCSid = text[0]
              # print(subdir)
              # pprint.pprint((partnerCSid, sids))

        ret_dict[submitCSid] = {'submitCSid':submitCSid,
                                'partnerCSid':partnerCSid,
                                'mark':mark,
                                'sids':sids}

        if partnerCSid in ret_dict:
          if ret_dict[partnerCSid]['mark'] <= mark:
            ret_dict.pop(partnerCSid)
          elif ret_dict[partnerCSid]['partnerCSid'] == submitCSid:
            ret_dict.pop(submitCSid)

  return ret_dict

# pprint.pprint(parseMark('.'))
