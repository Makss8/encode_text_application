import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def caesar_cipher(text, shift):
    encrypted = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            encrypted += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            encrypted += char
    return encrypted

def transposition_cipher(text, columns):
    rows = len(text) // columns
    if len(text) % columns != 0:
        rows += 1
    table = [[" " for c in range(columns)] for r in range(rows)]
    r, c = 0, 0
    for letter in text:
        table[r][c] = letter
        c += 1
        if c == columns:
            r += 1
            c = 0
    coded = ""
    r, c = 0, 0
    for _ in range(rows * columns):
        coded += table[r][c]
        r += 1
        if r == rows:
            r = 0
            c += 1
    return coded

def vigenere_cipher(text, key):
    key = key.lower()
    key_indices = [ord(i) - 97 for i in key]
    text_indices = [(ord(char) - 97 if char.isalpha() else char) for char in text.lower()]
    encrypted = ""
    key_index = 0
    for index in text_indices:
        if isinstance(index, int):
            shift = key_indices[key_index % len(key)]
            encrypted += chr((index + shift) % 26 + 97)
            key_index += 1
        else:
            encrypted += index
    return encrypted

def encrypt_text():
    text = input_text.get("1.0", tk.END).strip()
    cipher_type = cipher_choice.get()
    key = key_entry.get().strip()

    if not text:
        messagebox.showerror("Error", "Please enter some text to encrypt.")
        return

    if cipher_type == "Caesar Cipher":
        try:
            shift = int(key)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid shift value for Caesar Cipher.")
            return
        encrypted_text.set(caesar_cipher(text, shift))
    elif cipher_type == "Transposition Cipher":
        try:
            columns = int(key)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid column value for Transposition Cipher.")
            return
        encrypted_text.set(transposition_cipher(text, columns))
    elif cipher_type == "Vigenère Cipher":
        if not key.isalpha():
            messagebox.showerror("Error", "Please enter a valid keyword for Vigenère Cipher.")
            return
        encrypted_text.set(vigenere_cipher(text, key))
    else:
        messagebox.showerror("Error", "Please select a valid cipher method.")

def export_to_pdf():
    encrypted = encrypted_text.get()
    if not encrypted:
        messagebox.showerror("Error", "There is no encrypted text to export.")
        return

    filename = "encrypted_text.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, encrypted)
    c.save()
    messagebox.showinfo("Success", f"Encrypted text has been exported to {filename}")


root = tk.Tk()
root.title("Text Encryptor")

# Widgets
tk.Label(root, text="Input Text:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
input_text = tk.Text(root, height=10, width=50)
input_text.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Cipher Method:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
cipher_choice = ttk.Combobox(root, values=["Caesar Cipher", "Transposition Cipher", "Vigenère Cipher"])
cipher_choice.grid(row=1, column=1, padx=10, pady=10)
cipher_choice.current(0)

tk.Label(root, text="Key:").grid(row=2, column=0, padx=10, pady=10, sticky='w')
key_entry = tk.Entry(root)
key_entry.grid(row=2, column=1, padx=10, pady=10)

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_text)
encrypt_button.grid(row=3, column=0, columnspan=2, pady=10)

tk.Label(root, text="Encrypted Text:").grid(row=4, column=0, padx=10, pady=10, sticky='w')
encrypted_text = tk.StringVar()
tk.Entry(root, textvariable=encrypted_text, state='readonly', width=50).grid(row=4, column=1, padx=10, pady=10)

export_button = tk.Button(root, text="Export to PDF", command=export_to_pdf)
export_button.grid(row=5, column=0, columnspan=2, pady=10)


root.mainloop()
