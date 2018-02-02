import tensorflow as tf
from nets import nets_factory


CHAR_SET_LEN = 10
IMAGE_HEIGHT = 60
IMAGE_WIDTH = 160
BATCH_SIZE = 50

TF_RECORD_FILE = '/home/qinjiahu521/.virtualenvs/python3/GIT/get_captcha/tf_num_record_four/train.tfrecords'

x = tf.placeholder(tf.float32, [None, 224, 224])
y0 = tf.placeholder(tf.float32, [None])
y1 = tf.placeholder(tf.float32, [None])
y2 = tf.placeholder(tf.float32, [None])
y3 = tf.placeholder(tf.float32, [None])

lr = tf.Variable(0.003, dtype=tf.float32)


def read_and_decode(filename):
    filename_queue = tf.train.string_input_producer([filename])
    reader = tf.TFRecordReader()

    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example, features={
        'image': tf.FixedLenFeature([], tf.string),
        'num_table1': tf.FixedLenFeature([], tf.string),
        'num_table2': tf.FixedLenFeature([], tf.int64),
        'num_table3': tf.FixedLenFeature([], tf.int64),
        'num_table4': tf.FixedLenFeature([], tf.int64),
    })
    image = tf.decode_raw(features['image'], tf.uint8)

    image = tf.reshape(image, [224, 224])
    image = tf.cast(image, tf.float32) / 255.0

    image = tf.subtract(image, 0.5)
    image = tf.multiply(image, 2.0)

    num_table1 = tf.cast(features['num_table1'], tf.float32)
    num_table2 = tf.cast(features['num_table2'], tf.float32)
    num_table3 = tf.cast(features['num_table3'], tf.float32)
    num_table4 = tf.cast(features['num_table4'], tf.float32)

    return image, num_table1, num_table2, num_table3, num_table4


with tf.Session() as sess:

    filename_queue = tf.train.string_input_producer([TF_RECORD_FILE])
    reader = tf.TFRecordReader()

    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example, features={
        'image': tf.FixedLenFeature([], tf.string),
        'num_table1': tf.FixedLenFeature([], tf.string),
        'num_table2': tf.FixedLenFeature([], tf.int64),
        'num_table3': tf.FixedLenFeature([], tf.int64),
        'num_table4': tf.FixedLenFeature([], tf.int64),
    })
    image = tf.decode_raw(features['image'], tf.uint8)

    image = tf.reshape(image, [224, 224])
    image = tf.cast(image, tf.float32) / 255.0

    image = tf.subtract(image, 0.5)
    image = tf.multiply(image, 2.0)

    num_table1 = tf.cast(features['num_table1'], tf.int32)
    num_table2 = tf.cast(features['num_table2'], tf.int32)
    num_table3 = tf.cast(features['num_table3'], tf.int32)
    num_table4 = tf.cast(features['num_table4'], tf.int32)

    # image, num_table1, num_table2, num_table3, num_table4 = read_and_decode(TF_RECORD_FILE)

    image_batch, num_table1_batch, num_table2_batch, num_table3_batch, num_table4_batch = tf.train.shuffle_batch(
        [image, num_table1, num_table2, num_table3, num_table4], batch_size=BATCH_SIZE,
        capacity=10000, min_after_dequeue=5000, allow_smaller_final_batch=True)

    train_network_fn = nets_factory.get_network_fn(
        'alexnet_v2',
        num_classes=CHAR_SET_LEN,
        weight_decay=0.005,
        is_training=True)

    X = tf.reshape(x, [BATCH_SIZE, 224, 224, 1])
    log_its0, log_its1, log_its2, log_its3, end_points = train_network_fn(X)

    one_hot_num_table0 = tf.one_hot(indices=tf.cast(y0, tf.int32), depth=CHAR_SET_LEN)
    one_hot_num_table1 = tf.one_hot(indices=tf.cast(y1, tf.int32), depth=CHAR_SET_LEN)
    one_hot_num_table2 = tf.one_hot(indices=tf.cast(y2, tf.int32), depth=CHAR_SET_LEN)
    one_hot_num_table3 = tf.one_hot(indices=tf.cast(y3, tf.int32), depth=CHAR_SET_LEN)

    loss0 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=log_its0, labels=one_hot_num_table0))
    loss1 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=log_its1, labels=one_hot_num_table1))
    loss2 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=log_its2, labels=one_hot_num_table2))
    loss3 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=log_its3, labels=one_hot_num_table3))

    total_loss = (loss0 + loss1 + loss2 + loss3) / 4.0

    optimizer = tf.train.AdamOptimizer(learning_rate=lr).minimize(total_loss)

    correct_prediction0 = tf.equal(tf.argmax(one_hot_num_table0, 1), tf.argmax(log_its0, 1))
    accuracy0 = tf.reduce_mean(tf.cast(correct_prediction0, tf.float32))
    correct_prediction1 = tf.equal(tf.argmax(one_hot_num_table1, 1), tf.argmax(log_its0, 1))
    accuracy1 = tf.reduce_mean(tf.cast(correct_prediction1, tf.float32))
    correct_prediction2 = tf.equal(tf.argmax(one_hot_num_table2, 1), tf.argmax(log_its0, 1))
    accuracy2 = tf.reduce_mean(tf.cast(correct_prediction2, tf.float32))
    correct_prediction3 = tf.equal(tf.argmax(one_hot_num_table3, 1), tf.argmax(log_its0, 1))
    accuracy3 = tf.reduce_mean(tf.cast(correct_prediction3, tf.float32))
    saver = tf.train.Saver()
    
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())

    # sess.run(tf.initialize_all_variables())
    # init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
    # sess.run(init_op)

    coord = tf.train.Coordinator()

    threads = tf.train.start_queue_runners(coord=coord, sess=sess)

    for i in range(6001):
        b_image, b_table0, b_table1, b_table2, b_table3 = sess.run([
            image_batch, num_table1_batch, num_table2_batch, num_table3_batch, num_table4_batch])
        print(b_image, b_table0, b_table1, b_table2, b_table3)

        sess.run(optimizer, feed_dict={x: b_image, y0: b_table0, y1: b_table1, y2: b_table2, y3: b_table3})

        if i % 20 == 0:
            if i % 1000 == 0:
                sess.run(tf.assign(lr, lr/3))
            acc0, acc1, acc2, acc3, loss_ = sess.run([
                accuracy0, accuracy1, accuracy2, accuracy3, total_loss], feed_dict={x: b_image,
                                                                                    y0: b_table0,
                                                                                    y1: b_table1,
                                                                                    y2: b_table2,
                                                                                    y3: b_table3})
            learning_rate = sess.run(lr)
            print('Iter: %d  Loss:%.3F  Accuracy: %.2f, %.2f, %.2f, %.2f  Learning_rate: %.4f'
                  % (i, loss_, acc0, acc1, acc2, acc3, learning_rate))

            if i == 6000:
                saver.save(sess, './tf_save_model/tf_save_model.model', global_step=i)
                break
    coord.request_stop()
    coord.join(threads)





