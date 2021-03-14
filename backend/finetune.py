from pymongo import MongoClient
from detectron2.config import get_cfg
import numpy as np
import wget
import os
import cv2
import json
from detectron2.structures import BoxMode
from detectron2.data import MetadataCatalog, DatasetCatalog
from sklearn.model_selection import train_test_split
from shutil import copyfile
from detectron2.engine import DefaultTrainer, DefaultPredictor

from detectron2.utils.logger import setup_logger

setup_logger()

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

train_path = 'train/'
val_path = 'val/'
json_file_name = 'instances_default.json'
n = 5

def load_json_labels(image_folder):
    """
    Returns Detectron2 style labels of images (list of dictionaries) in image_folder based on JSON label file in image_folder.

    Note: Requires JSON label to be in image_folder. See get_image_dicts().

    Params
    ------
    image_folder (str): target folder containing images
    """
    # Get absolute path of JSON label file
    for file in os.listdir(image_folder):
      if file.endswith(".json"):
        json_file = os.path.join(image_folder, file)

    # Check to see if json_file exists
    assert json_file, "No .json label file found, please make one with get_image_dicts()"

    with open(json_file, "r") as f:
      img_dicts = json.load(f)

    # Convert bbox_mode to Enum of BoxMode.XYXY_ABS (doesn't work loading normal from JSON)
    for img_dict in img_dicts:
      for annot in img_dict["annotations"]:
        annot["bbox_mode"] = BoxMode.XYXY_ABS

    return img_dicts

def getData():
    client = MongoClient(connection_string)
    db = client.cs329s
    misclassifieds = db.misclassifieds.find({})
    properties = db.properties.find({})
    return misclassifieds, properties

def addInstance(annotations, instance):
    for j in range(len(instance)):
        a = {}
        a['bbox'] = list(instance.pred_boxes[j])[0].tolist()
        a["bbox_mode"] = BoxMode.XYXY_ABS
        a['category_id'] = int(instance.pred_classes[j])
        annotations.append(a)

def combineAnnotations(new_annotations, fn, filenames, counter, img_dict):
    for i in range(len(new_annotations)):
        elem = {}
        elem['file_name'] = filenames[i]
        elem['image_id'] = counter - len(new_annotations) + i
        h, w = new_annotations[i].image_size
        elem['height'] = h
        elem['width'] = w
        annotations = []
        addInstance(annotations, new_annotations[i])
        for neg in fn:
            conf, instance, ind = fn[neg]
            if ind == i:
                addInstance(annotations, instance)
        elem['annotations'] = annotations
        img_dict.append(elem)

def registerData(dataset_name):
    # Register the datasets with Detectron2's DatasetCatalog, which has space for a lambda function to preprocess it
    DatasetCatalog.register(dataset_name, lambda dataset_name=dataset_name: load_json_labels(dataset_name))

    # Create the metadata for our dataset (the main thing being the classnames we're using)
    MetadataCatalog.get(dataset_name).set(thing_classes=list(str_to_id.keys()))

def saveJson(img_dict, directory):
    with open(directory + 'instances_default.json', 'w') as f:
        json.dump(img_dict, f)

def format_data(cfg, misclassifieds, properties):
    property_map = {str(p['_id']): p for p in properties}
    counter = 0
    img_dict = []
    predictor = DefaultPredictor(cfg)
    for example in misclassifieds:
        property_id = example['property']
        prop = property_map[str(property_id)]
        fp = set([str_to_id[ex] for ex in example['false_positives']])
        fn = {str_to_id[ex]: (0,None, -1) for ex in example['false_negatives']}
        fn[21] = (0, None, -1)
        new_annotations = []
        filenames = []
        for i in range(len(prop['photo_urls'])):
            counter += 1
            photo_url = prop['photo_urls'][i]
            wget.download(photo_url, train_path)
            print()
            filename = train_path + os.path.basename(photo_url)
            filenames.append(filename)
            img = cv2.imread(filename)
            outputs = predictor(img)
            prev_preds = outputs["instances"][:n]
            for false in fp:
                prev_preds = prev_preds[prev_preds.pred_classes != false]
            # prev_preds = [prev_preds[j] for j in range(len(prev_preds)) if prev_preds.pred_classes[j] not in fp]
            for neg in fn:
                candidates = outputs["instances"][outputs["instances"].pred_classes == neg]
                if len(candidates) != 0:
                    fn[neg] = max(fn[neg], (candidates.scores[0],candidates[0], i))
            new_annotations.append(prev_preds)
        combineAnnotations(new_annotations, fn, filenames, counter, img_dict)
    train_img_dict, val_img_dict = train_test_split(img_dict, test_size=0.33)
    for i in range(len(val_img_dict)):
        if os.path.exists(val_path + os.path.basename(val_img_dict[i]['file_name'])):
            copyfile(val_img_dict[i]['file_name'], val_path + os.path.basename(val_img_dict[i]['file_name']))
        val_img_dict[i]['file_name'] = val_path + os.path.basename(val_img_dict[i]['file_name'])
    saveJson(train_img_dict, train_path)
    saveJson(val_img_dict, val_path)
    registerData(train_path[:-1])
    registerData(val_path[:-1])
    print(len(train_img_dict))
    print(len(val_img_dict))
    print(val_img_dict[0])

def finetune(cfg):
    cfg.DATASETS.TRAIN = (train_path[:-1],)
    cfg.DATASETS.TEST = (val_path[:-1],)
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.SOLVER.IMS_PER_BATCH = 2
    cfg.SOLVER.BASE_LR = 0.00125
    cfg.SOLVER.MAX_ITER = 10
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
    cfg.MODEL.RETINANET.NUM_CLASSES = len(str_to_id)
    cfg.OUTPUT_DIR = './'
    #import pdb; pdb.set_trace()
    trainer = DefaultTrainer(cfg)
    trainer.resume_or_load(resume=False)
    trainer.train()

def main():
    misclassifieds, properties = getData()
    cfg = get_cfg()
    cfg.merge_from_file("./retinanet_model_final_config.yaml")
    cfg.MODEL.WEIGHTS = "./retinanet_model_final.pth"
    format_data(cfg, misclassifieds, properties)
    finetune(cfg)

if __name__ == '__main__':
    main()
