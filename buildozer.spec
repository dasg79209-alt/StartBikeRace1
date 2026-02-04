[app]
title = Start Bike Race
package.name = bike_race
package.domain = org.gopal
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3
version = 0.1
requirements = python3,kivy

orientation = portrait
fullscreen = 1
android.archs = armeabi-v7a, arm64-v8a

# এটি খুব গুরুত্বপূর্ণ (API 33 অ্যান্ড্রয়েড ১৩ এর জন্য)
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.accept_sdk_license = True

# আপনার গেমের জন্য পারমিশন
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# বিল্ড করার সময় যাতে গিটহাব আটকে না যায়
android.skip_update = False
android.warn_on_root = False