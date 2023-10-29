import tkinter as tk
from tkinter import ttk
import threading
from socket import *
import time

def start_scan():
    progress_var.set(0)
    scan_button.config(text="Scanning...", state="disabled")
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Scanning...\n")
    result_text.config(state="disabled")
    
    scan_thread = threading.Thread(target=scan_ports)
    scan_thread.start()

def scan_ports():
    target = host_entry.get()
    t_IP = gethostbyname(target)
    result = ""

    for i in range(50, 500):
        s = socket(AF_INET, SOCK_STREAM)
        conn = s.connect_ex((t_IP, i))
        
        progress = int(((i - 50) / (500 - 50)) * 100)
        progress_var.set(progress)
        
        if conn == 0:
            result += f'Port {i}: OPEN\n'
        s.close()

    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, result)
    result_text.config(state="disabled")

    scan_button.config(text="Start Scan", state="normal")

def main():
    global host_entry, result_text, scan_button, progress_var

    window = tk.Tk()
    window.title("Port Scanner")

    frame = tk.Frame(window)
    frame.pack(padx=20, pady=20)

    host_label = tk.Label(frame, text="Host:")
    host_label.pack(side="left")

    host_entry = tk.Entry(frame)
    host_entry.pack(side="left", padx=10)

    scan_button = tk.Button(frame, text="Start Scan", command=start_scan)
    scan_button.pack(side="left", padx=10)

    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(window, variable=progress_var, maximum=100)
    progress_bar.pack(fill="x", padx=20, pady=(0, 10))

    result_text = tk.Text(window, width=40, height=10, state="disabled")
    result_text.pack(padx=20, pady=10)

    window.mainloop()

if __name__ == '__main__':
    main()
