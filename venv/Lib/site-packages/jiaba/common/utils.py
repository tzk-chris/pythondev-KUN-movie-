"""
功能函数.
"""
import tensorflow as tf
import re


def get_vocab():
    """
    构造包含全部英文，中文，英文标点，中文标点的词典。其余字符视为<UNK>
    """
    vocab = {'<UNK>': 0}
    idx = 1
    # 添加ascii字符
    for i in range(1, 128):
        ch = chr(i)
        vocab[ch] = idx
        idx += 1
    # 添加常用中文字符\u4e00-\u9fa5，将整数转成bytes，在转成对应的中文字符
    low = int.from_bytes(b'\x4e\x00', 'big')
    high = int.from_bytes(b'\x9f\xa5', 'big')
    for i in range(low, high+1):
        ch = chr(i)
        vocab[ch] = idx
        idx += 1
    # 中文标点暂时当成<UNK>处理

    return vocab


def get_segment_train_data(file_name, batch_size):
    """
    获取分词模型训练数据.
    Args:
        file_name:
        batch_size:
    Returns:
        TextLineDataSet
    """
    train_data = tf.data.TextLineDataset(file_name).prefetch(batch_size)
    train_data = train_data.filter(lambda text: tf.py_function(
        lambda x: len(x.numpy()) > 0, [text], bool)).map(_map_func)
    train_data = train_data.padded_batch(batch_size, padded_shapes=(tf.TensorShape(
        [None]), tf.TensorShape([]), tf.TensorShape([None])))
    return train_data


def pre_process_raw(sentence: str):
    """
    处理一个句子.
    Args:
        sentence: 待分词的句子.
    Returns:
        x_data:
        xlen_data:
    """
    s = sentence.strip()
    x_data = [_word2idx.get(w, 0) for w in s]
    xlen_data = len(x_data)
    return x_data, xlen_data


def pre_process_train(sentence):
    """
    处理训练数据中的一个句子(要求以空格分割).
    """
    sentence = sentence.numpy().decode('utf8')
    s = sentence.strip()
    words = _sep.split(s)
    x_data, xlen_data = pre_process_raw(''.join(words))
    xtag_data = [0]*xlen_data
    i = 0
    for w in words:
        w_len = len(w)
        if w_len == 1:
            i += w_len
        else:
            xtag_data[i] = 1
            xtag_data[i+w_len-1] = 3
            for j in range(i+1, i+w_len-1):
                xtag_data[j] = 2
            i += w_len
    return x_data, xlen_data, xtag_data


def _map_func(text):
    """
    把分词原始数据转换成可训练的形式.
    """
    return tf.py_function(lambda x: pre_process_train(x), [text], (tf.int32, tf.int32, tf.int32))


_sep = re.compile(r'\s')
_word2idx = get_vocab()

VOCAB_SIZE = len(_word2idx)
