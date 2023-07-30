import onnx
from onnx_tf.backend import prepare
import tensorflow as tf

import torch
from train import dummy_input
from train import model,input_size,output_size

#torch.onnx.export(model, dummy_input, "model.onnx")
input_names = ['input']
output_names = ['output']
torch.onnx.export(model, dummy_input, "model.onnx",input_names=input_names, output_names=output_names)

# Load the ONNX file
model = onnx.load('model.onnx')

# Convert to format
tf_rep = prepare(model)

# Export model as .pb file
tf_rep.export_graph('model.pb')

# Convert the model to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_saved_model('model.pb')
tflite_model = converter.convert()
open("model.tflite", "wb").write(tflite_model)




