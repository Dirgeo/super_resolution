from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
import json

import base64
from PIL import Image
import io

import numpy as np

from models.common.edsr import model

import torch
import imageio.v3 as imageio

def _np2Tensor(img):
    rgb_range = 255
    np_transpose = np.ascontiguousarray(img.transpose((2, 0, 1)))
    tensor = torch.from_numpy(np_transpose).float()
    tensor.mul_(rgb_range / 255)

    return tensor

# Create your views here.

# 推理img图片，并return一个推理后的图片，这里默认scale为4
# x: numpy.array HWC
# return res:numpy.array HWC
def inference(x):
    img = _np2Tensor(x)
    img = img.unsqueeze(0)
    res = model.forward(img)
    normalized = res[0]
    tensor_cpu = normalized.byte().permute(1, 2, 0).cpu()
    return tensor_cpu.detach().numpy()

def check_b64(b64):
    while len(b64) % 4 != 0:
        b64 = b64 + "="
    return b64

@require_http_methods(['POST'])
def edsr(request):

    res = {
        "state": "error",
        "data": "",
    }

    b64 = request.POST["source"]

    # 解码Base64数据
    # b64 = check_b64(b64)
    decoded_data = base64.b64decode(b64)

    bin_stream = io.BytesIO(decoded_data)

    img = imageio.imread(bin_stream)

    if img.shape[2] != 3:
        res["data"] = "你的图片类型貌似不支持,因为通道数不为3"
        return JsonResponse(res)
    elif min(img.shape[0], img.shape[1]) > 500:
        res["data"] = "你的图片分辨率好像不低了吧?绕过我的服务器吧!"
        return JsonResponse(res)

    inference_img = inference(img)

    # 保存图片在resource/image目录下，生产环境下不需要
    # imageio.imwrite("resource/image/receive_img.jpg", img)
    # imageio.imwrite("resource/image/inference_img.jpg", inference_img)

    img_bytesio = io.BytesIO()
    imageio.imwrite(img_bytesio, inference_img, format="PNG")

    data = base64.b64encode(img_bytesio.getvalue()).decode()
    res = {
        "state": "success",
        "data": data,
    }
    return JsonResponse(res)