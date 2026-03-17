"""
Folder Zipper with Versioning
A simple Tkinter GUI app to zip folders with automatic version numbering.
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import re
from pathlib import Path
from datetime import datetime
import json
import threading


class FolderZipperApp:
    def __init__(self, root):
        self.version = "1.1"
        self.root = root
        self.root.title(f"Folder Zipper with Versioning v{self.version}")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        self.selected_folder = None
        # Default to the directory where the app is located
        self.app_dir = os.path.dirname(os.path.abspath(__file__))

        # Fix: When running as PyInstaller executable, use the executable's directory
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            self.start_directory = os.path.dirname(sys.executable)
        else:
            # Running as script
            self.start_directory = self.app_dir

        self.current_directory = None
        # Config file is saved next to the executable, not in bundled app-files
        if getattr(sys, 'frozen', False):
            self.config_file = os.path.join(os.path.dirname(sys.executable), "folderzipperconfig.json")
        else:
            self.config_file = os.path.join(self.app_dir, "folderzipperconfig.json")

        self.setup_ui()
        self.load_config()
        self.apply_system_theme()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame,
            text=f"Folder Zipper v{self.version}",
            font=('Segoe UI', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10))

        # Directory navigation frame
        nav_frame = ttk.Frame(main_frame)
        nav_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        nav_frame.columnconfigure(1, weight=1)
        
        # Back button
        back_btn = ttk.Button(
            nav_frame, 
            text="⬆ Up", 
            command=self.go_up_directory,
            width=10
        )
        back_btn.grid(row=0, column=0, padx=(0, 5))
        
        # Current directory label
        self.dir_label = ttk.Label(
            nav_frame, 
            text="Current: ", 
            font=('Segoe UI', 9, 'bold'),
            cursor="hand2"
        )
        self.dir_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.dir_label.bind("<Button-1>", lambda e: self.go_up_directory())
        
        # Browse button
        browse_btn = ttk.Button(
            nav_frame, 
            text="📁 Browse", 
            command=self.browse_directory
        )
        browse_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Folder list frame with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(list_frame)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Folder listbox
        self.folder_listbox = tk.Listbox(
            list_frame,
            font=('Segoe UI', 11),
            yscrollcommand=self.scrollbar.set,
            selectmode=tk.SINGLE
        )
        self.folder_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.config(command=self.folder_listbox.yview)
        
        # Store reference for theme switching
        self.scrollbar_widget = self.scrollbar
        
        # Bind single-click to select folder, double-click to enter and zip
        self.folder_listbox.bind('<ButtonRelease-1>', self.on_folder_select)
        self.folder_listbox.bind('<Double-Button-1>', self.on_folder_enter_and_zip)
        self.folder_listbox.bind('<Return>', self.on_folder_enter_and_zip)
        
        # Zip button with version input
        zip_frame = ttk.Frame(main_frame)
        zip_frame.grid(row=4, column=0, pady=(10, 10))
        zip_frame.columnconfigure(1, weight=1)

        # Version label
        version_label = ttk.Label(
            zip_frame,
            text="Version:",
            font=('Segoe UI', 10, 'bold')
        )
        version_label.grid(row=0, column=0, padx=(0, 5))

        # Version entry
        self.version_entry = ttk.Entry(
            zip_frame,
            font=('Segoe UI', 10),
            width=48
        )
        self.version_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Bind window close event to save config
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Zip button
        self.zip_btn = ttk.Button(
            zip_frame,
            text="📦 Zip Selected Folder",
            command=self.zip_selected_folder,
            width=25
        )
        self.zip_btn.grid(row=0, column=2, padx=(20, 0))

        # Progress bar
        self.progress_var = tk.DoubleVar()
        
        # Create a style for the green progress bar
        self.style = ttk.Style()
        # Ensure we're using a theme that supports custom colors (clam is good)
        if self.style.theme_use() not in ['clam', 'alt', 'default']:
            self.style.theme_use('clam')
            
        self.style.configure(
            "Green.Horizontal.TProgressbar", 
            troughcolor='#2d2d2d', 
            background='#28a745', 
            bordercolor='#2d2d2d', 
            lightcolor='#28a745', 
            darkcolor='#28a745'
        )

        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            style="Green.Horizontal.TProgressbar"
        )
        self.progress_bar.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

        # Current file being zipped label
        self.current_file_label = ttk.Label(
            main_frame,
            text="",
            font=('Segoe UI', 8),
            foreground='gray'
        )
        self.current_file_label.grid(row=6, column=0, sticky=(tk.W, tk.E))

        # Status label with wrap
        self.status_label = ttk.Label(
            main_frame,
            text="Ready - Select a folder to zip",
            font=('Segoe UI', 9),
            foreground='gray',
            wraplength=600
        )
        self.status_label.grid(row=7, column=0, pady=(5, 10))

        # Support & Feedback section
        support_frame = ttk.Frame(main_frame)
        support_frame.grid(row=8, column=0, pady=(10, 10))

        # Support label
        support_label = ttk.Label(
            support_frame,
            text="Support & Feedback:",
            font=('Segoe UI', 9, 'bold')
        )
        support_label.grid(row=0, column=0, pady=(0, 5))

        # Donation buttons frame
        donate_frame = ttk.Frame(support_frame)
        donate_frame.grid(row=1, column=0, pady=(5, 0))

        # Buy Me a Coffee button
        coffee_btn = ttk.Button(
            donate_frame,
            text="☕ Buy Me a Coffee",
            command=self.open_coffee_link,
            width=20
        )
        coffee_btn.grid(row=0, column=0, padx=(0, 5))

        # PayPal button
        paypal_btn = ttk.Button(
            donate_frame,
            text="💳 PayPal Donate",
            command=self.open_paypal_link,
            width=20
        )
        paypal_btn.grid(row=0, column=1, padx=(5, 0))

        # GitHub issues link
        github_frame = ttk.Frame(support_frame)
        github_frame.grid(row=2, column=0, pady=(5, 0))

        github_link = ttk.Label(
            github_frame,
            text="🐛 Report Issue / Request Feature",
            font=('Segoe UI', 9),
            foreground='#0066CC',
            cursor="hand2"
        )
        github_link.grid(row=0, column=0)
        github_link.bind("<Button-1>", lambda e: self.open_github_issues())

        # Load initial directory (start from parent of app-files folder)
        self.load_directory(self.start_directory)
        
    def on_folder_select(self, event=None):
        """Handle single-click on folder - just select it."""
        folder_path = self.get_selected_folder()
        if folder_path:
            folder_name = os.path.basename(folder_path)
            self.status_label.config(text=f"Selected: {folder_name} (double-click to enter/zip)", foreground='gray')
        
    def on_folder_enter_and_zip(self, event=None):
        """Handle double-click on folder - enter if it's a folder, or zip if already selected."""
        folder_path = self.get_selected_folder()
        if folder_path and os.path.isdir(folder_path):
            # Enter the folder on first double-click
            self.load_directory(folder_path)
        
    def apply_system_theme(self):
        """Apply dark or light theme based on system settings."""
        try:
            # Check Windows registry for app mode (0=light, 1=dark)
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            ) as key:
                apps_use_dark, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                
            if apps_use_dark == 0:
                # Dark mode
                self.set_dark_theme()
            else:
                # Light mode (default, no changes needed)
                pass
        except Exception as e:
            # If registry check fails, stick with light mode
            pass
        
    def set_dark_theme(self):
        """Apply dark theme colors."""
        # Colors
        bg_color = "#1e1e1e"
        frame_bg = "#2d2d2d"
        fg_color = "#ffffff"
        listbox_bg = "#2d2d2d"
        listbox_fg = "#ffffff"
        listbox_select = "#0078d4"
        scrollbar_bg = "#4a4a4a"
        scrollbar_trough = "#2d2d2d"
        scrollbar_arrow = "#ffffff"
        
        # Configure root
        self.root.configure(bg=bg_color)
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("TFrame", background=frame_bg)
        style.configure("TLabel", background=frame_bg, foreground=fg_color)
        style.configure("TButton", background="#3d3d3d", foreground=fg_color)
        style.map("TButton", background=[("active", "#505050")])
        style.configure("Vertical.TScrollbar", background=scrollbar_bg, troughcolor=scrollbar_trough, arrowcolor=scrollbar_arrow)
        style.configure("Horizontal.TScrollbar", background=scrollbar_bg, troughcolor=scrollbar_trough, arrowcolor=scrollbar_arrow)
        
        # Configure listbox
        self.folder_listbox.configure(
            bg=listbox_bg,
            fg=listbox_fg,
            selectbackground=listbox_select,
            selectforeground=fg_color,
            highlightthickness=0
        )
        
        # Configure status label
        self.status_label.configure(background=frame_bg)

        # Try to set window title bar color (Windows 10/11 only)
        try:
            import winreg
            # Enable dark title bar for the app window
            hwnd = self.root.winfo_id()
            # This requires ctypes for full implementation
            import ctypes
            hwnd = ctypes.windll.user32.GetParent(hwnd)
            # Set window attribute for dark mode (Windows 10 20H1+)
            try:
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, 
                    20,  # DWMWA_USE_IMMERSIVE_DARK_MODE
                    ctypes.byref(ctypes.c_int(1)), 
                    ctypes.sizeof(ctypes.c_int)
                )
            except:
                pass  # Not supported on older Windows versions
        except:
            pass  # Fall back gracefully
        
    def load_directory(self, path):
        """Load all folders from the given directory."""
        try:
            self.current_directory = path
            parent = os.path.dirname(path)
            
            # Show if we're at root level
            if parent == path:
                self.dir_label.config(text=f"📁 {path} (click to go up)")
            else:
                self.dir_label.config(text=f"📁 {path} (click to go up)")
            
            # Clear listbox
            self.folder_listbox.delete(0, tk.END)
            
            # Get all directories
            folders = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    folders.append(item)
            
            # Sort folders alphabetically
            folders.sort(key=str.lower)
            
            # Add to listbox
            for folder in folders:
                self.folder_listbox.insert(tk.END, f"📁 {folder}")
            
            self.status_label.config(text=f"Found {len(folders)} folders")
            
        except PermissionError:
            self.status_label.config(text=f"⚠ Permission denied: {path}", foreground='red')
        except Exception as e:
            self.status_label.config(text=f"⚠ Error: {str(e)}", foreground='red')
    
    def go_up_directory(self):
        """Navigate to parent directory."""
        if self.current_directory:
            parent = os.path.dirname(self.current_directory)
            if parent and parent != self.current_directory:
                self.load_directory(parent)
    
    def browse_directory(self):
        """Open folder browser dialog."""
        folder = filedialog.askdirectory(
            title="Select Directory to Browse",
            initialdir=self.current_directory or os.path.expanduser("~")
        )
        if folder:
            self.load_directory(folder)
    
    def get_selected_folder(self):
        """Get the currently selected folder path."""
        selection = self.folder_listbox.curselection()
        if not selection:
            return None
        
        folder_name = self.folder_listbox.get(selection[0])
        # Remove the folder emoji prefix
        folder_name = folder_name.replace("📁 ", "")
        
        return os.path.join(self.current_directory, folder_name)
    
    def on_folder_double_click(self, event=None):
        """Handle double-click on folder."""
        self.zip_selected_folder()
    
    def get_next_version_number(self, folder_path, custom_version=None):
        """Find the next available version number for the zip file."""
        parent_dir = os.path.dirname(folder_path)
        folder_name = os.path.basename(folder_path)

        # If custom version is provided, use it directly
        if custom_version and custom_version.strip():
            return custom_version.strip()

        # Pattern to match foldername_XXX_timestamp.zip (where XXX is 1-3 digits)
        pattern = re.compile(rf'^{re.escape(folder_name)}_(\d{{1,3}})_.*\.zip$', re.IGNORECASE)

        existing_versions = []

        # Scan parent directory for existing zips
        for item in os.listdir(parent_dir):
            match = pattern.match(item)
            if match:
                version_num = int(match.group(1))
                existing_versions.append(version_num)

        # Return next version number
        if existing_versions:
            return max(existing_versions) + 1
        else:
            return 1
    
    def get_human_readable_size(self, size_bytes):
        """Convert bytes to human-readable format."""
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def zip_selected_folder(self):
        """Zip the currently selected folder with auto-versioning (threaded)."""
        folder_path = self.get_selected_folder()

        if not folder_path:
            self.status_label.config(text="⚠ No folder selected", foreground='orange')
            return

        if not os.path.exists(folder_path):
            self.status_label.config(text=f"⚠ Folder not found", foreground='red')
            return

        parent_dir = os.path.dirname(folder_path)
        if not os.access(parent_dir, os.W_OK):
            self.status_label.config(text="⚠ Parent directory is read-only", foreground='red')
            return

        # Disable button during zipping
        self.zip_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        
        # Get version info
        custom_version = self.version_entry.get().strip()
        version_num = self.get_next_version_number(folder_path, custom_version)
        
        # Start zipping in a background thread
        thread = threading.Thread(
            target=self.run_zipping_thread, 
            args=(folder_path, version_num, parent_dir)
        )
        thread.daemon = True
        thread.start()

    def run_zipping_thread(self, folder_path, version_num, parent_dir):
        """Perform the actual zipping in a background thread."""
        folder_name = os.path.basename(folder_path)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        
        if isinstance(version_num, str):
            zip_filename = f"{version_num}-{folder_name}_{timestamp}.zip"
        else:
            zip_filename = f"{folder_name}_{version_num:03d}_{timestamp}.zip"
        
        zip_path = os.path.join(parent_dir, zip_filename)

        try:
            # Step 1: Count total files for progress bar
            self.root.after(0, lambda: self.status_label.config(text="Calculating files...", foreground='gray'))
            total_files = 0
            for root, dirs, files in os.walk(folder_path):
                total_files += len(files)
            
            if total_files == 0:
                self.root.after(0, lambda: self.status_label.config(text="⚠ Folder is empty", foreground='orange'))
                self.root.after(0, lambda: self.zip_btn.config(state=tk.NORMAL))
                return

            # Step 2: Create the zip file
            zipped_count = 0
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, parent_dir)
                        
                        # Update UI
                        self.root.after(0, lambda f=file: self.current_file_label.config(text=f"Zipping: {f}"))
                        
                        zipf.write(file_path, arcname)
                        
                        zipped_count += 1
                        progress = (zipped_count / total_files) * 100
                        self.root.after(0, lambda p=progress: self.progress_var.set(p))

            # Step 3: Success! Get final size
            final_size = os.path.getsize(zip_path)
            human_size = self.get_human_readable_size(final_size)
            
            self.root.after(0, lambda: self.status_label.config(
                text=f"✓ {zip_filename} | Size: {human_size}",
                foreground='green'
            ))
            self.root.after(0, lambda: self.current_file_label.config(text="Done!"))

        except Exception as e:
            self.root.after(0, lambda msg=str(e): self.status_label.config(text=f"⚠ Error: {msg}", foreground='red'))
        finally:
            self.root.after(0, lambda: self.zip_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.progress_var.set(100))

    def open_coffee_link(self):
        """Open Buy Me a Coffee donation page."""
        import webbrowser
        webbrowser.open("https://buymeacoffee.com/codingiymynewgaming")

    def open_paypal_link(self):
        """Open PayPal donation page."""
        import webbrowser
        webbrowser.open("https://www.paypal.com/donate/?hosted_button_id=ZXHJFTUW9NQK8")

    def open_github_issues(self):
        """Open GitHub issues page for bug reports and feature requests."""
        import webbrowser
        webbrowser.open("https://github.com/codingismynewgaming/folder-zip-versioning/issues")

    def load_config(self):
        """Load saved configuration from config file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    saved_version = config.get('last_version', '')
                    if saved_version:
                        self.version_entry.insert(0, saved_version)
        except Exception as e:
            print(f"Could not load config: {e}")

    def save_config(self):
        """Save current configuration to config file."""
        try:
            config = {
                'last_version': self.version_entry.get().strip()
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Could not save config: {e}")

    def on_close(self):
        """Handle app close event - save config before closing."""
        self.save_config()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = FolderZipperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
