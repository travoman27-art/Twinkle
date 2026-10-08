[app]

# (str) Title of your application
title = TwinkleHub

# (str) Package name
package.name = twinklehub

# (str) Package domain (needed for android packaging)
package.domain = org

# (str) Source files to include (let it include standard assets)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application source directory
source.dir = .

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,kivy,jnius

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, BIND_VPN_SERVICE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.min_api = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 33

# (str) python-for-android branch to use
p4a.branch = master

# (list) Source files to add to the Android project (Java wrapper for VPN)
android.add_src = java

# (bool) Enable/disable gnu stl shared library
android.copy_libs = 1

# (str) Supported architectures
android.archs = arm64-v8a

[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1
