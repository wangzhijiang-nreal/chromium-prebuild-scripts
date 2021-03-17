#!/usr/bin/env python

import os
import re
import sys
import shutil
import helpers.file_helper as FileHelper

g_play_services_dependencies = """
    implementation 'com.google.android.gms:play-services-auth:17.0.0'
    implementation 'com.google.android.gms:play-services-auth-api-phone:17.1.0'
    implementation 'com.google.android.gms:play-services-auth-base:17.0.0'
    implementation 'com.google.android.gms:play-services-base:17.0.0'
    implementation 'com.google.android.gms:play-services-basement:17.0.0'
    implementation 'com.google.android.gms:play-services-cast:17.0.0'
    implementation 'com.google.android.gms:play-services-cast-framework:17.0.0'
    implementation 'com.google.android.gms:play-services-clearcut:17.0.0'
    implementation 'com.google.android.gms:play-services-fido:18.1.0'
    implementation 'com.google.android.gms:play-services-flags:17.0.0'
    implementation 'com.google.android.gms:play-services-gcm:17.0.0'
    implementation 'com.google.android.gms:play-services-iid:17.0.0'
    implementation 'com.google.android.gms:play-services-instantapps:17.0.0'
    implementation 'com.google.android.gms:play-services-location:17.0.0'
    implementation 'com.google.android.gms:play-services-phenotype:17.0.0'
    implementation 'com.google.android.gms:play-services-places-placereport:17.0.0'
    implementation 'com.google.android.gms:play-services-stats:17.0.0'
    implementation 'com.google.android.gms:play-services-tasks:17.0.0'
    implementation 'com.google.android.gms:play-services-vision:18.0.0'
    implementation 'com.google.android.gms:play-services-vision-common:18.0.0'
"""

g_play_services_dependencies_unused = """
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_auth/play-services-auth-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_auth_api_phone/play-services-auth-api-phone-17.1.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_auth_base/play-services-auth-base-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_base/play-services-base-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_basement/play-services-basement-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_cast/play-services-cast-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_cast_framework/play-services-cast-framework-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_clearcut/play-services-clearcut-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_fido/play-services-fido-18.1.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_flags/play-services-flags-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_gcm/play-services-gcm-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_iid/play-services-iid-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_instantapps/play-services-instantapps-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_location/play-services-location-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_phenotype/play-services-phenotype-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_places_placereport/play-services-places-placereport-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_stats/play-services-stats-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_tasks/play-services-tasks-17.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_vision/play-services-vision-18.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_gms_play_services_vision_common/play-services-vision-common-18.0.0.aar")
"""

g_androidx_dependencies = """
    implementation 'androidx.annotation:annotation:1.1.0'
    implementation 'androidx.activity:activity:1.1.0'
    implementation 'androidx.annotation:annotation-experimental:1.0.0'
    implementation 'androidx.appcompat:appcompat:1.2.0-beta01'
    implementation 'androidx.appcompat:appcompat-resources:1.2.0-beta01'
    implementation 'androidx.arch.core:core-runtime:2.1.0'

    implementation 'androidx.asynclayoutinflater:asynclayoutinflater:1.0.0'
    implementation 'androidx.cardview:cardview:1.0.0'
    implementation 'androidx.coordinatorlayout:coordinatorlayout:1.1.0'
    implementation 'androidx.core:core:1.3.0-beta01'
    implementation 'androidx.cursoradapter:cursoradapter:1.0.0'
    implementation 'androidx.customview:customview:1.0.0'
    implementation 'androidx.documentfile:documentfile:1.0.0'
    implementation 'androidx.drawerlayout:drawerlayout:1.0.0'
    implementation 'androidx.exifinterface:exifinterface:1.0.0'
    implementation 'androidx.fragment:fragment:1.2.5'
    implementation 'androidx.gridlayout:gridlayout:1.0.0'
    implementation 'androidx.interpolator:interpolator:1.0.0'
    implementation 'androidx.leanback:leanback:1.0.0'
    implementation 'androidx.leanback:leanback-preference:1.0.0'
    implementation 'androidx.legacy:legacy-preference-v14:1.0.0'
    implementation 'androidx.legacy:legacy-support-core-ui:1.0.0'
    implementation 'androidx.legacy:legacy-support-core-utils:1.0.0'
    implementation 'androidx.legacy:legacy-support-v13:1.0.0'
    implementation 'androidx.legacy:legacy-support-v4:1.0.0'
    implementation 'androidx.lifecycle:lifecycle-livedata:2.0.0'
    implementation 'androidx.lifecycle:lifecycle-livedata-core:2.2.0'
    implementation 'androidx.lifecycle:lifecycle-runtime:2.2.0'
    implementation 'androidx.lifecycle:lifecycle-viewmodel:2.2.0'
    implementation 'androidx.lifecycle:lifecycle-viewmodel-savedstate:2.2.0'
    implementation 'androidx.loader:loader:1.0.0'
    implementation 'androidx.localbroadcastmanager:localbroadcastmanager:1.0.0'
    implementation 'androidx.media:media:1.0.0'
    implementation 'androidx.mediarouter:mediarouter:1.0.0'
    implementation 'androidx.multidex:multidex:2.0.0'
    implementation 'androidx.palette:palette:1.0.0'
    implementation 'androidx.preference:preference:1.1.1'
    implementation 'androidx.print:print:1.0.0'
    implementation 'androidx.recyclerview:recyclerview:1.1.0'
    implementation 'androidx.savedstate:savedstate:1.0.0'
    implementation 'androidx.slidingpanelayout:slidingpanelayout:1.0.0'
    implementation 'androidx.swiperefreshlayout:swiperefreshlayout:1.0.0'
    androidTestImplementation 'androidx.test:core:1.2.0'
    androidTestImplementation 'androidx.test.espresso:espresso-contrib:3.2.0'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.2.0'
    androidTestImplementation 'androidx.test.espresso:espresso-idling-resource:3.2.0'
    androidTestImplementation 'androidx.test.espresso:espresso-intents:3.2.0'
    androidTestImplementation 'androidx.test.espresso:espresso-web:3.2.0'
    androidTestImplementation 'androidx.test.ext:junit:1.1.1'
    androidTestImplementation 'androidx.test:monitor:1.2.0'
    androidTestImplementation 'androidx.test:rules:1.2.0'
    androidTestImplementation 'androidx.test:runner:1.2.0'
    androidTestImplementation 'androidx.test.uiautomator:uiautomator:2.2.0'
    implementation 'androidx.transition:transition:1.2.0'
    implementation 'androidx.tvprovider:tvprovider:1.0.0'
    implementation 'androidx.vectordrawable:vectordrawable:1.1.0'
    implementation 'androidx.vectordrawable:vectordrawable-animated:1.1.0'
    implementation 'androidx.versionedparcelable:versionedparcelable:1.1.0'
    implementation 'androidx.viewpager2:viewpager2:1.0.0'
    implementation 'androidx.viewpager:viewpager:1.0.0'

"""

g_extra_dependencies = """
    implementation "androidx.annotation:annotation:1.1.0"
    implementation "androidx.collection:collection:1.1.0"
    implementation 'androidx.lifecycle:lifecycle-common:2.2.0'
    // implementation files("../../../../../../third_party/android_deps/libs/androidx_annotation_annotation/annotation-1.1.0.jar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_activity_activity/activity-1.1.0.aar")
    // implementation files("../../../../../../third_party/android_deps/libs/androidx_annotation_annotation_experimental/annotation-experimental-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_appcompat_appcompat/appcompat-1.2.0-beta01.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_appcompat_appcompat_resources/appcompat-resources-1.2.0-beta01.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_arch_core_core_runtime/core-runtime-2.1.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_asynclayoutinflater_asynclayoutinflater/asynclayoutinflater-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_cardview_cardview/cardview-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_coordinatorlayout_coordinatorlayout/coordinatorlayout-1.1.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_core_core/core-1.3.0-beta01.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_cursoradapter_cursoradapter/cursoradapter-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_customview_customview/customview-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_documentfile_documentfile/documentfile-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_drawerlayout_drawerlayout/drawerlayout-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_exifinterface_exifinterface/exifinterface-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_fragment_fragment/fragment-1.2.5.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_gridlayout_gridlayout/gridlayout-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_interpolator_interpolator/interpolator-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_leanback_leanback/leanback-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_leanback_leanback_preference/leanback-preference-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_legacy_legacy_preference_v14/legacy-preference-v14-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_legacy_legacy_support_core_ui/legacy-support-core-ui-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_legacy_legacy_support_core_utils/legacy-support-core-utils-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_legacy_legacy_support_v13/legacy-support-v13-1.0.0.aar")
    // implementation files("../../../../../../third_party/android_deps/libs/androidx_legacy_legacy_support_v4/legacy-support-v4-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_lifecycle_lifecycle_livedata/lifecycle-livedata-2.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_lifecycle_lifecycle_livedata_core/lifecycle-livedata-core-2.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_lifecycle_lifecycle_runtime/lifecycle-runtime-2.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_lifecycle_lifecycle_viewmodel/lifecycle-viewmodel-2.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_lifecycle_lifecycle_viewmodel_savedstate/lifecycle-viewmodel-savedstate-2.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_loader_loader/loader-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_localbroadcastmanager_localbroadcastmanager/localbroadcastmanager-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_media_media/media-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_mediarouter_mediarouter/mediarouter-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_multidex_multidex/multidex-2.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_palette_palette/palette-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_preference_preference/preference-1.1.1.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_print_print/print-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_recyclerview_recyclerview/recyclerview-1.1.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_savedstate_savedstate/savedstate-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_slidingpanelayout_slidingpanelayout/slidingpanelayout-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_swiperefreshlayout_swiperefreshlayout/swiperefreshlayout-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_test_core/core-1.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_test_espresso_espresso_contrib/espresso-contrib-3.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_test_espresso_espresso_core/espresso-core-3.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_test_espresso_espresso_idling_resource/espresso-idling-resource-3.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_test_espresso_espresso_intents/espresso-intents-3.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_test_espresso_espresso_web/espresso-web-3.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_test_ext_junit/junit-1.1.1.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_test_monitor/monitor-1.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_test_rules/rules-1.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_test_runner/runner-1.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_test_uiautomator_uiautomator/uiautomator-2.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_transition_transition/transition-1.2.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_tvprovider_tvprovider/tvprovider-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_vectordrawable_vectordrawable/vectordrawable-1.1.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_vectordrawable_vectordrawable_animated/vectordrawable-animated-1.1.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_versionedparcelable_versionedparcelable/versionedparcelable-1.1.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_viewpager2_viewpager2/viewpager2-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_viewpager_viewpager/viewpager-1.0.0.aar")
    implementation files("../../../../../../third_party/android_deps/libs/com_google_android_material_material/material-1.2.0-alpha06.aar")
    implementation files("../../../../../../third_party/android_deps/libs/javax_annotation_javax_annotation_api/javax.annotation-api-1.3.2.jar")
"""

g_comment_out_dependencies = """
    implementation files("../../../../obj/third_party/android_deps/google_play_services_auth_base_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/google_play_services_auth_api_phone_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/google_play_services_base_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/google_play_services_basement_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/google_play_services_cast_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/google_play_services_iid_java/classes.jar")
	  implementation files("../../../../obj/third_party/android_deps/google_play_services_fido_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/google_play_services_tasks_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/google_play_services_cast_framework_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/google_play_services_vision_java/classes.jar")
	  implementation files("../../../../obj/third_party/android_deps/google_play_services_location_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/google_play_services_vision_common_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/google_play_services_gcm_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_preference_preference_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_gridlayout_gridlayout_java/classes.jar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_lifecycle_lifecycle_common_java8/lifecycle-common-java8-2.0.0.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_recyclerview_recyclerview_java/classes.jar")
    implementation files("../../../../../../third_party/android_deps/libs/com_android_support_support_annotations/support-annotations-28.0.0.jar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_collection_collection/collection-1.1.0.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_appcompat_appcompat_resources_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_lifecycle_lifecycle_viewmodel_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/com_google_android_material_material_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_drawerlayout_drawerlayout_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_lifecycle_lifecycle_runtime_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_asynclayoutinflater_asynclayoutinflater_java/classes.jar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_annotation_annotation/annotation-1.1.0.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_viewpager_viewpager_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_core_core_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_multidex_multidex_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_interpolator_interpolator_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_swiperefreshlayout_swiperefreshlayout_java/classes.jar")
    implementation files("../../../../../../third_party/android_deps/libs/androidx_lifecycle_lifecycle_common/lifecycle-common-2.2.0.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_vectordrawable_vectordrawable_animated_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_fragment_fragment_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_legacy_legacy_support_v13_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_media_media_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_vectordrawable_vectordrawable_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_legacy_legacy_support_core_ui_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_mediarouter_mediarouter_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_cardview_cardview_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_coordinatorlayout_coordinatorlayout_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_legacy_legacy_support_v4_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_customview_customview_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_legacy_legacy_support_core_utils_java/classes.jar")
    implementation files("../../../../obj/third_party/android_deps/androidx_appcompat_appcompat_java/classes.jar")
"""

androidx_settings = """
android.useAndroidX=true
android.enableJetifier=true
"""

def _AddExtraDependencies(gradle_path):
  gradle_path_t = gradle_path + ".tmp"

  lines = g_extra_dependencies.splitlines()
  lines.reverse()
  for line in lines:
    if line and not line.isspace():
      if not FileHelper.ContainsLine(gradle_path, line):
        
        with open(gradle_path,'r') as fin:
          with open(gradle_path_t,'w') as fout:
            for line_in in fin:
              if "dependencies {" in line_in:
                fout.write(line_in)

                # Write extra dependencies to build.gradle
                fout.write(line + os.linesep)
              else:
                fout.write(line_in)
        shutil.move(gradle_path_t, gradle_path)

def _CommentOutDependencies(gradle_path, comment_out_dependencies_content):
  def _PrependComment(s):
    # Find start position of non-whitespace char
    offset = -1
    for i in range(0, len(s)):
      c = s[i]
      if c and not c.isspace():
        offset = i
        break
    
    if offset >= 0:
      return s[:offset] + "//" + s[offset:]
    else:
      return s

  gradle_path_t = gradle_path + ".tmp"    
  comment_out_lines = comment_out_dependencies_content.splitlines()
  comment_out_lines.reverse()
  
  in_dep_block = False
  with open(gradle_path,'r') as fin:
    with open(gradle_path_t,'w') as fout:
      for line in fin:
        if in_dep_block and "}" in line:
          in_dep_block = False

        should_comment_out = False
        if in_dep_block and not line.lstrip().startswith("//"):
          m = re.search(r"\s+implementation\s+files\(\"([^\"]+)\"", line)
          if m:
            depfile = m.group(1)

            for comment_out_line in comment_out_lines:
              if comment_out_line and not comment_out_line.isspace():
                if depfile in comment_out_line:
                  should_comment_out = True
                  break

        if should_comment_out:
          fout.write(_PrependComment(line) + os.linesep)
        else:
          fout.write(line)

        if "dependencies {" in line:
          in_dep_block = True
  shutil.move(gradle_path_t, gradle_path)

def _EnableAndroidX(gradle_properties_path):
  lines = androidx_settings.splitlines()
  lines.reverse()
  for line in lines:
    if line and not line.isspace():
      if not FileHelper.ContainsLine(gradle_properties_path, line):
        FileHelper.AppendLine(gradle_properties_path, os.linesep + line, False)

def _ResolveDuplicateJarNames(work_dir, gradle_dir, gradle_path):

  def _NewJarName(jar_path):
    begin = False
    name = ''
    for c in jar_path:
      if not begin:
        if c.isalnum() or c == '_' or c == '-':
          begin = True
        
      if begin:
        if c == '/':
          name += '_'
        else:
          name += c
    return name
  
  gradle_path_t = gradle_path + ".tmp"
  in_dep_block = False
  libs_dir = os.path.abspath(os.path.join(work_dir, "libs"))

  if os.path.exists(libs_dir):
    shutil.rmtree(libs_dir)
  os.mkdir(libs_dir)

  with open(gradle_path,'r') as fin:
    with open(gradle_path_t,'w') as fout:
      for line in fin:
        if "dependencies {" in line:
          in_dep_block = True
        else:
          if in_dep_block and "}" in line:
            in_dep_block = False
        
        if in_dep_block and re.search(r"\s+implementation\s+", line):
          if not line.lstrip().startswith("//") and "classes.jar" in line:
            m = re.search(r"files\(\"([^\"]+)\"", line)
            jar_path_r = m.group(1)
            jar_path = os.path.abspath(os.path.join(gradle_dir, jar_path_r))
            
            new_jar_path = _NewJarName(jar_path_r)
            new_jar_path = os.path.abspath(os.path.join(libs_dir, new_jar_path))
            new_jar_path_r = os.path.relpath(new_jar_path, gradle_dir)

            if libs_dir not in jar_path:
              shutil.copyfile(jar_path, new_jar_path)

              out_line = '''\timplementation files(\"{}\") // [{}]'''.format(
                new_jar_path_r, jar_path_r
              )
              fout.write(out_line + os.linesep)
              continue
      
        fout.write(line)
  shutil.move(gradle_path_t, gradle_path)

  libs_dir_r = os.path.relpath(libs_dir, gradle_dir)
  in_dep_block = False
  with open(gradle_path,'r') as fin:
    for line in fin:
      if in_dep_block and "}" in line:
        in_dep_block = False
      if in_dep_block:
        m = re.search(r"\s+implementation\s+files\(\"([^\"]+)\"", line)
        if m:
          depfile = m.group(1)

          if libs_dir_r in depfile and ".jar" in depfile:
            m = re.search(r"\[([^\[\]]+)\]", line)
            if m:
              jar_path_r = m.group(1)
              jar_path = os.path.abspath(os.path.join(gradle_dir, jar_path_r))

              depfile_full = os.path.abspath(os.path.join(gradle_dir, depfile))
              shutil.copyfile(jar_path, depfile_full)

      if "dependencies {" in line:
        in_dep_block = True

def _AddPlayServicesDependencies(gradle_path, region_name, extra_dependencies):
  gradle_path_t = gradle_path + ".tmp"
  begin_tag = "// @begin {}".format(region_name)
  end_tag = "// @end {}".format(region_name)

  if FileHelper.ContainsLine(gradle_path, begin_tag):
    in_block = False
    with open(gradle_path, 'r') as fin:
      with open(gradle_path_t,'w') as fout:
        for line in fin:
          if end_tag in line:
            in_block = False

          if not in_block:
            fout.write(line)
          
          if begin_tag in line:
            in_block = True
    shutil.move(gradle_path_t, gradle_path)
  else:
    with open(gradle_path, 'r') as fin:
      with open(gradle_path_t,'w') as fout:
        for line in fin:
          if "dependencies {" in line:
            fout.write(line)
            fout.write("\t" + begin_tag + os.linesep)
            fout.write("\t" + end_tag + os.linesep)
          else:
            fout.write(line)
    shutil.move(gradle_path_t, gradle_path)

  block_lines = []
  in_block = False
  with open(gradle_path, 'r') as fin:
    for line in fin:
      if end_tag in line:
        in_block = False

      if in_block:
        block_lines.append(line)
      
      if begin_tag in line:
        in_block = True

  with open(gradle_path, 'r') as fin:
    with open(gradle_path_t,'w') as fout:
      for line in fin:
        fout.write(line)

        if begin_tag in line:  
          extra_lines = extra_dependencies.splitlines()
          for extra_line in extra_lines:
            if extra_line and not extra_line.isspace():
              
              exists = False
              for block_line in block_lines:
                if extra_line in block_line:
                  exists = True
                  break
              
              if not exists:
                fout.write(extra_line + os.linesep)
  shutil.move(gradle_path_t, gradle_path)

def _AddPackagingOptions(gradle_path):
  if not FileHelper.ContainsRegion(gradle_path, "PackagingOptionsRegion"):
    region_content = """\t// @begin {}\n\t// @end {}\n\t""".format("PackagingOptionsRegion", "PackagingOptionsRegion")
    FileHelper.AddTextBefore(gradle_path, region_content, lambda line: "sourceSets {" in line)

  FileHelper.ReplaceRegion(gradle_path, "PackagingOptionsRegion", 
"""    packagingOptions {
        exclude '/lib/arm64-v8a/libnr_state_provider.so'
        exclude '/lib/arm64-v8a/libnr_nebulaspaceproxy.so'

        exclude '/lib/arm64-v8a/libnr_api.so'
        exclude '/lib/arm64-v8a/libnr_rgb_camera.so'
    }
""")

  if not FileHelper.ContainsRegion(gradle_path, "CompileOnlyRegion"):
    region_content = """\t// @begin {}\n\t// @end {}\n\t""".format("CompileOnlyRegion", "CompileOnlyRegion")
    FileHelper.AddTextAfter(gradle_path, region_content, lambda line: "dependencies {" in line)

  FileHelper.ReplaceRegion(gradle_path, "CompileOnlyRegion", 
"""    compileOnly files("../../../../obj/third_party/nr_sdk/nr_api_java/libs/nrstate-provider.jar")
    compileOnly files("../../../../obj/third_party/nr_sdk/nr_api_java/libs/nebulaspaceproxy.jar")

    compileOnly files("../../../../obj/third_party/nr_sdk/nr_api_java/libs/nrcontroller.jar")
    compileOnly files("../../../../obj/third_party/nr_sdk/nr_api_java/libs/nrdisplay.jar")
    compileOnly files("../../../../obj/third_party/nr_sdk/nr_api_java/libs/framework.jar")
    compileOnly files("../../../../obj/third_party/nr_sdk/nr_api_java/classes.jar")
""")

  _CommentOutDependencies(gradle_path, """
    implementation files("../../../../obj/third_party/nr_sdk/nr_api_java/libs/nrstate-provider.jar")
    implementation files("../../../../obj/third_party/nr_sdk/nr_api_java/libs/nebulaspaceproxy.jar")

    implementation files("../../../../obj/third_party/nr_sdk/nr_api_java/libs/nrcontroller.jar")
    implementation files("../../../../obj/third_party/nr_sdk/nr_api_java/libs/nrdisplay.jar")
    implementation files("../../../../obj/third_party/nr_sdk/nr_api_java/libs/framework.jar")
    implementation files("../../../../obj/third_party/nr_sdk/nr_api_java/classes.jar")
""")

def Process(env):
  print("[dependencies] start")

  gradle_path = env["GRADLE_PATH"]
  project_dir = env["PROJECT_DIR"]
  work_dir = env["WORK_DIR"]
  gradle_dir = env["GRADLE_DIR"]
  gradle_properties_path = os.path.abspath(os.path.join(project_dir, "gradle.properties"))

  _AddExtraDependencies(gradle_path)
  _CommentOutDependencies(gradle_path, g_comment_out_dependencies)
  _EnableAndroidX(gradle_properties_path)
  _AddPackagingOptions(gradle_path)
  _ResolveDuplicateJarNames(work_dir, gradle_dir, gradle_path)

  _AddPlayServicesDependencies(gradle_path, "PlayServices", g_play_services_dependencies)
  
  