__author__ = 'amin'

import base64
from PIL import Image
import cStringIO


def canvas2image(canvas):
    canvas = canvas.split(',')[1]
    pic = cStringIO.StringIO()
    image_string = cStringIO.StringIO(base64.b64decode(canvas))
    image = Image.open(image_string)
    image.save(pic, image.format, quality = 100)
    pic.seek(0)

    del canvas
    del pic

    return image