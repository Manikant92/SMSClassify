from flask import Flask, request, jsonify
from spam import is_spam_predict
from az_classify import az_classify_text
from gcp_classify import gcp_classify_text
import os

app = Flask(__name__)


def sms_wrapper(msg):
    msg_lst = msg.split(' ')
    gcp_class = 'Normal'
    is_spam = is_spam_predict(msg)
    az_class = az_classify_text()
    if len(msg_lst) >= 20:
        gcp_class = gcp_classify_text(text_content=msg)
    if is_spam:
        if gcp_class == 'Finance':
            return 'Spam'
        elif az_class == 'Abusive':
            return 'Spam'
        elif gcp_class == 'Promotions':
            return 'Spam'
        else:
            return 'Spam'
    elif not is_spam:
        # if az_class == 'Adult':
        #     return 'Adult'
        if gcp_class == 'Adult' and az_class == 'Abusive':
            return 'Adult'
        elif gcp_class == 'Promotions' and az_class == 'Abusive':
            return 'Adult'
        elif az_class == 'Abusive':
            return 'Adult'
        elif gcp_class ==  'Normal' and az_class == 'Good':
            return 'Normal'
        elif gcp_class == 'Normal':
            return 'Normal'
        elif gcp_class == 'Promotions':
            return 'Promotions'
        else:
            return 'Normal'


@app.route('/smscategory', methods=['POST'])
def sms_category():
    if request.method == 'POST':
        try:
            request_data = request.get_json()
            msg = request_data['msg']
            TEXT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "text_files")
            with open(os.path.join(TEXT_FOLDER, 'content_moderator_text_moderation.txt'), "w") as f:
                f.write(msg)
            category = sms_wrapper(msg)
            return jsonify({'classification': category})
        except Exception as e:
            return jsonify({'classification': 'Normal' + str(e)})


if __name__ == '__main__':
    app.run()
