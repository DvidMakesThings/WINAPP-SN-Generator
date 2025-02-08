import os
import datetime
import hashlib
import qrcode
import random
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog  # for browse dialog

# Global variable for storing the QR code image for saving/display
qr_pil_image = None  # The PIL Image used for saving later

def generate_serial_number(project_name, revision, finish_date):
    """
    Generate a serial number using the finish date (DDMMYY) and a 4-digit hash
    computed from the concatenation of project name and revision. Instead of
    appending a random value, a random number (0–9999) is added to the base hash.
    
    final_hash = (base_hash + (random_value mod 10000)) mod 1000000
    Final format: SN-XXXXDDMMYY   (where XXXX is the final hash formatted as at least 4 digits)
    """
    try:
        date_obj = datetime.datetime.strptime(finish_date, "%d%m%y")
        date_str = date_obj.strftime("%d%m%y")
    except ValueError:
        return None, "Finish Date format invalid. Use DDMMYY."
    
    input_string = project_name + revision
    md5_hash = hashlib.md5(input_string.encode())
    base_hash = int(md5_hash.hexdigest(), 16)
    
    random_mod = random.getrandbits(32) % 10000
    final_hash = (base_hash + random_mod) % 1000000
    final_hash_str = f"{final_hash:04}"  # Adjust width as needed
    
    sn = f"SN-{final_hash_str}{date_str}"
    return sn, None

def generate_qr_code(sn):
    """
    Generate a QR code image from the given serial number,
    then resize it to exactly 150×150 pixels.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(sn)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    try:
        resample_filter = Image.Resampling.LANCZOS
    except AttributeError:
        resample_filter = Image.LANCZOS

    img = img.resize((150, 150), resample_filter)
    return img

def browse_save_location():
    """Opens a directory selection dialog and updates the save location entry."""
    directory = filedialog.askdirectory()
    if directory:
        save_entry.delete(0, "end")
        save_entry.insert(0, directory)

def on_generate():
    """Called when the Generate SN button is pressed."""
    global qr_pil_image

    has_error = False
    if not project_entry.get().strip():
        project_entry.configure(border_color="red")
        has_error = True
    else:
        project_entry.configure(border_color="gray")
    if not revision_entry.get().strip():
        revision_entry.configure(border_color="red")
        has_error = True
    else:
        revision_entry.configure(border_color="gray")
    if not finish_date_var.get().strip():
        finish_date_entry.configure(border_color="red")
        has_error = True
    else:
        finish_date_entry.configure(border_color="gray")
    if has_error:
        status_label.configure(text="Please fill in the highlighted fields!")
        return

    project_name = project_entry.get().strip()
    revision = revision_entry.get().strip()
    finish_date = finish_date_var.get().strip()
    
    sn, error = generate_serial_number(project_name, revision, finish_date)
    if error:
        status_label.configure(text=error)
        return

    # Update the serial number display (editable so text can be selected/copied)
    sn_display.configure(state="normal")
    sn_display.delete(0, "end")
    sn_display.insert(0, sn)

    # Generate the QR code and update the label's image
    qr_pil_image = generate_qr_code(sn)
    qr_ctk_image = ctk.CTkImage(light_image=qr_pil_image, size=(150, 150))
    qr_label.configure(image=qr_ctk_image)
    qr_label.image = qr_ctk_image

    status_label.configure(text="Serial number generated.")

def on_save_all():
    """Called when the Save All button is pressed."""
    global qr_pil_image
    project_name = project_entry.get().strip()
    revision = revision_entry.get().strip()
    save_location = save_entry.get().strip()
    if not save_location:
        save_location = os.getcwd()
    sn_text = sn_display.get().strip()
    
    if not (project_name and revision and sn_text.startswith("SN-")):
        status_label.configure(text="Missing info or SN not generated!")
        return
    
    if not os.path.isdir(save_location):
        try:
            os.makedirs(save_location)
        except Exception as e:
            status_label.configure(text=f"Error creating directory: {e}")
            return
    
    # Save files with the project name and SN included in the filename.
    sn_filename = f"{project_name}_{sn_text}.txt"
    qr_filename = f"{project_name}_{sn_text}.png"
    bmp_filename = f"{project_name}_{sn_text}.bmp"
    sn_filepath = os.path.join(save_location, sn_filename)
    qr_filepath = os.path.join(save_location, qr_filename)
    bmp_filepath = os.path.join(save_location, bmp_filename)
    
    try:
        with open(sn_filepath, "w") as f:
            f.write(sn_text)
    except Exception as e:
        status_label.configure(text=f"Error saving SN file: {e}")
        return
    
    if qr_pil_image:
        try:
            qr_pil_image.save(qr_filepath)
            qr_pil_image.save(bmp_filepath)
        except Exception as e:
            status_label.configure(text=f"Error saving QR files: {e}")
            return
    
    status_label.configure(text="Files saved successfully.")

def toggle_date_entry():
    """
    If "Use current date" is selected, disable the finish date entry
    and set its variable to today's date in DDMMYY format.
    Otherwise, enable the entry for manual input.
    """
    if use_current_date_var.get():
        current_date = datetime.datetime.now().strftime("%d%m%y")
        finish_date_var.set(current_date)
        finish_date_entry.configure(state="disabled")
    else:
        finish_date_entry.configure(state="normal")
        finish_date_var.set("")

# ==============================
# Setup the CustomTkinter Window
# ==============================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Serial Number Generator")
app.geometry("450x680")
app.grid_columnconfigure(0, weight=1)

# --- Top Frame: Project Name & Revision (side by side) ---
top_frame = ctk.CTkFrame(app)
top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
top_frame.grid_columnconfigure((0, 1), weight=1)

entry_bg = "#3B3B3B"

project_label = ctk.CTkLabel(top_frame, text="Project Name:")
project_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
project_entry = ctk.CTkEntry(top_frame, placeholder_text="Enter project name", fg_color=entry_bg)
project_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

revision_label = ctk.CTkLabel(top_frame, text="Revision:")
revision_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
revision_entry = ctk.CTkEntry(top_frame, placeholder_text="Enter revision", fg_color=entry_bg)
revision_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# --- Finish Date Input ---
finish_date_label = ctk.CTkLabel(app, text="Finish Date (DDMMYY):")
finish_date_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
finish_date_var = ctk.StringVar()
finish_date_entry = ctk.CTkEntry(app, textvariable=finish_date_var, placeholder_text="Enter finish date", fg_color=entry_bg)
finish_date_entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

# --- "Use current date" CheckBox ---
use_current_date_var = ctk.BooleanVar()
use_current_date_checkbox = ctk.CTkCheckBox(app, text="Use current date", variable=use_current_date_var, command=toggle_date_entry)
use_current_date_checkbox.grid(row=3, column=0, padx=10, pady=5, sticky="w")

# --- Generate SN Button (dark green) ---
generate_button = ctk.CTkButton(app, text="Generate SN", command=on_generate,
                                fg_color="#006400", hover_color="#004d00")
generate_button.grid(row=4, column=0, padx=10, pady=15, sticky="ew")

# --- Serial Number Display (selectable and copyable) ---
sn_label_title = ctk.CTkLabel(app, text="Serial Number:")
sn_label_title.grid(row=5, column=0, padx=10, pady=5, sticky="w")
sn_display = ctk.CTkEntry(app, font=("Helvetica", 14))
sn_display.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

# --- QR-Code Display (with placeholder) ---
qr_label_title = ctk.CTkLabel(app, text="QR-Code:")
qr_label_title.grid(row=7, column=0, padx=10, pady=5, sticky="w")
placeholder_img = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
placeholder_ctk_image = ctk.CTkImage(light_image=placeholder_img, size=(150, 150))
qr_label = ctk.CTkLabel(app, image=placeholder_ctk_image, text="")
qr_label.grid(row=8, column=0, padx=10, pady=5)

# --- Save Location Entry (PATH INPUT) ---
save_entry = ctk.CTkEntry(app, placeholder_text="Enter save directory path", fg_color=entry_bg)
save_entry.grid(row=9, column=0, padx=10, pady=5, sticky="ew")
default_save_location = os.getcwd()
save_entry.insert(0, default_save_location)

# --- Button Frame for Browse and Save All Buttons ---
button_frame = ctk.CTkFrame(app)
button_frame.grid(row=10, column=0, padx=10, pady=5, sticky="ew")
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

browse_button = ctk.CTkButton(button_frame, text="Browse", command=browse_save_location)
browse_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
save_all_button = ctk.CTkButton(button_frame, text="Save All", command=on_save_all,
                                fg_color="#006400", hover_color="#004d00")
save_all_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# --- Status / Message Label ---
status_label = ctk.CTkLabel(app, text="", font=("Helvetica", 12))
status_label.grid(row=11, column=0, padx=10, pady=5, sticky="w", columnspan=2)

app.mainloop()
