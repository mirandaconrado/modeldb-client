# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: CommonService.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='CommonService.proto',
  package='com.mitdbg.modeldb',
  syntax='proto3',
  serialized_options=_b('P\001'),
  serialized_pb=_b('\n\x13\x43ommonService.proto\x12\x12\x63om.mitdbg.modeldb\"g\n\x08KeyValue\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12?\n\nvalue_type\x18\x03 \x01(\x0e\x32+.com.mitdbg.modeldb.ValueTypeEnum.ValueType\"H\n\rValueTypeEnum\"7\n\tValueType\x12\n\n\x06STRING\x10\x00\x12\n\n\x06NUMBER\x10\x01\x12\x08\n\x04LIST\x10\x02\x12\x08\n\x04\x42LOB\x10\x03\"]\n\x10\x41rtifactTypeEnum\"I\n\x0c\x41rtifactType\x12\t\n\x05IMAGE\x10\x00\x12\t\n\x05MODEL\x10\x01\x12\x0f\n\x0bTENSORBOARD\x10\x02\x12\x08\n\x04\x44\x41TA\x10\x03\x12\x08\n\x04\x42LOB\x10\x04\"o\n\x08\x41rtifact\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12H\n\rartifact_type\x18\x03 \x01(\x0e\x32\x31.com.mitdbg.modeldb.ArtifactTypeEnum.ArtifactType\"\x17\n\x07\x46\x65\x61ture\x12\x0c\n\x04name\x18\x01 \x01(\t\"Y\n\rGetAttributes\x12\n\n\x02id\x18\x01 \x01(\t\x1a<\n\x08Response\x12\x30\n\nattributes\x18\x01 \x03(\x0b\x32\x1c.com.mitdbg.modeldb.KeyValue\"h\n\rAddAttributes\x12\n\n\x02id\x18\x01 \x01(\t\x12/\n\tattribute\x18\x02 \x01(\x0b\x32\x1c.com.mitdbg.modeldb.KeyValue\x1a\x1a\n\x08Response\x12\x0e\n\x06status\x18\x01 \x01(\x08\x42\x02P\x01\x62\x06proto3')
)



_VALUETYPEENUM_VALUETYPE = _descriptor.EnumDescriptor(
  name='ValueType',
  full_name='com.mitdbg.modeldb.ValueTypeEnum.ValueType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STRING', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NUMBER', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LIST', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BLOB', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=165,
  serialized_end=220,
)
_sym_db.RegisterEnumDescriptor(_VALUETYPEENUM_VALUETYPE)

_ARTIFACTTYPEENUM_ARTIFACTTYPE = _descriptor.EnumDescriptor(
  name='ArtifactType',
  full_name='com.mitdbg.modeldb.ArtifactTypeEnum.ArtifactType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='IMAGE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MODEL', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TENSORBOARD', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DATA', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BLOB', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=242,
  serialized_end=315,
)
_sym_db.RegisterEnumDescriptor(_ARTIFACTTYPEENUM_ARTIFACTTYPE)


_KEYVALUE = _descriptor.Descriptor(
  name='KeyValue',
  full_name='com.mitdbg.modeldb.KeyValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.mitdbg.modeldb.KeyValue.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.mitdbg.modeldb.KeyValue.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value_type', full_name='com.mitdbg.modeldb.KeyValue.value_type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=43,
  serialized_end=146,
)


_VALUETYPEENUM = _descriptor.Descriptor(
  name='ValueTypeEnum',
  full_name='com.mitdbg.modeldb.ValueTypeEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _VALUETYPEENUM_VALUETYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=148,
  serialized_end=220,
)


_ARTIFACTTYPEENUM = _descriptor.Descriptor(
  name='ArtifactTypeEnum',
  full_name='com.mitdbg.modeldb.ArtifactTypeEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ARTIFACTTYPEENUM_ARTIFACTTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=222,
  serialized_end=315,
)


_ARTIFACT = _descriptor.Descriptor(
  name='Artifact',
  full_name='com.mitdbg.modeldb.Artifact',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.mitdbg.modeldb.Artifact.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='path', full_name='com.mitdbg.modeldb.Artifact.path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='artifact_type', full_name='com.mitdbg.modeldb.Artifact.artifact_type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=317,
  serialized_end=428,
)


_FEATURE = _descriptor.Descriptor(
  name='Feature',
  full_name='com.mitdbg.modeldb.Feature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='com.mitdbg.modeldb.Feature.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=430,
  serialized_end=453,
)


_GETATTRIBUTES_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='com.mitdbg.modeldb.GetAttributes.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='attributes', full_name='com.mitdbg.modeldb.GetAttributes.Response.attributes', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=484,
  serialized_end=544,
)

_GETATTRIBUTES = _descriptor.Descriptor(
  name='GetAttributes',
  full_name='com.mitdbg.modeldb.GetAttributes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='com.mitdbg.modeldb.GetAttributes.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_GETATTRIBUTES_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=455,
  serialized_end=544,
)


_ADDATTRIBUTES_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='com.mitdbg.modeldb.AddAttributes.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='com.mitdbg.modeldb.AddAttributes.Response.status', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=624,
  serialized_end=650,
)

_ADDATTRIBUTES = _descriptor.Descriptor(
  name='AddAttributes',
  full_name='com.mitdbg.modeldb.AddAttributes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='com.mitdbg.modeldb.AddAttributes.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='attribute', full_name='com.mitdbg.modeldb.AddAttributes.attribute', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_ADDATTRIBUTES_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=546,
  serialized_end=650,
)

_KEYVALUE.fields_by_name['value_type'].enum_type = _VALUETYPEENUM_VALUETYPE
_VALUETYPEENUM_VALUETYPE.containing_type = _VALUETYPEENUM
_ARTIFACTTYPEENUM_ARTIFACTTYPE.containing_type = _ARTIFACTTYPEENUM
_ARTIFACT.fields_by_name['artifact_type'].enum_type = _ARTIFACTTYPEENUM_ARTIFACTTYPE
_GETATTRIBUTES_RESPONSE.fields_by_name['attributes'].message_type = _KEYVALUE
_GETATTRIBUTES_RESPONSE.containing_type = _GETATTRIBUTES
_ADDATTRIBUTES_RESPONSE.containing_type = _ADDATTRIBUTES
_ADDATTRIBUTES.fields_by_name['attribute'].message_type = _KEYVALUE
DESCRIPTOR.message_types_by_name['KeyValue'] = _KEYVALUE
DESCRIPTOR.message_types_by_name['ValueTypeEnum'] = _VALUETYPEENUM
DESCRIPTOR.message_types_by_name['ArtifactTypeEnum'] = _ARTIFACTTYPEENUM
DESCRIPTOR.message_types_by_name['Artifact'] = _ARTIFACT
DESCRIPTOR.message_types_by_name['Feature'] = _FEATURE
DESCRIPTOR.message_types_by_name['GetAttributes'] = _GETATTRIBUTES
DESCRIPTOR.message_types_by_name['AddAttributes'] = _ADDATTRIBUTES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

KeyValue = _reflection.GeneratedProtocolMessageType('KeyValue', (_message.Message,), dict(
  DESCRIPTOR = _KEYVALUE,
  __module__ = 'CommonService_pb2'
  # @@protoc_insertion_point(class_scope:com.mitdbg.modeldb.KeyValue)
  ))
_sym_db.RegisterMessage(KeyValue)

ValueTypeEnum = _reflection.GeneratedProtocolMessageType('ValueTypeEnum', (_message.Message,), dict(
  DESCRIPTOR = _VALUETYPEENUM,
  __module__ = 'CommonService_pb2'
  # @@protoc_insertion_point(class_scope:com.mitdbg.modeldb.ValueTypeEnum)
  ))
_sym_db.RegisterMessage(ValueTypeEnum)

ArtifactTypeEnum = _reflection.GeneratedProtocolMessageType('ArtifactTypeEnum', (_message.Message,), dict(
  DESCRIPTOR = _ARTIFACTTYPEENUM,
  __module__ = 'CommonService_pb2'
  # @@protoc_insertion_point(class_scope:com.mitdbg.modeldb.ArtifactTypeEnum)
  ))
_sym_db.RegisterMessage(ArtifactTypeEnum)

Artifact = _reflection.GeneratedProtocolMessageType('Artifact', (_message.Message,), dict(
  DESCRIPTOR = _ARTIFACT,
  __module__ = 'CommonService_pb2'
  # @@protoc_insertion_point(class_scope:com.mitdbg.modeldb.Artifact)
  ))
_sym_db.RegisterMessage(Artifact)

Feature = _reflection.GeneratedProtocolMessageType('Feature', (_message.Message,), dict(
  DESCRIPTOR = _FEATURE,
  __module__ = 'CommonService_pb2'
  # @@protoc_insertion_point(class_scope:com.mitdbg.modeldb.Feature)
  ))
_sym_db.RegisterMessage(Feature)

GetAttributes = _reflection.GeneratedProtocolMessageType('GetAttributes', (_message.Message,), dict(

  Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
    DESCRIPTOR = _GETATTRIBUTES_RESPONSE,
    __module__ = 'CommonService_pb2'
    # @@protoc_insertion_point(class_scope:com.mitdbg.modeldb.GetAttributes.Response)
    ))
  ,
  DESCRIPTOR = _GETATTRIBUTES,
  __module__ = 'CommonService_pb2'
  # @@protoc_insertion_point(class_scope:com.mitdbg.modeldb.GetAttributes)
  ))
_sym_db.RegisterMessage(GetAttributes)
_sym_db.RegisterMessage(GetAttributes.Response)

AddAttributes = _reflection.GeneratedProtocolMessageType('AddAttributes', (_message.Message,), dict(

  Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
    DESCRIPTOR = _ADDATTRIBUTES_RESPONSE,
    __module__ = 'CommonService_pb2'
    # @@protoc_insertion_point(class_scope:com.mitdbg.modeldb.AddAttributes.Response)
    ))
  ,
  DESCRIPTOR = _ADDATTRIBUTES,
  __module__ = 'CommonService_pb2'
  # @@protoc_insertion_point(class_scope:com.mitdbg.modeldb.AddAttributes)
  ))
_sym_db.RegisterMessage(AddAttributes)
_sym_db.RegisterMessage(AddAttributes.Response)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)