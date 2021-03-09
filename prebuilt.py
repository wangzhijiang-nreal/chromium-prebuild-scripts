#!/usr/bin/env python

import os
import sys
import helpers.file_helper as FileHelper

from tasks.dependencies import Process as ProcessDependencies
from tasks.process_r import Process as ProcessR
from tasks.process_resource import Process as ProcessResource
from tasks.process_java import Process as ProcessJava


SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
WORK_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
GRADLE_DIR = os.path.abspath(os.path.join(WORK_DIR, "chrome/android/chrome_public_apk"))
GRADLE_PATH = os.path.abspath(os.path.join(GRADLE_DIR, "build.gradle"))
GRADLE_PROPERTIES_PATH = os.path.abspath(os.path.join(WORK_DIR, "gradle.properties"))
RESOURCE_COLLECTIONS_DIR = os.path.abspath(os.path.join(WORK_DIR, "resource_collections"))
PROJ_GRADLE_PATH = os.path.abspath(os.path.join(WORK_DIR, "build.gradle"))

env = {
  "SCRIPT_PATH" : SCRIPT_PATH,
  "SCRIPT_DIR" : SCRIPT_DIR,
  "WORK_DIR" : WORK_DIR,
  "GRADLE_DIR" : GRADLE_DIR,
  "GRADLE_PATH" : GRADLE_PATH,
  "GRADLE_PROPERTIES_PATH" : GRADLE_PROPERTIES_PATH,
  "RESOURCE_COLLECTIONS_DIR" : RESOURCE_COLLECTIONS_DIR,
  "JAVA_COLLECTIONS_DIR" : os.path.abspath(os.path.join(WORK_DIR, "java_collections")),
  "PROJ_GRADLE_PATH" : PROJ_GRADLE_PATH,
  "PROJECT_DIR" : WORK_DIR,
}

def _FixJVMHeapSpaceExhausted():
  '''Fix issue "Expiring Daemon because JVM heap space is exhausted"

  https://stackoverflow.com/questions/56075455/expiring-daemon-because-jvm-heap-space-is-exhausted
  '''
  def _AddLine(file_path, text):
    if not FileHelper.ContainsLine(file_path, text):
      FileHelper.AppendLine(file_path, text)

  _AddLine(GRADLE_PROPERTIES_PATH, "org.gradle.daemon=true")
  _AddLine(GRADLE_PROPERTIES_PATH, "org.gradle.configureondemand=true")
  _AddLine(GRADLE_PROPERTIES_PATH, "org.gradle.jvmargs=-Xmx4g -XX:MaxPermSize=2048m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8")

  if not FileHelper.ContainsRegion(GRADLE_PATH, "DexOptions"):
    region_content = """\t// @begin {}\n\t// @end {}\n\t""".format("DexOptions", "DexOptions")
    FileHelper.AddTextBefore(GRADLE_PATH, region_content, lambda line: "sourceSets {" in line)

  FileHelper.ReplaceRegion(GRADLE_PATH, "DexOptions", 
"""    dexOptions {
        javaMaxHeapSize "4g"
    }
""")

def _FixGNI_JNI():
  '''Use `find ../gen -name GEN_JNI.java` to view all GEN_JNI.java'''
  os.system('''find ../gen -name GEN_JNI.java | grep -v "/chrome_public_apk/" | xargs -i mv {} {}.cp''')

def _FixNativeLibraries():
  os.system('''find ../gen -name NativeLibraries.java | grep -v "/chrome_public_apk/" | xargs -i mv {} {}.cp''')

def _FixProductConfig():
  os.system('''find ../gen -name ProductConfig.java | grep -v "/chrome_public_apk/" | xargs -i mv {} {}.cp''')

def _FixBuildConfig():
  os.system('''find ../gen -name BuildConfig.java | grep -v "/chrome_public_apk/" | xargs -i mv {} {}.cp''')

def _FixR():
  os.system('''find ../gen/ -name R.java | xargs -i mv {} {}.cp''')

def _SetOutputAsLibrary():
  FileHelper.ReplaceText(GRADLE_PATH, "com.android.application", "com.android.library")
  FileHelper.ReplaceText(GRADLE_PATH, "task.enabled = false", 'task.enabled = true')

  if not FileHelper.ContainsLine(PROJ_GRADLE_PATH, "allprojects"):
    FileHelper.AppendLine(PROJ_GRADLE_PATH, """
allprojects {
    repositories {
        google()
        jcenter()
    }
}
""")

def _ModifyNativeLibrariesFolderName():
  os.system('''mv chrome/android/chrome_public_apk/symlinked-libs/armeabi chrome/android/chrome_public_apk/symlinked-libs/arm64-v8a''')

def main(args):
  _FixJVMHeapSpaceExhausted()
  _FixNativeLibraries()
  _FixGNI_JNI()
  _FixProductConfig()
  _FixR()
  _SetOutputAsLibrary()
  _ModifyNativeLibrariesFolderName()

  ProcessDependencies(env)
  ProcessR(env)
  ProcessResource(env)
  ProcessJava(env)

if __name__ == "__main__":
  main(sys.argv[1:])
