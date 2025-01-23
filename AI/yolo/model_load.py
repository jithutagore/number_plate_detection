from pathlib import Path
import sys
import os
import torch


from AI.yolo.models.common import DetectMultiBackend


def load_model(weights,data):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = DetectMultiBackend(weights, device=device, dnn=True, data=data, fp16=False)
    stride, names, pt = model.stride, model.names, model.pt
    return model,stride,names,pt
