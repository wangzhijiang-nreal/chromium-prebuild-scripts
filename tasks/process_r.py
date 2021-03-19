#!/usr/bin/env python

import os
import re
import sys
import shutil
import helpers.file_helper as FileHelper

# Java source directories relative to GRADLE_DIR
java_srcdirs = [
  "../../../../../../base/android/java/src",
  "../../../../../../chrome/android/features/autofill_assistant/public/java/src",
  "../../../../../../chrome/android/features/dev_ui/internal/java/src",
  "../../../../../../chrome/android/features/dev_ui/public/java/src",
  "../../../../../../chrome/android/features/keyboard_accessory/factory/java/src",
  "../../../../../../chrome/android/features/keyboard_accessory/internal/java/src",
  "../../../../../../chrome/android/features/keyboard_accessory/public/java/src",
  "../../../../../../chrome/android/features/media_router/java/src",
  "../../../../../../chrome/android/features/start_surface/internal/java/src",
  "../../../../../../chrome/android/features/start_surface/public/java/src",
  "../../../../../../chrome/android/features/tab_ui/java/src",
  "../../../../../../chrome/android/features/vr/java/src",
  "../../../../../../chrome/android/feed/core/java/src",
  "../../../../../../chrome/android/java/src",
  "../../../../../../chrome/android/modules/cablev2_authenticator/public/java/src",
  "../../../../../../chrome/android/modules/chime/public/java/src",
  "../../../../../../chrome/android/modules/dev_ui/provider/java/src",
  "../../../../../../chrome/android/modules/extra_icu/provider/java/src",
  "../../../../../../chrome/android/modules/extra_icu/public/java/src",
  "../../../../../../chrome/android/modules/image_editor/provider/java/src",
  "../../../../../../chrome/android/modules/image_editor/public/java/src",
  "../../../../../../chrome/android/modules/stack_unwinder/provider/java/src",
  "../../../../../../chrome/android/modules/stack_unwinder/public/java/src",
  "../../../../../../chrome/android/modules/test_dummy/provider/java/src",
  "../../../../../../chrome/android/modules/test_dummy/public/java/src",
  "../../../../../../chrome/android/third_party/compositor_animator/java/src",
  "../../../../../../chrome/android/webapk/libs/client/src",
  "../../../../../../chrome/android/webapk/libs/common/src",
  "../../../../../../chrome/browser/android/crypto/java/src",
  "../../../../../../chrome/browser/android/lifecycle/java/src",
  "../../../../../../chrome/browser/android/thin_webview/internal/java/src",
  "../../../../../../chrome/browser/android/thin_webview/java/src",
  "../../../../../../chrome/browser/browser_controls/android/java/src",
  "../../../../../../chrome/browser/contextmenu/java/src",
  "../../../../../../chrome/browser/download/android/java/src",
  "../../../../../../chrome/browser/download/internal/android/java/src",
  "../../../../../../chrome/browser/engagement/android/java/src",
  "../../../../../../chrome/browser/enterprise/util/android/java/src",
  "../../../../../../chrome/browser/flags/android/java/src",
  "../../../../../../chrome/browser/fullscreen/android/java/src",
  "../../../../../../chrome/browser/image_editor/public/android/java/src",
  "../../../../../../chrome/browser/image_fetcher/android/java/src",
  "../../../../../../chrome/browser/notifications/chime/android/java/src",
  "../../../../../../chrome/browser/offline_pages/android/java/src",
  "../../../../../../chrome/browser/optimization_guide/android/java/src",
  "../../../../../../chrome/browser/paint_preview/android/java/src",
  "../../../../../../chrome/browser/password_check/android/internal/java/src",
  "../../../../../../chrome/browser/password_check/android/java/src",
  "../../../../../../chrome/browser/performance_hints/android/java/src",
  "../../../../../../chrome/browser/preferences/android/java/src",
  "../../../../../../chrome/browser/profiles/android/java/src",
  "../../../../../../chrome/browser/safe_browsing/android/java/src",
  "../../../../../../chrome/browser/safety_check/android/java/src",
  "../../../../../../chrome/browser/settings/android/java/src",
  "../../../../../../chrome/browser/share/android/java/src",
  "../../../../../../chrome/browser/tab/java/src",
  "../../../../../../chrome/browser/tabmodel/android/java/src",
  "../../../../../../chrome/browser/tabpersistence/android/java/src",
  "../../../../../../chrome/browser/test_dummy/android/java/src",
  "../../../../../../chrome/browser/test_dummy/internal/android/java/src",
  "../../../../../../chrome/browser/thumbnail/generator/android/java/src",
  "../../../../../../chrome/browser/touch_to_fill/android/internal/java/src",
  "../../../../../../chrome/browser/touch_to_fill/android/java/src",
  "../../../../../../chrome/browser/ui/android/appmenu/internal/java/src",
  "../../../../../../chrome/browser/ui/android/appmenu/java/src",
  "../../../../../../chrome/browser/ui/android/default_browser_promo/java/src",
  "../../../../../../chrome/browser/ui/android/favicon/java/src",
  "../../../../../../chrome/browser/ui/android/native_page/java/src",
  "../../../../../../chrome/browser/ui/messages/android/java/src",
  "../../../../../../chrome/browser/util/android/java/src",
  "../../../../../../chrome/browser/xsurface/android/java/src",
  "../../../../../../components/autofill/android/java/src",
  "../../../../../../components/background_task_scheduler/android/java/src",
  "../../../../../../components/background_task_scheduler/internal/android/java/src",
  "../../../../../../components/bookmarks/common/android/java/src",
  "../../../../../../components/browser_ui/android/bottomsheet/internal/java/src",
  "../../../../../../components/browser_ui/android/bottomsheet/java/src",
  "../../../../../../components/browser_ui/banners/android/java/src",
  "../../../../../../components/browser_ui/client_certificate/android/java/src",
  "../../../../../../components/browser_ui/http_auth/android/java/src",
  "../../../../../../components/browser_ui/media/android/java/src",
  "../../../../../../components/browser_ui/modaldialog/android/java/src",
  "../../../../../../components/browser_ui/notifications/android/java/src",
  "../../../../../../components/browser_ui/settings/android/java/src",
  "../../../../../../components/browser_ui/settings/android/widget/java/src",
  "../../../../../../components/browser_ui/share/android/java/src",
  "../../../../../../components/browser_ui/site_settings/android/java/src",
  "../../../../../../components/browser_ui/styles/android/java/src",
  "../../../../../../components/browser_ui/util/android/java/src",
  "../../../../../../components/browser_ui/webshare/android/java/src",
  "../../../../../../components/browser_ui/widget/android/java/src",
  "../../../../../../components/content_capture/android/java/src",
  "../../../../../../components/content_settings/android/java/src",
  "../../../../../../components/crash/android/java/src",
  "../../../../../../components/dom_distiller/content/browser/android/java/src",
  "../../../../../../components/dom_distiller/core/android/java/src",
  "../../../../../../components/download/internal/background_service/android/java/src",
  "../../../../../../components/download/internal/common/android/java/src",
  "../../../../../../components/download/network/android/java/src",
  "../../../../../../components/embedder_support/android/java/src",
  "../../../../../../components/external_intents/android/java/src",
  "../../../../../../components/feature_engagement/internal/android/java/src",
  "../../../../../../components/feature_engagement/public/android/java/src",
  "../../../../../../components/find_in_page/android/java/src",
  "../../../../../../components/gcm_driver/android/java/src",
  "../../../../../../components/gcm_driver/instance_id/android/java/src",
  "../../../../../../components/infobars/android/java/src",
  "../../../../../../components/javascript_dialogs/android/java/src",
  "../../../../../../components/language/android/java/src",
  "../../../../../../components/location/android/java/src",
  "../../../../../../components/minidump_uploader/android/java/src",
  "../../../../../../components/module_installer/android/java/src",
  "../../../../../../components/navigation_interception/android/java/src",
  "../../../../../../components/offline_items_collection/core/android/java/src",
  "../../../../../../components/omnibox/browser/android/java/src",
  "../../../../../../components/page_info/android/java/src",
  "../../../../../../components/paint_preview/browser/android/java/src",
  "../../../../../../components/paint_preview/player/android/java/src",
  "../../../../../../components/payments/content/android/java/src",
  "../../../../../../components/permissions/android/java/src",
  "../../../../../../components/policy/android/java/src",
  "../../../../../../components/prefs/android/java/src",
  "../../../../../../components/query_tiles/android/java/src",
  "../../../../../../components/safe_browsing/android/java/src",
  "../../../../../../components/search_engines/android/java/src",
  "../../../../../../components/security_interstitials/content/android/java/src",
  "../../../../../../components/security_state/content/android/java/src",
  "../../../../../../components/signin/core/browser/android/java/src",
  "../../../../../../components/signin/public/android/java/src",
  "../../../../../../components/spellcheck/browser/android/java/src",
  "../../../../../../components/subresource_filter/android/java/src",
  "../../../../../../components/sync/android/java/src",
  "../../../../../../components/translate/content/android/java/src",
  "../../../../../../components/url_formatter/android/java/src",
  "../../../../../../components/user_prefs/android/java/src",
  "../../../../../../components/variations/android/java/src",
  "../../../../../../components/version_info/android/java/src",
  "../../../../../../components/viz/common/java/src",
  "../../../../../../components/viz/service/java/src",
  "../../../../../../components/webapk/android/libs/client/src",
  "../../../../../../components/webapk/android/libs/common/src",
  "../../../../../../components/webrtc/android/java/src",
  "../../../../../../content/public/android/java/src",
  "../../../../../../device/bluetooth/android/java/src",
  "../../../../../../device/gamepad/android/java/src",
  "../../../../../../device/vr/android/java/src",
  "../../../../../../media/base/android/java/src",
  "../../../../../../media/capture/content/android/java/src",
  "../../../../../../media/capture/video/android/java/src",
  "../../../../../../media/midi/java/src",
  "../../../../../../mojo/public/java/base/src",
  "../../../../../../mojo/public/java/bindings/src",
  "../../../../../../mojo/public/java/system/src",
  "../../../../../../net/android/java/src",

  "../../../../../../printing/android/java/src",
  "../../../../../../services/data_decoder/public/cpp/android/java/src",
  "../../../../../../services/device/android/java/src",
  "../../../../../../services/device/battery/android/java/src",
  "../../../../../../services/device/generic_sensor/android/java/src",
  "../../../../../../services/device/geolocation/android/java/src",
  "../../../../../../services/device/nfc/android/java/src",
  "../../../../../../services/device/public/java/src",
  "../../../../../../services/device/screen_orientation/android/java/src",
  "../../../../../../services/device/time_zone_monitor/android/java/src",
  "../../../../../../services/device/usb/android/java/src",
  "../../../../../../services/device/vibration/android/java/src",
  "../../../../../../services/device/wake_lock/power_save_blocker/android/java/src",
  "../../../../../../services/media_session/public/cpp/android/java/src",
  "../../../../../../services/service_manager/public/java/src",
  "../../../../../../services/shape_detection/android/java/src",
  "../../../../../../third_party/android_data_chart/java/src",
  "../../../../../../third_party/android_media/java/src",
  "../../../../../../third_party/android_protobuf/src/java/src/device/main/java",
  "../../../../../../third_party/android_protobuf/src/java/src/main/java",
  "../../../../../../third_party/android_provider/java/src",
  "../../../../../../third_party/android_sdk/androidx_browser/src/browser/browser/src/main/java",
  "../../../../../../third_party/android_swipe_refresh/java/src",
  "../../../../../../third_party/cacheinvalidation/src/java",
  "../../../../../../third_party/gif_player/src",
  "../../../../../../url/android/java/src",
  "../../../../../../ui/android/java/src",

  "../../../../gen/chrome/android/app_hooks_java/generated_java",
  "../../../../gen/chrome/android/chrome_java/generated_java",
  "../../../../gen/chrome/android/chrome_public_apk/generated_java",
  "../../../../gen/chrome/android/critical_persisted_tab_data_proto_java/generated_java",
  "../../../../gen/chrome/android/features/dev_ui/java/generated_java",
  "../../../../gen/chrome/android/features/dev_ui/public/java/generated_java",
  "../../../../gen/chrome/android/features/keyboard_accessory/factory/internal_java/generated_java",
  #"../../../../gen/chrome/android/features/keyboard_accessory/factory/public_java/chrome/android/features/keyboard_accessory/factory/java/src",
  "../../../../gen/chrome/android/features/keyboard_accessory/factory/public_java/generated_java",
  "../../../../gen/chrome/android/features/keyboard_accessory/internal/internal_java/generated_java",
  "../../../../gen/chrome/android/features/keyboard_accessory/public/public_java/generated_java",
  "../../../../gen/chrome/android/features/media_router/java/generated_java",
  "../../../../gen/chrome/android/features/start_surface/internal/java/generated_java",
  "../../../../gen/chrome/android/features/tab_ui/java/generated_java",
  "../../../../gen/chrome/android/features/tab_ui/module_desc_java/generated_java",
  "../../../../gen/chrome/android/features/vr/java/generated_java",
  "../../../../gen/chrome/android/modules/cablev2_authenticator/public/java/generated_java",
  "../../../../gen/chrome/android/modules/chime/public/java/generated_java",
  "../../../../gen/chrome/android/modules/dev_ui/provider/java/generated_java",
  "../../../../gen/chrome/android/modules/extra_icu/provider/java/generated_java",
  "../../../../gen/chrome/android/modules/extra_icu/public/java/generated_java",
  "../../../../gen/chrome/android/modules/image_editor/provider/java/generated_java",
  "../../../../gen/chrome/android/modules/image_editor/public/java/generated_java",
  "../../../../gen/chrome/android/modules/stack_unwinder/provider/java/generated_java",
  "../../../../gen/chrome/android/modules/stack_unwinder/public/java/generated_java",
  "../../../../gen/chrome/android/modules/test_dummy/provider/java/generated_java",
  "../../../../gen/chrome/android/modules/test_dummy/public/java/generated_java",
  "../../../../gen/chrome/android/partner_location_descriptor_proto_java/generated_java",
  "../../../../gen/chrome/android/templates",
  "../../../../gen/chrome/android/third_party/compositor_animator/compositor_animator_java/generated_java",
  "../../../../gen/chrome/android/update_proto_java/generated_java",
  "../../../../gen/chrome/android/usage_stats_proto_java/generated_java",
  "../../../../gen/chrome/android/webapk/libs/client/client_java/generated_java",
  "../../../../gen/chrome/android/webapk/libs/common/common_java/generated_java",
  "../../../../gen/chrome/android/webapk/libs/common/splash_java/generated_java",
  "../../../../gen/chrome/android/webapk/libs/runtime_library/webapk_service_aidl_java/generated_java",
]

test_java_srcdirs = [
  "../../../../../../ui/android/java/src",
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

def _ReplaceRJavaPackageName(dstdir, package_name):
  r_class_name = "{package_name}.R".format(package_name = package_name)
  import_clause = "import {package_name}.R;".format(package_name = package_name)
  import_clause_search_pattern = r"import\s+({package_name}.*\.R)([^a-zA-Z0-9_]|$)"
  import_clause_search_pattern = import_clause_search_pattern.format(package_name = package_name.replace(".", r"\."))

  for root, dirs, files in os.walk(dstdir, topdown=False):
    for name in files:
      filename = os.path.join(root, name)
      tmpname = os.path.join(root, name + ".tmp")
      with open(filename,'r') as fin:
        with open(tmpname, "w") as fout:
          for line in fin:
            line_ = re.sub(r"(org\.chromium.*\.R)([^a-zA-Z0-9_]|$)", lambda m: r_class_name + m.group(2), line)
            fout.write(line_)
      shutil.move(tmpname, filename)

      # Add import clause
      has_import_clause = False
      with open(filename, 'r') as f:
        for line in f:
          if re.search(import_clause_search_pattern, line):
            has_import_clause = True

      if not has_import_clause:
        with open(filename, 'r') as fin:
          with open(tmpname, "w") as fout:
            for line in fin:
              if not has_import_clause:
                if re.search(r"package\s+", line):
                  fout.write(line)
                  fout.write(import_clause + os.linesep)
                  has_import_clause = True
              else:
                fout.write(line)
        shutil.move(tmpname, filename)

def _ReplaceJavaSrcDir(gradle_path, srcdir, dstdir_r):
  gradle_path_t = gradle_path + ".tmp"
  with open(gradle_path, 'r') as fin:
    with open(gradle_path_t, "w") as fout:
      for line in fin:
        if ("\"" + srcdir + "\"") in line or ("\'" + srcdir + "\'") in line :
          line_ = line.replace(srcdir, dstdir_r, 1)
          line_ = line_.rstrip(os.linesep)

          offset = line_.find("//")
          if offset >= 0:
            line_ = line_[:offset]
          line_ += " //" + srcdir
          line_ += os.linesep
          fout.write(line_)
        else:
          fout.write(line)
  shutil.move(gradle_path_t, gradle_path)

def _FixIntDefNotFoundIssue(java_collections_dir):
  java_srcfiles = [
      "chrome_android_java_src/org/chromium/chrome/browser/customtabs/content/CustomTabActivityNavigationController.java",
      "chrome_android_features_keyboard_accessory_internal_java_src/org/chromium/chrome/browser/keyboard_accessory/ManualFillingProperties.java",
      "chrome_android_features_tab_ui_java_src/org/chromium/chrome/browser/tasks/tab_management/TabListModel.java",
      "chrome_android_features_tab_ui_java_src/org/chromium/chrome/browser/tasks/TrendyTermsCoordinator.java",
  ]

  for file_path_r in java_srcfiles:
    file_path = os.path.join(java_collections_dir, file_path_r)
    if os.path.exists(file_path):
        FileHelper.ReplaceText(file_path, "@IntDef(", "//@IntDef(")
        FileHelper.ReplaceText(file_path, "@Retention(", "//@Retention(")
        FileHelper.ReplaceText(file_path, "FLOATING_SHEET})", "//FLOATING_SHEET})")

def Process(env):
  print("[process_r] start")
  
  java_collections_dir = env["JAVA_COLLECTIONS_DIR"]
  gradle_dir = env["GRADLE_DIR"]
  gradle_path = env["GRADLE_PATH"]
  package_name = env["PACKAGE_NAME"]

  if os.path.exists(java_collections_dir):
    shutil.rmtree(java_collections_dir)
  os.mkdir(java_collections_dir)

  for srcdir in java_srcdirs:
    print("[process_r] " + srcdir)
    
    srcdir_ = os.path.abspath(os.path.join(gradle_dir, srcdir))
    dstdir = os.path.abspath(os.path.join(java_collections_dir, _NewCollectionName(srcdir)))
    shutil.copytree(srcdir_, dstdir)

    _ReplaceRJavaPackageName(dstdir, package_name)

    dstdir_r = os.path.relpath(dstdir, gradle_dir)
    _ReplaceJavaSrcDir(gradle_path, srcdir, dstdir_r)

  _FixIntDefNotFoundIssue(java_collections_dir)
