#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import os
import sys
import pytest
import uuid

root_path = os.path.realpath('.')
sys.path.append(root_path)

from uamqp import c_uamqp


def test_null_value():
    value = c_uamqp.null_value()
    assert value.value == None
    assert value.type == c_uamqp.AMQPType.NullValue
    assert str(value) == "NULL"


def test_boolean_value():
    false_value = c_uamqp.bool_value(False)
    assert false_value.value == False
    assert str(false_value) == "false"

    true_value = c_uamqp.bool_value(True)
    assert true_value.value == True
    assert true_value.type == c_uamqp.AMQPType.BoolValue
    assert str(true_value) == "true"


def test_ubyte_value():
    value = c_uamqp.ubyte_value(255)
    assert value.value == 255
    assert value.type == c_uamqp.AMQPType.UByteValue
    assert str(value) == "255"


def test_ushort_value():
    value = c_uamqp.ushort_value(255)
    assert value.value == 255
    assert value.type == c_uamqp.AMQPType.UShortValue
    assert str(value) == "255"


def test_uint_value():
    value = c_uamqp.uint_value(255)
    assert value.value == 255
    assert value.type == c_uamqp.AMQPType.UIntValue
    assert str(value) == "255"


def test_ulong_value():
    value = c_uamqp.ulong_value(255)
    assert value.value == 255
    assert value.type == c_uamqp.AMQPType.ULongValue
    assert str(value) == "255"


def test_byte_value():
    value = c_uamqp.byte_value(5)
    assert value.value == 5
    assert value.type == c_uamqp.AMQPType.ByteValue
    assert str(value) == "5"


def test_short_value():
    value = c_uamqp.short_value(255)
    assert value.value == 255
    assert value.type == c_uamqp.AMQPType.ShortValue
    assert str(value) == "255"


def test_int_value():
    value = c_uamqp.int_value(255)
    assert value.value == 255
    assert value.type == c_uamqp.AMQPType.IntValue
    assert str(value) == "255"


def test_long_value():
    value = c_uamqp.long_value(5)
    assert value.value == 5
    assert value.type == c_uamqp.AMQPType.LongValue
    assert str(value) == "5"


def test_float_value():
    value = c_uamqp.float_value(5.0)
    assert value.value == 5.0
    assert value.type == c_uamqp.AMQPType.FloatValue
    assert str(value) == "5.00"


def test_double_value():
    value = c_uamqp.double_value(5.0)
    assert value.value == 5.0
    assert value.type == c_uamqp.AMQPType.DoubleValue
    assert str(value) == "5.00"


def test_char_value():
    value = c_uamqp.char_value(ord('x'))
    assert value.value == 'x'
    assert value.type == c_uamqp.AMQPType.CharValue
    assert str(value) == "U00000078"


def test_timestamp_value():
    value = c_uamqp.timestamp_value(255)
    assert value.value == 255
    assert value.type == c_uamqp.AMQPType.TimestampValue
    assert str(value) == "255"


def test_uuid_value():
    test_uuid = uuid.UUID('37f9db00-fbb7-11e7-85ee-ecb1d755839a')
    value = c_uamqp.uuid_value(test_uuid)
    assert str(value) == '37f9db00-fbb7-11e7-85ee-ecb1d755839a'
    assert value.value == test_uuid
    assert value.type == c_uamqp.AMQPType.UUIDValue

    test_uuid = uuid.uuid4()
    value = c_uamqp.uuid_value(test_uuid)
    assert str(value) == str(test_uuid)
    assert value.value == test_uuid


def test_binary_value():
    value = c_uamqp.binary_value(bytes([50]))
    assert len(value) == 1
    assert value.value == bytes([50])
    assert value.type == c_uamqp.AMQPType.BinaryValue
    assert str(value) == "<32>"
    
    value = c_uamqp.binary_value(b'Test')
    assert len(value) == 4
    assert value.value == b'Test'
    assert value.type == c_uamqp.AMQPType.BinaryValue
    assert str(value) == "<54 65 73 74>"


def test_string_value():
    value = c_uamqp.string_value('Test'.encode('utf-8'))
    assert value.value == 'Test'
    assert value.type == c_uamqp.AMQPType.StringValue
    assert str(value) == "Test"


def test_symbol_value():
    value = c_uamqp.symbol_value(b'Test')
    assert value.value == b'Test'
    assert value.type == c_uamqp.AMQPType.SymbolValue
    assert str(value) == "Test"


def test_list_value():
    value = c_uamqp.list_value()
    assert value.type == c_uamqp.AMQPType.ListValue
    assert value.size == 0

    value.size = 2
    assert len(value) == 2
    assert value.size == 2

    val_1 = c_uamqp.bool_value(True)
    val_2 = c_uamqp.ubyte_value(125)

    value[0] = val_1
    value[1] = val_2
    with pytest.raises(IndexError):
        value[2] = c_uamqp.null_value()

    assert value[0].value == True
    assert value[1].value == 125
    assert value.value == [True, 125]
    assert str(value) == "{true,125}"


def test_dict_value():
    value = c_uamqp.dict_value()
    assert value.type == c_uamqp.AMQPType.DictValue

    one = c_uamqp.string_value(b'One')
    two = c_uamqp.string_value(b'Two')
    i_one = c_uamqp.int_value(1)
    i_two = c_uamqp.int_value(2)
    value[one] = i_one
    value[two] = i_two

    assert len(value) == 2
    assert value[one].value == 1
    assert value[two].value == 2
    with pytest.raises(KeyError):
        value[c_uamqp.null_value()]

    assert value.get(0) == (one, i_one)
    assert value.get(1) == (two, i_two)
    with pytest.raises(IndexError):
        value.get(2)
    
    assert value.value == {"One": 1, "Two": 2}
    assert str(value) == "{[One:1],[Two:2]}"


def test_array_value():
    value = c_uamqp.array_value()
    assert value.type == c_uamqp.AMQPType.ArrayValue
    assert value.size == 0

    val_1 = c_uamqp.ubyte_value(122)
    val_2 = c_uamqp.ubyte_value(125)

    value.append(val_1)
    assert value[0].value == 122

    value.append(val_2)
    assert value[1].value == 125
    assert len(value) == 2
    
    with pytest.raises(IndexError):
        value[2]
    assert value.value == [122, 125]
    assert str(value) == "{122,125}"
    #assert value.get_encoded_size() == 5


def test_equal_values():
    value_a = c_uamqp.null_value()
    value_b = c_uamqp.null_value()
    value_c = c_uamqp.int_value(42)
    value_d = c_uamqp.int_value(42)
    value_e = c_uamqp.string_value(b'Test')

    assert value_a == value_b
    assert value_c == value_d
    assert value_a != value_c
    assert value_d != value_e