import torch
from transformers import AutoTokenizer

def load_model():

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    #load model
    model = torch.load('knave_model/kcelectra_trained_model.pt', map_location=device)
    model.eval()

    return model

# 토크나이저

def knave_tokenizer():
    MODEL_NAME = "beomi/KcELECTRA-base"
    okenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    return okenizer
