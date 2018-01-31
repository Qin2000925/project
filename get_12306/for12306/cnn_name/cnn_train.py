# coding: utf-8
import tensorflow as tf
import for12306.cnn_name.cnn_inference as cnn_inference
import for12306.cnn_name.get_input_data as get

BATCH_SIZE = 100
LEARNING_RATE_BASE = 0.2  # 学习率
LEARNING_RATE_DECAY = 0.97  # 学习率衰减率
REGULARIZATION_RATE = 0.0001  # 正则化函数中损失系数
TRAINING_STEPS = 30000  # 训练次数
MOVING_AVERAGE_DECAY = 0.99  # 滑动平均衰减率
MODEL_SAVE_PATH = 'd:/12306/cnn_net/save/'
MODEL_NAME = 'model.ckpt'


def train(path):
    x = tf.placeholder(dtype=tf.float32,
                       shape=[None, 25, 60, 1],
                       name='x-input')
    y_ = tf.placeholder(dtype=tf.float32,
                        shape=[None, cnn_inference.NUM_LABELS],
                        name='y-input')
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    y = cnn_inference.inference(input_tensor=x, train=True,
                              reuse=False, regularizer=regularizer)
    global_step = tf.Variable(0, trainable=False)
    variable_averages = tf.train.ExponentialMovingAverage(
        MOVING_AVERAGE_DECAY, num_updates=global_step
    )
    variable_averages_op = variable_averages.apply(tf.trainable_variables())
    cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(
        logits=y, labels=y_
    )
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
    learning_rate = tf.train.exponential_decay(  # 设置指数衰减学习率
        LEARNING_RATE_BASE,  # 基础学习率
        global_step,   # 迭代轮数
        70,   # 所有数据训练一次的迭代次数
        LEARNING_RATE_DECAY  # 学习衰减速度
    )
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(
        loss, global_step=global_step
    )
    train_op = tf.group(train_step, variable_averages_op)  # 把这两个操作放在一个组，同时一起执行
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean((tf.cast(correct_prediction, tf.float32)))
    saver = tf.train.Saver()
    with tf.Session() as sess:
        # tf.global_variables_initializer().run()
        ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
        if ckpt and ckpt.model_checkpoint_path:  # 判断文件路径是否存在
            saver.restore(sess=sess, save_path=ckpt.model_checkpoint_path)
        else:
            print('没有保存的模型数据')
            return 0
        data = get.get_data1(path)
        for i in range(TRAINING_STEPS):
            batch = get.get_random_data1(data, 100)
            sess.run(train_op, feed_dict={x: batch[0], y_: batch[1]})
            a = sess.run(accuracy, feed_dict={x: batch[0], y_: batch[1]})
            if i % 10 == 0:

                print('accuracy: %f' % a,
                      'steps: %d' % i)
            if a > 0.98:
                saver.save(sess=sess, save_path=MODEL_SAVE_PATH + MODEL_NAME)
                print('保存完毕......', a)
                return


def main():
    root_path = 'D:/12306/cnn_net/name'
    train(root_path)


if __name__ == "__main__":
    main()