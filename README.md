# chromium-prebuild-scripts

### How to use chromium library?

Add following to build.gradle

    aaptOptions {
        noCompress "dat", "pak", "bin"
    }
    
    
