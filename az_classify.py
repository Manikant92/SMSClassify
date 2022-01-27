import os.path
from pprint import pprint
import time
from io import BytesIO
from random import random
import uuid

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
import azure.cognitiveservices.vision.contentmoderator.models
from msrest.authentication import CognitiveServicesCredentials

CONTENT_MODERATOR_ENDPOINT = "https://contentclassify.cognitiveservices.azure.com/"
subscription_key = "Azure ContentModerator API KEY"

client = ContentModeratorClient(endpoint=CONTENT_MODERATOR_ENDPOINT, credentials=CognitiveServicesCredentials(subscription_key))

TEXT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "text_files")


# text = "Is this a grabage email abcdef@abcd.com, phone: 4255550111, IP: 255.255.255.255, 1234 Main Boulevard, Panapolis WA 96555." \
#        "fuckoff is the profanity here. Is this information PII? phone 2065550111"


def az_classify_text():
    with open(os.path.join(TEXT_FOLDER, 'content_moderator_text_moderation.txt'), "rb") as text_fd:
        screen = client.text_moderation.screen_text(
            text_content_type="text/plain",
            text_content=text_fd,
            language="eng",
            autocorrect=False,
            classify=True
        )
# assert isinstance(screen, Screen)
    response = screen.as_dict()
    class_cat_resp = response['classification']
    cat1 = class_cat_resp['category1']['score']*100
    cat2 = class_cat_resp['category2']['score']*100
    cat3 = class_cat_resp['category3']['score']*100
    is_rev_recom = class_cat_resp['review_recommended']
    # print(class_cat_resp)
    if cat1 >= 50 or cat3 >= 50 or is_rev_recom:
        return 'Abusive'
    else:
        return 'Good'

