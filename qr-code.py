import qrcode
from tkinter import Tk, Label, Entry, Button, messagebox, Frame, filedialog
from PIL import Image, ImageTk

# Custom colors and fonts
BG_COLOR = "#2E3440"  # Dark background
FG_COLOR = "#D8DEE9"  # Light text
ACCENT_COLOR = "#5E81AC"  # Accent color for buttons
BUTTON_HOVER_COLOR = "#81A1C1"  # Hover color for buttons
FONT = ("Helvetica", 12)
BUTTON_FONT = ("Helvetica", 12, "bold")
TITLE_FONT = ("Helvetica", 20, "bold")

# Global variable to store the QR code image
qr_img = None

def generate_qr_code():
    global qr_img
    data = entry_data.get()
    if not data:
        messagebox.showwarning("Input Error", "Please enter some text or a URL!")
        return

    try:
        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Display the QR code
        show_qr_code(qr_img)
        download_button.config(state="normal")  # Enable the download button
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_qr_code(img):
    # Resize the image for display
    img = img.resize((200, 200), Image.LANCZOS)  # Use Image.LANCZOS for older Pillow versions
    img_tk = ImageTk.PhotoImage(img)
    qr_label.config(image=img_tk)
    qr_label.image = img_tk  # Keep a reference to avoid garbage collection

def download_qr_code():
    global qr_img
    if not qr_img:
        messagebox.showwarning("Error", "No QR code generated yet!")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        title="Save QR Code As"
    )
    if file_path:
        try:
            qr_img.save(file_path)
            messagebox.showinfo("Success", f"QR code saved as {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = Tk()
root.title("QR Code Generator")
root.geometry("450x550")  # Set window size
root.configure(bg=BG_COLOR)

# Add a frame for better organization
frame = Frame(root, bg=BG_COLOR)
frame.pack(pady=20, padx=20)

# Add title
title_label = Label(frame, text="QR Code Generator", font=TITLE_FONT, bg=BG_COLOR, fg=FG_COLOR)
title_label.pack(pady=10)

# Add input field
input_frame = Frame(frame, bg=BG_COLOR)
input_frame.pack(pady=10)

Label(input_frame, text="Enter text or URL:", font=FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
entry_data = Entry(input_frame, width=40, font=FONT, bg=FG_COLOR, fg=BG_COLOR, bd=2, relief="flat")
entry_data.pack(pady=10, ipady=5)

# Add generate button
generate_button = Button(frame, text="Generate QR Code", command=generate_qr_code, bg=ACCENT_COLOR, fg=FG_COLOR, font=BUTTON_FONT, bd=0, padx=20, pady=10, activebackground=BUTTON_HOVER_COLOR)
generate_button.pack(pady=20)

# Label to display the generated QR code
qr_label = Label(frame, bg=BG_COLOR)
qr_label.pack(pady=10)

# Download button (initially disabled)
download_button = Button(frame, text="Download QR Code", command=download_qr_code, bg=ACCENT_COLOR, fg=FG_COLOR, font=BUTTON_FONT, bd=0, padx=20, pady=10, state="disabled", activebackground=BUTTON_HOVER_COLOR)
download_button.pack(pady=10)

# Run the application
root.mainloop()