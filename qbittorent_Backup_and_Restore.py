import os
import shutil
import zipfile
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
from threading import Thread
import tempfile

def log_message(message):
    """Insert message to the log window."""
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)

def reset_log():
    """Clear log and reset it."""
    log_text.config(state=tk.NORMAL)
    log_text.delete('1.0', tk.END)
    log_text.config(state=tk.DISABLED)

def clean_previous_backups(dest_dir):
    """Delete all previous zip files in the destination directory."""
    try:
        for root, _, files in os.walk(dest_dir):
            for file in files:
                if file.endswith(".zip"):
                    os.remove(os.path.join(root, file))
                    log_message(f"Deleted old backup file: {file}")
    except Exception as e:
        log_message(f"Error cleaning previous backups: {e}")

def zip_dir(source_dir, zip_path):
    """Zip the source directory into the zip file path."""
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, start=source_dir)
                    zipf.write(full_path, arcname)
    except Exception as e:
        log_message(f"Error zipping directory {source_dir}: {e}")

def make_backup(local_qBittorrent, roaming_qBittorrent):
    """Create a zip archive from the source directory."""
    try:
        temp_dir = tempfile.mkdtemp()

        # Create temporary backups
        local_temp_zip = os.path.join(temp_dir, 'Local_qBittorrent.zip')
        roaming_temp_zip = os.path.join(temp_dir, 'Roaming_qBittorrent.zip')

        zip_dir(local_qBittorrent, local_temp_zip)
        log_message(f"Temporary backup for Local: {local_qBittorrent}")

        zip_dir(roaming_qBittorrent, roaming_temp_zip)
        log_message(f"Temporary backup for Roaming: {roaming_qBittorrent}")

        # Clear existing backups and move new ones
        final_dir = 'qBittorrent'
        os.makedirs(final_dir, exist_ok=True)
        clean_previous_backups(final_dir)

        shutil.move(local_temp_zip, os.path.join(final_dir, 'Local_qBittorrent.zip'))
        shutil.move(roaming_temp_zip, os.path.join(final_dir, 'Roaming_qBittorrent.zip'))

        log_message(f"Backup completed. Files saved in {final_dir}.")

    except Exception as e:
        log_message(f"Error during backup: {e}")

def restore(local_qBittorrent, roaming_qBittorrent):
    """Extract a zip archive to the destination directory."""
    try:
        local_zip_path = 'qBittorrent/Local_qBittorrent.zip'
        roaming_zip_path = 'qBittorrent/Roaming_qBittorrent.zip'

        if not os.path.exists(local_zip_path) or not os.path.exists(roaming_zip_path):
            raise FileNotFoundError("Backup files not found. Perform a backup first.")

        with zipfile.ZipFile(local_zip_path, 'r') as local_obj:
            local_obj.extractall(local_qBittorrent)
        log_message(f"Restored: {local_zip_path}")

        with zipfile.ZipFile(roaming_zip_path, 'r') as roaming_obj:
            roaming_obj.extractall(roaming_qBittorrent)
        log_message(f"Restored: {roaming_zip_path}")

    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))
    except zipfile.BadZipFile:
        messagebox.showerror("Error", "One of the backup files is corrupted.")
    except Exception as e:
        messagebox.showerror("Error", f"Error during restore: {str(e)}")

def check_qbittorrent_installed():
    """Check if qBittorrent is installed on Windows."""
    potential_paths = [
        r"C:\Program Files\qBittorrent\qbittorrent.exe",
        r"C:\Program Files (x86)\qBittorrent\qbittorrent.exe"
    ]

    for path in potential_paths:
        if os.path.exists(path):
            return True

    # If not found, display an error
    messagebox.showerror("Error", "qBittorrent is not installed on this system or is installed in a non-standard directory.")
    return False

def kill_qbittorrent():
    """Kill the qBittorrent process."""
    try:
        subprocess.run('Taskkill /IM qbittorrent.exe /F', shell=True, check=True)
        log_message("qBittorrent process killed.")
    except subprocess.CalledProcessError as e:
        log_message(f"Error killing qBittorrent: {e}")
    except Exception as e:
        log_message(f"Unexpected error killing qBittorrent: {e}")

def launch_qbittorrent():
    """Launch qBittorrent."""
    try:
        subprocess.Popen('C:\\Program Files\\qBittorrent\\qbittorrent.exe', shell=False)
        log_message("qBittorrent launched.")
    except FileNotFoundError:
        log_message("qBittorrent executable not found.")
    except Exception as e:
        log_message(f"Error launching qBittorrent: {e}")

def show_spinner(spinner):
    """Display the spinner (loader)."""
    spinner.pack(side=tk.LEFT, padx=10)
    spinner.start()

def hide_spinner(spinner):
    """Hide the spinner (loader)."""
    spinner.stop()
    spinner.pack_forget()

def backup_button_clicked():
    """Handle backup button click."""
    reset_log()
    if not check_qbittorrent_installed():
        return
    kill_qbittorrent()
    
    # Show the spinner and update the UI
    show_spinner(backup_spinner)
    root.update_idletasks()  # Update the UI immediately before starting the task

    # Run the backup task in a separate thread to keep the UI responsive
    def backup_task():
        try:
            make_backup(Local_qBittorrent, Roaming_qBittorrent)
        finally:
            launch_qbittorrent()
            hide_spinner(backup_spinner)

    Thread(target=backup_task).start()

def restore_button_clicked():
    """Handle restore button click."""
    reset_log()
    if not check_qbittorrent_installed():
        return
    kill_qbittorrent()
    
    # Show the spinner and update the UI
    show_spinner(restore_spinner)
    root.update_idletasks()  # Update the UI immediately before starting the task

    # Run the restore task in a separate thread to keep the UI responsive
    def restore_task():
        try:
            restore(Local_qBittorrent, Roaming_qBittorrent)
        finally:
            launch_qbittorrent()
            hide_spinner(restore_spinner)

    Thread(target=restore_task).start()

def create_placeholder_image(size):
    """Create a colorful placeholder image if the logo is missing."""
    image = Image.new("RGB", (size, size), (240, 240, 240))  # Light gray background
    draw = ImageDraw.Draw(image)
    
    # Create a gradient
    for i in range(size):
        draw.line((0, i, size, i), fill=(255 - i, 100, 150))  # Pink to white gradient
    
    # Draw a simple icon in the center
    draw.ellipse((size*0.25, size*0.25, size*0.75, size*0.75), fill=(100, 100, 255), outline=(255, 255, 255), width=2)
    
    return image

def set_icon_or_placeholder(root, icon_path):
    """Set the window icon or show a placeholder if icon not found."""
    try:
        # Load and set the window icon
        if os.path.exists(icon_path):
            # Display the Icon
            icon_img = Image.open(icon_path).resize((64, 64), Image.Resampling.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_img)
            root.iconphoto(False, icon_photo)
            
            # Display the logo
            logo_img = Image.open(icon_path).resize((150, 150), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label.config(image=logo_photo)
            logo_label.image = logo_photo  # Keep a reference to prevent garbage collection
        else:
            # Use placeholder image if icon not found
            # Display the Icon
            placeholder_icn_img = create_placeholder_image(64)
            placeholder_icn_photo = ImageTk.PhotoImage(placeholder_icn_img)
            root.iconphoto(False, placeholder_icn_photo)

            # Display the logo
            placeholder_img = create_placeholder_image(150)
            placeholder_photo = ImageTk.PhotoImage(placeholder_img)
            logo_label.config(image=placeholder_photo)
            logo_label.image = placeholder_photo  # Keep a reference to prevent garbage collection

            # Display a more elegant message inside the window
            placeholder_text.config(text="Backup Logo Missing")
    except Exception as e:
        log_message(f"Error setting window icon: {e}")

# Paths
home = os.path.expanduser('~')
Local_qBittorrent = os.path.join(home, 'AppData', 'Local', 'qBittorrent')
Roaming_qBittorrent = os.path.join(home, 'AppData', 'Roaming', 'qBittorrent')

# GUI setup
root = tk.Tk()
root.title("qBittorrent Backup and Restore")
root.geometry("500x600")

# Title Label
title_label = tk.Label(root, text="qBittorrent Backup & Restore", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Logo Label
logo_label = tk.Label(root)
logo_label.pack(pady=10)

# Placeholder text
placeholder_text = tk.Label(root, font=("Arial", 14), fg="darkred")
placeholder_text.pack(pady=10)

# Set icon or placeholder
icon_path = "backup_logo.png"
set_icon_or_placeholder(root, icon_path)

# Buttons
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=12, relief='raised')
style.map("TButton", background=[('active', 'lightblue'), ('!disabled', 'white')])

backup_button = ttk.Button(root, text="Backup qBittorrent", command=backup_button_clicked, style="TButton")
backup_button.pack(pady=15)

restore_button = ttk.Button(root, text="Restore qBittorrent", command=restore_button_clicked, style="TButton")
restore_button.pack(pady=15)

# Spinners for Backup and Restore
backup_spinner = ttk.Progressbar(root, mode='indeterminate')
restore_spinner = ttk.Progressbar(root, mode='indeterminate')

# Log area (log_text placed at bottom of the window)
log_text = ScrolledText(root, height=12, wrap=tk.WORD, state=tk.DISABLED)
log_text.pack(pady=10, padx=10)

root.mainloop()
