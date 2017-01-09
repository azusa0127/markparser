# Automated marking parsing Script - module
#
# Author: Phoenix Song (c.song@alumni.ubc.ca)
# Version: 20161225-a7-complete

import os
import re
import pprint

ROOTDIR = './a7/'

# Merge and parse marks from Marking files
def mergeMarks(subdir, files):
  # Process Q2
  q2text = ''
  recordFlag = 0;
  with open(os.path.join(subdir, 'MARKING-UNPARSED-Q2.txt'), 'r') as q2file:
    for line in q2file.read().splitlines():
      if 'Question 2: Modelling Polymorphism in C [' in line:
        recordFlag = 1
        temp_str = line.split('[')[1].split('/')[0]
        q2mark = float(temp_str) if temp_str != '' else None
      elif 'Question 3: Using Function Pointers on Lists [' in line:
        recordFlag = 0

      if recordFlag == 1:
        q2text += line + '\n'
  # print(q2text)

  # Process Q1
  q1text = ''
  if 'marking-scheme-A7-Q1.txt' not in files:
    print('ERROR: marking-scheme-A7-Q1.txt is not in ' + subdir)
  with open(os.path.join(subdir, 'marking-scheme-A7-Q1.txt'), 'r') as q1file:
    q1text = q1file.read()
    temp_str = q1text.split('\n', 1)[0].split('[')[1].split('/')[0]
    q1mark = float(temp_str) if temp_str != '' else None

  # Process Q3
  q3text = ''
  if 'marking-scheme-A7-Q3.txt' not in files:
    print('ERROR: marking-scheme-A7-Q3.txt is not in ' + subdir)
  with open(os.path.join(subdir, 'marking-scheme-A7-Q3.txt'), 'r') as q3file:
    q3text = q3file.read()
    temp_str = q3text.split('\n', 1)[0].split('[')[1].split('/')[0]
    q3mark = float(temp_str) if temp_str != '' else None
    if q3mark is None:
      print('[ERROR!][A7]Q3 marks missing in foler ' + subdir)

  # Process Q4
  q4text = ''
  if 'marking-scheme-A7-Q4.txt' not in files:
    print('ERROR: marking-scheme-A7-Q4.txt is not in ' + subdir)
  with open(os.path.join(subdir, 'marking-scheme-A7-Q4.txt'), 'r') as q4file:
    q4text = q4file.read()
    temp_str = q4text.split('\n', 1)[0].split('[')[1].split('/')[0]
    q4mark = float(temp_str) if temp_str != '' else None

  # Process Q5
  q5text = ''
  if 'marking-scheme-A7-Q5.txt' not in files:
    print('ERROR: marking-scheme-A7-Q5.txt is not in ' + subdir)
  with open(os.path.join(subdir, 'marking-scheme-A7-Q5.txt'), 'r') as q5file:
    q5text = q5file.read()
    temp_str = q5text.split('\n', 1)[0].split('[')[1].split('/')[0]
    q5mark = float(temp_str) if temp_str != '' else None


  totalMarks = q1mark + q2mark + q3mark + q4mark + q5mark

  markingText = "Total before late penalty: [{}/100]\n\n".format(totalMarks)
  markingText += "{}\n\n{}{}\n\n{}\n\n{}".format(q1text,q2text,q3text,q4text,q5text)

  # print(markingText)

  # Create new merged marking file
  # with open(os.path.join(subdir,'MARKING.txt'), 'w') as mrkfile:
  #   mrkfile.write(markingText)
  # if totalMarks < 50:
  #   print('MARK - [a7] ' + str(totalMarks) + ' ' + subdir)

  return totalMarks

# Returns a dictionary with folder csID as index
def parseMark(rootdir = ROOTDIR):
  ret_dict = {}

  for subdir, dirs, files in os.walk(rootdir):
    for file in files:
      if file == 'MARKING-UNPARSED-Q2.txt':
        submitCSid = None
        partnerCSid = None
        mark = None
        sids = []

        # pprint.pprint((os.path.split(subdir)[-1],file))
        submitCSid = os.path.split(subdir)[-1]

        mark = mergeMarks(subdir, files)

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
