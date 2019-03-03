#!/usr/bin/python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import time
import os
import requests
import json
from geo import geodict_lib

import numpy as np
import tensorflow as tf


from scrape_tweets import scrape


def run_quickstart(file_name):
    import io
    import os
    
    # Imports the Google Cloud client library
    from google.cloud import vision
    from google.cloud.vision import types
    
    # Instantiates a client
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/osboxes/hoohacks/halogen-oxide-233408-a42829cf139a.json"
    client = vision.ImageAnnotatorClient()

    
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    labelsFiltered = []
    labelsTags = []
    print('Labels:')
    for label in labels:
        print(label.description)
        if (label.description == "Hurricane" or label.description== "Flood" or label.description=="Tornado" or label.description=="Landslide" or label.description== "Earthquake" or label.description== "Volcano" or label.description=="Disaster" or label.description=="Typhoon" or label.description=="Fire"):
            labelsFiltered.append(label.description)
        else:
            labelsTags.append(label.description)

    labelsFiltStr = ','.join(str(labelsFiltered).split(", "))
    labelsTagsStr = ','.join(str(labelsTags).split(", "))
    
    return labelsFiltStr, labelsTagsStr


def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
				input_mean=0, input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels = 3,
                                       name='png_reader')
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                  name='gif_reader'))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                        name='jpeg_reader')
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0);
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

def tens_Two(file_name):
  graph = load_graph(model_file)
  t = read_tensor_from_image_file(file_name,
                                  input_height=input_height,
                                  input_width=input_width,
                                  input_mean=input_mean,
                                  input_std=input_std)

  input_name = "import/" + input_layer
  output_name = "import/" + output_layer
  input_operation = graph.get_operation_by_name(input_name)
  output_operation = graph.get_operation_by_name(output_name)

  with tf.Session(graph=graph) as sess:
    start = time.time()
    results = sess.run(output_operation.outputs[0],
                      {input_operation.outputs[0]: t})
    end=time.time()
  results = np.squeeze(results)

  top_k = results.argsort()[-5:][::-1]
  labels = load_labels(label_file)

  print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))
  template = "{} (score={:0.5f})"

  for i in top_k:
    print(template.format(labels[i], results[i]))

  maxResult = max(results)

  for j in range(0, len(results)):
    if (results[j]==maxResult):
        condition = labels[j]

  return condition

if __name__ == "__main__":

  file_name = "tf_files/disaster_images.jpg"
  model_file = "tf_files/retrained_graph.pb"
  label_file = "tf_files/retrained_labels.txt"
  input_height = 299
  input_width = 299
  input_mean = 128
  input_std = 128
  input_layer = "Mul"
  output_layer = "final_result"

  parser = argparse.ArgumentParser()
  parser.add_argument("--image", help="image to be processed")
  parser.add_argument("--graph", help="graph/model to be executed")
  parser.add_argument("--labels", help="name of file containing labels")
  parser.add_argument("--input_height", type=int, help="input height")
  parser.add_argument("--input_width", type=int, help="input width")
  parser.add_argument("--input_mean", type=int, help="input mean")
  parser.add_argument("--input_std", type=int, help="input std")
  parser.add_argument("--input_layer", help="name of input layer")
  parser.add_argument("--output_layer", help="name of output layer")
  args = parser.parse_args()

  if args.graph:
    model_file = args.graph
  if args.image:
    file_name = args.image
  if args.labels:
    label_file = args.labels
  if args.input_height:
    input_height = args.input_height
  if args.input_width:
    input_width = args.input_width
  if args.input_mean:
    input_mean = args.input_mean
  if args.input_std:
    input_std = args.input_std
  if args.input_layer:
    input_layer = args.input_layer
  if args.output_layer:
    output_layer = args.output_layer

  url = 'https://hoos-disaster-relief.herokuapp.com/api/add'
  tweets = scrape()
  for tweet in tweets:
    # location not currently working
    # location = geodict_lib.find_locations_in_text(tweet["text"])
    location = ""
    path = os.path.join(os.getcwd(), "media_images/" + tweet["pic"])
    tags = run_quickstart(path)
    disaster_tags = tags[0]
    other_tags = tags[1]
    severity = tens_Two(path)

    tweet.update({
      'location_name': location,
      'disaster_type': disaster_tags,
      'tags': other_tags,
      'disaster_severity': severity,
    })

    response = requests.post(url, data=json.loads(json.dumps(tweet)))