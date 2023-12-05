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
import paramiko
import sys

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


def ssh_connect(_host, _username, _password):
    try:
        _ssh_fd = paramiko.SSHClient()
        _ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _ssh_fd.connect(_host, username=_username, password=_password)
    except Exception as e:
        print('Authorization Failed! Please check the username, password, or your device is connected to the Internet.')
        exit()
    return _ssh_fd

def ssh_exec_cmd(_ssh_fd, _cmd):
    return _ssh_fd.exec_command(_cmd)

def ssh_close(_ssh_fd):
    _ssh_fd.close()

def print_ssh_exec_cmd_return(_ssh_fd, _cmd):
    stdin, stdout, stderr = ssh_exec_cmd(_ssh_fd, _cmd)
    err_list = stderr.readlines()
    if len(err_list) > 0:
        for err_content in err_list:
            print('ERROR:' + err_content)
        exit()
    for item in stdout:
        print(item)




@require_http_methods(['POST'])
def take_pic(request):
    # 要求raspberry拍照
    sshd = ssh_connect('192.168.137.174', 'pi' , 'raspberry')
    print('Executing raspistill command, remote controlling raspberrypi.')
    print_ssh_exec_cmd_return(sshd,'cd Raspberry_pi_study;cd RemoteControl;python main.py ')
    ssh_close(sshd)

    # 存照片并读取
    img_path = r'resource\image\a.jpg'
    img = imageio.imread(img_path)

    # 把图片解码成b64
    img_bytesio = io.BytesIO()
    imageio.imwrite(img_bytesio, img, format="PNG")

    data = base64.b64encode(img_bytesio.getvalue()).decode()
    res = {
        "state": "success",
        "data": data,
    }
    return JsonResponse(res)