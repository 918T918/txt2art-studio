#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import os
import re

try:
    import pyfiglet
    from pyfiglet import FigletFont
except ImportError:
    error_message = (
        "Error: Required library 'pyfiglet' not found.\n\n"
        "Please install it using pip from your terminal:\n"
        "  pip install pyfiglet\n"
        "or if using Python 3:\n"
        "  pip3 install pyfiglet\n\n"
        "Then restart the application."
    )
    print(error_message, file=sys.stderr)
    try:
        root_check = tk.Tk()
        root_check.withdraw()
        messagebox.showerror("Dependency Error", error_message)
        root_check.destroy()
    except tk.TclError:
        pass
    sys.exit(1)

APP_VERSION = "1.3"
AVAILABLE_FONTS = sorted(FigletFont.getFonts())
update_job = None
MIN_WIDTH = 10
MAX_WIDTH = 500
DEFAULT_WIDTH = 80
current_theme = "light"
CODE_FORMATS = [
    "Plain Text",
    "Python Triple Quote",
    "JavaScript Backtick",
    "C++ Raw String",
    "Bash Heredoc"
]

light_theme = {
    "bg": "#F0F0F0", "fg": "#000000", "input_bg": "#FFFFFF", "input_fg": "#000000",
    "output_bg": "#F5F5F5", "output_fg": "#000000", "button_bg": "#E1E1E1",
    "button_fg": "#000000", "accent": "#D0D0D0"
}
dark_theme = {
    "bg": "#2E2E2E", "fg": "#EAEAEA", "input_bg": "#3C3C3C", "input_fg": "#EAEAEA",
    "output_bg": "#252525", "output_fg": "#EAEAEA", "button_bg": "#505050",
    "button_fg": "#EAEAEA", "accent": "#454545"
}

def apply_theme(theme_name):
    global current_theme
    theme = light_theme if theme_name == "light" else dark_theme
    current_theme = theme_name
    root.configure(bg=theme["bg"])
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('.', background=theme["bg"], foreground=theme["fg"])
    style.configure('TFrame', background=theme["bg"])
    style.configure('TLabel', background=theme["bg"], foreground=theme["fg"])
    style.configure('TButton', background=theme["button_bg"], foreground=theme["button_fg"])
    style.map('TButton', background=[('active', theme["accent"])])
    style.configure('TCombobox', fieldbackground=theme["input_bg"], foreground=theme["fg"], background=theme["button_bg"], selectbackground=theme["input_bg"], selectforeground=theme["fg"])
    root.option_add('*TCombobox*Listbox.background', theme["accent"])
    root.option_add('*TCombobox*Listbox.foreground', theme["fg"])
    root.option_add('*TCombobox*Listbox.selectBackground', theme["button_bg"])
    root.option_add('*TCombobox*Listbox.selectForeground', theme["fg"])
    style.configure('TSpinbox', fieldbackground=theme["input_bg"], foreground=theme["fg"], background=theme["button_bg"], arrowcolor=theme["fg"])
    text_input.configure(background=theme["input_bg"], foreground=theme["input_fg"], insertbackground=theme["fg"])
    output_text.configure(background=theme["output_bg"], foreground=theme["output_fg"])
    theme_button.configure(text="Light Theme" if theme_name == "dark" else "Dark Theme")

def toggle_theme():
    new_theme = "dark" if current_theme == "light" else "light"
    apply_theme(new_theme)

def schedule_update(event=None):
    global update_job
    if update_job:
        root.after_cancel(update_job)
    update_job = root.after(500, lambda: generate_art(show_warnings=False))

def generate_art(show_warnings=True):
    global update_job
    if update_job and show_warnings:
         root.after_cancel(update_job)
         update_job = None
    input_text = text_input.get("1.0", tk.END).strip()
    selected_font = font_var.get()
    try:
        width_value = width_var.get()
        if not (MIN_WIDTH <= width_value <= MAX_WIDTH):
            if show_warnings: messagebox.showwarning("Invalid Width", f"Width must be between {MIN_WIDTH} and {MAX_WIDTH}. Resetting to {DEFAULT_WIDTH}.")
            width_value = DEFAULT_WIDTH
            width_var.set(DEFAULT_WIDTH)
    except tk.TclError:
        if show_warnings: messagebox.showwarning("Invalid Width", f"Invalid width value entered. Resetting to {DEFAULT_WIDTH}.")
        width_value = DEFAULT_WIDTH
        width_var.set(DEFAULT_WIDTH)
    if show_warnings:
        if not input_text: messagebox.showwarning("Input Required", "Please enter some text to convert."); return
        if not selected_font: messagebox.showwarning("Font Required", "Please select a font."); return
    elif not input_text or not selected_font: clear_output(); return
    try:
        fig = pyfiglet.Figlet(font=selected_font, width=width_value)
        ascii_art = fig.renderText(input_text)
        output_text.configure(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, ascii_art)
        output_text.configure(state=tk.DISABLED)
    except pyfiglet.FontNotFound:
         if show_warnings: messagebox.showerror("Font Error", f"Font '{selected_font}' not found. This shouldn't happen!")
         clear_output()
    except Exception as e:
         if show_warnings: messagebox.showerror("Generation Error", f"An unexpected error occurred during generation:\n{e}")
         clear_output()

def clear_input():
    text_input.delete("1.0", tk.END)
    schedule_update()

def clear_output():
    output_text.configure(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.configure(state=tk.DISABLED)

def format_for_code(raw_art, code_format):
    if code_format == "Python Triple Quote":
        escaped_art = raw_art.replace('"""', '\\"\\"\\"')
        return f'"""\n{escaped_art}\n"""'
    elif code_format == "JavaScript Backtick":
        escaped_art = raw_art.replace('`', '\\`').replace('${', '\\${')
        return f'`\n{escaped_art}\n`'
    elif code_format == "C++ Raw String":
        delimiter = "EOF"
        count = 0
        while f"){delimiter}" in raw_art:
            delimiter = f"EOF{count}"
            count += 1
            if count > 10:
                 return "# Error: Could not find suitable C++ raw string delimiter\n" + raw_art
        return f'R"delimiter(\n{raw_art}\n)delimiter"'
    elif code_format == "Bash Heredoc":
        delimiter = "EOF"
        if f"\n{delimiter}\n" in raw_art or raw_art.startswith(f"{delimiter}\n") or raw_art.endswith(f"\n{delimiter}"):
             return "# Warning: Bash Heredoc delimiter 'EOF' might conflict with art content.\n" + \
                    f"# Consider manually changing the delimiter.\ncat << 'MANUAL_DELIMITER'\n{raw_art}\nMANUAL_DELIMITER"
        return f"cat << 'EOF'\n{raw_art}\nEOF"
    else:
        return raw_art

def copy_to_clipboard():
    raw_art = output_text.get("1.0", tk.END).strip()
    if not raw_art:
        messagebox.showinfo("Clipboard", "Nothing to copy from the output area.")
        return

    selected_format = code_format_var.get()
    formatted_art = format_for_code(raw_art, selected_format)

    try:
        root.clipboard_clear()
        root.clipboard_append(formatted_art)
        messagebox.showinfo("Clipboard", f"Art copied to clipboard as:\n{selected_format}")
    except tk.TclError as e:
         messagebox.showerror("Clipboard Error", f"Could not access clipboard:\n{e}")
    except Exception as e:
        messagebox.showerror("Clipboard Error", f"An unexpected error occurred during copy:\n{e}")

def save_as_file():
    art = output_text.get("1.0", tk.END).strip()
    if not art: messagebox.showwarning("Save Error", "Nothing to save from the output area."); return
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Save ASCII Art As...")
    if not filepath: return
    try:
        with open(filepath, 'w', encoding='utf-8') as f: f.write(art)
        messagebox.showinfo("Save Successful", f"Art saved successfully to:\n{filepath}")
    except PermissionError: messagebox.showerror("Save Error", f"Permission denied.\nCannot write to the selected location:\n{filepath}")
    except IOError as e: messagebox.showerror("Save Error", f"An I/O error occurred while saving:\n{e}")
    except Exception as e: messagebox.showerror("Save Error", f"An unexpected error occurred while saving:\n{e}")

root = tk.Tk()
root.title(f"Txt2Art Studio v{APP_VERSION}")
root.minsize(500, 450)
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=0)

control_frame = ttk.Frame(root, padding="10")
control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
control_frame.columnconfigure(1, weight=1)
input_label = ttk.Label(control_frame, text="Enter Text:")
input_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
text_input = scrolledtext.ScrolledText(control_frame, height=5, width=50, wrap=tk.WORD)
text_input.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=(tk.W, tk.E))
text_input.bind("<KeyRelease>", schedule_update)
clear_input_button = ttk.Button(control_frame, text="Clear Input", command=clear_input)
clear_input_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
font_label = ttk.Label(control_frame, text="Font:")
font_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
font_var = tk.StringVar(root)
font_dropdown = ttk.Combobox(control_frame, textvariable=font_var, state="readonly", width=30)
font_dropdown['values'] = AVAILABLE_FONTS
if 'standard' in AVAILABLE_FONTS: font_var.set('standard')
elif AVAILABLE_FONTS: font_var.set(AVAILABLE_FONTS[0])
font_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
font_dropdown.bind("<<ComboboxSelected>>", schedule_update)
width_label = ttk.Label(control_frame, text="Width:")
width_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
width_var = tk.IntVar(value=DEFAULT_WIDTH)
width_spinbox = ttk.Spinbox(control_frame, from_=MIN_WIDTH, to=MAX_WIDTH, textvariable=width_var, width=5, command=schedule_update)
width_spinbox.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
width_spinbox.bind("<KeyRelease>", schedule_update)
generate_button = ttk.Button(control_frame, text="Generate Now", command=lambda: generate_art(show_warnings=True))
generate_button.grid(row=3, column=2, padx=10, pady=5, sticky=tk.E)

output_frame = ttk.Frame(root, padding="10")
output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
output_frame.columnconfigure(0, weight=1)
output_frame.rowconfigure(1, weight=1)
output_controls_frame = ttk.Frame(output_frame)
output_controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
output_label = ttk.Label(output_controls_frame, text="Result:")
output_label.pack(side=tk.LEFT, padx=5, pady=5)

clear_output_button = ttk.Button(output_controls_frame, text="Clear Output", command=clear_output)
clear_output_button.pack(side=tk.RIGHT, padx=5, pady=5)
copy_button = ttk.Button(output_controls_frame, text="Copy", command=copy_to_clipboard)
copy_button.pack(side=tk.RIGHT, padx=5, pady=5)
code_format_var = tk.StringVar(value=CODE_FORMATS[0])
code_format_dropdown = ttk.Combobox(output_controls_frame, textvariable=code_format_var, values=CODE_FORMATS, state="readonly", width=20)
code_format_dropdown.pack(side=tk.RIGHT, padx=5, pady=5)
code_format_label = ttk.Label(output_controls_frame, text="Copy Format:")
code_format_label.pack(side=tk.RIGHT, padx=0, pady=5)
save_button = ttk.Button(output_controls_frame, text="Save As...", command=save_as_file)
save_button.pack(side=tk.RIGHT, padx=5, pady=5)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.NONE, state=tk.DISABLED, font=("monospace", 10))
output_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

footer_frame = ttk.Frame(root, padding=(10, 0, 10, 10))
footer_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.S))
footer_frame.columnconfigure(0, weight=1)
theme_button = ttk.Button(footer_frame, text="Dark Theme", command=toggle_theme)
theme_button.grid(row=0, column=0, sticky=tk.E, padx=5)

apply_theme(current_theme)

root.mainloop()
