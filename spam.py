# from flask import Flask, render_template, url_for, flash, redirect
from flask import Flask, request, jsonify
import joblib
# import sklearn
# from flask import request
# import numpy as np

# Load the Multinomial Naive Bayes' pkl model and TF|IDF Vectorizer using joblib
classifier = joblib.load('SMS_Detection_Model.pkl')
cv = joblib.load('TF_IDF.pkl')

# app = Flask(__name__)


# @app.route('/predict',methods=['POST'])
def is_spam_predict(msg):
	# if request.method == 'POST':
	# 	request_data = request.get_json()
	# 	msg = request_data['msg']
		# SMS = request.form['SMS']
	data = [msg]
	vectorized = cv.transform(data).toarray()
	my_prediction = classifier.predict(vectorized)
	# print(my_prediction)
	if my_prediction == 1:
		return True
		# return 'spam'
	elif my_prediction == 0:
		return False


# if __name__ == '__main__':
# 	# Use below for local flask deployment
# 	app.run(debug=True)
