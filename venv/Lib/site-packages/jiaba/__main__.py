from .import common
from .import models
import tensorflow as tf
import os
import numpy as np
import pkg_resources
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--train', type=bool, default=False, help='是否自己训练分词模型')
parser.add_argument('--train_file_path', type=str, help='训练文件路径，空格分割')
parser.add_argument('--model_save_path', type=str, help='模型保存路径')

args = parser.parse_args()
if args.train:
    train_file_path = args.train_file_path
    model_save_path = args.model_save_path

    model = models.BiLSTMCRFModel(common.VOCAB_SIZE, 4, 64, 32)
    model.compile(optimizer=tf.keras.optimizers.Adam(
        0.02), metrics=['accuracy'])

    train_data = common.get_segment_train_data(train_file_path, 512)
    model.fit(train_data, epochs=3)

    model.save_weights(model_save_path)
