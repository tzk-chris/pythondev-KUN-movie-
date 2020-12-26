"""
建立BiLSTM-CRF分词模型
"""
import tensorflow as tf
import tensorflow_addons as tfa
import tensorflow.keras as keras


class BiLSTMCRFModel(keras.Model):
    def __init__(self, input_dim, num_tags, embed_dim, rnn_units, *args, **kwargs):
        """
        BiLSTM-CRF模型构造方法.
        """
        super(BiLSTMCRFModel, self).__init__(*args, **kwargs)
        # 构造Bi_LSTM模型
        inputs = keras.Input(shape=(None,), dtype=tf.int32)
        x = keras.layers.Embedding(input_dim, embed_dim)(inputs)
        # 对于序列标注问题, LSTM需要return_sequences=True
        x = keras.layers.Bidirectional(
            keras.layers.LSTM(rnn_units, return_sequences=True))(x)
        outputs = keras.layers.Dense(num_tags)(x)
        self.bi_lstm = keras.Model(inputs=inputs, outputs=outputs)
        # CRF转移矩阵参数, 需要指定参数name，否则保存出错
        self.crf_transition = self.add_weight(
            shape=(num_tags, num_tags), trainable=True, name='crf_transition')

    def call(self, inputs):
        """
        模型前向传播, 对序列进行标注.
        Args:
            inputs: input_seq (batch, n), input_seq_length (batch, )
        Returns:
            标注结果: input_seq_tag (batch, n, num_tags)
        """
        input_seq, input_seq_length = inputs
        # (batch, n, num_tags)
        bi_lstm_outs = self.bi_lstm(input_seq)
        tags, score = tfa.text.crf_decode(
            bi_lstm_outs, self.crf_transition, input_seq_length)
        return tags, score

    @tf.function
    def train_step(self, data):
        """
        控制训练流程.
        Args:
            data: x (batch, n), xlen (batch, ), x_tags (batch, n)
        """
        x, xlen, x_tags = data
        x_tags_pred, _ = self((x, xlen))
        self.compiled_metrics.update_state(x_tags, x_tags_pred)
        ans = {m.name: m.result() for m in self.metrics}
        # 前向传播, 计算crf损失
        with tf.GradientTape() as tape:
            x = self.bi_lstm(x)
            log_likelihood, _ = tfa.text.crf_log_likelihood(
                x, x_tags, xlen, self.crf_transition)
            crf_loss = -1.0 * tf.reduce_mean(log_likelihood)
        # 求梯度, 更新模型参数
        trainable_vars = self.trainable_variables
        g = tape.gradient(crf_loss, trainable_vars)
        self.optimizer.apply_gradients(zip(g, trainable_vars))
        ans['loss'] = crf_loss
        return ans
