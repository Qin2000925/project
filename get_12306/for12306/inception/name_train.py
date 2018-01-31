# coding: utf-8
import glob  # 可以通过windows中的*,?,[]等方式来查找文件
import os.path
import random
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile

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

# 验证和测试数据的百分比
VALIDATAION_PERCENTAGE = 10
TEST_PERCENTAGE = 10

# 神经网络参数
LEARNING_RATE = 0.1
STEPS = 2000
BATCH = 100
# 分类列表
LABEL_NAME_LISTS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80']


def create_image_lists(test_percentage, validation_percentage):
    result = {}
    sub_dirs = [x[0] for x in os.walk(INPUT_DATA_DIR)]  # x[0]获取列表第一个元素
    is_root_dir = True
    for sub_dir in sub_dirs:
        if is_root_dir:  # 得到的第一个目录是当前目录，不考虑
            is_root_dir = False
            continue
        extensions = ['jpg', 'jpeg']
        file_list = []
        dir_name = os.path.basename(sub_dir)  # 获取路径中最后一级的名称,此作用作为图片标识
        for extension in extensions:
            file_glob = os.path.join(sub_dir, '*.' + extension)
            file_list.extend(glob.glob(file_glob))  # 在指定路径下搜索文件，并将结果添加到列表
        if not file_list:
            continue
        label_name = dir_name.lower()  # 将字符串转化为小写
        # 初始化训练，测试，验证数据集
        training_images = []
        testing_images = []
        validation_images = []
        for file_name in file_list:
            base_name = os.path.basename(file_name)  # 获取图片文件名称
            # 随机将数据分到训练，测试，验证数据集
            chance = np.random.randint(100)
            if chance < validation_percentage:
                validation_images.append(base_name)
            elif chance < (validation_percentage + test_percentage):
                testing_images.append(base_name)
            else:
                training_images.append(base_name)
        # 将当前类别数据放入结果字典
        result[label_name] = {
            'dir': dir_name,  # 根目录下级目录
            'training': training_images,
            'testing': testing_images,
            'validation': validation_images
        }
    return result  # 用字典保存了图片数据


#  参数依次意义，上面函数返回数据，目标目录上一级目录目录，类别，图片编号，选择哪个数据集
def get_image_path(image_dict, root_dir, label_name, index, category):
    label_lists = image_dict[label_name]
    category_list = label_lists[category]
    mod_index = index % len(category_list)
    base_name = category_list[mod_index]  # 获取哪一张图片文件名
    sub_dir = label_lists['dir']  # 根目录下级目录
    full_path = os.path.join(root_dir, sub_dir, base_name)
    return full_path  # 返回一张图片的绝对路径


# 返回经过inception-v3处理过图片的特征向量文件绝对路径
def get_bottleneck_path(image_dict, label_name, index, category):
    return get_image_path(image_dict, CACHE_DIR, label_name, index, category) + '.txt'


# 使用训练好的inception-v3模型处理一张图片，得到这个图片新的特征向量
def run_bottleneck_on_images(sess, image_data, image_data_tensor, bottleneck_tensor):
    bottleneck_values = sess.run(bottleneck_tensor,  # 瓶颈处节点计算流
                                 {image_data_tensor: image_data})  # image_data_tensor图片数据输入占位符
    bottleneck_values = np.squeeze(bottleneck_values)  # 把长度为一的维度压缩去掉
    return bottleneck_values


def get_or_create_bottleneck(
        sess, image_dict, label_name, index, category, jpeg_input_tensor, bottleneck_tensor
):
    label_lists = image_dict[label_name]
    sub_dir = label_lists["dir"]
    sub_dir_path = os.path.join(CACHE_DIR, sub_dir)
    if not os.path.exists(sub_dir_path):
        os.makedirs(sub_dir_path)  # 创建通过inception-v3处理过的特征向量文件保存的父级目录
    # 获取经过处理后的图片特征向量文件的绝对路径
    bottleneck_path = get_bottleneck_path(image_dict, label_name, index, category)
    if not os.path.exists(bottleneck_path):  # 如果文件不存在则通过加载的模型处理并保存
        image_path = get_image_path(image_dict,  # 获取某张图片路径
                    INPUT_DATA_DIR, label_name, index, category)
        image_data = gfile.FastGFile(image_path, 'rb').read()  # 将图片像素信息读取出来，存入列表
        # 通过inception-v3模型计算特征向量
        bottleneck_values = run_bottleneck_on_images(
            sess, image_data, jpeg_input_tensor, bottleneck_tensor
        )
        # 将计算得到的特征向量存入文件,将序列用,隔开，并转化为字符串
        bottleneck_string = ','.join(str(x) for x in bottleneck_values)
        with open(bottleneck_path, 'w') as f:
            f.write(bottleneck_string)
    else:
        with open(bottleneck_path, 'r') as f:
            bottleneck_string = f.read()
        bottleneck_values = [float(x) for x in bottleneck_string.split(',')]
    return bottleneck_values


# 随机获取batch图片作为训练数据
def get_random_cached_bottlenecks(
        sess, n_classes, image_dict, how_many, category,
        jpeg_data_tensor, bottleneck_tensor
):
    bottlenecks = []
    ground_truths = []
    for _ in range(how_many):
        label_index = random.randrange(n_classes)  # 在1到n_classes间取一个整数
        # list(image_dict.keys())程序没有结束，这个列表顺序和第一次调用是一样的
        label_name = LABEL_NAME_LISTS[label_index]
        image_index = random.randrange(65536)  # 在1-65536间取一个整数
        bottleneck = get_or_create_bottleneck(
            sess, image_dict, label_name, image_index, category,
            jpeg_data_tensor, bottleneck_tensor
        )
        ground_truth = np.zeros(n_classes, dtype=np.float32)
        ground_truth[label_index] = 1.0  # 输出标记向量
        bottlenecks.append(bottleneck)
        ground_truths.append(ground_truth)
    return bottlenecks, ground_truths  # 输入，输出向量


# 获取全部测试数据
def get_test_bottlenecks(
        sess, image_dict, n_classes, category, jpe_data_tensor, bottleneck_tensor
):
    bottlenecks = []
    ground_truths = []
    for label_index, label_name in enumerate(LABEL_NAME_LISTS):
        for index, unused_base_name in enumerate(
            image_dict[label_name][category]):
            bottleneck = get_or_create_bottleneck(
                sess, image_dict, label_name, index, category,
                jpe_data_tensor, bottleneck_tensor)
            ground_truth = np.zeros(n_classes, dtype=np.float32)
            ground_truth[label_index] = 1.0
            bottlenecks.append(bottleneck)
            ground_truths.append(ground_truth)
    return bottlenecks, ground_truths


def main():
    # 读取所有图片
    image_dict = create_image_lists(TEST_PERCENTAGE, VALIDATAION_PERCENTAGE)
    n_class = len(image_dict.keys())
    print(n_class)
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
        dtype=tf.float32, shape=[None, BOTTLENECK_TENSOR_SIZE], name='new_input'
    )
    # 定义标准答案输出
    ground_truth_input = tf.placeholder(
        dtype=tf.float32, shape=[None, n_class], name='new_output'
    )

    # 定义全连接层传播
    with tf.variable_scope('result', reuse=False):
        weights = tf.get_variable(
            'weight', shape=[2048, 80],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        biases = tf.get_variable(
            'biases', shape=[80],
            initializer=tf.constant_initializer(0.0)
        )
        logits = tf.matmul(bottleneck_input, weights) + biases
        final_tensor = tf.nn.softmax(logits)  # 预测作用的

    # 交叉熵
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(
        logits=logits, labels=ground_truth_input
    )
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    train_step = tf.train.GradientDescentOptimizer(LEARNING_RATE)\
        .minimize(cross_entropy_mean)

    # 计算正确率
    with tf.name_scope('evaluation'):
        correct_prediction = tf.equal(tf.argmax(final_tensor, 1),
                                      tf.argmax(ground_truth_input, 1))
        evaluation_step = tf.reduce_mean(
            tf.cast(correct_prediction, tf.float32)
        )
    saver = tf.train.Saver()
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        # 训练
        for i in range(STEPS):
            train_bottlenecks, train_ground_truth = get_random_cached_bottlenecks(
                sess, n_class, image_dict, BATCH, 'training',
                jpeg_data_tensor, bottleneck_tensor
            )
            sess.run(train_step,
                     feed_dict={bottleneck_input: train_bottlenecks,
                                ground_truth_input: train_ground_truth})
            if i % 10 == 0 or i + 1 == STEPS:
                validation_bottlenecks, validation_ground_truth = get_test_bottlenecks(
                    sess, image_dict, n_class, 'training',
            jpeg_data_tensor, bottleneck_tensor
                )
                validation_accuracy = sess.run(
                    evaluation_step, feed_dict={
                        bottleneck_input: validation_bottlenecks,
                        ground_truth_input: validation_ground_truth
                    }
                )
                print('steps is: %d,  accuracy is: %.1f' % (i, validation_accuracy * 100))

        # 在最后的测试数据上测试正确率
        # test_bottlenecks, test_ground_truth = get_test_bottlenecks(
        #     sess, image_dict, n_class, 'testing',
        #     jpeg_data_tensor, bottleneck_tensor
        # )
        # test_accuracy = sess.run(
        #     evaluation_step, feed_dict={
        #         bottleneck_input: test_bottlenecks,
        #         ground_truth_input: test_ground_truth
        #     }
        # )
        # print('最后测试正确率 = % .1f%%' % (test_accuracy * 100))
        saver.save(sess=sess, save_path='D:/12306/inception_name/save/model.ckpt')
        print('保存完毕')


if __name__ == '__main__':
        main()

