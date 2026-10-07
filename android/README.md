# Marginalia for Android

## Install (once)

1. On your phone, open this repository's **Releases** page and find **Marginalia (latest)**.
2. Tap `marginalia.apk` to download it, then open it. If Android asks, allow your browser to install apps.
3. Long-press the home screen, choose **Widgets**, find **Marginalia** and drag **Today's line** onto the screen. Make it as big as you like.

New and edited cards arrive by themselves. The app checks this repository for a new `content/cards.json` every few hours, when you open it, and when the widget refreshes. You only reinstall when the app's own code changes. Every build is signed with the same key (`app/marginalia.keystore`, used only for this sideloaded app), so a new version installs over the old one.

## Using it

- **Widget:** tap the right side for the next slide and the left side to go back. **Open ↗** opens the slide full screen. A new card appears just after midnight.
- **App:** swipe sideways through the slides. Previous and Next browse other cards, and the top-right label takes you back to today. You can hide the “Steal it” slide, which also hides it in the widget.

## Build it yourself

You need JDK 17 and the Android SDK.

```
cd android
./gradlew assembleRelease
```
