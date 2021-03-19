#!/usr/bin/env python

import os
import re
import sys
import shutil
import helpers.file_helper as FileHelper

def _RemoveNeedlessCodes(manifest_path):
  found_application_block = False
  manifest_path_t = manifest_path + ".tmp"
  with open(manifest_path,'r') as fin:
    with open(manifest_path_t,'w') as fout:
      for line in fin:
        if "<application" in line:
            found_application_block = True

        if found_application_block:
            if ">" in line:
                found_application_block = False
        
        if found_application_block:
            if "android:icon" in line or "android:roundIcon" in line:
                continue

        # Skip category LAUNCHER
        if "android.intent.category.LAUNCHER" in line:
            continue

        fout.write(line)
  shutil.move(manifest_path_t, manifest_path)

def _SetNewManifestPathInGradle(gradle_path, manifest_path):
  gradle_path_t = gradle_path + ".tmp"
  with open(gradle_path,'r') as fin:
    with open(gradle_path_t,'w') as fout:
      for line in fin:
        if "manifest.srcFile" in line:
            found_application_block = True
            fout.write('''            manifest.srcFile "../../../AndroidManifest.xml" 
''')
        else:
            fout.write(line)
  shutil.move(gradle_path_t, gradle_path)

def Process(env):
  print("[process_manifest] start")
  project_dir = env["PROJECT_DIR"]
  gradle_path = env["GRADLE_PATH"]
  
  manifest_src_path = os.path.abspath(os.path.join(project_dir, "../gen/chrome/android/chrome_public_apk/AndroidManifest.xml"))
  manifest_dst_path = os.path.abspath(os.path.join(project_dir, "AndroidManifest.xml"))
  shutil.copyfile(manifest_src_path, manifest_dst_path)

  _RemoveNeedlessCodes(manifest_dst_path)
  _SetNewManifestPathInGradle(gradle_path, manifest_dst_path)

  