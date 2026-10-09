[app]
title = TwinkleHub
package.name = twinklehub
package.domain = org
source.include_exts = py,png,jpg,kv,atlas
source.dir = .
version = 1.0
requirements = python3,kivy,jnius
orientation = portrait
fullscreen = 0

android.permissions = INTERNET, BIND_VPN_SERVICE
android.api = 33
android.min_api = 21
android.ndk = 25b

# Подключаем папку с Java-сервисом
android.add_src = java

android.copy_libs = 1
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
