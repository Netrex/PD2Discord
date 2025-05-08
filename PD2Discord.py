import subprocess
import sys
import os
import tkinter as tk
import threading
import time
import psutil

def launch_game(exe_path):
    try:
        print(f"[INFO] Launching: {exe_path}")
        return subprocess.Popen([exe_path], shell=True)
    except Exception as e:
        print(f"[ERROR] Failed to launch game: {e}")
        return None

def monitor_process(proc, root):
    while True:
        time.sleep(1)
        if proc.poll() is not None or not psutil.pid_exists(proc.pid):
            print("[INFO] Detected game closed. Exiting app.")
            break
    root.quit()

def create_gui():
    base_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
    target_exe = os.path.join(base_dir, 'PD2Launcher.exe')

    print(f"[INFO] Base directory: {base_dir}")
    print(f"[INFO] Target EXE: {target_exe}")

    if not os.path.isfile(target_exe):
        print(f"[ERROR] Could not find {target_exe}")
        return

    proc = launch_game(target_exe)

    root = tk.Tk()
    root.title("PD2Discord")
    root.geometry("200x100")
    root.resizable(False, False)

    # Set the icon
    try:
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "PD2Discord.ico")
        else:
            icon_path = os.path.join(os.path.dirname(__file__), "PD2Discord.ico")
        root.iconbitmap(icon_path)
        print(f"[INFO] Loaded icon: {icon_path}")
    except Exception as e:
        print(f"[WARN] Failed to set icon: {e}")

    label = tk.Label(root, text="PD2Discord is running...")
    label.pack(expand=True)

    root.update()
    root.iconify()  # Start minimized to taskbar

    if proc:
        threading.Thread(target=monitor_process, args=(proc, root), daemon=True).start()
    else:
        print("[ERROR] Game process could not be started.")
        return

    print("[INFO] GUI running.")
    root.mainloop()
    print("[INFO] GUI closed.")

if __name__ == '__main__':
    create_gui()
