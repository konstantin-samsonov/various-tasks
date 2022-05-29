"""
Translation of text using Google Cloud Platform
"""

from google.oauth2 import service_account
from google.cloud import translate_v2 as translate
import six

key = '../credentials/grebi-nu-664c0e090534.json'
credentials = service_account.Credentials.from_service_account_file(key)


def translate_text(text, target_language='ru', source_language='en'):
    translate_client = translate.Client(credentials=credentials)

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language, source_language=source_language)

    return result["translatedText"]