# Automated marking parsing Script
#
# Automatically generate csv for uploading back to the grade center on Connect
#
# Author: Phoenix Song (c.song@alumni.ubc.ca)
# Version: 20161108-a3

import os
import re
import pprint

ROOTDIR = '.'

student_dict = {};

no_readme_list = []

zero_mark_list = []

# Read and modify .csv file from connect
CSV_FILENAME = 'gc_SIS.UBC.CPSC.213.101.2016W1.69672_column_2016-11-08-15-11-10.csv'

# load up student_dict
for subdir, dirs, files in os.walk(ROOTDIR):
  for file in files:
    if file == 'README.txt':
      rdmfile = open(os.path.join(subdir, file), 'r')
      stuids = re.findall('\d\d\d\d\d\d\d\d', rdmfile.read())
      rdmfile.close()
      # print(stuids)
      for sid in stuids:
        student_dict[sid] = {'folder' : subdir}
    elif file == 'MARKING.txt':
      if not os.path.exists(os.path.join(subdir, 'README.txt')):
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

# Parse Marks
for sid, student in student_dict.items():
  if os.path.exists(os.path.join(student['folder'], 'MARKING.txt')):
    markfile = open(os.path.join(student['folder'], 'MARKING.txt'), 'r')
    # print(student['folder'])
    temp_str = (markfile.readline().split('['))[1].split('/')[0]
    # print(temp_str)
    if temp_str == '':
      temp_str = 0
    mark = float(temp_str)
    # print(mark)
    markfile.close()
    
    student_dict[sid]['mark'] = mark
    if mark == 0:
      zero_mark_list.append(student)

# Read and modify .csv file from connect
def recordCsv(inputCsvFile, student_dict):
  inputfile = open(inputCsvFile, 'r')
  outputcsv = open('[marked]' + inputCsvFile, 'w')
  for line in inputfile:
    s = line.split(',')[2][1:-1]
    if s.isdigit():
      if s in student_dict:
        if 'mark' in student_dict[s]:
          # print(student_dict[s]['mark'])
          line = line.replace(line.split(',')[-1],'"'+ str(student_dict[s]['mark']) + '"\n')
          # print(line)
        else:
          print('error!');
          pprint.pprint(student_dict[s])
    outputcsv.write(line)

  inputfile.close()
  outputcsv.close()
  print('Record csv file - ' + '[marked]' + inputCsvFile + ' - Created.')

recordCsv(CSV_FILENAME, student_dict)


# printout processed
pprint.pprint(student_dict)
print('processed count: ', len(student_dict))
# Printout list of students without readme
print('No_readme_list')
pprint.pprint(no_readme_list)
print('Zero_marks:')
pprint.pprint(zero_mark_list)

