[app]

# (str) Title of your application
title = TwinkleHub Server Selector

# (str) Package name
package.name = serverselector

# (str) Package domain (needed for android packaging)
package.domain = org.twinklehub

# (list) Source files to include (let it be relative to the dir)
source.include_exts = py,png,jpg,kv,atlas,java,json

# (list) Directory where the source files are stored
source.dir = .

# (str) Application versioning
version = 1.2

# (list) Application requirements
requirements = python3,kivy

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions (для работы системной службы VPN)
android.permissions = INTERNET,ACCESS_NETWORK_STATE,BIND_VPN_SERVICE,FOREGROUND_SERVICE

# (str) Путь к нативным Java-файлам (папка java/org/twinklehub/)
android.add_src = java

# (list) Target architectures
android.archs = arm64-v8a

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug command)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
