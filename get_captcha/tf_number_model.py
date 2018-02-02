import tensorflow as tf
from PIL import Image
import numpy
import random
import sys
import os


NUM_TEST = 500
RANDOM_SEED = 0
IMAGE_PATH = '/home/qinjiahu521/.virtualenvs/python3/GIT/get_captcha/number_images/'
TF_RECORD_PATH = '/home/qinjiahu521/.virtualenvs/python3/GIT/get_captcha/tf_number_record/'


def data_set_exists(image_path):
    for split_name in ['train', 'test']:
        output_name = os.path.join(image_path, split_name + '.tfrecords')
        if not tf.gfile.Exists(output_name):
            return False
    return True


def image_name():
    file_path = []
    for i in os.listdir(IMAGE_PATH):
        path = os.path.join(IMAGE_PATH, i)
        file_path.append(path)
    return file_path


def bytes_feature(values):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[values]))


def int64_feature(values):
    if not isinstance(values, (tuple, list)):
        values = [values]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=values))


def image_to_tf_example(image_data, num_table1, num_table2, num_table3, num_table4, num_table5, num_table6):
    return tf.train.Example(features=tf.train.Features(feature={
        'image': bytes_feature(image_data),
        'num_table1': int64_feature(num_table1),
        'num_table2': int64_feature(num_table2),
        'num_table3': int64_feature(num_table3),
        'num_table4': int64_feature(num_table4),
        'num_table5': int64_feature(num_table5),
        'num_table6': int64_feature(num_table6)
    }))


def convert_data_set(split_name, file_name):
    assert split_name in ['train', 'test']

    with tf.Session() as sess:
        output_filename = os.path.join(TF_RECORD_PATH, split_name + '.tfrecords')
        with tf.python_io.TFRecordWriter(output_filename) as tfrecord_write:
            for i, filename in enumerate(file_name):
                try:
                    sys.stdout.write('\r>>Creating image %d/%d' % (i + 1, len(file_name)))
                    sys.stdout.flush()

                    image_data = Image.open(filename)
                    image_data = image_data.resize((224, 224))
                    image_data = numpy.array(image_data.convert('L'))
                    image_data = image_data.tobytes()

                    labels = filename.split('/')[-1][0: 6]
                    print(labels)
                    num_table = []
                    for j in range(6):
                        num_table.append(int(labels[j]))

                    example = image_to_tf_example(image_data, num_table[0], num_table[1], num_table[2],
                                                  num_table[3], num_table[4], num_table[5])
                    tfrecord_write.write(example.SerializeToString())

                except IOError as e:
                    print('Could not read', filename)
                    print('Error: ', e)
                    print('Skip it\n')
            sys.stdout.write('\n')
            sys.stdout.flush()


if __name__ == '__main__':
    if data_set_exists(IMAGE_PATH):
        print('文件已存在:')
    else:
        file_path = image_name()
        random.seed(RANDOM_SEED)
        random.shuffle(file_path)

        training_file_name = file_path[NUM_TEST:]
        testing_file_name = file_path[:NUM_TEST]

        convert_data_set('train', training_file_name)
        convert_data_set('test', testing_file_name)
        print('SUCCESS')
