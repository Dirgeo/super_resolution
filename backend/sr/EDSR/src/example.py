import torch
from torch import nn
from torchvision import transforms
import numpy as np

from PIL import Image
import imageio.v3 as imageio

from model import EDSR

import argparse
import os

def _np2Tensor(img):
    rgb_range = 255
    np_transpose = np.ascontiguousarray(img.transpose((2, 0, 1)))
    tensor = torch.from_numpy(np_transpose).float()
    tensor.mul_(rgb_range / 255)

    return tensor

class Inference:

    def __init__(self, model) -> None:
        self.model = model

    # x 是PIL.Image对象
    # return也是PIL.Image对象
    def inference(self, x):
        img = _np2Tensor(x)
        img = img.unsqueeze(0)
        res = self.model.forward(img)
        normalized = res[0].mul(255 / 255)
        tensor_cpu = normalized.byte().permute(1, 2, 0).cpu()
        imageio.imwrite("./image/test.jpg", tensor_cpu.detach().numpy())

        return res
    
    def inferenceAndSave(self, x, save_path):
        res = self.inference(x)
        res.save(save_path)

model = EDSR(4)
weight = torch.load("../models/edsr_baseline_x4-6b446fab.pt")
model.load_state_dict(weight)
model.eval()

inference = Inference(model)

img_path = "../test/img_003_SRF_4_HRx4.png"
# img = Image.open(img_path).convert("RGB")
img = imageio.imread(img_path)
print(type(img))

inference.inferenceAndSave(img, "./image/submean_head.jpg")

# def inference():
#     pass

# def main(args):
#     pass

# if __name__ == "__main__":

#     parser = argparse.ArgumentParser(description='inference')

#     parser.add_argument('--weight', type=str, default='../models/edsr_baseline_x4-6b446fab.pt',
#                     help='model weight directory')
#     parser.add_argument('--LR_image', type=str, default='../test/img_097_SRF_4_HRx4.png',
#                     help='LR_image path for inference')
#     parser.add_argument('--HR_image', type=str, default='../test/img_097_SRF_4_HR.png',
#                     help='HR_image path for inference')
#     parser.add_argument('--save', type=str, default='../experiment/tmp',
#                     help='save path for inference result')
#     args = parser.parse_args()
#     main(args)