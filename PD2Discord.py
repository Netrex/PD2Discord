import subprocess
import sys
import os
import tkinter as tk
import threading
import time
import psutil

def launch_game(exe_path):
    try:
        return subprocess.Popen([exe_path], shell=True)
    except Exception as e:
        print(f"Failed to launch game: {e}")
        return None

def monitor_process(proc, root):
    while True:
        time.sleep(1)
        if proc.poll() is not None or not psutil.pid_exists(proc.pid):
            break
    try:
        root.after(0, root.quit)
    except:
        pass

def create_gui():
    base_dir = os.path.dirname(os.path.abspath(sys.executable))
    target_exe = os.path.join(base_dir, 'PD2Launcher.exe')

    proc = launch_game(target_exe)

    root = tk.Tk()
    root.title("PD2Discord")
    root.geometry("200x100")
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", root.quit)

    label = tk.Label(root, text="PD2Discord is running...")
    label.pack(expand=True)

    # Start minimized
    root.update_idletasks()
    root.iconify()

    if proc:
        threading.Thread(target=monitor_process, args=(proc, root), daemon=True).start()

    root.mainloop()

if __name__ == '__main__':
    create_gui()
