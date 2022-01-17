from __future__ import division
import tensorflow as tf
import numpy as np
import os 
import pydicom
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
from skimage.util import img_as_float
from skimage.segmentation import slic
import os
import sys
import random
import scipy.ndimage

DIRECTORY_IMAGES = './'

RANDOM_SEED = 4242
SAMPLES_PER_FILES = 300

def get_image_data_from_pydicom(dm, q):
    dm = pydicom.read_file(dm)
    #x = 1260
    #y = 910
    #xscale = x/dm.Rows
    #yscale = y/dm.Columns
    image_data = np.array(dm.pixel_array)
    #image_data = np.float32(image_data)
    #image_data = scipy.ndimage.interpolation.zoom(image_data, [xscale,yscale])
    print(image_data.shape)

    for p in range(175):

        img_data = image_data[p,:,:,0]
        #image = img_as_float(image_data)
        #superpixels = slic(image_data, n_segments = 2000, compactness=0.01, max_iter=10)
        im = Image.fromarray(img_data)
        #jpeg_dir = os.makedirs("./datasets/jpeg_%s"%q)
        ###im.save("./png/png_%s"%q + "out_%s.png"%p)
        im.save("./png/217a" + "out%s.png" % p)
    return image_data

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _convert_to_example(image_data):

    """Build an Example proto for an image example.
    Args:
      image_data: string, JPEG encoding of RGB image.
      labels: list of integers, identifier for the ground truth;
      instance: instance labels.
      labels_text: list of strings, human-readable labels.
      mask_instance: numpy matrix of instance.
      mask_class: numpy matrix of class.
      shape: 3 integers, image shapes in pixels.
    Returns:
      Example proto
    """
    example = tf.train.Example(features=tf.train.Features(feature={
        #'image/height': _int64_feature(shape[0]),
        #'image/width': _int64_feature(shape[1]),
        #'image/channels': _int64_feature(shape[2]),
        #'image/shape': _int64_feature(shape),
        'image/image_data':_bytes_feature(image_data.tostring()),
        #'image/superpixels':_bytes_feature(superpixels.tostring()),
        #'image/mask_instance':_bytes_feature(mask_instance.tostring()),
        #'image/mask_class':_bytes_feature(mask_class.tostring()),
        #'image/class_labels':_int64_feature(class_labels),
        #'image/instance_labels':_int64_feature(instance_labels)
    }))
    return example

def _add_to_tfrecord(dataset_dir, name, tfrecord_writer, q):
    """Loads data from image and annotations files and add them to a TFRecord.
    Args:
      dataset_dir: Dataset directory;
      name: Image name to add to the TFRecord;
      tfrecord_writer: The TFRecord writer to use for writing.
    """

    dm = dataset_dir + DIRECTORY_IMAGES + name +'.dcm'
    #xml = dataset_dir + DIRECTORY_ANNOTATIONS + name + '.xml'
    image_data = get_image_data_from_pydicom(dm, q)
    #mask_instance, mask_class, shape, class_labels, class_labels_text, instance_labels = groundtruth_to_mask(xml)
    example = _convert_to_example(image_data)
    tfrecord_writer.write(example.SerializeToString())

def _get_output_filename(output_dir, name, idx):
    return '%s/%s.tfrecord' % (output_dir, name)

def run(dataset_dir, output_dir, name='diameter_measurement', shuffling=False):
    """
    Args:
      dataset_dir: The dataset directory where the dataset is stored.
      output_dir: Output directory.
    """
    if not tf.gfile.Exists(output_dir):
        tf.gfile.MakeDirs(output_dir)
    path = os.path.join(dataset_dir)
    filenames = sorted(os.listdir(path))
    if shuffling:
        random.seed(RANDOM_SEED)
        random.shuffle(filenames)
    i = 0
    fidx = 0
    while i < len(filenames):
    # Open new TFRecord file.
        tf_filename  = _get_output_filename(output_dir, name, fidx)   
        with tf.python_io.TFRecordWriter(tf_filename) as tfrecord_writer:
            j = 0
            #while i < len(filenames) and j < SAMPLES_PER_FILES:
            for q in range(1):
                sys.stdout.write('\r>> Converting image %d/%d' % (i+1, len(filenames)))
                sys.stdout.flush()
                filename = filenames[i]
                img_name = filename[:-4]
                _add_to_tfrecord(dataset_dir, img_name, tfrecord_writer, q)
                i += 1
                j += 1
            fidx += 1
    print('\nFinished converting the diameter measure dataset!')



        
        
