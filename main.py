import threading, sys, subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from utils import parse_config_versions
from config import read_config, write_config_key

class MinecraftServerManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Minecraft Server Manager")
        self.master.geometry("400x300")
        
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_frame()
        
        tk.Label(self.main_frame, text="Minecraft Server Manager", font=("Arial", 16)).pack(pady=10)
        
        ttk.Button(self.main_frame, text="Configure a new Minecraft Server", command=self.create_new_minecraft_server).pack(fill='x', pady=5)
        ttk.Button(self.main_frame, text="Start an existing Minecraft Server", command=self.start_existing_server).pack(fill='x', pady=5)
        ttk.Button(self.main_frame, text="Settings", command=self.open_settings).pack(fill='x', pady=5)
        ttk.Button(self.main_frame, text="Exit", command=self.master.quit).pack(fill='x', pady=5)

    def create_new_minecraft_server(self):
        self.clear_frame()
        
        tk.Label(self.main_frame, text="Choose name for your server", font=("Arial", 14)).pack(pady=10)
        
        self.server_name_entry = ttk.Entry(self.main_frame)
        self.server_name_entry.pack(fill='x', pady=5)
        
        ttk.Button(self.main_frame, text="Next", command=self.choose_core).pack(fill='x', pady=5)
        ttk.Button(self.main_frame, text="Back", command=self.show_main_menu).pack(fill='x', pady=5)

    def choose_core(self):
        server_name = self.server_name_entry.get()
        if not server_name:
            messagebox.showerror("Error", "Please enter a server name.")
            return
        
        self.clear_frame()
        
        tk.Label(self.main_frame, text="Choose your server's core", font=("Arial", 14)).pack(pady=10)
        
        ttk.Button(self.main_frame, text="Spigot", command=lambda: self.choose_version(server_name, 'spigot')).pack(fill='x', pady=5)
        ttk.Button(self.main_frame, text="Back", command=self.create_new_minecraft_server).pack(fill='x', pady=5)

    def choose_version(self, server_name, core):
        self.clear_frame()
        
        tk.Label(self.main_frame, text="Choose your server's version", font=("Arial", 14)).pack(pady=10)
        
        core_versions = parse_config_versions(core)
        self.version_var = tk.StringVar()
        version_dropdown = ttk.Combobox(self.main_frame, textvariable=self.version_var, values=core_versions)
        version_dropdown.pack(fill='x', pady=5)
        version_dropdown.set(core_versions[0])  # Set default value
        
        ttk.Button(self.main_frame, text="Create Server", command=lambda: self.create_server(server_name, core)).pack(fill='x', pady=5)
        ttk.Button(self.main_frame, text="Back", command=lambda: self.choose_core()).pack(fill='x', pady=5)

    def create_server(self, server_name, core):
        version = self.version_var.get()
        self.open_output_window(server_name, core, version)

    def open_output_window(self, server_name, core, version):
        output_window = tk.Toplevel(self.master)
        output_window.title(f"Server Creation: {server_name}")
        output_window.geometry("800x600")

        output_text = tk.Text(output_window, wrap=tk.WORD, state='disabled')
        output_text.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(output_text, orient="vertical", command=output_text.yview)
        scrollbar.pack(side="right", fill="y")
        output_text.configure(yscrollcommand=scrollbar.set)

        # Configure tags for formatting
        output_text.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))
        output_text.tag_configure("info", foreground="blue")
        output_text.tag_configure("error", foreground="red")

        process = None

        def run_server_creation():
            nonlocal process
            try:
                process = subprocess.Popen(
                    [sys.executable, "-c", f"from cores import CORES; CORES['{core}']('{server_name}', '{version}')"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )

                for line in process.stdout:
                    output_text.configure(state='normal')
                    if line.startswith("[INFO]"):
                        output_text.insert(tk.END, line, ("info", "bold"))
                    elif line.startswith("[ERROR]"):
                        output_text.insert(tk.END, line, ("error", "bold"))
                    else:
                        output_text.insert(tk.END, line)
                    output_text.see(tk.END)
                    output_text.configure(state='disabled')
                    output_text.update()

                process.wait()
            except Exception as e:
                output_text.configure(state='normal')
                output_text.insert(tk.END, f"An error occurred: {str(e)}\n", "error")
                output_text.configure(state='disabled')

        def stop_process():
            nonlocal process
            if process:
                process.terminate()
                output_text.configure(state='normal')
                output_text.insert(tk.END, "Process terminated by user.\n", "error")
                output_text.configure(state='disabled')

        thread = threading.Thread(target=run_server_creation)
        thread.start()

        stop_button = ttk.Button(output_window, text="Stop", command=stop_process)
        stop_button.pack(pady=10)

        self.show_main_menu()

    def start_existing_server(self):
        messagebox.showinfo("Info", "This feature is not implemented yet.")
        self.show_main_menu()

    def open_settings(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("600x400")

        config = read_config()

        def save_settings():
            for section, keys in settings_entries.items():
                for key, entry in keys.items():
                    value = entry.get()
                    write_config_key(section, key, value)
            messagebox.showinfo("Settings", "Settings saved successfully!")
            settings_window.destroy()

        main_frame = ttk.Frame(settings_window)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        canvas = tk.Canvas(main_frame, bg='white')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='White.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)

        settings_entries = {}

        for section in config.sections():
            section_frame = ttk.Frame(scrollable_frame, style='White.TFrame')
            section_frame.pack(fill='x', pady=(10, 5))
            tk.Label(section_frame, text=section, font=("Arial", 12, "bold"), bg='white').pack(anchor="w")
            settings_entries[section] = {}
            for key, value in config[section].items():
                frame = ttk.Frame(scrollable_frame, style='White.TFrame')
                frame.pack(fill='x', pady=2)
                ttk.Label(frame, text=key, style='White.TLabel').pack(side='left')
                entry = ttk.Entry(frame)
                entry.insert(0, value)
                entry.pack(side='right', expand=True, fill='x')
                settings_entries[section][key] = entry

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        save_button = ttk.Button(settings_window, text="Save", command=save_settings)
        save_button.pack(pady=10)

        # Configure styles
        style = ttk.Style()
        style.configure('White.TFrame', background='white')
        style.configure('White.TLabel', background='white')

        # Make sure the canvas expands to fill the window
        settings_window.grid_rowconfigure(0, weight=1)
        settings_window.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftServerManager(root)
    root.mainloop()