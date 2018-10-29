import tensorflow as tf

flags = tf.app.flags

#####################
#command prompt flags
#####################
flags.DEFINE_integer('number_of_neurons', 126, 'Number of neurons')
flags.DEFINE_integer('image_width', 14, 'Image width')
flags.DEFINE_integer('steps', 100, 'Step count in update')
flags.DEFINE_integer('number_of_tests', 100, 'Number of tests')

flags.DEFINE_float('distortion', 0.1, 'Step size')

flags.DEFINE_string('update_type', 'asynchronous', 'Network update type: [asynchronous, synchronous]')
flags.DEFINE_string('images_path', r'.\data\animals-14x9.csv', 'Training file path')

cfg = tf.app.flags.FLAGS
