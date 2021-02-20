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

	img_url = request.json['img_url']
	file_name = 'input.jpg'
	urllib.request.urlretrieve(img_url, file_name)
	# no_preds = request.json['no_preds']
	output = m.predict(file_name, 7, 'output.jpg')
	#print(output)
	# boxes, confidence, predicted_classes = output
	predicted_classes = output

	upload_res = cloudinary.uploader.upload("output.jpg")
	output_url = upload_res['url']

	return jsonify(preds=predicted_classes,img_url=img_url,output_url=output_url)

if __name__ == "__main__":
	m = Model()
	app.run(debug=True)
