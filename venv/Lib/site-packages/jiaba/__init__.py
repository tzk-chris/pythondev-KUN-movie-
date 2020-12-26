from .import common
from .import models
import tensorflow as tf
import os
import numpy as np
import pkg_resources


# 获取预训练模型保存路径
__BILSTM_CRF_MODEL_PATH = pkg_resources.resource_filename(
    'jiaba', 'datas/saved_models/bilstm_crf/bilstm_crf_v1')

_model = models.BiLSTMCRFModel(common.VOCAB_SIZE, 4, 64, 32)
_model.load_weights(__BILSTM_CRF_MODEL_PATH)


def cut(text, return_tags=False):
    """
    实现分词功能
    """
    if not text:
        return ['']
    x, xlen = common.pre_process_raw(text)
    x, xlen = np.array([x]), np.array([xlen])
    tags, _ = _model((x, xlen))
    tags = tags.numpy()

    i, j = 0, 1
    n = len(tags[0])
    ans = []
    while i < n:
        if tags[0, i] == 0:
            ans.append(text[i:j])
            i, j = j, j+1
        else:
            while j < n and tags[0, j] != 3:
                j += 1
            ans.append(text[i:j+1])
            i, j = j+1, j+2

    if return_tags:
        return ans, tags
    else:
        return ans
