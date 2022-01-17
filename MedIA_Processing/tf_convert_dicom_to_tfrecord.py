"""Convert a dataset to TFRecords format, which can be easily integrated into
a TensorFlow pipeline.
Usage:
```shell
python tf_convert_dicom_to_tfrecord.py \
    --dataset_name=diameter \
    --dataset_dir=./datasets/dicom/ \
    --output_name=diameter_pixel \
    --output_dir=./datasets/tfrecords_diameter_with_superpixels
```
"""
import tensorflow as tf

import convert_dicom_to_tfrecord

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string(
    'dataset_name', 'diameter',
    'The name of the dataset to convert.')
tf.app.flags.DEFINE_string(
    'dataset_dir', 'E:/Heart Data/yuanshi/2/217a',
    'Directory where the original dataset 6is stored.')
tf.app.flags.DEFINE_string(
    'output_name','pixel',
    'Basename used for TFRecords output files.')
tf.app.flags.DEFINE_string(
    'output_dir', 'E:/Heart Data/png',
    'Output directory where to store TFRecords files.')

def main(_):
    if not FLAGS.dataset_dir:
        raise ValueError('You must supply the dataset directory with --dataset_dir')
    print('Dataset directory:', FLAGS.dataset_dir)
    print('Output directory:', FLAGS.output_dir)

    if FLAGS.dataset_name == 'diameter':
        convert_dicom_to_tfrecord.run(FLAGS.dataset_dir, FLAGS.output_dir, FLAGS.output_name)
    else:
        raise ValueError('Dataset [%s] was not recognized.' % FLAGS.dataset_name)
        
        
if __name__ == '__main__':
    tf.app.run()