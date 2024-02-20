import qrcode
from io import BytesIO


def generate_qr_code(date, unit_code):
    # Combine date and unit code to create a unique string
    data = f"Date: {date}\nUnit Code: {unit_code}"

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add the data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the image to bytes
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Return the image data
    return buffer.getvalue()
