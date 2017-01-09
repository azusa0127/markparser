#!/usr/bin/env python3

# Handback file generating Script
#
# Automatically generate handbacks according to MARKING.txt
#
# Author: Phoenix Song (c.song@alumni.ubc.ca)
# Environment: python >= 3.4 / 2.7.8
# Version: 20161230-Documented
#
# License: APACHE LICENSE, VERSION 2.0
#          http://www.apache.org/licenses/LICENSE-2.0

import os
import re
import shutil

# The root folder where the marked a1~a9 folders are stored
ASSIGNMENTS_ROOT = '/home/c/cs213/git/grading/'
# The folder to store handbacks
HANDBACK_FOLDER = './handback/'
# Assignments folder name patterns in regular-expresion
ASSIGNMENTS_RE = '/a[1-9]/'
# Making filename, file that used for handback
MARKING_FILENAME = 'MARKING.txt'

# Determine the csIDs
#
# Argument:
#   folder - path string that ends with csid
# Returns:
#   a list of 0~2 csid strings
def getCSIDs(folder):
  assert(os.path.isdir(folder))
  retlist = []
  retlist.append(os.path.split(folder)[-1])

  if os.path.isfile(os.path.join(folder,'PARTNER.txt')):
    with open(os.path.join(folder, 'PARTNER.txt'), 'r') as ptnfile:
      text = re.findall('[a-z][0-9][a-z][0-9][a-z]?', ptnfile.read().lower())
      if len(text) > 0 and text[0] != os.path.split(folder)[-1]:
        retlist.append(text[0])

  return retlist

# Generate Handbacks
#
# Argument:
#   folder - path string that contains the folder owner csid
# Returns:
#   a list of 0~2 csid strings
def generateHandbacks(handback_folder=HANDBACK_FOLDER):
  root = os.path.abspath(handback_folder)

  for subdir, dirs, files in os.walk(ASSIGNMENTS_ROOT):
    for file in files:
      if file == MARKING_FILENAME:
        assignment_name = re.findall(ASSIGNMENTS_RE, subdir)[0][1:-1]
        assignment_handback_dir = os.path.join(root, assignment_name)
        if not os.path.isdir(assignment_handback_dir):
          os.makedirs(assignment_handback_dir,0o700)
        for csid in getCSIDs(subdir):
          shutil.copyfile(os.path.join(subdir, MARKING_FILENAME),
                          os.path.join(assignment_handback_dir,
                            "{}_marking_{}.txt".format(assignment_name,csid)))
  print('Done!')

generateHandbacks()
