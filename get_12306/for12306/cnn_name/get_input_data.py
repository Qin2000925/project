# coding: utf-8
import os
import tensorflow as tf
import numpy as np
import PIL.Image as Image
import for12306.cnn_name.cnn_inference as cnn_inference


def get_dict(path):
    result = []
    n = 0
    for i in os.walk(path):
        if i[1]:
            for j in i[1]:
                result.append(j)
                n += 1
    return result


def do(path):
    for i in os.walk(path):
        if i[2]:
            n = 1000
            for j in i[2]:
                path = os.path.join(i[0], j)
                img = Image.open(path)
                data = img.load()
                for k in range(img.size[1]):
                    for m in range(img.size[0]):
                        if data[m, k][0] > 180:
                            img.putpixel((m, k), (255, 255, 255))
                        else:
                            img.putpixel((m, k), (0, 0, 0))
                n += 1
                img.save(path)


def get_data1(path):
    inputs = []
    outputs = []
    for i in os.walk(path):
        if i[2]:
            # print(os.path.basename(i[0]))
            for j in i[2]:
                inp = []
                path = os.path.join(i[0], j)
                img = Image.open(path)
                n = int(os.path.basename(i[0]))
                data = img.load()
                for k in range(img.size[1]):
                    inp.append([])
                    for m in range(img.size[0]):
                        inp[k].append([])
                        if data[m, k][0] > 180:
                            inp[k][m].append(0.0)
                        else:
                            inp[k][m].append(1.0)
                out = np.zeros(cnn_inference.NUM_LABELS, dtype=np.float32)
                out[n - 1] = 1.0
                inputs.append(inp)
                outputs.append(out)
    return inputs, outputs


def get_data_one(path):
    inputs = []
    inp = []
    img = Image.open(path)
    data = img.load()
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


def get_random_data1(tup, batch):
    inputs = []
    outputs = []
    m = len(tup[0])
    for i in range(batch):
        n = np.random.randint(m)
        inputs.append(tup[0][n])
        outputs.append(tup[1][n])
    return inputs, outputs




def get_data(root_path):
    inputs = []
    outputs = []
    sess = tf.Session()
    for i in os.walk(root_path):
        if i[2]:
            for j in i[2]:
                path = os.path.join(i[0], j)
                n = int(os.path.basename(i[0]))
                image_data = tf.image.decode_jpeg(tf.gfile.FastGFile(path, 'rb').read())
                image_data = tf.image.convert_image_dtype(image_data, dtype=tf.float32)
                image_data = sess.run(image_data)
                out = np.zeros(10, dtype=np.float32)
                out[n - 1] = 1.0
                inputs.append(image_data)
                outputs.append(out)
    return inputs, outputs


def get_data_test(root_path, m):
    inputs = []
    inputs1 = []
    sess = tf.Session()
    for i in os.walk(root_path):
        if i[2]:
            for j in i[2]:
                path = os.path.join(i[0], j)
                image_data = tf.image.decode_jpeg(tf.gfile.FastGFile(path, 'rb').read())
                image_data = tf.image.convert_image_dtype(image_data, dtype=tf.float32)
                image_data = sess.run(image_data)
                inputs.append(image_data)
    inputs1.append(inputs[m])
    return inputs1

# print(get_dict('D:/12306/test1'))
# get_data1('D:/12306/test1')

# do('D:/12306/test1')



