"""
Folder Zipper with Versioning
A simple Tkinter GUI app to zip folders with automatic version numbering.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import re
from pathlib import Path
from datetime import datetime


class FolderZipperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Zipper with Versioning")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        self.selected_folder = None
        # Default to the directory where the app is located
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.start_directory = self.app_dir  # Start in app directory, not parent
        self.current_directory = None
        self.custom_version = tk.StringVar()
        self.last_version = ""  # Store last entered version

        self.setup_ui()
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
            text="Select a Folder to Zip",
            font=('Segoe UI', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10))

        # Version input field
        version_frame = ttk.Frame(main_frame)
        version_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        version_frame.columnconfigure(1, weight=1)

        version_label = ttk.Label(
            version_frame,
            text="Version (optional):",
            font=('Segoe UI', 10)
        )
        version_label.grid(row=0, column=0, padx=(0, 5))

        self.version_entry = ttk.Entry(
            version_frame,
            textvariable=self.custom_version,
            font=('Segoe UI', 10),
            width=20
        )
        self.version_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        # Restore last version if available
        if self.last_version:
            self.version_entry.insert(0, self.last_version)

        version_hint = ttk.Label(
            version_frame,
            text="Leave empty for auto-increment",
            font=('Segoe UI', 8),
            foreground='gray'
        )
        version_hint.grid(row=0, column=2, padx=(5, 0))

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
        
        # Zip button
        self.zip_btn = ttk.Button(
            main_frame,
            text="📦 Zip Selected Folder",
            command=self.zip_selected_folder,
            width=30
        )
        self.zip_btn.grid(row=4, column=0, pady=(10, 10))

        # Status label with wrap
        self.status_label = ttk.Label(
            main_frame,
            text="Ready - Select a folder to zip",
            font=('Segoe UI', 9),
            foreground='gray',
            wraplength=600
        )
        self.status_label.grid(row=5, column=0, pady=(0, 10))
        
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

        # If custom version is provided, save it and use it directly
        if custom_version and custom_version.strip():
            self.last_version = custom_version.strip()
            return self.last_version

        # Pattern to match foldername_XXX_timestamp.zip (where XXX is 1-3 digits)
        # Also match custom version format: version-foldername_timestamp.zip
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
    
    def zip_folder(self, folder_path, version_num):
        """Create a zip file of the folder with version number and timestamp."""
        parent_dir = os.path.dirname(folder_path)
        folder_name = os.path.basename(folder_path)

        # Add timestamp to filename: foldername_001_2026-03-14_16-30.zip or 1.0.1-foldername_2026-03-14_16-30.zip
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        
        # Check if version is a custom string (not auto-increment number)
        if isinstance(version_num, str):
            zip_filename = f"{version_num}-{folder_name}_{timestamp}.zip"
        else:
            zip_filename = f"{folder_name}_{version_num:03d}_{timestamp}.zip"
        
        zip_path = os.path.join(parent_dir, zip_filename)

        # Create the zip file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calculate relative path for the archive
                    arcname = os.path.relpath(file_path, parent_dir)
                    zipf.write(file_path, arcname)

        return zip_path
    
    def zip_selected_folder(self):
        """Zip the currently selected folder with auto-versioning."""
        folder_path = self.get_selected_folder()

        if not folder_path:
            self.status_label.config(text="⚠ No folder selected", foreground='orange')
            return

        # Check if folder exists
        if not os.path.exists(folder_path):
            self.status_label.config(text=f"⚠ Folder not found", foreground='red')
            return

        # Check if parent directory is writable
        parent_dir = os.path.dirname(folder_path)
        if not os.access(parent_dir, os.W_OK):
            self.status_label.config(text="⚠ Parent directory is read-only", foreground='red')
            return

        try:
            # Get custom version from input field
            custom_version = self.custom_version.get().strip()
            
            # Get next version number (uses custom version if provided)
            version_num = self.get_next_version_number(folder_path, custom_version)

            # Create zip
            zip_path = self.zip_folder(folder_path, version_num)

            # Success - show detailed info in status
            zip_name = os.path.basename(zip_path)
            self.status_label.config(
                text=f"✓ {zip_name} | Saved to: {parent_dir}",
                foreground='green'
            )
            # Note: Keep version in field for reuse (don't clear it)

        except PermissionError:
            self.status_label.config(text="⚠ Permission denied", foreground='red')
        except Exception as e:
            self.status_label.config(text=f"⚠ Error: {str(e)}", foreground='red')


def main():
    root = tk.Tk()
    app = FolderZipperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
