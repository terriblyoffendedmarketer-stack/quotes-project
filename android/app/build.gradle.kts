plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.marginalia"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.marginalia"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "0.1"
    }

    // A fixed key so every build (local or CI) can update the installed app in place.
    // It only signs this personal sideloaded app; it is not a Play Store key.
    signingConfigs {
        create("sideload") {
            storeFile = file("marginalia.keystore")
            storePassword = "marginalia"
            keyAlias = "marginalia"
            keyPassword = "marginalia"
        }
    }

    buildTypes {
        debug {
            signingConfig = signingConfigs.getByName("sideload")
        }
        release {
            isMinifyEnabled = false
            signingConfig = signingConfigs.getByName("sideload")
        }
    }

    // The cards live in writing-examples/content, shared with the web prototype.
    sourceSets["main"].assets.srcDir("../../content")
    androidResources {
        ignoreAssetsPattern = "!*.md:!.*:!*~"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.viewpager2:viewpager2:1.1.0")
    implementation("androidx.recyclerview:recyclerview:1.3.2")
}
