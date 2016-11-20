# Automated marking parsing Script
#
# Automatically generate csv for uploading back to the grade center on Connect
#
# Author: Phoenix Song (c.song@alumni.ubc.ca)
# Version: 20161115

import os
import re
import pprint

# Sample rubric object
RUBRIC = {'Q1':{'weight':4 , 'marks':5.0},
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


ROOTDIR = '.'

# Target CSV file to add marks.
CSV_FILENAME = 'gc_SIS.UBC.CPSC.213.101.2016W1.69672_column_2016-10-11-03-04-03.csv'




# Infomation dictionary
student_dict = {};

# Incidents which
no_readme_list = []

# Read and modify .csv file from connect
CSV_FILENAME = 'gc_SIS.UBC.CPSC.213.101.2016W1.69672_column_2016-10-11-03-04-03.csv'

# load up student_dict
for subdir, dirs, files in os.walk(ROOTDIR):
  for file in files:
    if file == 'readme.txt' or file == 'README.txt' or file == 'ReadMe.txt':
      rdmfile = open(os.path.join(subdir, file), 'r')
      stuids = re.findall('\d\d\d\d\d\d\d\d', rdmfile.read())
      rdmfile.close()
      # print(stuids)
      for sid in stuids:
        student_dict[sid] = {'folder' : subdir}
    elif file == 'MARKING.txt':
      if not os.path.exists(os.path.join(subdir, 'README.txt')):
        if not os.path.exists(os.path.join(subdir, 'readme.txt')):
          mrkfile = open(os.path.join(subdir, file), 'r')
          stuids = re.findall('\d\d\d\d\d\d\d\d', mrkfile.read())
          mrkfile.close()
          # print(stuids)
          if not stuids:
            no_readme_list.append(subdir)
          else:
            for sid in stuids:
              student_dict[sid] = {'folder' : subdir}

# pprint.pprint(no_readme_list)
# pprint.pprint(student_dict)
# print('count: ', len(student_dict))


# Compute percentage mark from the rubric
def computePercentageMark(markrec_dict, rubric_dict):
  if sum(markrec_dict.values()) == rubric_dict['FULLMARK']:
    return 100
  total_mark = 0
  for key, value in markrec_dict.items():
    total_mark += round(float("{0:.1f}".format((value/rubric_dict[key]['marks'])*rubric_dict[key]['weight'])))
  return total_mark;


# Parse marks from MARKING.txt
def parseMarking(folderDir, markfile):
  mark = None

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
    mark = computePercentageMark(markrec, RUBRIC_A1)
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
    mark = computePercentageMark(markrec, RUBRIC_A1)
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
    mark = computePercentageMark(markrec, RUBRIC_A1)
    # print(mark)

  else:
    mark = float((markfile.readline().split('['))[1].split('/')[0])
  return mark

# Parse Marks
for sid, student in student_dict.items():
  if os.path.exists(os.path.join(student['folder'], 'MARKING.txt')):
    markfile = open(os.path.join(student['folder'], 'MARKING.txt'), 'r')
    # print(student['folder'])
    mark = parseMarking(student['folder'], markfile)
    # print(mark)
    markfile.close()
    student_dict[sid]['mark'] = mark


# Read and modify .csv file from connect
def recordCsv(inputCsvFile, student_dict):
  inputfile = open(inputCsvFile, 'r')
  outputcsv = open('[marked]' + inputCsvFile, 'w')
  for line in inputfile:
    s = line.split(',')[2][1:-1]
    if s.isdigit():
      if s in student_dict:
        # print(student_dict[s]['mark'])
        line = line.replace(line.split(',')[-1],'"'+ str(student_dict[s]['mark']) + '"\n')
        # print(line)
    outputcsv.write(line)

  inputfile.close()
  outputcsv.close()
  print('Record csv file - ' + '[marked]' + inputCsvFile + ' - Created.')

recordCsv(CSV_FILENAME, student_dict)


# printout processed
pprint.pprint(student_dict)
print('processed count: ', len(student_dict))
# Printout list of students without readme
pprint.pprint(no_readme_list)


