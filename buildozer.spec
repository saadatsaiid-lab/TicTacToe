[app]

# عنوان برنامه
title = Tic Tac Toe

# نام بسته
package.name = tictactoe

# شناسه بسته
package.domain = org.example

# نسخه
version = 1.0.0
version.code = 1

# نیازمندی‌ها
requirements = python3,kivy==2.2.1

# فایل اصلی
source.dir = .
main.py = main.py

# مجوزها
android.permissions = INTERNET

# معماری
android.arch = arm64-v8a

# نسخه‌های اندروید
android.minapi = 21
android.targetsdk = 33

# نام فایل خروجی
android.filenames = TicTacToe.apk

[buildozer]
log_level = 2
warn_on_root = 1
