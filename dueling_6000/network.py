import tensorflow as tf

n_hidden_1 = 256
n_hidden_2 = 256
n_hidden_3 = 256

def variable_summaries(var):
    """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
    with tf.name_scope('summaries'):
        mean = tf.reduce_mean(var)
    tf.summary.scalar('mean', mean)
    with tf.name_scope('stddev'):
        stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
    tf.summary.scalar('stddev', stddev)
    tf.summary.scalar('max', tf.reduce_max(var))
    tf.summary.scalar('min', tf.reduce_min(var))
    tf.summary.histogram('histogram', var)

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.01)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.03, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W, stride_h, stride_w):
    return tf.nn.conv2d(x, W, strides=[1, stride_h, stride_w, 1], padding="SAME")


class Network(object):

    def __init__(self, sess, beam, hist, target_size, velocity_size, action_dim, action_bound, learning_rate, tau):
        
        self.sess = sess
        self.beam = beam
        self.hist = hist
        self.target_size = target_size
        self.velocity_size = velocity_size
        self.a_dim = action_dim
        self.action_bound = action_bound
        self.learning_rate = learning_rate
        self.tau = tau

        # Network
        self.inputs, self.target, self.velocity, self.out = self.CreateNetwork()
        self.network_params = tf.trainable_variables()

        # Target Network
        self.target_inputs, self.target_target, self.target_velocity, self.target_out = self.CreateNetwork()

        self.target_network_params = tf.trainable_variables()[len(self.network_params):]

        #  Op for periodically updating target network with online network weights
        self.update_target_network_params = \
            [self.target_network_params[i].assign(tf.multiply(self.network_params[i], self.tau) + \
                                                  tf.multiply(self.target_network_params[i], 1. - self.tau))
             for i in range(len(self.target_network_params))]

        self.num_trainable_vars = len(self.network_params) + len(self.target_network_params)

        self.action = tf.placeholder(tf.float32, [None, self.a_dim])
        self.target_q_value = tf.placeholder(tf.float32, [None])
        self.readout_action = tf.reduce_sum(tf.multiply(self.out, self.action), reduction_indices=1)
        self.loss = tf.reduce_mean(tf.square(self.target_q_value-self.readout_action))
    
        self.optimize = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)


    def CreateNetwork(self):
 	with tf.name_scope("Conv1"):
            W_conv1 = weight_variable([7, 1, self.hist, 16])
            variable_summaries(W_conv1)
            b_conv1 = bias_variable([16])
        # 360x1x16
        with tf.name_scope("Conv2"):
            W_conv2 = weight_variable([5, 1, 16, 16])
            variable_summaries(W_conv2)
            b_conv2 = bias_variable([16])
        # 120x1x16
        with tf.name_scope("Conv3"):
            W_conv3 = weight_variable([5, 1, 16, 32])
            variable_summaries(W_conv3)
            b_conv3 = bias_variable([32])
        # 40x1x32
        with tf.name_scope("Conv4"):
            W_conv4 = weight_variable([3, 1, 32, 32])
            variable_summaries(W_conv4)
            b_conv4 = bias_variable([32])
        # 20x1x32
        with tf.name_scope("Conv5"):
            W_conv5 = weight_variable([3, 1, 32, 64])
            variable_summaries(W_conv5)
            b_conv5 = bias_variable([64])
        # 10x1x64
        with tf.name_scope("Conv6"):
            W_conv6 = weight_variable([3, 1, 64, 64])
            variable_summaries(W_conv6)
            b_conv6 = bias_variable([64])
        # 10x1x64
        with tf.name_scope("FC1"):
            W_fc1 = weight_variable([1080/3/3/3/2/2/1*64, n_hidden_1])
            variable_summaries(W_fc1)
            b_fc1 = bias_variable([n_hidden_1])
        with tf.name_scope("FC2"):
            W_fc2 = weight_variable([n_hidden_1 + 4, n_hidden_2])
            variable_summaries(W_fc2)
            b_fc2 = bias_variable([n_hidden_2])
        with tf.name_scope("FC3"):
            W_fc3 = weight_variable([n_hidden_2, n_hidden_3])
            variable_summaries(W_fc3)
            b_fc3 = bias_variable([n_hidden_3])
        # out_v
        with tf.name_scope("out_v"):
            W_v = weight_variable([n_hidden_3, 1])
            variable_summaries(W_v)
            b_v = bias_variable([1])
        # out_a
        with tf.name_scope("out_a"):
            W_a = weight_variable([n_hidden_3, self.a_dim])
            variable_summaries(W_a)
            b_a = bias_variable([self.a_dim])

        # input layer
        inputs = tf.placeholder(tf.float32, [None, self.beam, 1, self.hist])
        target = tf.placeholder(tf.float32, [None, self.target_size])
        velocity = tf.placeholder(tf.float32, [None, self.velocity_size])

        h_conv1 = tf.nn.relu(conv2d(inputs, W_conv1, 3, 1) + b_conv1)
        h_conv2 = tf.nn.relu(conv2d(h_conv1, W_conv2, 3, 1) + b_conv2)
        h_conv3 = tf.nn.relu(conv2d(h_conv2, W_conv3, 3, 1) + b_conv3)
        h_conv4 = tf.nn.relu(conv2d(h_conv3, W_conv4, 2, 1) + b_conv4)
        h_conv5 = tf.nn.relu(conv2d(h_conv4, W_conv5, 2, 1) + b_conv5)
        h_conv6 = tf.nn.relu(conv2d(h_conv5, W_conv6, 1, 1) + b_conv6)
        h_conv3_flat = tf.reshape(h_conv6, [-1, 1080/3/3/3/2/2/1*64])
        h_fc1 = tf.nn.relu(tf.matmul(h_conv3_flat, W_fc1) + b_fc1)
        h_fc1_tv = tf.concat([h_fc1, target, velocity], axis=1)
        h_fc2 = tf.nn.relu(tf.matmul(h_fc1_tv, W_fc2) + b_fc2)
        h_fc3 = tf.nn.relu(tf.matmul(h_fc2, W_fc3) + b_fc3)
        out_v = tf.matmul(h_fc3, W_v) + b_v
        out_a = tf.matmul(h_fc3, W_a) + b_a
        advAvg = tf.expand_dims(tf.reduce_mean(out_a, axis=1), axis=1)
        advIdentifiable = tf.subtract(out_a, advAvg)
        out = tf.add(out_v, advIdentifiable)
        return inputs, target, velocity, out

    def train(self, inputs, target, velocity, action, target_q_value):
        return self.sess.run([self.out, self.optimize], feed_dict={
            self.inputs: inputs,
            self.target: target,
            self.velocity: velocity,
            self.action: action,
            self.target_q_value: target_q_value
        })


    def predict(self, inputs, target, velocity):
        return self.sess.run(self.out, feed_dict={
            self.inputs: inputs,
            self.target: target,
            self.velocity: velocity
        })

    def predict_target(self, inputs, target, velocity):
        return self.sess.run(self.target_out, feed_dict={
            self.target_inputs: inputs,
            self.target_target: target,
            self.target_velocity: velocity
        })

    def update_target_network(self):
        self.sess.run(self.update_target_network_params)

    def get_num_trainable_vars(self):
        return self.num_trainable_vars

    def get_the_whole_loss(self, inputs, target, velocity, action, target_q_value):
        return self.sess.run(self.loss, feed_dict={
            self.inputs: inputs,
            self.target: target,
            self.velocity: velocity,
            self.action: action,
            self.target_q_value: target_q_value
        })
