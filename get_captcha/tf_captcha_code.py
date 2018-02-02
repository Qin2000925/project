import tensorflow as tf
from nets import nets_factory


CHAR_SET_LEN = 10
IMAGE_HEIGHT = 60
IMAGE_WIDTH = 160
BATCH_SIZE = 50

TF_RECORD_FILE = '/home/qinjiahu521/.virtualenvs/python3/GIT/get_captcha/tf_number_record/train.tfrecords'

x = tf.placeholder(tf.float32, [None, 224, 224])
y0 = tf.placeholder(tf.float32, [None])
y1 = tf.placeholder(tf.float32, [None])
y2 = tf.placeholder(tf.float32, [None])
y3 = tf.placeholder(tf.float32, [None])
y4 = tf.placeholder(tf.float32, [None])
y5 = tf.placeholder(tf.float32, [None])

lr = tf.Variable(0.003, dtype=tf.float32)
print('lr:', lr)


def read_and_decode(filename):
    filename_queue = tf.train.string_input_producer([filename], num_epochs=None)
    reader = tf.TFRecordReader()

    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example, features={
        'image': tf.FixedLenFeature([], tf.string),
        'num_table1': tf.FixedLenFeature([], tf.string),
        'num_table2': tf.FixedLenFeature([], tf.int64),
        'num_table3': tf.FixedLenFeature([], tf.int64),
        'num_table4': tf.FixedLenFeature([], tf.int64),
        'num_table5': tf.FixedLenFeature([], tf.int64),
        'num_table6': tf.FixedLenFeature([], tf.int64),
    })
    image = tf.decode_raw(features['image'], tf.uint8)
    image = tf.reshape(image, [224, 224])
    image = tf.cast(image, tf.float32) / 255.0
    image = tf.subtract(image, 0.5)
    image = tf.multiply(image, 2.0)
    num_table1 = tf.cast(features['num_table1'], tf.int64)
    num_table2 = tf.cast(features['num_table2'], tf.int64)
    num_table3 = tf.cast(features['num_table3'], tf.int64)
    num_table4 = tf.cast(features['num_table4'], tf.int64)
    num_table5 = tf.cast(features['num_table5'], tf.int64)
    num_table6 = tf.cast(features['num_table6'], tf.int64)

    print(image, num_table1, num_table2, num_table3, num_table4, num_table5, num_table6)

    return image, num_table1, num_table2, num_table3, num_table4, num_table5, num_table6


image, num_table1, num_table2, num_table3, num_table4, num_table5, num_table6 = read_and_decode(TF_RECORD_FILE)

image_batch, num_table1_batch, num_table2_batch, num_table3_batch, num_table4_batch, \
num_table5_batch, num_table6_batch = tf.train.shuffle_batch([image, num_table1, num_table2, num_table3, num_table4, num_table5, num_table6],
                                                            batch_size=100, capacity=100000, min_after_dequeue=50000, num_threads=1)
train_network_fn = nets_factory.get_network_fn(
    'alexnet_v2',
    num_classes=CHAR_SET_LEN,
    weight_decay=0.005,
    is_training=True)
with tf.Session() as sess:
    X = tf.reshape(x, [BATCH_SIZE, 224, 224, 1])
    log_its0, log_its1, log_its2, log_its3, log_its4, log_its5, end_points = train_network_fn(X)

    one_hot_num_table0 = tf.one_hot(indices=tf.cast(y0, tf.int32), depth=CHAR_SET_LEN)
    one_hot_num_table1 = tf.one_hot(indices=tf.cast(y1, tf.int32), depth=CHAR_SET_LEN)
    one_hot_num_table2 = tf.one_hot(indices=tf.cast(y2, tf.int32), depth=CHAR_SET_LEN)
    one_hot_num_table3 = tf.one_hot(indices=tf.cast(y3, tf.int32), depth=CHAR_SET_LEN)
    one_hot_num_table4 = tf.one_hot(indices=tf.cast(y4, tf.int32), depth=CHAR_SET_LEN)
    one_hot_num_table5 = tf.one_hot(indices=tf.cast(y5, tf.int32), depth=CHAR_SET_LEN)

    loss0 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=log_its0, labels=one_hot_num_table0))
    loss1 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=log_its1, labels=one_hot_num_table1))
    loss2 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=log_its2, labels=one_hot_num_table2))
    loss3 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=log_its3, labels=one_hot_num_table3))
    loss4 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=log_its4, labels=one_hot_num_table4))
    loss5 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=log_its5, labels=one_hot_num_table5))

    total_loss = (loss0 + loss1 + loss2 + loss3 + loss4 + loss5) / 6.0

    optimizer = tf.train.AdamOptimizer(learning_rate=lr).minimize(total_loss)

    correct_prediction0 = tf.equal(tf.argmax(one_hot_num_table0, 1), tf.argmax(log_its0, 1))
    accuracy0 = tf.reduce_mean(tf.cast(correct_prediction0, tf.float32))
    correct_prediction1 = tf.equal(tf.argmax(one_hot_num_table1, 1), tf.argmax(log_its0, 1))
    accuracy1 = tf.reduce_mean(tf.cast(correct_prediction1, tf.float32))
    correct_prediction2 = tf.equal(tf.argmax(one_hot_num_table2, 1), tf.argmax(log_its0, 1))
    accuracy2 = tf.reduce_mean(tf.cast(correct_prediction2, tf.float32))
    correct_prediction3 = tf.equal(tf.argmax(one_hot_num_table3, 1), tf.argmax(log_its0, 1))
    accuracy3 = tf.reduce_mean(tf.cast(correct_prediction3, tf.float32))
    correct_prediction4 = tf.equal(tf.argmax(one_hot_num_table4, 1), tf.argmax(log_its0, 1))
    accuracy4 = tf.reduce_mean(tf.cast(correct_prediction4, tf.float32))
    correct_prediction5 = tf.equal(tf.argmax(one_hot_num_table5, 1), tf.argmax(log_its0, 1))
    accuracy5 = tf.reduce_mean(tf.cast(correct_prediction5, tf.float32))

    saver = tf.train.Saver()
    # sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())

    coord = tf.train.Coordinator()

    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    for i in range(15000):
        b_image, b_table0, b_table1, b_table2, b_table3, b_table4, b_table5 = sess.run([
            image_batch, num_table1_batch, num_table2_batch, num_table3_batch,
            num_table4_batch, num_table5_batch, num_table6_batch])

        sess.run(optimizer, feed_dict={x: b_image, y0: b_table0, y1: b_table1, y2: b_table2,
                                       y3: b_table3, y4: b_table4, y5: b_table5})

        if i % 20 == 0:
            if i % 3000 == 0:
                sess.run(tf.assign(lr, lr/3))
            acc0, acc1, acc2, acc3, acc4, acc5, loss_ = sess.run([accuracy0, accuracy1, accuracy2, accuracy3,
                                                           accuracy4, accuracy5, total_loss], feed_dict={x: b_image,
                                                                                                         y0: b_table0,
                                                                                                         y1: b_table1,
                                                                                                         y2: b_table2,
                                                                                                         y3: b_table3,
                                                                                                         y4: b_table4,
                                                                                                         y5: b_table5})
            learning_rate = sess.run(lr)
            print('Iter: %d  Loss:%.3F  Accuracy: %.2f, %.2f, %.2f, %.2f, %.2f, %.2f  Learning_rate: %.4f'
                  % (i, loss_, acc0, acc1, acc2, acc3, acc4, acc5, learning_rate))

            if i == 15000:
                saver.save(sess, './tf_save_model/tf_save_model.model', global_step=i)
                break
    coord.request_stop()
    coord.join(threads)





