# chromium-prebuild-scripts

Make sure you have followed [android build instructions](https://chromium.googlesource.com/chromium/src/+/master/docs/android_build_instructions.md) already.

    $ gn args out/Default
    
    target_os = "android"
    target_cpu = "arm64"
    is_component_build = true
    symbol_level = 0
    blink_symbol_level = 0
    is_debug = false
    is_java_debug = false
    dcheck_always_on = true
    disable_android_lint = true
    enable_nacl = false

Generate gradle project:

    $ build/android/gradle/generate_gradle.py --output-directory out/Debug \
        --target //chrome/android:chrome_public_apk \
        --project-dir out/Debug/nreal

### How to use chromium library?

Add following to build.gradle

    aaptOptions {
        noCompress "dat", "pak", "bin"
    }
    
    
