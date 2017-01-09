# Automated marking parsing Script - module
#
# Author: Phoenix Song (c.song@alumni.ubc.ca)
# Version: 20161225-a7-complete

import os
import re
import pprint

ROOTDIR = './a7/'

# Merge and parse marks from Marking files
def parseHelper(folderDir, markfile):
  string_contains_total_mark = (markfile.readline().split('['))[1].split('/')[0]
  # print(string_contains_total_mark)
  mark = float(string_contains_total_mark) if string_contains_total_mark != '' else None

  if mark is None:
    print('[a7] WARNING: ' + folderDir + ' does not contain a valid mark')
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
