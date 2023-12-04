import torch
from EDSR.src.model import edsr_django

weight_path = "resource/model_best.pt"

weight = torch.load(weight_path)

model = edsr_django.EDSR(4)

model.load_state_dict(weight)
