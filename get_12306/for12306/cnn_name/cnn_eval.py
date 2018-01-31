# coding: utf-8
import tensorflow as tf
import get_12306.for12306.cnn_name.cnn_inference as cnn_inference
import get_12306.for12306.cnn_name.get_input_data as get
import get_12306.for12306.cnn_name.cnn_train as cnn_train
from PIL import Image
import get_12306.for12306.picture.get_code_picture as get_code_picture
import get_12306.for12306.picture.picture_cut as picture_cut
import time
import os


img_path = 'D:/12306/code_download/name/1.jpg'
save_path = 'D:/12306/add'


result_dict = {1: '安全帽', 10: '刺绣', 11: '打字机', 12: '档案袋', 13: '电饭煲', 14: '电线', 15: '电子秤', 16: '订书机', 17: '耳塞', 18: '风铃', 19: '高压锅',
               2: '本子', 20: '公交卡', 21: '挂钟', 22: '锅铲', 23: '海报', 24: '海鸥', 25: '海苔', 26: '航母', 27: '黑板', 28: '红豆', 29: '红酒',
               3: '鞭炮', 30: '红枣', 31: '护腕', 32: '话梅', 33: '剪纸', 34: '金字塔', 35: '锦旗', 36: '卷尺', 37: '开瓶器', 38: '口哨', 39: '蜡烛',
               4: '冰箱', 40: '辣椒酱', 41: '篮球', 42: '老虎', 43: '铃铛', 44: '龙舟', 45: '漏斗', 46: '路灯', 47: '锣', 48: '绿豆', 49: '蚂蚁',
               5: '菠萝', 50: '毛线', 51: '蜜蜂', 52: '棉棒', 53: '排风机', 54: '牌坊', 55: '盘子', 56: '跑步机', 57: '啤酒', 58: '热水袋', 59: '日历',
               6: '苍蝇拍', 60: '沙包', 61: '沙拉', 62: '珊瑚', 63: '狮子', 64: '手掌印', 65: '薯条', 66: '双面胶', 67: '调色板', 68: '拖把', 69: '网球拍',
               7: '茶几', 70: '文具盒', 71: '蜥蜴', 72: '药片', 73: '仪表盘', 74: '印章', 75: '樱桃', 76: '雨靴', 77: '蒸笼', 78: '中国结', 79: '钟表',
               8: '茶盅', 80: '烛台', 9: '创可贴'}


def get_data(path):
    inputs = []
    img = Image.open(path)
    data = img.load()
    inp = []
    for k in range(img.size[1]):
        inp.append([])
        for m in range(img.size[0]):
            inp[k].append([])
            if data[m, k][0] > 180:
                inp[k][m].append(0.0)
            else:
                inp[k][m].append(1.0)
    inputs.append(inp)
    return inputs


def evaluate():
    x = tf.placeholder(dtype=tf.float32, shape=[None, 25, 60, 1], name='x-input')
    y_ = tf.placeholder(dtype=tf.float32, shape=[None, cnn_inference.NUM_LABELS], name='y-input')
    # y = mnist_inference.inference(x_image, True, False, None)  # 先要创建变量才能加载，此处reuse为False，即创建变量
    y = cnn_inference.inference(x, False, False, None)
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean((tf.cast(correct_prediction, tf.float32)))

    variable_averages = tf.train.ExponentialMovingAverage(cnn_train.MOVING_AVERAGE_DECAY)
    variables_to_restore = variable_averages.variables_to_restore()
    saver = tf.train.Saver(variables_to_restore)  # 将滑动平均值加载到对应的权矩阵和偏置

    with tf.Session() as sess:
        # batch = get.get_data1('D:/12306/add/3')
        inp = get.get_data_one('D:/12306/code_download/name/1.jpg')
        # 找到最后一次保存模型的数据
        ckpt = tf.train.get_checkpoint_state(cnn_train.MODEL_SAVE_PATH)
        if ckpt and ckpt.model_checkpoint_path:  # 判断文件路径是否存在
            saver.restore(sess=sess, save_path=ckpt.model_checkpoint_path)
            result = sess.run(tf.argmax(y, 1), feed_dict={x: inp})
            return result_dict[result[0] + 1]
        else:
            print('没有保存的模型数据')
        # save(sess, x, y)
        # together(sess, x, y)


# 二次分类
def save(sess, x, logits):
    for i in range(10000):
        n = i + 10907
        while True:
            try:
                get_code_picture.save_one()
                picture_cut.cut_name1()
                image_data = get.get_data_one(img_path)
                name = sess.run(tf.argmax(logits, 1), feed_dict={x: image_data})
                save_path1 = save_path + '/' + result_dict[name[0] + 1] + '/' + str(n) + '.jpg'
                img = Image.open(img_path)
                print(save_path1, '等待5s......')
                img.save(save_path1)
            except Exception as e:
                print(e)
                continue
            else:
                break
        time.sleep(4)


def together(sess, x, logits):
    n = 0
    path = 'D:/12306/add1'
    for i in os.walk(path):
        if i[2]:
            for j in i[2]:
                data_path = os.path.join(i[0], j)
                image_data = get.get_data_one(data_path)
                name = sess.run(tf.argmax(logits, 1), feed_dict={x: image_data})
                save_path1 = 'D:/12306/together' + '/' + result_dict[name[0] + 1] + '/' + j
                print(data_path, save_path1, n)
                img = Image.open(data_path)
                img.save(save_path1)
                n += 1


def main():
    evaluate()


if __name__ == '__main__':
    main()


