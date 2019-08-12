import mimetypes
import os
from urllib.parse import urlparse

from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)


GOOD_BOY_URL = "https://petgroomingclub.com/wp-content/uploads/2019/05/20-Strange-Cat-Behaviors-Explained.jpg"
BAD_BOY_URL = "https://static.boredpanda.com/blog/wp-content/uploads/2014/08/cat-furniture-creative-design-1.jpg"

@app.route("/", methods=["GET", "POST"])
def reply_whatsapp():
    num_media = int(request.values.get("NumMedia"))
    media_files = []
    for idx in range(num_media):
        media_url = request.values.get(f'MediaUrl{idx}')
        mime_type = request.values.get(f'MediaContentType{idx}')
        media_files.append((media_url, mime_type))

        req = requests.get(media_url)
        file_extension = mimetypes.guess_extension(mime_type)
        media_sid = os.path.basename(urlparse(media_url).path)

        with open(f"app_data/{media_sid}{file_extension}", 'wb') as f:
            f.write(req.content)

    response = MessagingResponse()
    if not num_media:
        msg = response.message("Hola hola! Soy GatoBot, envíame una imagen del artículo que andas buscando!")
        msg.media(GOOD_BOY_URL)
    else:
        msg = response.message("Esto es lo más cercano que encontramos!")
        msg.media(BAD_BOY_URL)
    return str(response)


if __name__ == "__main__":
    app.run()
