[app]
# Smart PDF Studio – VIP Edition Android build
# Created by Moinuddin Chishti | Chishti Bro Computers and Developers

package.name = smartpdfstudio
package.domain = com.chishtibro
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,yaml,yml,md,txt
source.exclude_exts = spec
version = 1.0.0
requirements = python3,kivy==2.3.1,pypdf,Pillow,reportlab,python-docx,PyMuPDF
orientation = portrait
fullscreen = 0
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 35
android.minapi = 23
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
