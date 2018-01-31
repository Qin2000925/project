# coding: utf-8
# import glob  # 可以通过windows中的*,?,[]等方式来查找文件
import os.path
from PIL import Image
import for12306.picture.get_code_picture as get_code_picture
import for12306.picture.picture_cut as picture_cut
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile
import time


img_path = 'D:/12306/code_download/name/1.jpg'
save_path = 'D:/12306/add/name'

# Inception-v3模型瓶颈层节点数
BOTTLENECK_TENSOR_SIZE = 2048
BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape:0'

# 图像输入张量对应名称
JPEN_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'

# 下载好的谷歌训练好的Inception-v3模型文目录
MODEL_DIR = 'd:/12306/inception-v3_path_to_model'
# 下载好谷歌训练好的Inception-v3模型名称
MODEL_FILE = 'classify_image_graph_def.pb'

# 由于训练数据会被使用多次，所以将原始图片通过inception-v3计算得到的特征
# 向量保存在文件中，免去重复计算，下面为地址
CACHE_DIR = 'd:/12306/inception_name/tmp_tensor'

# 训练图片的路径
INPUT_DATA_DIR = 'd:/12306/inception_name/code'

MODEL_SAVE_PATH = 'd:/12306/inception_name/save'


result_dict = {1: '安全帽', 10: '刺绣', 11: '打字机', 12: '档案袋', 13: '电饭煲', 14: '电线', 15: '电子秤', 16: '订书机', 17: '耳塞', 18: '风铃', 19: '高压锅',
               2: '本子', 20: '公交卡', 21: '挂钟', 22: '锅铲', 23: '海报', 24: '海鸥', 25: '海苔', 26: '航母', 27: '黑板', 28: '红豆', 29: '红酒',
               3: '鞭炮', 30: '红枣', 31: '护腕', 32: '话梅', 33: '剪纸', 34: '金字塔', 35: '锦旗', 36: '卷尺', 37: '开瓶器', 38: '口哨', 39: '蜡烛',
               4: '冰箱', 40: '辣椒酱', 41: '篮球', 42: '老虎', 43: '铃铛', 44: '龙舟', 45: '漏斗', 46: '路灯', 47: '锣', 48: '绿豆', 49: '蚂蚁',
               5: '菠萝', 50: '毛线', 51: '蜜蜂', 52: '棉棒', 53: '排风机', 54: '牌坊', 55: '盘子', 56: '跑步机', 57: '啤酒', 58: '热水袋', 59: '日历',
               6: '苍蝇拍', 60: '沙包', 61: '沙拉', 62: '珊瑚', 63: '狮子', 64: '手掌印', 65: '薯条', 66: '双面胶', 67: '调色板', 68: '拖把', 69: '网球拍',
               7: '茶几', 70: '文具盒', 71: '蜥蜴', 72: '药片', 73: '仪表盘', 74: '印章', 75: '樱桃', 76: '雨靴', 77: '蒸笼', 78: '中国结', 79: '钟表',
               8: '茶盅', 80: '烛台', 9: '创可贴'}


def run_bottleneck_on_images(sess, image_data, image_data_tensor, bottleneck_tensor):
    bottleneck_values = sess.run(bottleneck_tensor,  # 瓶颈处节点计算流
                                 {image_data_tensor: image_data})  # image_data_tensor图片数据输入占位符
    bottleneck_values = np.squeeze(bottleneck_values)  # 把长度为一的维度压缩去掉
    return bottleneck_values


def main():
    # 加载模型，以二进制读取，并转换为graph
    with gfile.FastGFile(os.path.join(MODEL_DIR, MODEL_FILE), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    # 加载模型，返回输入数据的张量，以及计算瓶颈结果的张量
    bottleneck_tensor, jpeg_data_tensor = tf.import_graph_def(
        graph_def, return_elements=[BOTTLENECK_TENSOR_NAME, JPEN_DATA_TENSOR_NAME]
    )
    # 定义新的神经网络输入，即特征提取后的输入
    bottleneck_input = tf.placeholder(
        dtype=tf.float32, shape=[None, 2048], name='new_input'
    )
    # # 定义标准答案输出
    # ground_truth_input = tf.placeholder(
    #     dtype=tf.float32, shape=[None, 80], name='new_output'
    # )
    # 定义全连接层传播
    with tf.variable_scope('result', reuse=False):
        weights = tf.get_variable(
            'weight', shape=[2048, 80],
            initializer=tf.truncated_normal_initializer(stddev=0.1))
        biases = tf.get_variable(
            'biases', shape=[80],
            initializer=tf.constant_initializer(0.0))
    logits = tf.matmul(bottleneck_input, weights) + biases
    saver = tf.train.Saver()


    with tf.Session() as sess:
        # a = []
        ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
        if ckpt and ckpt.model_checkpoint_path:  # 判断文件路径是否存在
            saver.restore(sess=sess, save_path=ckpt.model_checkpoint_path)
        else:
            print('没有保存的模型数据')
        # image_data = gfile.FastGFile(img_path, 'rb').read()
        # bottleneck_values = run_bottleneck_on_images(
        #     sess, image_data, jpeg_data_tensor, bottleneck_tensor
        # )
        # a.append(bottleneck_values)
        # result = sess.run(tf.argmax(logits, 1), feed_dict={bottleneck_input: a})
        # return result_dict[result[0] + 1]
        # save(sess, jpeg_data_tensor, bottleneck_tensor, logits, bottleneck_input)
        # together(sess, jpeg_data_tensor, bottleneck_tensor, logits, bottleneck_input)


def save(sess, jpeg_data_tensor, bottleneck_tensor, logits, bottleneck_input):
    for i in range(10000):
        a = []
        n = i + 2500
        while True:
            try:
                get_code_picture.save_one()
                picture_cut.cut_name1()
                image_data = gfile.FastGFile(img_path, 'rb').read()
                bottleneck_values = run_bottleneck_on_images(
                    sess, image_data, jpeg_data_tensor, bottleneck_tensor
                )
                a.append(bottleneck_values)
                name = sess.run(tf.argmax(logits, 1), feed_dict={bottleneck_input: a})
                save_path1 = save_path + '/' + result_dict[name[0] + 1] + '/' + str(n) + '.jpg'
                img = Image.open(img_path)
                print(save_path1)
                img.save(save_path1)
                n += 1
            except Exception as e:
                print(e)
                continue
            else:
                break

        time.sleep(3)


def together(sess, jpeg_data_tensor, bottleneck_tensor, logits, x):
    n = 0
    path = 'D:/12306/add1'
    for i in os.walk(path):
        if i[2]:
            for j in i[2]:
                a = []
                data_path = os.path.join(i[0], j)
                image_data = gfile.FastGFile(data_path, 'rb').read()
                bottleneck_values = run_bottleneck_on_images(
                    sess, image_data, jpeg_data_tensor, bottleneck_tensor
                )
                a.append(bottleneck_values)
                name = sess.run(tf.argmax(logits, 1), feed_dict={x: a})
                save_path1 = 'D:/12306/together' + '/' + result_dict[name[0] + 1] + '/' + j
                print(data_path, save_path1, n)
                img = Image.open(data_path)
                img.save(save_path1)
                n += 1



if __name__ == '__main__':

    # get_code_picture.save_one()
    # path = picture_cut.cut_name1()
    # # path = 'D:\\12306\\inception_name\\code\\64\\1.jpg'
    main()