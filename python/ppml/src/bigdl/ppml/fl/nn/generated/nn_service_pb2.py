# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nn_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import fl_base_pb2 as fl__base__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10nn_service.proto\x12\x02nn\x1a\rfl_base.proto\"O\n\x0cTrainRequest\x12\x12\n\nclientuuid\x18\x01 \x01(\t\x12\x18\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\n.TensorMap\x12\x11\n\talgorithm\x18\x03 \x01(\t\"I\n\rTrainResponse\x12\x10\n\x08response\x18\x01 \x01(\t\x12\x18\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\n.TensorMap\x12\x0c\n\x04\x63ode\x18\x03 \x01(\x05\"b\n\x0f\x45valuateRequest\x12\x12\n\nclientuuid\x18\x01 \x01(\t\x12\x18\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\n.TensorMap\x12\x11\n\talgorithm\x18\x03 \x01(\t\x12\x0e\n\x06return\x18\x04 \x01(\x08\"]\n\x10\x45valuateResponse\x12\x10\n\x08response\x18\x01 \x01(\t\x12\x18\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\n.TensorMap\x12\x0c\n\x04\x63ode\x18\x03 \x01(\x05\x12\x0f\n\x07message\x18\x04 \x01(\t\"Q\n\x0ePredictRequest\x12\x12\n\nclientuuid\x18\x01 \x01(\t\x12\x18\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\n.TensorMap\x12\x11\n\talgorithm\x18\x03 \x01(\t\"K\n\x0fPredictResponse\x12\x10\n\x08response\x18\x01 \x01(\t\x12\x18\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\n.TensorMap\x12\x0c\n\x04\x63ode\x18\x03 \x01(\x05\"r\n\x11UploadMetaRequest\x12\x13\n\x0b\x63lient_uuid\x18\x01 \x01(\t\x12\x0f\n\x07loss_fn\x18\x02 \x01(\x0c\x12#\n\toptimizer\x18\x03 \x01(\x0b\x32\x10.nn.ClassAndArgs\x12\x12\n\naggregator\x18\x04 \x01(\t\"\x1b\n\tByteChunk\x12\x0e\n\x06\x62uffer\x18\x01 \x01(\x0c\")\n\x0c\x43lassAndArgs\x12\x0b\n\x03\x63ls\x18\x01 \x01(\x0c\x12\x0c\n\x04\x61rgs\x18\x02 \x01(\x0c\"3\n\x12UploadMetaResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x05\"J\n\x10LoadModelRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x0f\n\x07\x62\x61\x63kend\x18\x02 \x01(\t\x12\x12\n\nmodel_path\x18\x03 \x01(\t\"2\n\x11LoadModelResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x05\"J\n\x10SaveModelRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x0f\n\x07\x62\x61\x63kend\x18\x02 \x01(\t\x12\x12\n\nmodel_path\x18\x03 \x01(\t\"$\n\x11SaveModelResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2\xac\x03\n\tNNService\x12.\n\x05train\x12\x10.nn.TrainRequest\x1a\x11.nn.TrainResponse\"\x00\x12\x37\n\x08\x65valuate\x12\x13.nn.EvaluateRequest\x1a\x14.nn.EvaluateResponse\"\x00\x12\x34\n\x07predict\x12\x12.nn.PredictRequest\x1a\x13.nn.PredictResponse\"\x00\x12>\n\x0bupload_meta\x12\x15.nn.UploadMetaRequest\x1a\x16.nn.UploadMetaResponse\"\x00\x12\x38\n\x0bupload_file\x12\r.nn.ByteChunk\x1a\x16.nn.UploadMetaResponse\"\x00(\x01\x12\x42\n\x11save_server_model\x12\x14.nn.SaveModelRequest\x1a\x15.nn.SaveModelResponse\"\x00\x12\x42\n\x11load_server_model\x12\x14.nn.LoadModelRequest\x1a\x15.nn.LoadModelResponse\"\x00\x42=\n+com.intel.analytics.bigdl.ppml.fl.generatedB\x0eNNServiceProtob\x06proto3')



_TRAINREQUEST = DESCRIPTOR.message_types_by_name['TrainRequest']
_TRAINRESPONSE = DESCRIPTOR.message_types_by_name['TrainResponse']
_EVALUATEREQUEST = DESCRIPTOR.message_types_by_name['EvaluateRequest']
_EVALUATERESPONSE = DESCRIPTOR.message_types_by_name['EvaluateResponse']
_PREDICTREQUEST = DESCRIPTOR.message_types_by_name['PredictRequest']
_PREDICTRESPONSE = DESCRIPTOR.message_types_by_name['PredictResponse']
_UPLOADMETAREQUEST = DESCRIPTOR.message_types_by_name['UploadMetaRequest']
_BYTECHUNK = DESCRIPTOR.message_types_by_name['ByteChunk']
_CLASSANDARGS = DESCRIPTOR.message_types_by_name['ClassAndArgs']
_UPLOADMETARESPONSE = DESCRIPTOR.message_types_by_name['UploadMetaResponse']
_LOADMODELREQUEST = DESCRIPTOR.message_types_by_name['LoadModelRequest']
_LOADMODELRESPONSE = DESCRIPTOR.message_types_by_name['LoadModelResponse']
_SAVEMODELREQUEST = DESCRIPTOR.message_types_by_name['SaveModelRequest']
_SAVEMODELRESPONSE = DESCRIPTOR.message_types_by_name['SaveModelResponse']
TrainRequest = _reflection.GeneratedProtocolMessageType('TrainRequest', (_message.Message,), {
  'DESCRIPTOR' : _TRAINREQUEST,
  '__module__' : 'nn_service_pb2'
  # @@protoc_insertion_point(class_scope:nn.TrainRequest)
  })
_sym_db.RegisterMessage(TrainRequest)

TrainResponse = _reflection.GeneratedProtocolMessageType('TrainResponse', (_message.Message,), {
  'DESCRIPTOR' : _TRAINRESPONSE,
  '__module__' : 'nn_service_pb2'
  # @@protoc_insertion_point(class_scope:nn.TrainResponse)
  })
_sym_db.RegisterMessage(TrainResponse)

EvaluateRequest = _reflection.GeneratedProtocolMessageType('EvaluateRequest', (_message.Message,), {
  'DESCRIPTOR' : _EVALUATEREQUEST,
  '__module__' : 'nn_service_pb2'
  # @@protoc_insertion_point(class_scope:nn.EvaluateRequest)
  })
_sym_db.RegisterMessage(EvaluateRequest)

EvaluateResponse = _reflection.GeneratedProtocolMessageType('EvaluateResponse', (_message.Message,), {
  'DESCRIPTOR' : _EVALUATERESPONSE,
  '__module__' : 'nn_service_pb2'
  # @@protoc_insertion_point(class_scope:nn.EvaluateResponse)
  })
_sym_db.RegisterMessage(EvaluateResponse)

PredictRequest = _reflection.GeneratedProtocolMessageType('PredictRequest', (_message.Message,), {
  'DESCRIPTOR' : _PREDICTREQUEST,
  '__module__' : 'nn_service_pb2'
  # @@protoc_insertion_point(class_scope:nn.PredictRequest)
  })
_sym_db.RegisterMessage(PredictRequest)

PredictResponse = _reflection.GeneratedProtocolMessageType('PredictResponse', (_message.Message,), {
  'DESCRIPTOR' : _PREDICTRESPONSE,
  '__module__' : 'nn_service_pb2'
  # @@protoc_insertion_point(class_scope:nn.PredictResponse)
  })
_sym_db.RegisterMessage(PredictResponse)

UploadMetaRequest = _reflection.GeneratedProtocolMessageType('UploadMetaRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPLOADMETAREQUEST,
  '__module__' : 'nn_service_pb2'
  # @@protoc_insertion_point(class_scope:nn.UploadMetaRequest)
  })
_sym_db.RegisterMessage(UploadMetaRequest)

ByteChunk = _reflection.GeneratedProtocolMessageType('ByteChunk', (_message.Message,), {
  'DESCRIPTOR' : _BYTECHUNK,
  '__module__' : 'nn_service_pb2'
  # @@protoc_insertion_point(class_scope:nn.ByteChunk)
  })
_sym_db.RegisterMessage(ByteChunk)

ClassAndArgs = _reflection.GeneratedProtocolMessageType('ClassAndArgs', (_message.Message,), {
  'DESCRIPTOR' : _CLASSANDARGS,
  '__module__' : 'nn_service_pb2'
  # @@protoc_insertion_point(class_scope:nn.ClassAndArgs)
  })
_sym_db.RegisterMessage(ClassAndArgs)

UploadMetaResponse = _reflection.GeneratedProtocolMessageType('UploadMetaResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPLOADMETARESPONSE,
  '__module__' : 'nn_service_pb2'
  # @@protoc_insertion_point(class_scope:nn.UploadMetaResponse)
  })
_sym_db.RegisterMessage(UploadMetaResponse)

LoadModelRequest = _reflection.GeneratedProtocolMessageType('LoadModelRequest', (_message.Message,), {
  'DESCRIPTOR' : _LOADMODELREQUEST,
  '__module__' : 'nn_service_pb2'
  # @@protoc_insertion_point(class_scope:nn.LoadModelRequest)
  })
_sym_db.RegisterMessage(LoadModelRequest)

LoadModelResponse = _reflection.GeneratedProtocolMessageType('LoadModelResponse', (_message.Message,), {
  'DESCRIPTOR' : _LOADMODELRESPONSE,
  '__module__' : 'nn_service_pb2'
  # @@protoc_insertion_point(class_scope:nn.LoadModelResponse)
  })
_sym_db.RegisterMessage(LoadModelResponse)

SaveModelRequest = _reflection.GeneratedProtocolMessageType('SaveModelRequest', (_message.Message,), {
  'DESCRIPTOR' : _SAVEMODELREQUEST,
  '__module__' : 'nn_service_pb2'
  # @@protoc_insertion_point(class_scope:nn.SaveModelRequest)
  })
_sym_db.RegisterMessage(SaveModelRequest)

SaveModelResponse = _reflection.GeneratedProtocolMessageType('SaveModelResponse', (_message.Message,), {
  'DESCRIPTOR' : _SAVEMODELRESPONSE,
  '__module__' : 'nn_service_pb2'
  # @@protoc_insertion_point(class_scope:nn.SaveModelResponse)
  })
_sym_db.RegisterMessage(SaveModelResponse)

_NNSERVICE = DESCRIPTOR.services_by_name['NNService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n+com.intel.analytics.bigdl.ppml.fl.generatedB\016NNServiceProto'
  _TRAINREQUEST._serialized_start=39
  _TRAINREQUEST._serialized_end=118
  _TRAINRESPONSE._serialized_start=120
  _TRAINRESPONSE._serialized_end=193
  _EVALUATEREQUEST._serialized_start=195
  _EVALUATEREQUEST._serialized_end=293
  _EVALUATERESPONSE._serialized_start=295
  _EVALUATERESPONSE._serialized_end=388
  _PREDICTREQUEST._serialized_start=390
  _PREDICTREQUEST._serialized_end=471
  _PREDICTRESPONSE._serialized_start=473
  _PREDICTRESPONSE._serialized_end=548
  _UPLOADMETAREQUEST._serialized_start=550
  _UPLOADMETAREQUEST._serialized_end=664
  _BYTECHUNK._serialized_start=666
  _BYTECHUNK._serialized_end=693
  _CLASSANDARGS._serialized_start=695
  _CLASSANDARGS._serialized_end=736
  _UPLOADMETARESPONSE._serialized_start=738
  _UPLOADMETARESPONSE._serialized_end=789
  _LOADMODELREQUEST._serialized_start=791
  _LOADMODELREQUEST._serialized_end=865
  _LOADMODELRESPONSE._serialized_start=867
  _LOADMODELRESPONSE._serialized_end=917
  _SAVEMODELREQUEST._serialized_start=919
  _SAVEMODELREQUEST._serialized_end=993
  _SAVEMODELRESPONSE._serialized_start=995
  _SAVEMODELRESPONSE._serialized_end=1031
  _NNSERVICE._serialized_start=1034
  _NNSERVICE._serialized_end=1462
# @@protoc_insertion_point(module_scope)
