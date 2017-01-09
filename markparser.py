# Automated mark parsing Script
#
# Automatically generate csv for uploading back to the grade center on Connect
#
# Author: Phoenix Song (c.song@alumni.ubc.ca)
# Version: 20161228-all-assignments-handback

import a1.parsingmodule as a1
import a2.parsingmodule as a2
import a3.parsingmodule as a3
import a4.parsingmodule as a4
import a5.parsingmodule as a5
import a6.parsingmodule as a6
import a7.parsingmodule as a7
import a8.parsingmodule as a8
import a9.parsingmodule as a9

connect_records = {}
CSID_SID_MAPPING = {}

# ====================================================
# Record build
# ====================================================
# CSV_File from connect
CSV_FILENAME = 'gc_SIS.UBC.CPSC.213.101.2016W1.69672_fullgc_2016-12-23-12-20-39.csv'

# Load connect records from the csv file
with open(CSV_FILENAME, 'r') as input_csv:
  # read table headers.
  ignored = input_csv.readline()[:-33]
  # print(TABLE_HEADER)
  for line in input_csv:
    texts = line.split(',')
    # pprint.pprint(texts)
    connect_records[texts[2][1:-1]] = { 'lastname':texts[0][1:-1],
                                        'firstname':texts[1][1:-1],
                                        'sid':texts[2][1:-1],
                                        'availability':texts[3][1:-1],
                                        'username':texts[4][1:-1],
                                        'weighted_total':texts[5][1:-1],
                                        'total':texts[6][1:-1],
                                        'lab':texts[7][1:-1],
                                        'a1':texts[8][1:-1],
                                        'a2':texts[9][1:-1],
                                        'mt1':texts[10][1:-1],
                                        'a3':texts[11][1:-1],
                                        'a5':texts[12][1:-1],
                                        'a6':texts[13][1:-1],
                                        'mt2':texts[14][1:-1],
                                        'a4':texts[15][1:-1],
                                        'final':texts[16][1:-1],
                                        'attendance':texts[17][1:-1],
                                        'a7':texts[18][1:-1],
                                        'a8':texts[19][1:-1],
                                        'a9':texts[20][1:-1],}
# pprint.pprint(connect_records)


# Load csid-sid mapping
with open('213.csv', 'r') as mapping_file:
  mapping_file.readline()
  for line in mapping_file:
    CSID_SID_MAPPING[line.split(',')[1][:-1]] = line.split(',')[0]
# pprint.pprint(CSID_SID_MAPPING)

# Generate a new csv from the record updated.
def buildCSVfile(OUTPUT_FILENAME):
  with open(OUTPUT_FILENAME, 'w') as output_csv:
    TABLE_HEADER = '''Username,Assignment 1 [Total Pts: 100] |1402785,Assignment 2 [Total Pts: 100] |1403751,Assignment 3 [Total Pts: 100] |1413726,Assignment 4 [Total Pts: 100] |1423936,Assignment 5 [Total Pts: 100] |1415137,Assignment 6 [Total Pts: 100] |1415229,Assignment 7 [Total Pts: 100] |1448794,Assignment 8 [Total Pts: 100] |1448795,Assignment 9 [Total Pts: 100] |1448796,Midterm 1 [Total Pts: 100] |1404420,Midterm 2 [Total Pts: 100] |1415988,Final Exam [Total Pts: 100] |1447465,Attendance Score [Total Pts: 100] |1448569\n'''
    output_csv.write(TABLE_HEADER)
    for student in connect_records:
      line = '"' + connect_records[student]['username'] + '",'
      line += '"' + connect_records[student]['a1'] + '",'
      line += '"' + connect_records[student]['a2'] + '",'
      line += '"' + connect_records[student]['a3'] + '",'
      line += '"' + connect_records[student]['a4'] + '",'
      line += '"' + connect_records[student]['a5'] + '",'
      line += '"' + connect_records[student]['a6'] + '",'
      line += '"' + connect_records[student]['a7'] + '",'
      line += '"' + connect_records[student]['a8'] + '",'
      line += '"' + connect_records[student]['a9'] + '",'
      line += '"' + connect_records[student]['mt1'] + '",'
      line += '"' + connect_records[student]['mt2'] + '",'
      line += '"' + connect_records[student]['final'] + '",'
      line += '"' + connect_records[student]['attendance'] + '"\n'
      output_csv.write(line)

def updateHigherMark(sid, newMark, assignment_index, submitCSid):
  if sid in connect_records:
    if connect_records[sid][assignment_index] == '' or float(connect_records[sid][assignment_index]) < newMark:
      connect_records[sid][assignment_index] = str(newMark)
  else:
    print('WARNING: [' + sid + '][mark:' + str(newMark) +'] is not in connect_records dict. Submitted by [' + submitCSid + ']')

def updateHelper(module_ret_dict, connect_records_key):
  for k,v in module_ret_dict.items():
    csid = v['submitCSid']
    ptnid = v['partnerCSid']
    sids = v['sids']
    mark = v['mark']

    if csid in CSID_SID_MAPPING:
      sid = CSID_SID_MAPPING[csid]
      updateHigherMark(sid, mark, connect_records_key, csid)

      ptnsid = next(iter(filter(lambda x: x != sid,sids)), None)
      if ptnsid is None or ptnsid not in connect_records:
        if ptnsid is not None and ptnid in CSID_SID_MAPPING:
          ptnsid = CSID_SID_MAPPING[ptnid]

      if ptnsid is not None:
        updateHigherMark(ptnsid, mark, connect_records_key, csid)

    else:
      print('['+ connect_records_key +'] Notice: ' + csid + ' is not in mapping list')

# Update connect_record for each assignments.
def updateRecords():
  # a1
  updateHelper(a1.parseMark(), 'a1')
  # a2
  updateHelper(a2.parseMark(), 'a2')
  # a3
  updateHelper(a3.parseMark(), 'a3')
  # a4
  updateHelper(a4.parseMark(), 'a4')
  # a5
  updateHelper(a5.parseMark(), 'a5')
  # a6
  updateHelper(a6.parseMark(), 'a6')
  # a7
  updateHelper(a7.parseMark(), 'a7')
  # a8
  updateHelper(a8.parseMark(), 'a8')
  # a9
  updateHelper(a9.parseMark(), 'a9')

updateRecords()
buildCSVfile('[MARKED]' + CSV_FILENAME)
