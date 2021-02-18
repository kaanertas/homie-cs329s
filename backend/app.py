from flask import Flask, request, jsonify
import pickle
# import model

app = Flask(__name__)

@app.route('/predict',methods=['POST'])
def predict():

	#request: url, no of preds

	img_url = request.json['img_url']
	# no_preds = request.json['no_preds']
	# output = m.predict(img_url,no_preds)
	# boxes, confidence, predicted_classes = output
	predicted_classes = [1,2]

	return jsonify(preds=predicted_classes,img_url=img_url)

if __name__ == "__main__":
	# m = model.Model()
	app.run(debug=True)