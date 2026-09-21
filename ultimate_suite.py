import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

# Safe imports for optional conversion libraries
try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

try:
    from pdf2docx import Converter
    HAS_PDF2DOCX = True
except ImportError:
    HAS_PDF2DOCX = False

try:
    from docx2pdf import convert as docx_to_pdf_conv
    HAS_DOCX2PDF = True
except ImportError:
    HAS_DOCX2PDF = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import fitz  # PyMuPDF for high-speed PDF to image conversion
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

class UltimateSuiteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate PDF Toolkit & PC Cleaner Suite - Pro Edition")
        self.root.geometry("1150x780")
        self.root.configure(bg="#0f172a")

        # Header Title
        header_frame = tk.Frame(self.root, bg="#1e293b", pady=12)
        header_frame.pack(fill="x")

        title_lbl = tk.Label(header_frame, text="🚀 ULTIMATE PDF TOOLKIT & PC CLEANER SUITE", font=("Arial", 16, "bold"), bg="#1e293b", fg="#38bdf8")
        title_lbl.pack()

        # Notebook Tabs Container
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        # Tab 1: PDF Advanced Toolkit
        self.tab_pdf = tk.Frame(self.notebook, bg="#0f172a")
        self.notebook.add(self.tab_pdf, text="  📄 Advanced PDF Toolkit  ")
        self.build_pdf_tab()

        # Tab 2: PC Cleaner & Organizer
        self.tab_cleaner = tk.Frame(self.notebook, bg="#0f172a")
        self.notebook.add(self.tab_cleaner, text="  🧹 PC Cleaner & Organizer  ")
        self.build_cleaner_tab()

        # Footer Branding (Strictly Maintained)
        footer_label = tk.Label(self.root, text="Created by Chishti Bro Computer & Developers | Founder: Moinuddin Chishti", font=("Arial", 10, "italic"), bg="#0f172a", fg="#94a3b8")
        footer_label.pack(side="bottom", pady=8)

    def build_pdf_tab(self):
        frame = tk.Frame(self.tab_pdf, bg="#1e293b", bd=2, relief="groove")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(frame, text="All-in-One PDF Conversion, Merge, Split & Security Hub", font=("Arial", 12, "bold"), bg="#1e293b", fg="white").pack(anchor="w", padx=15, pady=10)

        # Buttons Grid for PDF Tools
        btn_grid = tk.Frame(frame, bg="#1e293b")
        btn_grid.pack(anchor="w", padx=15, pady=10)

        tk.Button(btn_grid, text="PDF to Word (.docx)", font=("Arial", 9, "bold"), bg="#2563eb", fg="white", width=22, command=self.pdf_to_word).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_grid, text="Word to PDF", font=("Arial", 9, "bold"), bg="#2563eb", fg="white", width=22, command=self.word_to_pdf).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_grid, text="Images to PDF", font=("Arial", 9, "bold"), bg="#2563eb", fg="white", width=22, command=self.images_to_pdf).grid(row=0, column=2, padx=5, pady=5)

        tk.Button(btn_grid, text="PDF to Images", font=("Arial", 9, "bold"), bg="#16a34a", fg="white", width=22, command=self.pdf_to_images).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_grid, text="Merge Multiple PDFs", font=("Arial", 9, "bold"), bg="#16a34a", fg="white", width=22, command=self.merge_pdfs).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_grid, text="Split PDF (Ranges)", font=("Arial", 9, "bold"), bg="#16a34a", fg="white", width=22, command=self.split_pdf).grid(row=1, column=2, padx=5, pady=5)

        tk.Button(btn_grid, text="Password Protect PDF", font=("Arial", 9, "bold"), bg="#d97706", fg="white", width=22, command=self.protect_pdf).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(btn_grid, text="Unlock / Decrypt PDF", font=("Arial", 9, "bold"), bg="#d97706", fg="white", width=22, command=self.unlock_pdf).grid(row=2, column=1, padx=5, pady=5)

    def build_cleaner_tab(self):
        frame = tk.Frame(self.tab_cleaner, bg="#1e293b", bd=2, relief="groove")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(frame, text="PC Cleaner, SHA-256 Duplicate Finder & Smart Organizer", font=("Arial", 12, "bold"), bg="#1e293b", fg="white").pack(anchor="w", padx=15, pady=10)

        btn_frame = tk.Frame(frame, bg="#1e293b")
        btn_frame.pack(anchor="w", padx=15, pady=5)

        tk.Button(btn_frame, text="Scan & Clean Temp Files", font=("Arial", 9, "bold"), bg="#dc2626", fg="white", width=25, command=self.scan_temp_files).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Find Duplicates (SHA-256)", font=("Arial", 9, "bold"), bg="#2563eb", fg="white", width=25, command=self.find_duplicates).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Auto-Organize Directory", font=("Arial", 9, "bold"), bg="#16a34a", fg="white", width=25, command=self.organize_files).pack(side="left", padx=5)

        self.log_box = tk.Text(frame, height=14, bg="#0f172a", fg="#22c55e", font=("Consolas", 10))
        self.log_box.pack(padx=15, pady=15, fill="both", expand=True)
        self.log_box.insert(tk.END, "=== SYSTEM & PDF SUITE LOGS ===\nReady for execution...\n")

    # --- PDF MODULE FUNCTIONS ---
    def pdf_to_word(self):
        if not HAS_PDF2DOCX:
            messagebox.showerror("Missing Library", "Please install pdf2docx library via 'pip install pdf2docx'")
            return
        file = filedialog.askopenfilename(title="Select PDF file", filetypes=[("PDF Files", "*.pdf")])
        if not file: return
        save_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Document", "*.docx")])
        if not save_path: return
        try:
            cv = Converter(file)
            cv.convert(save_path, start=0, end=None)
            cv.close()
            messagebox.showinfo("Success", f"PDF successfully converted to Word:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def word_to_pdf(self):
        if not HAS_DOCX2PDF:
            messagebox.showerror("Missing Library", "Please install docx2pdf library via 'pip install docx2pdf'")
            return
        file = filedialog.askopenfilename(title="Select Word file", filetypes=[("Word Files", "*.docx")])
        if not file: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF File", "*.pdf")])
        if not save_path: return
        try:
            docx_to_pdf_conv(file, save_path)
            messagebox.showinfo("Success", f"Word successfully converted to PDF:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def images_to_pdf(self):
        if not HAS_PIL:
            messagebox.showerror("Missing Library", "Please install Pillow library via 'pip install Pillow'")
            return
        files = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if not files: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF File", "*.pdf")])
        if not save_path: return
        try:
            images = [Image.open(f).convert('RGB') for f in files]
            images[0].save(save_path, save_all=True, append_images=images[1:])
            messagebox.showinfo("Success", f"Images successfully merged into PDF:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def pdf_to_images(self):
        if not HAS_FITZ:
            messagebox.showerror("Missing Library", "Please install PyMuPDF library via 'pip install PyMuPDF'")
            return
        file = filedialog.askopenfilename(title="Select PDF file", filetypes=[("PDF Files", "*.pdf")])
        if not file: return
        folder = filedialog.askdirectory(title="Select Output Folder for Images")
        if not folder: return
        try:
            doc = fitz.open(file)
            for i, page in enumerate(doc):
                pix = page.get_pixmap()
                pix.save(os.path.join(folder, f"page_{i+1}.png"))
            messagebox.showinfo("Success", f"All pages converted to PNG images in folder:\n{folder}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def merge_pdfs(self):
        if not HAS_PYPDF: return
        files = filedialog.askopenfilenames(title="Select PDFs to Merge", filetypes=[("PDF Files", "*.pdf")])
        if not files: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF File", "*.pdf")])
        if not save_path: return
        try:
            merger = pypdf.PdfMerger()
            for f in files: merger.append(f)
            merger.write(save_path)
            merger.close()
            messagebox.showinfo("Success", f"PDFs merged successfully:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def split_pdf(self):
        if not HAS_PYPDF: return
        file = filedialog.askopenfilename(title="Select PDF to Split", filetypes=[("PDF Files", "*.pdf")])
        if not file: return
        folder = filedialog.askdirectory(title="Select Output Folder")
        if not folder: return
        
        # Simple split example: split every single page or ask range logic
        try:
            reader = pypdf.PdfReader(file)
            for i, page in enumerate(reader.pages):
                writer = pypdf.PdfWriter()
                writer.add_page(page)
                out_path = os.path.join(folder, f"split_page_{i+1}.pdf")
                with open(out_path, "wb") as f:
                    writer.write(f)
            messagebox.showinfo("Success", f"PDF successfully split page by page into folder:\n{folder}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def protect_pdf(self):
        if not HAS_PYPDF: return
        file = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF Files", "*.pdf")])
        if not file: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF File", "*.pdf")])
        if not save_path: return
        pwd = "securepassword123" # Can be customized with a popup dialog if needed
        try:
            reader = pypdf.PdfReader(file)
            writer = pypdf.PdfWriter()
            for page in reader.pages: writer.add_page(page)
            writer.encrypt(pwd)
            with open(save_path, "wb") as f: writer.write(f)
            messagebox.showinfo("Success", f"PDF protected with password '{pwd}'!\nSaved to: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def unlock_pdf(self):
        if not HAS_PYPDF: return
        file = filedialog.askopenfilename(title="Select Encrypted PDF", filetypes=[("PDF Files", "*.pdf")])
        if not file: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF File", "*.pdf")])
        if not save_path: return
        pwd = "securepassword123"
        try:
            reader = pypdf.PdfReader(file)
            if reader.is_encrypted:
                reader.decrypt(pwd)
            writer = pypdf.PdfWriter()
            for page in reader.pages: writer.add_page(page)
            with open(save_path, "wb") as f: writer.write(f)
            messagebox.showinfo("Success", f"PDF unlocked successfully!\nSaved to: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- CLEANER & ORGANIZER LOGIC ---
    def scan_temp_files(self):
        self.log_box.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S সিস্ট')}] Scanning temp files...\n")
        temp_dir = os.environ.get('TEMP', '/tmp')
        count = sum(1 for _ in Path(temp_dir).glob('*') if _.is_file())
        messagebox.showinfo("Scan Complete", f"Found {count} temporary items in system directory.")
        self.log_box.insert(tk.END, f"-> Found {count} temp files.\n")

    def find_duplicates(self):
        folder = filedialog.askdirectory(title="Select Directory for Duplicate Scan")
        if not folder: return
        self.log_box.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Running SHA-256 duplicate scan...\n")
        hashes = {}
        dups = 0
        for path in Path(folder).rglob('*'):
            if path.is_file():
                try:
                    hasher = hashlib.sha256()
                    with open(path, 'rb') as f:
                        hasher.update(f.read())
                    h = hasher.hexdigest()
                    if h in hashes:
                        dups += 1
                        self.log_box.insert(tk.END, f"-> Duplicate: {path.name}\n")
                    else:
                        hashes[h] = path
                except Exception: pass
        self.log_box.insert(tk.END, f"-> Duplicate scan complete. Found {dups} duplicates.\n")

    def organize_files(self):
        folder = filedialog.askdirectory(title="Select Folder to Organize")
        if not folder: return
        self.log_box.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Organizing folder contents...\n")
        
        exts_map = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
            'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
            'Videos': ['.mp4', '.mkv', '.avi'],
            'Audio': ['.mp3', '.wav'],
            'Archives': ['.zip', '.rar', '.7z'],
            'Code': ['.py', '.js', '.html', '.css', '.cpp']
        }
        
        path_obj = Path(folder)
        moved = 0
        for item in path_obj.iterdir():
            if item.is_file():
                ext = item.suffix.lower()
                target = 'Others'
                for cat, lst in exts_map.items():
                    if ext in lst:
                        target = cat
                        break
                dest_dir = path_obj / target
                dest_dir.mkdir(exist_ok=True)
                dest = dest_dir / item.name
                if dest.exists():
                    dest = dest_dir / f"{item.stem}_copy{item.suffix}"
                shutil.move(str(item), str(dest))
                moved += 1
        self.log_box.insert(tk.END, f"-> Successfully organized {moved} files with safe renaming!\n")
        messagebox.showinfo("Success", f"Successfully organized {moved} files!")

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateSuiteApp(root)
    root.mainloop()
  
