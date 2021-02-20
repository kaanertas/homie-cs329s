from flask import Flask, request, jsonify
import urllib.request
from model import Model
import pickle
# import model

app = Flask(__name__)

@app.route('/predict',methods=['POST'])
def predict():

	#request: url, no of preds

	img_url = request.json['img_url']
	file_name = 'uploaded.jpg'
	urllib.request.urlretrieve(img_url, file_name)
	# no_preds = request.json['no_preds']
	output = m.predict(file_name, 7)
	#print(output)
	# boxes, confidence, predicted_classes = output
	predicted_classes = output

	return jsonify(preds=predicted_classes,img_url=img_url)

if __name__ == "__main__":
	m = Model()
	app.run(debug=True)