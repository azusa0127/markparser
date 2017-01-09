# Automated marking parsing Script - module
#
# Automatically parse assignment grades
#
# Author: Phoenix Song (c.song@alumni.ubc.ca)
# Version: 20161224-a2

import os
import re
import pprint

ROOTDIR = './a2/'

# Compute percentage mark from the rubric
def computePercentageMark(markrec_dict):
  rubric_dict = {'CPU':{'weight':80 , 'marks':6.0},
                'Test':{'weight':20 , 'marks':5.0},
                'FULLMARK':11.0
                }
  if sum(markrec_dict.values()) == rubric_dict['FULLMARK']:
    return 100
  total_mark = 0
  for key, value in markrec_dict.items():
    total_mark += round(float("{0:.1f}".format((value/rubric_dict[key]['marks'])*rubric_dict[key]['weight'])))
  return total_mark;


# Parse marks from MARKING.txt
def parseHelper(folderDir, fileName):
  mark = None
  
  with open(fileName,'r') as markfile:
    if 'Frank' in folderDir:
      markrec = {}
      text = markfile.read().replace('. ', ': ')
      # print(folderDir)
      # print(text)
      for line in text.splitlines():
        if 'CPU: ' in line:
          markrec['CPU'] = float(line.split('CPU: ')[1].split('/')[0])
        elif 'Tests: ' in line:
          markrec['Test'] = float(line.split('Tests: ')[1].split('/')[0])
      # pprint.pprint(markrec)
      mark = computePercentageMark(markrec)
      # print(mark)

    else:
      markrec = {}
      text = markfile.read()
      # print(text)
      for line in text.splitlines():
        if 'CPU ' in line:
          markrec['CPU'] = float(line.split('CPU ')[1].split('/')[0])
        elif 'Test ' in line:
          markrec['Test'] = float(line.split('Test ')[1].split('/')[0])
          # print(folderDir)
      # pprint.pprint(markrec)
      mark = computePercentageMark(markrec)
      # print(mark)

  return mark


# Returns a dictionary with folder csID as index
def parseMark():
  ret_dict = {}
  
  for subdir, dirs, files in os.walk(ROOTDIR):
    for file in files:
      if file == 'MARKING.txt':
        submitCSid = None
        partnerCSid = None
        mark = None
        sids = []

        # pprint.pprint((os.path.split(subdir)[-1],file))
        submitCSid = os.path.split(subdir)[-1]
        
        mark = parseHelper(subdir,os.path.join(subdir, file))

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

# pprint.pprint(parseMark())