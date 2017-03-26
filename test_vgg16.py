import numpy as np
import tensorflow as tf

from tensorflow_vgg_train import utils
from tensorflow_vgg_train.vgg import vgg16

img1 = utils.load_image("./test_data/dog.png")[:, :, :3]
img2 = utils.load_image("./test_data/quail227.jpg")[:, :, :3]

batch1 = img1.reshape((1, 224, 224, 3))
batch2 = img2.reshape((1, 224, 224, 3))

batch = np.concatenate((batch1, batch2), 0)

# with tf.Session(config=tf.ConfigProto(gpu_options=(tf.GPUOptions(per_process_gpu_memory_fraction=0.7)))) as sess:
with tf.device('/cpu:0'):
    with tf.Session() as sess:
        images = tf.placeholder("float", [2, 224, 224, 3])
        feed_dict = {images: batch}

        vgg = vgg16.Vgg16()
        with tf.name_scope("content_vgg"):
            vgg.build(images)

        prob = sess.run(vgg.prob, feed_dict=feed_dict)

        utils.print_prob(prob[0], './synset.txt')
        utils.print_prob(prob[1], './synset.txt')