# coding: utf-8
import tensorflow as tf



IMAGE_SIZE_x = 60  # 图片尺寸
IMAGE_SIZE_y = 25
NUM_CHANNELS = 1  # 输入层深度
NUM_LABELS = 80  # 输出向量长度

# 第一层卷积层的尺寸和深度
CONV1_DEEP = 128  # 第一层卷积深度
CONV1_SIZE = 5  # 第一层卷积核尺寸
# 第二层卷积层的尺寸和深度
CONV2_DEEP = 256  # 第二层卷积深度
CONV2_SIZE = 5  # 第二层卷积核尺寸
# 第三层卷积层的尺寸和深度
CONV3_DEEP = 128  # 第三层卷积深度
CONV3_SIZE = 5  # 第三层卷积核尺寸
# 全连接层节点数
FC_SIZE = 1024


# 卷积网络前向传播
def inference(input_tensor, train, reuse, regularizer):  # 提供了一个新参数train：TRUE,FALSE只在训练过程中调用对应方法
    # 卷积第一层
    with tf.variable_scope('layer1_conv1', reuse=reuse):
        conv1_weights = tf.get_variable(
            'weight', shape=[CONV1_SIZE, CONV1_SIZE,
                             NUM_CHANNELS, CONV1_DEEP],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        conv1_biases = tf.get_variable(
            'biases', shape=[CONV1_DEEP],
            initializer=tf.constant_initializer(0.0)
        )
        conv1 = tf.nn.conv2d(
            input_tensor, conv1_weights,
            strides=[1, 1, 2, 1], padding='SAME'
        )
        relu1 = tf.nn.relu(tf.nn.bias_add(conv1, conv1_biases))

    # 池化层1
    with tf.name_scope('layer2_pool1'):
        pool1 = tf.nn.max_pool(relu1, ksize=[1, 2, 2, 1],
                               strides=[1, 2, 2, 1], padding='SAME')

    # 卷积第二层
    with tf.variable_scope('layer3_conv2', reuse=reuse):
        conv2_weights = tf.get_variable(
            'weight', shape=[CONV2_SIZE, CONV2_SIZE,
                             CONV1_DEEP, CONV2_DEEP],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        conv2_biasess = tf.get_variable(
            'biasess', shape=[CONV2_DEEP],
            initializer=tf.constant_initializer(0.0)
        )
        conv2 = tf.nn.conv2d(pool1, conv2_weights,
                             strides=[1, 1, 1, 1],  # 不跨不同输入例子和深度的不同维度的步长
                             padding='SAME')
        relu2 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_biasess))

    # 池化层2
    with tf.name_scope('layer4_pool2'):
        pool2 = tf.nn.max_pool(relu2, ksize=[1, 2, 2, 1],
                               strides=[1, 2, 2, 1], padding='SAME')

    pool_shape = pool2.get_shape().as_list()  # 获取向量维度，返回一个列表
    nodes = pool_shape[1] * pool_shape[2] * pool_shape[3]  # 算出拉直向量后的长度
    reshape = tf.reshape(pool2, [-1, nodes])  # 拉直运算

    # # 卷积层第三层
    # with tf.variable_scope('layer8_conv3', reuse=reuse):
    #     conv3_weights = tf.get_variable(
    #         'weight', shape=[CONV3_SIZE, CONV3_SIZE,
    #                          CONV2_DEEP, CONV3_DEEP],
    #         initializer=tf.truncated_normal_initializer(stddev=0.1)
    #     )
    #     conv2_biasess = tf.get_variable(
    #         'biasess', shape=[CONV3_DEEP],
    #         initializer=tf.constant_initializer(0.0)
    #     )
    #     conv2 = tf.nn.conv2d(pool2, conv3_weights,
    #                          strides=[1, 1, 1, 1],  # 不跨不同输入例子和深度的不同维度的步长
    #                          padding='SAME')
    #     relu3 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_biasess))
    #
    # # 池化层3
    # with tf.name_scope('layer9_pool3'):
    #     pool3 = tf.nn.max_pool(relu3, ksize=[1, 2, 2, 1],
    #                            strides=[1, 2, 2, 1], padding='SAME')
    #
    # pool_shape = pool3.get_shape().as_list()  # 获取向量维度，返回一个列表
    # nodes = pool_shape[1] * pool_shape[2] * pool_shape[3]  # 算出拉直向量后的长度
    # reshape = tf.reshape(pool3, [-1, nodes])  # 拉直运算

    # 第七层全连接前向传播
    with tf.variable_scope('layer5_fc1', reuse=reuse):
        fc1_weights = tf.get_variable(
            'weight', [nodes, FC_SIZE],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        fc1_biases = tf.get_variable(
            'biasess', [FC_SIZE],
            initializer=tf.constant_initializer(0.1)
        )
        if regularizer is not None:
            tf.add_to_collection('losses', regularizer(fc1_weights))
        fc1 = tf.nn.relu(tf.matmul(reshape, fc1_weights) + fc1_biases)
        if train:
            fc1 = tf.nn.dropout(fc1, 0.5)

    # 第八层全连接前向传播
    with tf.variable_scope('layer6_fc2', reuse=reuse):
        fc2_weights = tf.get_variable(
            'weight', [FC_SIZE, NUM_LABELS],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        fc2_biases = tf.get_variable(
            'biasess', [NUM_LABELS],
            initializer=tf.constant_initializer(0.1)
        )
        if regularizer is not None:
            tf.add_to_collection('losses', regularizer(fc2_weights))
        logit = tf.matmul(fc1, fc2_weights) + fc2_biases
    return logit






