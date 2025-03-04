# import random
# import string
# from PIL import Image, ImageDraw, ImageFont,ImageFilter

# def generate_captcha(length=6, width=200, height=80, font_size=40, font_path="arial.ttf", distortion_level=2):
#     """
#     Generates a CAPTCHA image.

#     Args:
#         length (int): The length of the CAPTCHA text.
#         width (int): The width of the CAPTCHA image.
#         height (int): The height of the CAPTCHA image.
#         font_size (int): The font size of the CAPTCHA text.
#         font_path (str): The path to the font file (TTF).
#         distortion_level (int): Higher value = more complex.

#     Returns:
#         tuple: A tuple containing the CAPTCHA text and the PIL Image object.
#     """

#     # 1. Generate Random Text
#     characters = string.ascii_uppercase + string.digits
#     captcha_text = ''.join(random.choice(characters) for _ in range(length))

#     # 2. Create Image
#     image = Image.new('RGB', (width, height), color=(255, 255, 255))  # White background
#     draw = ImageDraw.Draw(image)

#     # 3. Load Font
#     try:
#         font = ImageFont.truetype(font_path, size=font_size)
#     except IOError:
#         print(f"Font file not found: {font_path}. Using default font.")
#         font = ImageFont.load_default()  # Use default font if specified font not found


#     # 4. Calculate Text Position
#     text_width, text_height = draw.textsize(captcha_text, font=font)
#     x = (width - text_width) / 2
#     y = (height - text_height) / 2

#     # 5. Draw Text
#     draw.text((x, y), captcha_text, fill=(0, 0, 0), font=font)  # Black text

#     # 6. Add Distortion (Wave Effect)
#     for _ in range(distortion_level):  # More iterations for stronger distortion
#         x_offset = random.randint(-10, 10)
#         y_offset = random.randint(-5, 5)
#         image = image.transform(image.size, Image.AFFINE, (1, 0.1*random.random()-0.05, x_offset, 0.1*random.random()-0.05, 1, y_offset)) # added a slight vertical shearing distortion
#         #Affine transformation to add shear and translate

#     # 7. Add Noise (Optional)
#     for _ in range(width * height // 50): # Adjust the divisor to control noise density
#       x = random.randint(0, width - 1)
#       y = random.randint(0, height - 1)
#       draw.point((x, y), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))) # added noise

#     # 8. Add Blur (Optional)
#     image = image.filter(ImageFilter.GaussianBlur(radius=1)) #Gaussian blur filter


#     return captcha_text, image



# if __name__ == "__main__":
#     captcha_text, captcha_image = generate_captcha()

#     # 9. Save or Display Image
#     captcha_image.save("captcha.png")
#     print(f"CAPTCHA text: {captcha_text}")
#     print("CAPTCHA image saved as captcha.png")


#     # Optional: Display the image (requires a viewer)
#     # captcha_image.show() #commented out by default because requires viewer



import random
import string
import io  # For in-memory image creation
from math import sin, cos, radians  # For sine wave distortion

try:
    from reportlab.pdfgen import canvas  # type: ignore # Requires reportlab
    from reportlab.lib.pagesizes import letter  # type: ignore # Standard page size
    from reportlab.lib.colors import black, white, gray, toColor # type: ignore
    from reportlab.pdfbase import pdfmetrics # type: ignore
    from reportlab.pdfbase.ttfonts import TTFont # type: ignore
except ImportError:
    print("ReportLab library is required to generate images directly in memory.  Please install it with: pip install reportlab")
    exit()


def generate_captcha(length=6, width=200, height=80, font_size=40, font_name="Helvetica", distortion_level=1):
    """
    Generates a CAPTCHA using ReportLab without PIL.

    Args:
        length (int): The length of the CAPTCHA text.
        width (int): The width of the CAPTCHA image.
        height (int): The height of the CAPTCHA image.
        font_size (int): The font size of the CAPTCHA text.
        font_name (str): Name of a font for the CAPTCHA text.  Helvetica, Times-Roman, Courier.
        distortion_level (int): The level of distortion (sine wave).
    Returns:
        tuple: A tuple containing the CAPTCHA text and the image data as bytes.
    """

    # 1. Generate Random Text
    characters = string.ascii_uppercase + string.digits
    captcha_text = ''.join(random.choice(characters) for _ in range(length))

    # 2. Create Canvas in Memory
    buffer = io.BytesIO()  # Store the PDF (which will act as our image) in memory

    c = canvas.Canvas(buffer, pagesize=(width, height))

    # 3. Set Font
    c.setFont(font_name, font_size) # Helvetica, Times-Roman, Courier


    # 4. Draw Text with Sine Wave Distortion
    text_width = c.stringWidth(captcha_text, font_name, font_size)
    x_start = (width - text_width) / 2
    y_center = height / 2

    for i, char in enumerate(captcha_text):
        # Sine wave parameters
        amplitude = 10  # Adjust for stronger/weaker waves
        frequency = 0.1  # Adjust for more/fewer waves
        phase = i * 0.5 # Make each character start at a different phase in the wave

        # Calculate displacement
        x = x_start + c.stringWidth(captcha_text[:i], font_name, font_size)  # x position of the character
        y = y_center + amplitude * sin(frequency * x + phase)  # y position with sine wave

        c.setFillColorRGB(random.random(), random.random(), random.random()) # Random color

        c.drawString(x, y, char) # Draw the character

    # 5. Add Noise (Random Lines)
    for _ in range(50):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        c.setStrokeColorRGB(random.random(), random.random(), random.random())
        c.line(x1, y1, x2, y2)


    # 6. Finish and Get Image Data
    c.showPage()
    c.save()

    buffer.seek(0)  # Reset the buffer's position to the beginning
    image_data = buffer.read()  # Get the image data as bytes


    return captcha_text, image_data

if __name__ == "__main__":
    captcha_text, image_data = generate_captcha() # Can specify font

    # Save to PDF file (or other format with appropriate changes)
    with open("captcha.pdf", "wb") as f:  # Change to .png with appropriate library
        f.write(image_data)

    print(f"CAPTCHA text: {captcha_text}")
    print("CAPTCHA image saved as captcha.pdf")