[app]

title = Tic-Tac-Toe
package.name = tictactoe
package.domain = org.example

source.dir = .
source.include_exts = py,json,png,jpg,jpeg,kv,atlas
source.exclude_dirs = .git,.github,bin,.buildozer,__pycache__

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 24
android.archs = arm64-v8a

android.accept_sdk_license = True
android.debug_artifact = apk

p4a.bootstrap = sdl2


[buildozer]

log_level = 2
