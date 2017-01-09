# Automated marking parsing Script - module
#
# Automatically parse assignment grades
#
# Author: Phoenix Song (c.song@alumni.ubc.ca)
# Version: 20161223-a1

import os
import re
import pprint

ROOTDIR = './a1/'

# Compute percentage mark from the rubric
def computePercentageMark(markrec_dict):
  rubric_dict = {'Q1':{'weight':4 , 'marks':5.0},
          'Q2':{'weight':4 , 'marks':5.0},
          'Q3':{'weight':4 , 'marks':5.0},
          'Q4':{'weight':4 , 'marks':5.0},
          'End':{'weight':25 , 'marks':8.0},
          'EndTst':{'weight':5 , 'marks':5.0},
          'MAlg':{'weight':10 , 'marks':5.0},
          'MEnd':{'weight':10 , 'marks':5.0},
          'MGS':{'weight':15 , 'marks':10.0},
          'MemTst':{'weight':15 , 'marks':10.0},
          'FULLMARK':66.0
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
    if 'Zixuan' in folderDir:
      markrec = {}
      text = markfile.read()
      # print(text)
      for line in text.splitlines():
        if 'Q1: ' in line:
          markrec['Q1'] = float(line.split('Q1: ')[1].split('/')[0])
        elif 'Q2: ' in line:
          markrec['Q2'] = float(line.split('Q2: ')[1].split('/')[0])
        elif 'Q3: ' in line:
          markrec['Q3'] = float(line.split('Q3: ')[1].split('/')[0])
        elif 'Q4: ' in line:
          markrec['Q4'] = float(line.split('Q4: ')[1].split('/')[0])
        elif 'MEnd: ' in line:
          markrec['MEnd'] = float(line.split('MEnd: ')[1].split('/')[0])
        elif 'EndTest: ' in line:
          markrec['EndTst'] = float(line.split('EndTest: ')[1].split('/')[0])
        elif 'End: ' in line:
          markrec['End'] = float(line.split('End: ')[1].split('/')[0])
        elif 'MALg: ' in line:
          markrec['MAlg'] = float(line.split('MALg: ')[1].split('/')[0])
        elif 'MGS: ' in line:
          markrec['MGS'] = float(line.split('MGS: ')[1].split('/')[0])
        elif 'MemTst: ' in line:
          markrec['MemTst'] = float(line.split('MemTst: ')[1].split('/')[0])
      # print(folderDir)
      # pprint.pprint(markrec)
      mark = computePercentageMark(markrec)
      # print(mark)

    elif 'Qiushan' in folderDir:
      markrec = {}
      text = markfile.read().replace('.\n', ': ').replace('MemTst\n','MemTst: ')
      # print(text)
      for line in text.splitlines():
        if 'Q1: ' in line:
          markrec['Q1'] = float(line.split('Q1: ')[1].split('/')[0])
        elif 'Q2: ' in line:
          markrec['Q2'] = float(line.split('Q2: ')[1].split('/')[0])
        elif 'Q3: ' in line:
          markrec['Q3'] = float(line.split('Q3: ')[1].split('/')[0])
        elif 'Q4: ' in line:
          markrec['Q4'] = float(line.split('Q4: ')[1].split('/')[0])
        elif 'MEnd: ' in line:
          markrec['MEnd'] = float(line.split('MEnd: ')[1].split('/')[0])
        elif 'EndTst: ' in line:
          markrec['EndTst'] = float(line.split('EndTst: ')[1].split('/')[0])
        elif 'End: ' in line:
          markrec['End'] = float(line.split('End: ')[1].split('/')[0])
        elif 'MAlg: ' in line:
          markrec['MAlg'] = float(line.split('MAlg: ')[1].split('/')[0])
        elif 'MGS: ' in line:
          markrec['MGS'] = float(line.split('MGS: ')[1].split('/')[0])
        elif 'MemTst: ' in line:
          markrec['MemTst'] = float(line.split('MemTst: ')[1].split('/')[0])
      # print(folderDir)
      # pprint.pprint(markrec)
      mark = computePercentageMark(markrec)
      # print(mark)

    elif 'Frank' in folderDir:
      markrec = {}
      text = markfile.read().replace('. ', ': ')
      # print(folderDir)
      # print(text)
      for line in text.splitlines():
        if 'Q1: ' in line:
          markrec['Q1'] = float(line.split('Q1: ')[1].split('/')[0])
        elif 'Q2: ' in line:
          markrec['Q2'] = float(line.split('Q2: ')[1].split('/')[0])
        elif 'Q3: ' in line:
          markrec['Q3'] = float(line.split('Q3: ')[1].split('/')[0])
        elif 'Q4: ' in line:
          markrec['Q4'] = float(line.split('Q4: ')[1].split('/')[0])
        elif 'MEnd: ' in line:
          markrec['MEnd'] = float(line.split('MEnd: ')[1].split('/')[0])
        elif 'EndiannessTest: ' in line:
          markrec['EndTst'] = float(line.split('EndiannessTest: ')[1].split('/')[0])
        elif 'Endianness: ' in line:
          markrec['End'] = float(line.split('Endianness: ')[1].split('/')[0])
        elif 'MAlg: ' in line:
          markrec['MAlg'] = float(line.split('MAlg: ')[1].split('/')[0])
        elif 'MGS: ' in line:
          markrec['MGS'] = float(line.split('MGS: ')[1].split('/')[0])
        elif 'MemTst: ' in line:
          markrec['MemTst'] = float(line.split('MemTst: ')[1].split('/')[0])
      # pprint.pprint(markrec)
      mark = computePercentageMark(markrec)
      # print(mark)

    else:
      mark = float((markfile.readline().split('['))[1].split('/')[0])
  
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