import os
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights

from backend.detectors.CocoLabelsToNamesConverter import CocoLabelsToNamesConverter
from backend.detectors.TorchvisionDetector import TorchvisionDetector


class FasterRCnnResnet50FpnV2Detector(TorchvisionDetector):
    def __init__(self):
        super(FasterRCnnResnet50FpnV2Detector, self).__init__(
            network=fasterrcnn_resnet50_fpn_v2,
            weights=FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT,
            labels_to_names_converter=CocoLabelsToNamesConverter(
                os.path.join("backend", "annotations", "instances_val2017.json")
            ),
            probability_threshold=0.4
        )
