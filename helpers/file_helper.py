#!/usr/bin/env python

import os
import shutil

def ContainsLine(file_path, line_text):
  with open(file_path,'r') as fin:
    for line in fin:
      if line_text in line:
        return True
  return False
 
def AppendLine(file_path, line_text, new_line=True):
  with open(file_path, "a") as fout:
    if new_line:
      fout.write(line_text + os.linesep)
    else:
      fout.write(line_text)

def ReplaceText(file_path, match_text, replace_text):
  file_path_t = file_path + ".tmp"
  with open(file_path, 'r') as fin:
    with open(file_path_t, "w") as fout:
      for line in fin:
        if match_text in line:
          fout.write(line.replace(match_text, replace_text, 1))
        else:
          fout.write(line)
  shutil.move(file_path_t, file_path)

def AddTextBefore(file_path, text, match_fn):
  file_path_t = file_path + ".tmp"

  with open(file_path,'r') as fin:
    with open(file_path_t,'w') as fout:
      for line in fin:
        if match_fn(line):
          fout.write(text + os.linesep)
          fout.write(line)
        else:
          fout.write(line)
  shutil.move(file_path_t, file_path)

def ContainsRegion(file_path, region_name):
  begin_tag = "// @begin {}".format(region_name)
  return ContainsLine(file_path, begin_tag)

def ReplaceRegion(file_path, region_name, region_content):
  file_path_t = file_path + ".tmp"
  begin_tag = "// @begin {}".format(region_name)
  end_tag = "// @end {}".format(region_name)

  if not ContainsLine(file_path, begin_tag):
    return False
  
  # Clear the region content
  in_block = False
  with open(file_path, 'r') as fin:
    with open(file_path_t,'w') as fout:
      for line in fin:
        if end_tag in line:
          in_block = False

        if not in_block:
          fout.write(line)
          
        if begin_tag in line:
          in_block = True
  shutil.move(file_path_t, file_path)

  with open(file_path, 'r') as fin:
    with open(file_path_t,'w') as fout:
      for line in fin:
        fout.write(line)

        if begin_tag in line:
          fout.write(region_content)
  shutil.move(file_path_t, file_path)