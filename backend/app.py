from flask import Flask, request, jsonify
import urllib.request
from model import Model
import pickle
import cloudinary
import cloudinary.uploader

cloudinary.config(
  cloud_name = 'dlyjr71kx',  
  api_key = '833231282457385',  
  api_secret = 'LEFOthdVyM1Nuyot1fxtAW-xXaw'  
)

app = Flask(__name__)

@app.route('/predict',methods=['POST'])
def predict():
	#request: url, no of preds
	img_urls = request.json['img_urls']
	output_urls = []
	preds = []
	scores = []

	for img_url in img_urls:

		file_name = 'input.jpg'
		urllib.request.urlretrieve(img_url, file_name)
		# no_preds = request.json['no_preds']
		output = m.predict(file_name, 0.2, 'output.jpg')
		#print(output)
		# boxes, confidence, predicted_classes = output
		predicted_classes, confidence_scores = output

		upload_res = cloudinary.uploader.upload("output.jpg")

		preds.append(predicted_classes)
		scores.append(confidence_scores)
		output_urls.append(upload_res['url'])

	preds_consolidated = []
	for pred in preds:
		preds_consolidated += pred

	preds_consolidated = list(set(preds_consolidated))
	print("Here is list of preds: ", preds_consolidated)

	return jsonify(preds=preds,scores=scores,img_urls=img_urls,output_urls=output_urls,preds_consolidated=preds_consolidated)

if __name__ == "__main__":
	m = Model()
	app.run('0.0.0.0', 5000)
