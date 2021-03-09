#!/usr/bin/env python

import os
import re
import sys
import shutil
import helpers.file_helper as FileHelper

unwanted_srcdirs = [
  "../../../../gen/chrome/android/features/keyboard_accessory/factory/public_java/chrome/android/features/keyboard_accessory/factory/java/src",
  "../../../../gen/chrome/browser/download/android/factory_java/chrome/browser/download/internal/android/java/src",
  "../../../../gen/chrome/browser/password_check/android/internal/public_factory_java/chrome/browser/password_check/android/internal/java/src",
  "../../../../gen/chrome/browser/password_check/android/internal/public_ui_factory_java/chrome/browser/password_check/android/internal/java/src",
  "../../../../gen/chrome/browser/ui/android/appmenu/factory_java/chrome/browser/ui/android/appmenu/internal/java/src",
  "../../../../gen/components/browser_ui/android/bottomsheet/factory_java/components/browser_ui/android/bottomsheet/internal/java/src",
]

def _ProcessBuildConfig(work_dir):

  def _Replace(file_path_r, match_string, replace_string):
    file_path = os.path.join(work_dir, file_path_r)
    command = """sed -i -s 's/{}/{}/g' {}""".format(match_string, replace_string, file_path)
    os.system(command)

  os.system('''find ../gen -name BuildConfig.java | grep -v "/chrome_public_apk/" | xargs -i mv {} {}.cp''')
  _Replace("../gen/chrome/android/chrome_public_apk/generated_java/input_srcjars/org/chromium/base/BuildConfig.java", "org.chromium.base.R", "org.chromium.chrome.R")

def Process(env):
  print("[process_java] start")

  gradle_path = env["GRADLE_PATH"]
  work_dir = env["WORK_DIR"]

  for l in unwanted_srcdirs:
    match_text = "\"{}\"".format(l)
    replace_text = "//\"{}\"".format(l)
    if not FileHelper.ContainsLine(gradle_path, replace_text):
      FileHelper.ReplaceText(gradle_path, match_text, replace_text)
  
  _ProcessBuildConfig(work_dir)
