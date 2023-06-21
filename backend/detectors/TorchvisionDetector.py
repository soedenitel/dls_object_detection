from typing import Optional, Any
from PIL.Image import Image
import torch
from torchvision.models import WeightsEnum
from torchvision.transforms.functional import pil_to_tensor, to_pil_image
from torchvision.utils import draw_bounding_boxes

from backend.detectors.AbstractDetector import AbstractDetector
from backend.detectors.AbstractLabelsToNamesConverter import AbstractLabelsToNamesConverter


class TorchvisionDetector(AbstractDetector):
    def __init__(
            self,
            network: Any,
            weights: Optional[WeightsEnum],
            labels_to_names_converter: AbstractLabelsToNamesConverter,
            probability_threshold: float,
            labels_threshold: tuple[str] = ("dog", "cat"),
            image_normalization_delimiter: float = 255.0,
            use_cuda: bool = True
    ):
        super(TorchvisionDetector, self).__init__(labels_to_names_converter, probability_threshold, labels_threshold)
        self.__device = torch.device("cuda" if use_cuda and torch.cuda.is_available() else "cpu")

        self.__object_detection_model: Any = network(weights=weights)
        self.__object_detection_model.to(self.__device)

        self.__image_normalization_delimiter: Optional[float] = \
            image_normalization_delimiter if image_normalization_delimiter else None

    def process(self, picture: Image, markup_image: bool = True) -> Optional[tuple[dict, Optional[Image], list]]:
        """
        Детектировать объекты на исходном изображении
        :param picture: исходное изображение
        :param markup_image: нужно ли делать разметку на исходном изображении
        :return: tuple[словарь результатов, исходное изображение с Bounding Box'ми, названия детектированных классов]
        """
        self._object_detection_model.eval()
        with torch.no_grad():
            picture_tensor = pil_to_tensor(picture).unsqueeze(0).to(self._device)

            if self._image_normalization_delimiter:
                predictions_labels = self._cut_off(
                    self._object_detection_model(picture_tensor / self._image_normalization_delimiter)[0]
                )
            else:
                predictions_labels = self._cut_off(self._object_detection_model(picture_tensor)[0])

            if predictions_labels is None:
                return None

            return (
                predictions_labels[0],

                self._pil_image_with_detections(
                    picture_tensor.squeeze(), predictions_labels[0]
                ) if markup_image else None,

                predictions_labels[1]
            )

    @property
    def _object_detection_model(self) -> torch.nn.Module:
        return self.__object_detection_model

    @property
    def _image_normalization_delimiter(self) -> float:
        return self.__image_normalization_delimiter

    @property
    def _device(self):
        return self.__device

    def _cut_off(self, predictions: dict) -> Optional[tuple[dict, list]]:
        result = dict()
        result["boxes"] = predictions["boxes"][predictions["scores"] > self._probability_threshold]
        result["labels"] = predictions["labels"][predictions["scores"] > self._probability_threshold]
        result["scores"] = predictions["scores"][predictions["scores"] > self._probability_threshold]

        result_labels = list()
        result_indices = list()

        for i, name in enumerate(self._labels_to_names_converter(result["labels"].numpy())):
            if name in self._labels_threshold:
                result_labels.append(name)
                result_indices.append(i)

        if len(result_labels) == 0:
            return None

        result["boxes"] = result["boxes"][result_indices]
        result["labels"] = result["labels"][result_indices]
        result["scores"] = result["scores"][result_indices]

        return result, result_labels

    @staticmethod
    def _pil_image_with_detections(source_image: torch.Tensor, predictions: dict) -> Image:
        return to_pil_image(
            draw_bounding_boxes(
                image=source_image,
                boxes=predictions["boxes"],
                labels=[f"Probability: {prob:.2f}" for prob in predictions["scores"].numpy()],
                colors="red",
                width=2
            )
        )
