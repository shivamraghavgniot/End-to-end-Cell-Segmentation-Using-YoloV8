import os,sys
import yaml
from cellSegmentation.utils.main_utils import read_yaml_file
from cellSegmentation.logger import logging
from cellSegmentation.exception import AppException
from cellSegmentation.entity.config_entity import ModelTrainerConfig
from cellSegmentation.entity.artifacts_entity import ModelTrainerArtifact
import shutil
import logging
from pathlib import Path

def extract_zip(zip_path):
        shutil.unpack_archive(zip_path)

class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            logging.info("Extracting data")
            extract_zip("data.zip")
            os.remove("data.zip")

            os.system(f"yolo task=detect mode=train model={self.model_trainer_config.weight_name} data=data.yaml epochs={self.model_trainer_config.no_epochs} save=true")

            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)

            # Replace 'cp' with 'copy'
            shutil.copy("runs\\detect\\train\\weights\\best.pt", self.model_trainer_config.model_trainer_dir)
            
            # copy runs folder to just 
            source_directory = "runs"
            target_directory = "runs_result"
            # os.makedirs(target_directory, exist_ok=True)

            if not os.path.exists(target_directory):
                # Copy the entire directory
                shutil.copytree(source_directory, target_directory)
            else:
                shutil.rmtree(target_directory)
                shutil.copytree(source_directory, target_directory)

            #removing unneccessary files.
            os.remove("yolov8n.pt")
            shutil.rmtree("train", ignore_errors=True)
            shutil.rmtree("valid", ignore_errors=True)
            shutil.rmtree("test", ignore_errors=True)
            os.remove("data.yaml")

            # remove runs folder as in this folder train is created with a new suffix everytime it runs training. but we only have to pick train folder.
            shutil.rmtree("runs", ignore_errors=True)
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path="artifacts/model_trainer/best.pt",
            )

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise AppException(e, sys)