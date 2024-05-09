import sys
sys.path.append("..")
from models.svm import Svm

def init_models(model_manager):
    model_manager.add_model(Svm("svm"))
