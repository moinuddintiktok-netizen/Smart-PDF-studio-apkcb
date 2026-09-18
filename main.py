from kivy.app import App
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.utils import platform
from pathlib import Path
import threading
import os

from core.pdf_tools import (
    pdf_to_word, word_to_pdf, images_to_pdf, merge_pdfs, split_pdf,
    protect_pdf, unlock_pdf
)
from core.file_tools import scan_temp_files, duplicate_files, organize_files, disk_overview

KV = r'''
#:import dp kivy.metrics.dp

<Root@BoxLayout>:
    orientation: 'vertical'
    padding: dp(12)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: 0.018, 0.02, 0.035, 1
        Rectangle:
            pos: self.pos
            size: self.size

<TitleButton@Button>:
    size_hint_y: None
    height: dp(48)
    background_normal: ''
    background_color: 0.03, 0.65, 0.78, 1
    color: 1, 1, 1, 1
    bold: True

<SectionButton@Button>:
    size_hint_y: None
    height: dp(46)
    background_normal: ''
    background_color: 0.08, 0.09, 0.14, 1
    color: 0.85, 0.95, 1, 1
    halign: 'left'
    text_size: self.size
    padding_x: dp(16)

<Root>:
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: dp(105)
        spacing: dp(4)
        Label:
            text: 'SMART PDF STUDIO'
            color: 0.1, 0.9, 1, 1
            font_size: '25sp'
            bold: True
        Label:
            text: 'VIP EDITION  •  Android'
            color: 0.8, 0.25, 0.95, 1
            font_size: '13sp'
        Label:
            text: 'Created by Chishti Bro Computers and Developers'
            color: 0.65, 0.7, 0.78, 1
            font_size: '10sp'

    ScrollView:
        do_scroll_x: False
        GridLayout:
            cols: 1
            spacing: dp(8)
            size_hint_y: None
            height: self.minimum_height

            Label:
                text: 'PDF TOOLKIT'
                size_hint_y: None
                height: dp(34)
                color: 0.1, 0.9, 1, 1
                bold: True

            SectionButton:
                text: '📄  PDF → Word'
                on_release: app.pick('pdf_to_word')
            SectionButton:
                text: '📝  Word → PDF'
                on_release: app.pick('word_to_pdf')
            SectionButton:
                text: '🖼  Images → PDF'
                on_release: app.pick_images()
            SectionButton:
                text: '🔗  Merge PDFs'
                on_release: app.pick('merge')
            SectionButton:
                text: '✂  Split PDF'
                on_release: app.pick('split')
            SectionButton:
                text: '🔐  Password Protect PDF'
                on_release: app.pick('protect')
            SectionButton:
                text: '🔓  Unlock PDF'
                on_release: app.pick('unlock')

            Label:
                text: 'PC / FILE TOOLS'
                size_hint_y: None
                height: dp(34)
                color: 0.1, 0.9, 1, 1
                bold: True
            SectionButton:
                text: '🧹  Scan Temporary Files'
                on_release: app.run_task('temp')
            SectionButton:
                text: '💾  Storage Overview'
                on_release: app.run_task('disk')
            SectionButton:
                text: '🔎  Find Duplicate Files'
                on_release: app.pick_folder('duplicates')
            SectionButton:
                text: '📁  Organize Files by Extension'
                on_release: app.pick_folder('organize')

            Label:
                text: 'STATUS'
                size_hint_y: None
                height: dp(34)
                color: 0.1, 0.9, 1, 1
                bold: True
            Label:
                text: app.status
                size_hint_y: None
                height: dp(90)
                text_size: self.width - dp(20), None
                color: 0.75, 0.8, 0.88, 1
                valign: 'top'

            Label:
                text: 'Offline-first • Your files stay on your device'
                size_hint_y: None
                height: dp(45)
                color: 0.55, 0.6, 0.7, 1
'''

Builder.load_string(KV)

class Root(BoxLayout):
    pass

class SmartPDFStudioApp(App):
    status = StringProperty('Ready. Select a tool to begin.')

    def build(self):
        self.title = 'Smart PDF Studio – VIP Edition'
        self.root = Root()
        self._request_android_permissions()
        return self.root

    def _request_android_permissions(self):
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                perms = [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]
                if hasattr(Permission, 'MANAGE_EXTERNAL_STORAGE'):
                    perms.append(Permission.MANAGE_EXTERNAL_STORAGE)
                request_permissions(perms)
            except Exception:
                pass

    @mainthread
    def set_status(self, msg):
        self.status = msg

    def pick(self, action):
        chooser = FileChooserListView(path=self._start_path(), filters=['*.*'])
        box = BoxLayout(orientation='vertical', spacing=8)
        box.add_widget(chooser)
        buttons = BoxLayout(size_hint_y=None, height=52, spacing=8)
        select = Button(text='SELECT')
        cancel = Button(text='CANCEL')
        buttons.add_widget(select); buttons.add_widget(cancel)
        box.add_widget(buttons)
        pop = Popup(title='Choose a file', content=box, size_hint=(.96, .92))
        cancel.bind(on_release=pop.dismiss)
        select.bind(on_release=lambda *_: self._selected_file(pop, chooser, action))
        pop.open()

    def pick_images(self):
        chooser = FileChooserListView(path=self._start_path(), filters=['*.png','*.jpg','*.jpeg','*.webp'], multiselect=True)
        self._chooser_popup(chooser, 'Select images', lambda files: self._start_action('images_to_pdf', files))

    def pick_folder(self, action):
        chooser = FileChooserListView(path=self._start_path(), dirselect=True, multiselect=False)
        self._chooser_popup(chooser, 'Select folder', lambda files: self._start_action(action, files))

    def _chooser_popup(self, chooser, title, callback):
        box = BoxLayout(orientation='vertical', spacing=8)
        box.add_widget(chooser)
        buttons = BoxLayout(size_hint_y=None, height=52, spacing=8)
        select = Button(text='SELECT'); cancel = Button(text='CANCEL')
        buttons.add_widget(select); buttons.add_widget(cancel); box.add_widget(buttons)
        pop = Popup(title=title, content=box, size_hint=(.96, .92))
        cancel.bind(on_release=pop.dismiss)
        def go(*_):
            files = chooser.selection[:]
            if files:
                pop.dismiss(); callback(files)
            else:
                self.set_status('Please select at least one item.')
        select.bind(on_release=go)
        pop.open()

    def _selected_file(self, pop, chooser, action):
        if not chooser.selection:
            self.set_status('Please select a file.')
            return
        path = chooser.selection[0]
        pop.dismiss()
        self._start_action(action, [path])

    def _start_path(self):
        candidates = []
        if platform == 'android':
            candidates += ['/storage/emulated/0/Download', '/storage/emulated/0']
        candidates.append(str(Path.home()))
        for p in candidates:
            if os.path.isdir(p): return p
        return '.'

    def _start_action(self, action, files):
        threading.Thread(target=self._worker, args=(action, files), daemon=True).start()

    def run_task(self, action):
        self._start_action(action, [])

    def _output(self, src, suffix):
        p = Path(src)
        return str(p.with_name(p.stem + suffix))

    def _ask_text(self, title, hint, callback):
        from kivy.uix.textinput import TextInput
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        inp = TextInput(hint_text=hint, multiline=False, password='password' in hint.lower())
        ok = Button(text='CONTINUE', size_hint_y=None, height=50)
        box.add_widget(inp); box.add_widget(ok)
        pop = Popup(title=title, content=box, size_hint=(.9,.35))
        ok.bind(on_release=lambda *_: (pop.dismiss(), callback(inp.text)))
        pop.open()

    def _worker(self, action, files):
        try:
            if action == 'pdf_to_word':
                src=files[0]; out=self._output(src, '_converted.docx'); pdf_to_word(src,out); msg=f'Done: {out}'
            elif action == 'word_to_pdf':
                src=files[0]; out=self._output(src, '_converted.pdf'); word_to_pdf(src,out); msg=f'Done: {out}'
            elif action == 'images_to_pdf':
                out=str(Path(files[0]).parent / 'Images_Combined.pdf'); images_to_pdf(files,out); msg=f'Done: {out}'
            elif action == 'merge':
                # A simple sequential picker is safer for Android file chooser.
                if len(files) < 2:
                    self.set_status('Merge requires multiple PDFs. Use the Images/PDF picker or select files in a folder.')
                    return
                out=str(Path(files[0]).parent / 'Merged.pdf'); merge_pdfs(files,out); msg=f'Done: {out}'
            elif action == 'split':
                src=files[0]; out=str(Path(src).with_name(Path(src).stem+'_split.pdf')); split_pdf(src,out,1,1); msg=f'Split page 1 created: {out}'
            elif action == 'protect':
                src=files[0]
                self._ask_text('Password Protect', 'Enter password', lambda pw: self._start_action('protect_with_password',[src,pw])); return
            elif action == 'protect_with_password':
                src,pw=files; out=self._output(src,'_protected.pdf'); protect_pdf(src,out,pw); msg=f'Protected PDF: {out}'
            elif action == 'unlock':
                src=files[0]
                self._ask_text('Unlock PDF', 'Enter password', lambda pw: self._start_action('unlock_with_password',[src,pw])); return
            elif action == 'unlock_with_password':
                src,pw=files; out=self._output(src,'_unlocked.pdf'); unlock_pdf(src,out,pw); msg=f'Unlocked PDF: {out}'
            elif action == 'temp':
                result=scan_temp_files(); msg=f'Temporary files found: {len(result)}\nAndroid storage rules limit deletion outside the app sandbox.'
            elif action == 'disk':
                d=disk_overview(); msg=f"Storage: {d['used_human']} used / {d['total_human']} total\nFree: {d['free_human']}"
            elif action == 'duplicates':
                folder=files[0]; result=duplicate_files(folder); msg=f'Duplicate groups found: {len(result)}'
            elif action == 'organize':
                folder=files[0]; moved=organize_files(folder); msg=f'Files organized: {moved}'
            else:
                msg='Unknown action.'
            self.set_status(msg)
        except Exception as e:
            self.set_status(f'Error: {e}')

if __name__ == '__main__':
    SmartPDFStudioApp().run()
