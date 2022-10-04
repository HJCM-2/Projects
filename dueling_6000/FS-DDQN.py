import tensorflow as tf
import numpy as np
import rospy
import random
import time
import copy

from StageWorld import StageWorld
from ReplayBuffer import ReplayBuffer
from reward import Reward
from network import Network


import matplotlib.pyplot as plt
import matplotlib.colors as colors

# ==========================
#   Training Parameters
# ==========================

GAME = 'StageWorld'
ACTION = 9
SPEED = 2
GAMMA = 0.99
OBSERVE = 0
EXPLORE = 200000
FINAL_EPSILON = 0.001
INITIAL_EPSILON = 0.01
BUFFER_SIZE = 20000
MINIBATCH_SIZE = 64
MAX_EPISODES = 20000

LASER_BEAM = 1080
LASER_HIST = 3
TARGET = 2

# Reward parameters
REWARD_FACTOR = 0.1
LEARNING_RATE = 0.0001

SUMMARY_DIR = './results/tf_ddpg'
RANDOM_SEED = 1234


learning_rate = LEARNING_RATE
a_dim = ACTION
action_bound = [0.5, 1]
tau = 0.001


# ===========================
#   Tensorflow Summary Ops
# ===========================

def build_summaries():
    episode_reward = tf.Variable(0.)
    tf.summary.scalar("Reward", episode_reward)
    episode_ave_max_q = tf.Variable(0.)
    tf.summary.scalar("Qmax Value", episode_ave_max_q)

    summary_vars = [episode_reward, episode_ave_max_q]
    summary_ops = tf.summary.merge_all()

    return summary_ops, summary_vars

# ===========================
#   Agent Training
# ===========================


def train(sess, env, network, reward, discrete):  
    # Set up summary writer
    summary_writer = tf.summary.FileWriter("dqn_summary")

    saver = tf.train.Saver()
    sess.run(tf.global_variables_initializer())
    checkpoint = tf.train.get_checkpoint_state("saved_networks")
    print('checkpoint:', checkpoint)
    if checkpoint and checkpoint.model_checkpoint_path:
        saver.restore(sess, checkpoint.model_checkpoint_path)
        print("Successfully loaded:", checkpoint.model_checkpoint_path)
    else:
        print("Could not find old network weights")

    network.update_target_network()

    buff = ReplayBuffer(BUFFER_SIZE)  # Create replay buffer

    # plot settings
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(env.map, aspect='auto', cmap='hot', vmin=0., vmax=1.5)
    plt.show(block=False)

    epsilon = INITIAL_EPSILON

    rate = rospy.Rate(5)
    loop_time = time.time()
    last_loop_time = loop_time
    i = 0

    s1 = env.GetLaserObservation()
    s_1 = np.reshape(s1, (LASER_BEAM, 1))
    s__1 = np.stack((s_1, s_1, s_1), axis=2)

    T = 0
    for i in range(MAX_EPISODES):
        env.ResetWorld()
        env.GenerateTargetPoint()
        print 'Target: (%.4f, %.4f)' % (env.target_point[0], env.target_point[1])
        target_distance = copy.deepcopy(env.distance)
        ep_reward = 0.
        ep_ave_max_q = 0.
        loop_time_buf = []
        terminal = False

        j = 0
        c = []
        d = []
        action2 = [0.3, 0]
        ep_reward = 0
        ep_ave_max_q = 0
        ep_PID_count = 0.

        loss = 0.
        while not terminal and not rospy.is_shutdown():
            s1 = env.GetLaserObservation()
            s_1 = np.reshape(s1, (LASER_BEAM, 1, 1))
            s__1 = np.append(s_1, s__1[:, :, :(LASER_HIST - 1)], axis=2)

            target1 = env.GetLocalTarget()
            speed1 = env.GetSelfSpeed()
            state1 = s__1
            [x, y, theta] = env.GetSelfStateGT()
            map_img = env.RenderMap([[0, 0], env.target_point])
            
            r, terminal, result = env.GetRewardAndTerminate(j)
            ep_reward += r
            if j > 0:
                buff.add(state, a_t, r, state1, terminal, target, target1, speed, speed1)  # Add replay buffer
            j += 1
            
            state = state1
            target = target1
            speed = speed1

            readout_t = network.predict(np.reshape(state, (1, network.beam, 1, network.hist)), np.reshape(target, (1, network.target_size)), 
            np.reshape(speed, (1, network.velocity_size)))	
            
            a_t = np.zeros([ACTION])
            action_index = 0

            # a = env.PIDController([30.,np.pi/3])
            if i <= OBSERVE:
                action_index = random.randrange(ACTION)
                a_t[action_index] = 1
            else:
                if random.random() <= epsilon:
                    print("----------Random Action----------")
                    action_index = random.randrange(ACTION)
                    a_t[random.randrange(ACTION)] = 1
                else:
                    action_index = np.argmax(readout_t)
                    a_t[action_index] = 1

            action1 = [0., 0.]
            Q = np.array([[-action_bound[0], -action_bound[1]],
            [0, -action_bound[1]], [0, action_bound[1]], [0, 0],
            [-action_bound[0], 0], [action_bound[0], 0],  [-action_bound[0], action_bound[1]],
            [action_bound[0], -action_bound[1]], [action_bound[0], action_bound[1]]])
            action1 = Q[action_index, :]
            # action2 = action2 + action1*(loop_time - last_loop_time)
            action2 = action2 + action1*0.1

            if action2[1] > np.pi/2:
                action2[1] = np.pi/2
            if action2[1] < -np.pi/2:
                action2[1] = -np.pi/2
            if action2[0] > 0.5:
                action2[0] = 0.5
            if action2[0] < 0.05:
                action2[0] = 0.05

            env.Control(action2)

            # already define "c=[],d=[]" before
            c.insert(j, action2[0]) 
            d.insert(j, action2[1])
            if i % 200 == 0:
                # print ("v=%s"%(action2[0]))					#action[1]=w
                # print ("w=%s"%(action2[1]))				        #speed & action are different: speed is from running,while action is sampled from a specific time_step
                np.save("./data/speed_v%s.npy" % (i), c)
                np.save("./data/speed_w%s.npy" % (i), d)
                # print("save speed_v%s.npy & speed_w%s.npy are done"%(i,i))

            # plot
            if j == 1:
                im.set_array(map_img)
                fig.canvas.draw()

            # Keep adding experience to the memory until
            # there are at least minibatch size samples
            if i > OBSERVE:
                if buff.count() > MINIBATCH_SIZE:
                    batch = buff.getBatch(MINIBATCH_SIZE)
                    s_batch = np.asarray([e[0] for e in batch])
                    a_batch = np.asarray([e[1] for e in batch])
                    r_batch = np.asarray([e[2] for e in batch])
                    s2_batch = np.asarray([e[3] for e in batch])
                    t_batch = np.asarray([e[4] for e in batch])
                    target_batch = np.asarray([e[5] for e in batch])
                    target1_batch = np.asarray([e[6] for e in batch])
                    speed_batch = np.asarray([e[7] for e in batch])
                    speed1_batch = np.asarray([e[8] for e in batch])

                    q = network.predict(s2_batch, target1_batch, speed1_batch)
                    q_next = network.predict_target(s2_batch, target1_batch, speed1_batch)

                    y_i = []
                    for k in range(MINIBATCH_SIZE):
                        if t_batch[k]:
                            y_i.append(r_batch[k])
                        else:
                            y_i.append(r_batch[k] + GAMMA * q_next[k, np.argmax(q[k])])

                    loss = network.get_the_whole_loss(s_batch, target_batch, speed_batch, a_batch, y_i)
                    q_out, _ = network.train(s_batch, target_batch, speed_batch, a_batch, y_i)

                    ep_ave_max_q += np.amax(q_out)
                    network.update_target_network()

            last_loop_time = loop_time
            loop_time = time.time()
            loop_time_buf.append(loop_time - last_loop_time)
            T += 1
            rate.sleep()

        #  scale down epsilon
        if epsilon > FINAL_EPSILON and i > OBSERVE:
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

        summary = tf.Summary()
        summary.value.add(tag='Reward', simple_value=float(ep_reward))
        summary.value.add(tag='Qmax', simple_value=float(ep_ave_max_q / float(j)))
        summary.value.add(tag='PIDrate', simple_value=float(ep_PID_count / float(j)))
        summary.value.add(tag='Distance', simple_value=float(target_distance))
        summary.value.add(tag='Result', simple_value=float(result))
        summary.value.add(tag='Steps', simple_value=float(j))
        
        summary.value.add(tag='loss', simple_value=loss)

        summary_writer.add_summary(summary, T)

        summary_writer.flush()

        if i > 0 and i % 1000 == 0:
            saver.save(sess, 'saved_networks/' + GAME + '-dqn', global_step = i) 

        print ('| Reward: %.2f' % ep_reward, " | Episode:", i, " | LoopTime: %.4f" % (np.mean(loop_time_buf)), " | Step:", j-1, '\n')


def main(_):
    with tf.Session() as sess:
        init_op = tf.global_variables_initializer()
        sess.run(init_op)

        env = StageWorld(LASER_BEAM)
        np.random.seed(RANDOM_SEED)
        tf.set_random_seed(RANDOM_SEED)

        discrete = False
        print('Continuous Action Space')

        network = Network(sess, LASER_BEAM, LASER_HIST, TARGET, SPEED, a_dim, action_bound, learning_rate, tau)

        reward = Reward(REWARD_FACTOR, GAMMA)

        try:
            train(sess, env, network, reward, discrete)
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    tf.app.run()
