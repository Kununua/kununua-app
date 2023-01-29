import base64
import urllib.parse

def encode_image(image_url):
    
    decoded_image_url = urllib.parse.unquote(image_url)
    
    if decoded_image_url.startswith("/"):
        decoded_image_url = decoded_image_url[1:]
    
    with open(decoded_image_url, "rb") as img:
        encoded_image = base64.b64encode(bytes(img.read()))
        return encoded_image.decode("utf-8")