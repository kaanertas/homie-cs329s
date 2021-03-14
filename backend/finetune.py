from pymongo import MongoClient
from model import Model
import numpy as np
import wget
import os
import cv2

connection_string = 'mongodb+srv://max:max_is_a_b3ast@cs329s.gefiw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

str_to_id = {"Swimming pool":                 23,
"Bed":                            1,
"Pillow":                          16,
"Kitchen & dining room table":     12,
"Countertop":                      6,
"Sofa bed":                        21,
"Couch":                           5,
"Sink":                            20,
"Porch":                           17,
"Stairs":                          22,
"Television":                      24,
"Fireplace":                       8,
"Washing machine":                 28,
"Toilet":                          25,
"Oven":                            15,
"Mirror":                          14,
"Billiard table":                  2,
"Microwave oven":                  13,
"Refrigerator":                    18,
"Fountain":                        9,
"Gas stove":                       10,
"Coffeemaker":                     4,
"Bathtub":                         0,
"Wine rack":                       29,
"Jacuzzi":                         11,
"Tree house":                      27,
"Ceiling fan":                     3,
"Shower":                           19,
"Towel":                            26,
"Dishwasher":                       7}

image_path = 'images/'
n = 5

def getData():
    client = MongoClient(connection_string)
    db = client.cs329s
    misclassifieds = db.misclassifieds.find({})
    properties = db.properties.find({})
    return misclassifieds, properties

def format_data(old_model, misclassifieds, properties):
    property_map = {str(p['_id']): p for p in properties}
    for example in misclassifieds:
        property_id = example['property']
        prop = property_map[str(property_id)]
        fp = set(example['false_positives'])
        fn = {str_to_id[ex]: (0, -1) for ex in example['false_negatives']}
        new_annotations = []
        for photo_url in prop['photo_urls']:
            wget.download(photo_url, image_path)
            filename = image_path + os.path.basename(photo_url)
            img = cv2.imread(filename)
            outputs = old_model.predictor(img)
            prev_preds = outputs["instances"][:n]
            print(prev_preds)

def main():
    misclassifieds, properties = getData()
    # old_model = Model()
    # ft_data = format_data(old_model, misclassifieds, properties)
    # finetune(old_model, misclassifieds)

if __name__ == '__main__':
    main()
