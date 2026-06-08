[app]

# (string) Title of your application
title = My Kivy App

# (string) Package name
package.name = mykivyapp

# (string) Package domain (needed for android packaging)
package.domain = org.abdullah

# (string) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (string) Application version
version = 0.1

# (list) Application requirements
# এখানে hostpython3 যুক্ত করা হয়েছে যেন numpy এবং sympy অ্যান্ড্রয়েডের জন্য নিখুঁতভাবে কম্পাইল হতে পারে
requirements = hostpython3,python3,kivy,numpy,sympy

# (str) Supported orientations (one of landscape, portrait, all or some list of them)
orientation = portrait

# (string) Kivy version to use
osx.kivy_version = 2.1.0

# (int) Fullscreen mode, 0 or 1
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow backup
android.allow_backup = True

# (int) Target Android API
android.api = 34

# (int) Minimum API your APK will support
android.minapi = 21

# (string) Android NDK version to use
android.ndk = 25b

# (bool) Use private storage for data
android.private_storage = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of linking
android.copy_libs = 1

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add gradle/maven dependencies here.
# android.add_jars = foo.jar
