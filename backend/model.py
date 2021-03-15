import torch, torchvision
import detectron2
from detectron2.utils.logger import setup_logger
import numpy as np
import cv2
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog


class Model:
    def __init__(self):
        self.device = torch.device("cpu")
        self.cfg = get_cfg()
        self.cfg.MODEL.DEVICE = 'cpu'
        self.cfg.merge_from_file("./retinanet_model_final_config.yaml")
        self.cfg.MODEL.WEIGHTS = "./retinanet_model_final.pth"
        self.predictor = DefaultPredictor(self.cfg)
        self.target_classes =  ['Bathtub', 'Bed', 'Billiard table', 'Ceiling fan', 'Coffeemaker', 'Couch', 'Countertop', 'Dishwasher',
                  'Fireplace','Fountain', 'Gas stove', 'Jacuzzi', 'Kitchen & dining room table', 'Microwave oven',
                  'Mirror', 'Oven', 'Pillow', 'Porch', 'Refrigerator', 'Shower', 'Sink', 'Sofa bed', 'Stairs',
                  'Swimming pool', 'Television', 'Toilet', 'Towel', 'Tree house', 'Washing machine', 'Wine rack']

    def predict(self, input_img_pth, confidence_threshold, output_img_pth):
        img = cv2.imread(input_img_pth)
        # cv2.imshow('image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        outputs = self.predictor(img)
        thresh_ind = np.sum([True if x>confidence_threshold else False for x in list(outputs["instances"].scores)])
        formatted = zip(list(outputs["instances"][:thresh_ind].pred_classes),list(outputs["instances"][:thresh_ind].scores))
        seen = set()
        formatted_dedup = []
        for c, score in formatted:
            if c.numpy().item() not in seen:
                formatted_dedup.append((c.numpy().item(),score))
            seen.add(c.numpy().item())
        pred_classes = [self.target_classes[c] for c,sc in formatted_dedup]
        scores = [round(sc.numpy().item(),2) for c,sc in formatted_dedup]
        # print(outputs)
        visualizer = Visualizer(img_rgb=img[:, :, ::-1],
                                metadata=MetadataCatalog.get(self.cfg.DATASETS.TEST[0]).set(thing_classes=self.target_classes),
                                scale=0.7)
        # Draw the models predictions on the target image
        v = visualizer.draw_instance_predictions(outputs["instances"][:thresh_ind].to("cpu"))
        output_img = v.get_image()[:, :, ::-1]
        #print(output_img)
        cv2.imwrite(output_img_pth, output_img)

        return pred_classes, scores



