from qrcode.main import QRCode
import io
from flask import make_response


class GenerateQr():
    def __init__(self):
        pass

    def generate_qr(self, link):
        qr = QRCode(
        version=1,
        box_size=10,
        border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        buffer = io.BytesIO()
        img.save(buffer)
        buffer.seek(0)
        return make_response(buffer.getvalue())