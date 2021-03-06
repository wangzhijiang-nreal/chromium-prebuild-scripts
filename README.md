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
    
    $ autoninja -C out/Default chrome_public_apk

Generate gradle project:

    $ build/android/gradle/generate_gradle.py --output-directory out/Debug \
        --target //chrome/android:chrome_public_apk \
        --project-dir out/Default/nreal
        
Run prebuilt.py task before building gradle project

    $ cd out/Default/nreal
    $ git clone <git-url> scripts
    $ python scripts/prebuilt.py
    
### Use custom package name

1. Enter //chrome/android/BUILD.gn and modify *_default_package*.
2. Update ChromeBrowserProvider.java 

    private static String contextGetPackageName() {
        return "ai.nreal.chromium"; // package name
    }

3. Update prebuilt.py

    PACKAGE_NAME = "ai.nreal.chromium"

### How to use chromium library?

Add following to build.gradle

    aaptOptions {
        noCompress "dat", "pak", "bin"
    }
    
    
