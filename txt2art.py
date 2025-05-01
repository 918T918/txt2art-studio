#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import os

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

AVAILABLE_FONTS = sorted(FigletFont.getFonts())
update_job = None
MIN_WIDTH = 10
MAX_WIDTH = 500
DEFAULT_WIDTH = 80

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
            if show_warnings:
                 messagebox.showwarning("Invalid Width", f"Width must be between {MIN_WIDTH} and {MAX_WIDTH}. Resetting to {DEFAULT_WIDTH}.")
            width_value = DEFAULT_WIDTH
            width_var.set(DEFAULT_WIDTH)
    except tk.TclError:
        if show_warnings:
             messagebox.showwarning("Invalid Width", f"Invalid width value entered. Resetting to {DEFAULT_WIDTH}.")
        width_value = DEFAULT_WIDTH
        width_var.set(DEFAULT_WIDTH)

    if show_warnings:
        if not input_text:
            messagebox.showwarning("Input Required", "Please enter some text to convert.")
            return
        if not selected_font:
            messagebox.showwarning("Font Required", "Please select a font.")
            return
    elif not input_text or not selected_font:
         clear_output()
         return

    try:
        fig = pyfiglet.Figlet(font=selected_font, width=width_value)
        ascii_art = fig.renderText(input_text)

        output_text.configure(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, ascii_art)
        output_text.configure(state=tk.DISABLED)

    except pyfiglet.FontNotFound:
         if show_warnings:
            messagebox.showerror("Font Error", f"Font '{selected_font}' not found. This shouldn't happen!")
         clear_output()
    except Exception as e:
         if show_warnings:
            messagebox.showerror("Generation Error", f"An unexpected error occurred during generation:\n{e}")
         clear_output()

def clear_input():
    text_input.delete("1.0", tk.END)
    schedule_update()

def clear_output():
    output_text.configure(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.configure(state=tk.DISABLED)

def copy_to_clipboard():
    art = output_text.get("1.0", tk.END).strip()
    if not art:
        messagebox.showinfo("Clipboard", "Nothing to copy from the output area.")
        return
    try:
        root.clipboard_clear()
        root.clipboard_append(art)
    except tk.TclError as e:
         messagebox.showerror("Clipboard Error", f"Could not access clipboard:\n{e}")
    except Exception as e:
        messagebox.showerror("Clipboard Error", f"An unexpected error occurred during copy:\n{e}")

def save_as_file():
    art = output_text.get("1.0", tk.END).strip()
    if not art:
        messagebox.showwarning("Save Error", "Nothing to save from the output area.")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Save ASCII Art As..."
    )

    if not filepath:
        return

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(art)
        messagebox.showinfo("Save Successful", f"Art saved successfully to:\n{filepath}")
    except PermissionError:
         messagebox.showerror("Save Error", f"Permission denied.\nCannot write to the selected location:\n{filepath}")
    except IOError as e:
         messagebox.showerror("Save Error", f"An I/O error occurred while saving:\n{e}")
    except Exception as e:
        messagebox.showerror("Save Error", f"An unexpected error occurred while saving:\n{e}")

root = tk.Tk()
# Updated window title here
root.title("Txt2Art Studio")
root.minsize(500, 400)

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

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
if 'standard' in AVAILABLE_FONTS:
    font_var.set('standard')
elif AVAILABLE_FONTS:
    font_var.set(AVAILABLE_FONTS[0])
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

save_button = ttk.Button(output_controls_frame, text="Save As...", command=save_as_file)
save_button.pack(side=tk.RIGHT, padx=5, pady=5)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.NONE, state=tk.DISABLED, font=("monospace", 10))
output_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

root.mainloop()
