from clover.apps.vision.adapter.outbound.resource_adapters.local_yolo_dataset_adapter import LocalYoloDatasetAdapter
from vision.app.ports.input.face_train_use_case import FaceTrainUseCase
from vision.app.ports.output.face_dataset_port import FaceDatasetPort
from vision.app.use_cases.face_train_interactor import FaceTrainInteractor


def get_face_dataset_port() -> FaceDatasetPort:
    return LocalYoloDatasetAdapter()


def get_face_train_use_case() -> FaceTrainUseCase:
    return FaceTrainInteractor(dataset_port=get_face_dataset_port())
