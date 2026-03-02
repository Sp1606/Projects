import cv2
import numpy as np
import random
import string
import os
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from PIL import Image, ImageTk

# Generate random CAPTCHA text
def generate_captcha_text(length=5):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# Add noise to CAPTCHA
def add_noise(image):
    noise = np.random.randint(0, 50, image.shape, dtype='uint8')
    return cv2.add(image, noise)

# Add background patterns
def add_background_pattern(image):
    rows, cols, _ = image.shape
    for i in range(0, rows, 20):
        cv2.line(image, (0, i), (cols, i), (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)), 1)
    return image

# Generate CAPTCHA image
def generate_captcha_image(text, width=200, height=80, difficulty=1):
    image = np.ones((height, width, 3), dtype='uint8') * 255
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    thickness = 3
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]

    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2
    angle = random.randint(-15, 15)
    M = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1)

    cv2.putText(image, text, (text_x, text_y), font, font_scale, (0, 0, 0), thickness)
    image = cv2.warpAffine(image, M, (width, height))

    if difficulty >= 1:
        image = add_background_pattern(image)
    if difficulty >= 2:
        image = add_noise(image)

    return image

# Save and display CAPTCHA
def save_and_display_captcha():
    global captcha_text
    captcha_text = generate_captcha_text()
    image = generate_captcha_image(captcha_text, difficulty=2)
    filename = "captcha.png"
    cv2.imwrite(filename, image)

    # Convert OpenCV image to Tkinter-compatible format
    img = Image.open(filename)
    img = ImageTk.PhotoImage(img)
    captcha_label.config(image=img)
    captcha_label.image = img  # Store reference

# Verify user input
def verify_captcha():
    user_input = captcha_entry.get().strip()
    if user_input.lower() == captcha_text.lower():
        messagebox.showinfo("Success", "CAPTCHA verified successfully!")
    else:
        messagebox.showerror("Error", "CAPTCHA verification failed. Try again!")

# Create GUI window
root = Tk()
root.title("CAPTCHA Generator")
root.geometry("300x250")

Label(root, text="Generated CAPTCHA:", font=("Arial", 12)).pack()
captcha_label = Label(root)
captcha_label.pack()

Label(root, text="Enter CAPTCHA:", font=("Arial", 12)).pack()
captcha_entry = Entry(root, font=("Arial", 12))
captcha_entry.pack()

Button(root, text="Verify CAPTCHA", command=verify_captcha, font=("Arial", 12), bg="green", fg="white").pack(pady=5)
Button(root, text="Refresh CAPTCHA", command=save_and_display_captcha, font=("Arial", 12), bg="blue", fg="white").pack(pady=5)

save_and_display_captcha()  # Generate initial CAPTCHA

root.mainloop()
