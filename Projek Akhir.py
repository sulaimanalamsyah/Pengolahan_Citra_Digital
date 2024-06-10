import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

# Fungsi untuk membuka gambar dari file
def open_image():
    global original_image
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image = cv2.imread(file_path)
        update_display()

# Fungsi untuk mengaplikasikan filter pada citra dan menampilkan hasilnya
def apply_filter(filter_function):
    global original_image
    if original_image is not None:
        filtered_image = filter_function(original_image)
        update_display(filtered_image)

# Fungsi untuk mengaplikasikan filter penggeseran citra
def shift_image(image):
    # Implementasi filter penggeseran citra
    shifted_image = np.roll(image, shift=(50, 50, 0), axis=(0, 1, 2))
    return shifted_image

# Fungsi untuk mengaplikasikan filter memutar citra (0,0)
def rotate_image_0(image):
    # Implementasi filter memutar citra di titik (0,0)
    rows, cols, _ = image.shape
    rotation_matrix = cv2.getRotationMatrix2D((0, 0), 30, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))
    return rotated_image

# Fungsi untuk mengaplikasikan filter memutar citra sebarang derajat
def rotate_image(image):
    # Implementasi filter memutar citra sebarang derajat
    rows, cols, _ = image.shape
    rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), 30, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))
    return rotated_image

# Fungsi untuk mengaplikasikan filter memutar citra utuh
def rotate_image_full(image):
    # Implementasi filter memutar citra utuh
    rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    return rotated_image

# Fungsi untuk mengaplikasikan filter perbesaran citra
def zoom_image(image):
    # Implementasi filter perbesaran citra
    zoomed_image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    return zoomed_image

# Fungsi untuk mengaplikasikan filter pengecilan citra
def shrink_image(image):
    # Implementasi filter pengecilan citra
    shrunk_image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    return shrunk_image

# Fungsi untuk mengaplikasikan filter pencerminan citra horizontal
def flip_horizontal_image(image):
    # Implementasi filter pencerminan citra horizontal
    flipped_image = cv2.flip(image, 1)
    return flipped_image

# Fungsi untuk mengaplikasikan filter pencerminan citra vertikal
def flip_vertical_image(image):
    # Implementasi filter pencerminan citra vertikal
    flipped_image = cv2.flip(image, 0)
    return flipped_image

# Fungsi untuk mengaplikasikan filter efek ripple citra
def ripple_image(image):
    # Implementasi filter efek ripple citra
    rows, cols, _ = image.shape
    ripple_image = np.copy(image)
    
    # Ensure x_wave has the same length as the number of rows
    x_wave = 10 * np.sin(2 * np.pi * np.arange(rows) / 80)
    
    for i in range(rows):
        # Use modulo to handle index wrapping
        index = int(x_wave[i]) % cols
        ripple_image[i, :] = np.roll(ripple_image[i, :], shift=index, axis=0)
    
    return ripple_image


# Fungsi untuk mengaplikasikan filter efek swirl citra
def swirl_image(image):
    # Implementasi filter efek swirl/puntiran citra
    height, width, _ = image.shape
    center_x, center_y = width // 2, height // 2
    swirl_image = np.copy(image)
    strength = 0.05  # Ubah kekuatan swirl sesuai kebutuhan

    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            distance = np.sqrt(dx ** 2 + dy ** 2)
            if distance < center_x:
                angle = np.arctan2(dy, dx)
                radius = distance
                new_x = int(center_x + radius * np.cos(angle + strength * radius))
                new_y = int(center_y + radius * np.sin(angle + strength * radius))
                if 0 <= new_x < width and 0 <= new_y < height:
                    swirl_image[y, x] = image[new_y, new_x]
    return swirl_image


# Fungsi untuk mengaplikasikan filter efek spherical citra
def spherical_image(image):
    # Dapatkan tinggi dan lebar gambar asli
    height, width = image.shape[:2]

    # Buat gambar kosong dengan ukuran yang sama
    spherical_image = np.zeros_like(image)

    # Tentukan parameter efek spherical
    center_x, center_y = width // 2, height // 2  # Pusat efek spherical
    radius = min(center_x, center_y)  # Radius efek spherical
    strength = 0.05  # Kekuatan efek spherical

    # Loop melalui setiap pixel pada citra
    for y in range(height):
        for x in range(width):
            # Hitung koordinat relatif terhadap pusat
            dx = x - center_x
            dy = y - center_y

            # Hitung jarak dari titik saat ini ke pusat
            distance = np.sqrt(dx**2 + dy**2)

            # Hitung faktor deformasi spherical
            if distance < radius:
                factor = 1 - (distance / radius) ** 2
                factor = factor ** strength

                # Hitung koordinat baru setelah efek spherical
                new_x = int(center_x + dx * factor)
                new_y = int(center_y + dy * factor)

                # Pastikan koordinat baru dalam batas citra
                if 0 <= new_x < width and 0 <= new_y < height:
                    spherical_image[y, x] = image[new_y, new_x]

    return spherical_image

# Fungsi untuk memperbarui tampilan GUI dengan citra yang diberikan
def update_display(image=None):
    if image is None:
        image = original_image
    if image is not None:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image=image)
        canvas.create_image(0, 0, anchor=tk.NW, image=image)
        canvas.image = image

# Inisialisasi GUI
root = tk.Tk()
root.title("Filter Citra")

# Buat tombol-tombol untuk mengaplikasikan filter
open_button = tk.Button(root, text="Buka Gambar", command=open_image)
shift_button = tk.Button(root, text="Penggeseran Citra", command=lambda: apply_filter(shift_image))
rotate_0_button = tk.Button(root, text="Memutar Citra (0, 0)", command=lambda: apply_filter(rotate_image_0))
rotate_button = tk.Button(root, text="Memutar Citra Sebarang Derajat", command=lambda: apply_filter(rotate_image))
rotate_full_button = tk.Button(root, text="Memutar Citra Utuh", command=lambda: apply_filter(rotate_image_full))
zoom_button = tk.Button(root, text="Perbesar Citra", command=lambda: apply_filter(zoom_image))
shrink_button = tk.Button(root, text="Pengecilan Citra", command=lambda: apply_filter(shrink_image))
flip_horizontal_button = tk.Button(root, text="Pencerminan Citra Horizontal", command=lambda: apply_filter(flip_horizontal_image))
flip_vertical_button = tk.Button(root, text="Pencerminan Citra Vertikal", command=lambda: apply_filter(flip_vertical_image))
ripple_button = tk.Button(root, text="Efek Ripple Citra", command=lambda: apply_filter(ripple_image))
swirl_button = tk.Button(root, text="Efek Swirl Citra", command=lambda: apply_filter(swirl_image))
spherical_button = tk.Button(root, text="Efek Spherical Citra", command=lambda: apply_filter(spherical_image))

# Buat canvas untuk menampilkan gambar
canvas = tk.Canvas(root, width=400, height=400)

# Tampilkan tombol-tombol dan canvas pada GUI
open_button.pack()
shift_button.pack()
rotate_0_button.pack()
rotate_button.pack()
rotate_full_button.pack()
zoom_button.pack()
shrink_button.pack()
flip_horizontal_button.pack()
flip_vertical_button.pack()
ripple_button.pack()
swirl_button.pack()
spherical_button.pack()
canvas.pack()

# Citra asli
original_image = None

root.mainloop()