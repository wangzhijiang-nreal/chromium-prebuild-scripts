#!/usr/bin/env python

import os
import re
import sys
import shutil
import helpers.file_helper as FileHelper

res_srcdirs = [
  "../../../../../../chrome/android/feed/core/java/res",
  "../../../../../../chrome/android/java/res",
  "../../../../../../components/browser_ui/settings/android/java/res",
  
  "../../../../gen/components/strings/java/res",
  "../../../../gen/chrome/browser/ui/android/strings/ui_strings_grd_grit_output",
]

extra_res_srcdirs = [
  "../../../../../../third_party/android_media/java/res",
  "../../../../../../third_party/android_data_chart/java/res",
  # "../../../resource_collections/chrome_public_apk_template_resources",
  "../../../../gen/chrome/browser/ui/android/strings/ui_strings_grd_grit_output",# "../../../resource_collections/gen_chrome_browser_ui_android_strings_ui_strings_grd_grit_output",
  "../../../../gen/chrome/java/res",
  "../../../../gen/components/strings/java/res",
  "../../../../gen/components/autofill/android/autofill_strings_grd_grit_output",
  "../../../../gen/components/permissions/android/permissions_strings_grd_grit_output",
  "../../../../gen/components/embedder_support/android/web_contents_delegate_strings_grd_grit_output",
  "../../../../gen/components/browser_ui/strings/android/browser_ui_strings_grd_grit_output",
  "../../../../gen/components/javascript_dialogs/android/javascript_dialogs_strings_grd_grit_output",
  "../../../../gen/chrome/android/features/media_router/java_strings_grd_grit_output",
  "../../../../gen/chrome/android/features/vr/java_strings_grd_grit_output",
  "../../../../gen/chrome/android/features/tab_ui/java_strings_grd_grit_output",
  "../../../../gen/chrome/android/features/keyboard_accessory/internal/java_strings_grd_grit_output",
  "../../../../gen/chrome/android/features/start_surface/internal/java_strings_grd_grit_output",
  # // "../../../../gen/chrome/browser/ui/android/strings/ui_strings_grd_grit_output",
  "../../../../gen/chrome/browser/touch_to_fill/android/internal/java_strings_grd_grit_output",
  "../../../../gen/content/public/android/content_strings_grd_grit_output",
  "../../../../gen/ui/android/ui_strings_grd_grit_output",
#   "../../../resource_collections_v2/ui_locale_string_resources",
]

# Resource zip files relative to work_dir
resource_zip_paths = [
  "../../../../resource_zips/chrome/android/ui_locale_string_resources.zip",
  "../../../../obj/chrome/android/chrome_public_apk_template_resources.resources.zip",
]

def _NewCollectionName(srcdir):
  begin = False
  name = ''
  for c in srcdir:
    if not begin:
      if c.isalnum() or c == '_' or c == '-':
        begin = True
      
    if begin:
      if c == '/':
        name += '_'
      else:
        name += c
  return name

def _AddExtraResource(gradle_path, line_text):
  gradle_path_t = gradle_path + ".tmp"

  with open(gradle_path,'r') as fin:
    line_no = -1
    index = 0
    lines = fin.readlines()
    for line in lines:
      index += 1
      if "res.srcDirs = [" in line:
        line_no = index

    with open(gradle_path_t,'w') as fout:
      index = 0
      for line in lines:
        index += 1
        if index == line_no:
          fout.write(line)
          fout.write("\t\t\t\t" + line_text + os.linesep)
        else:
          fout.write(line)
  shutil.move(gradle_path_t, gradle_path)

def _RemoveDuplicateNames(resource_collections_dir):
  
  def _Rename(file_path_r, match_string):
    replace_string = match_string + "_dup" 
    file_path = os.path.join(resource_collections_dir, file_path_r)
    command = """sed -i -s 's/{}/{}/g' {}""".format(match_string, replace_string, file_path)
    os.system(command)

  def _GetFileNames(file_dir_r):
    file_path_list = []
    file_dir = os.path.join(resource_collections_dir, file_dir_r)
    for root, dirs, files in os.walk(file_dir, topdown=False):
      for name in files:
        file_path = os.path.join(root, name)
        file_path_r = os.path.relpath(file_path, resource_collections_dir)
        file_path_list.append(file_path_r)
    return file_path_list

  _Rename("chrome_android_java_res/values/dimens.xml", "bottom_sheet_min_full_half_distance")
  _Rename("chrome_android_java_res/values/dimens.xml", "bottom_sheet_peek_height")
  _Rename("chrome_android_java_res/values/dimens.xml", "bottom_sheet_toolbar_shadow_height")
  _Rename("chrome_android_java_res/values/dimens.xml", "bottom_sheet_shadow_top_offset")

  _Rename("chrome_android_feed_core_java_res/values/dimens.xml", "text_size_medium")
  _Rename("chrome_android_feed_core_java_res/values/dimens.xml", "text_size_large")

  file_paths = _GetFileNames("gen_chrome_browser_ui_android_strings_ui_strings_grd_grit_output")
  for file_path in file_paths:
    _Rename(file_path, "certtitle")
    _Rename(file_path, "link_copied")
  
  file_paths = _GetFileNames("gen_components_strings_java_res")
  for file_path in file_paths:
    _Rename(file_path, "show")

def _ProcessResourceZip(gradle_dir, gradle_path, resource_collections_dir, resource_zip_path):
  # Unzip resource
  resource_zip_path_ = os.path.abspath(os.path.join(gradle_dir, resource_zip_path))
  resource_zip_name = _NewCollectionName(resource_zip_path) #os.path.basename(resource_zip_path_)
  dst_path = os.path.abspath(os.path.join(resource_collections_dir, resource_zip_name))
  shutil.copy(resource_zip_path_, dst_path)

  unzip_path = os.path.abspath(os.path.join(resource_collections_dir, resource_zip_name))
  unzip_path = unzip_path.replace(".zip", "")
  unzip_path = unzip_path.replace(".", "_")
  
  os.system("unzip -d " + unzip_path + " " + resource_zip_path_ + " >/dev/null")
  os.remove(dst_path)

  unzip_path_r = os.path.relpath(unzip_path, gradle_dir)
 
  if not FileHelper.ContainsLine(gradle_path, unzip_path_r):
      replace_text = "\"{}\",".format(unzip_path_r)
      _AddExtraResource(gradle_path, replace_text)

def Process(env):
  print("[process_resource] start")

  gradle_dir = env["GRADLE_DIR"]
  gradle_path = env["GRADLE_PATH"]
  resource_collections_dir = env["RESOURCE_COLLECTIONS_DIR"]
  work_dir = env["WORK_DIR"]

  # Create resource collections folder
  if os.path.exists(resource_collections_dir):
    shutil.rmtree(resource_collections_dir)
  os.mkdir(resource_collections_dir)

  for resource_zip_path in resource_zip_paths:
    _ProcessResourceZip(gradle_dir, gradle_path, resource_collections_dir, resource_zip_path)

  extra_res_srcdirs.reverse()
  for srcdir in extra_res_srcdirs:
    if not FileHelper.ContainsLine(gradle_path, srcdir):
      replace_text = "\"{}\",".format(srcdir)
      _AddExtraResource(gradle_path, replace_text)

  for srcdir in res_srcdirs:
    print("[process_resource] " + srcdir)
    srcdir_ = os.path.abspath(os.path.join(gradle_dir, srcdir))
    dstdir = os.path.abspath(os.path.join(resource_collections_dir, _NewCollectionName(srcdir)))
    shutil.copytree(srcdir_, dstdir)
    dstdir_r = os.path.relpath(dstdir, gradle_dir)

    # Update build.gradle
    match_text = "\"{}\",".format(srcdir)
    replace_text = "\"{}\",//{}".format(dstdir_r, srcdir)

    if FileHelper.ContainsLine(gradle_path, srcdir):
      FileHelper.ReplaceText(gradle_path, match_text, replace_text)
    else:
      _AddExtraResource(gradle_path, replace_text)

  _RemoveDuplicateNames(resource_collections_dir)
