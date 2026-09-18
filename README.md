# SMART PDF STUDIO – VIP EDITION (Android)

Created by **Moinuddin Chishti**  
**Chishti Bro Computers and Developers**

Android/Kivy port of Smart PDF Studio with the same core PDF toolkit and file utilities as the desktop edition.

## Included

- PDF → Word
- Word → PDF
- Images → PDF
- Merge PDFs
- Split PDF
- Password protect PDF
- Unlock PDF with password
- Temporary-file scan
- Storage overview
- Duplicate finder (SHA-256)
- Extension-based file organizer
- Dark VIP mobile UI
- Offline-first processing

## Important Android notes

Android does not expose the same unrestricted filesystem as Windows. The cleaner and organizer therefore work within the storage locations Android allows the app to access. The app requests legacy storage permissions where supported.

The mobile Word → PDF converter is a basic text renderer. Complex Word documents containing advanced layouts, charts, floating objects, or special fonts may not reproduce exactly like Microsoft Word/LibreOffice.

## Build locally

1. Install Linux/WSL2 and Buildozer.
2. In this folder run:

```bash
pip install buildozer
buildozer android debug
```

3. The APK will be created in `bin/`.

## Build on GitHub

Upload this project to GitHub and open:

**Actions → Smart PDF Studio - Android APK → Run workflow**

After the workflow finishes, open the workflow run and download the artifact named:

`SmartPDFStudio-Android`

The artifact contains the generated `.apk`.

## Project files

- `main.py` – Android GUI/app entry point
- `core/pdf_tools.py` – PDF operations
- `core/file_tools.py` – storage/file utilities
- `buildozer.spec` – Android build configuration
- `app.yml` – app/build feature contract
- `.github/workflows/android-apk.yml` – GitHub Actions APK build
- `LICENSE` – MIT license
