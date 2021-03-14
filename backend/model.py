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

    def predict(self, input_img_pth, num_amenities, output_img_pth):
        img = cv2.imread(input_img_pth)
        # cv2.imshow('image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        outputs = self.predictor(img)
        formatted = zip(list(outputs["instances"][:num_amenities].pred_classes),list(outputs["instances"][:num_amenities].scores))
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
        v = visualizer.draw_instance_predictions(outputs["instances"][:num_amenities].to("cpu"))
        output_img = v.get_image()[:, :, ::-1]
        #print(output_img)
        cv2.imwrite(output_img_pth, output_img)

        return pred_classes, scores


# TARGET_CLASSES = ['Bathtub', 'Bed', 'Billiard table', 'Ceiling fan', 'Coffeemaker', 'Couch', 'Countertop', 'Dishwasher',
#                   'Fireplace','Fountain', 'Gas stove', 'Jacuzzi', 'Kitchen & dining room table' 'Microwave oven',
#                   'Mirror', 'Oven', 'Pillow', 'Porch', 'Refrigerator', 'Shower', 'Sink', 'Sofa bed', 'Stairs',
#                   'Swimming pool', 'Television', 'Toilet', 'Towel', 'Tree house', 'Washing machine', 'Wine rack']
#
# def load_model():
#     device = torch.device("cpu")
#     cfg = get_cfg()
#     cfg.MODEL.DEVICE = 'cpu'
#     cfg.merge_from_file("./retinanet_model_final_config.yaml")
#     cfg.MODEL.WEIGHTS = "./retinanet_model_final.pth"
#     predictor = DefaultPredictor(cfg)
#     return predictor, cfg
#
# def run_inference(predictor, cfg):
#     img = cv2.imread('test.jpg')
#     # cv2.imshow('image', img)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
#     outputs = predictor(img)
#     # print(outputs)
#     num_amenities = 7
#     visualizer = Visualizer(img_rgb=img[:, :, ::-1], metadata=MetadataCatalog.get(cfg.DATASETS.TEST[0]).set(thing_classes=TARGET_CLASSES), scale=0.7)
#     # Draw the models predictions on the target image
#     v = visualizer.draw_instance_predictions(outputs["instances"][:num_amenities].to("cpu"))
#     output_img = v.get_image()[:, :, ::-1]
#     print(output_img)
#     cv2.imwrite('output.jpg', output_img)
#
# def main():
#     predictor, cfg = load_model()
#     run_inference(predictor, cfg)
#
# if __name__ == "__main__":
#     main()



