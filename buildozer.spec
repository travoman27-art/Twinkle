[app]
title = TwinkleHub Server Selector
package.name = serverselector
package.domain = org.twinklehub
source.dir = .
source.include_exts = py,json
version = 1.0
requirements = python3,kivy,sdl2,glew
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.archs = arm64-v8a
android.allow_backup = True
android.api = 33
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
