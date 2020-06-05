import binascii
import struct
import datetime
import hashlib
from Encryptions.SHA256 import sha256
from Encryptions.RIPEMD160 import ripemd160
from Misc.Base58 import b58encode_int


def log(string):
    print(string)
    pass


def starts_with_op_n_code(pub):
    try:
        int_value = int(pub[0:2], 16)
        if 1 <= int_value <= 75:
            return True
    except:
        pass
    return False


def public_key_decode(pub):
    # Clip the unnecessary pseudo-byte string marker
    pub = pub[2:-1]
    if pub[0:6] == "76a914":
        result = "00" + pub[6:-4]
        hash_val = sha256(sha256(result))
        result += hash_val[0:8]
        return "1" + b58encode_int(int(result, 16))
    elif pub[0:2] == "a9":
        result = "00" + pub[2:-4]
        hash_val = sha256(sha256(result))
        result += hash_val[0:8]
        return "1" + b58encode_int(int(result, 16))
    elif starts_with_op_n_code(pub):
        pub = pub[2:-2]
        # If we are dealing with an uncompressed public key
        if pub[0:2] == "04" or pub[0:2] == "02" or pub[0:2] == "03":
            result = "00" + ripemd160(sha256(pub))
            hash_val = sha256(sha256(result))
            result += hash_val[0:8]
            return "1" + b58encode_int(int(result, 16))
    return ""


def string_little_endian_to_big_endian(string):
    string = binascii.hexlify(string)
    n = len(string) / 2
    fmt = '%dh' % n
    return struct.pack(fmt, *reversed(struct.unpack(fmt, string)))


def read_short_little_endian(block_file):
    return struct.pack(">H", struct.unpack("<H", block_file.read(2))[0])


def read_long_little_endian(block_file):
    return struct.pack(">Q", struct.unpack("<Q", block_file.read(8))[0])


def read_int_little_endian(block_file):
    return struct.pack(">I", struct.unpack("<I", block_file.read(4))[0])


def hex_to_int(value):
    return int(binascii.hexlify(value), 16)


def hex_to_str(value):
    return binascii.hexlify(value)


def read_var_int(block_file):
    var_int = ord(block_file.read(1))
    return_int = 0
    if var_int < 0xfd:
        return var_int
    if var_int == 0xfd:
        return_int = read_short_little_endian(block_file)
    if var_int == 0xfe:
        return_int = read_int_little_endian(block_file)
    if var_int == 0xff:
        return_int = read_long_little_endian(block_file)
    return int(binascii.hexlify(return_int), 16)


def read_input(block_file):
    previous_hash = binascii.hexlify(block_file.read(32)[::-1])
    out_id = binascii.hexlify(read_int_little_endian(block_file))
    script_length = read_var_int(block_file)
    script_signature_raw = hex_to_str(block_file.read(script_length))
    script_signature = script_signature_raw
    seq_no = binascii.hexlify(read_int_little_endian(block_file))


def read_output(block_file):
    value = hex_to_int(read_long_little_endian(block_file)) / 100000000.0
    script_length = read_var_int(block_file)
    script_signature_raw = hex_to_str(block_file.read(script_length))
    script_signature = script_signature_raw
    address = ''
    try:
        address = public_key_decode(str(script_signature))
    except Exception as e:
        print(e)
        address = ''
    f = open('addresses.txt', 'a')
    f.write(address + "\n")


def read_transaction(block_file):
    extended_format = False
    begin_byte = block_file.tell()
    input_ids = []
    output_ids = []
    version = hex_to_int(read_int_little_endian(block_file))
    cut_start1 = block_file.tell()
    cut_end1 = 0
    input_count = read_var_int(block_file)
    if input_count == 0:
        extended_format = True
        flags = ord(block_file.read(1))
        cut_end1 = block_file.tell()
        if flags != 0:
            input_count = read_var_int(block_file)
            # log("\nInput Count: " + str(input_count))
            for inputIndex in range(0, input_count):
                input_ids.append(read_input(block_file))
            output_count = read_var_int(block_file)
            for outputIndex in range(0, output_count):
                output_ids.append(read_output(block_file))
    else:
        cut_start1 = 0
        cut_end1 = 0
        for inputIndex in range(0, input_count):
            input_ids.append(read_input(block_file))
        output_count = read_var_int(block_file)
        for outputIndex in range(0, output_count):
            output_ids.append(read_output(block_file))
    cut_start2 = 0
    cut_end2 = 0
    if extended_format:
        if flags & 1:
            cut_start2 = block_file.tell()
            for inputIndex in range(0, input_count):
                count_of_stack_items = read_var_int(block_file)
                for stackItemIndex in range(0, count_of_stack_items):
                    stack_length = read_var_int(block_file)
                    stack_item = block_file.read(stack_length)[::-1]
            cut_end2 = block_file.tell()
    lock_time = hex_to_int(read_int_little_endian(block_file))
    end_byte = block_file.tell()
    block_file.seek(begin_byte)
    length_to_read = end_byte - begin_byte
    data_to_hash_for_transaction_id = block_file.read(length_to_read)
    if extended_format and cut_start1 != 0 and cut_end1 != 0 and cut_start2 != 0 and cut_end2 != 0:
        data_to_hash_for_transaction_id = data_to_hash_for_transaction_id[:(cut_start1 - begin_byte)] + data_to_hash_for_transaction_id[(cut_end1 - begin_byte):(cut_start2 - begin_byte)] + data_to_hash_for_transaction_id[(cut_end2 - begin_byte):]
    elif extended_format:
        quit()
    first_hash = hashlib.sha256(data_to_hash_for_transaction_id)
    second_hash = hashlib.sha256(first_hash.digest())
    hash_little_endian = second_hash.hexdigest()
    hash_transaction = string_little_endian_to_big_endian(binascii.unhexlify(hash_little_endian))


# Function to read the first section of a block file.
# USAGE: open(path_to_blockfile, "rb") as block_file
# USAGE2: read_block(block_file)
def read_block(block_file):
    magic_number = binascii.hexlify(block_file.read(4))
    block_size = hex_to_int(read_int_little_endian(block_file))
    version = hex_to_int(read_int_little_endian(block_file))
    previous_hash = binascii.hexlify(block_file.read(32))
    merkle_hash = binascii.hexlify(block_file.read(32))
    creation_time_timestamp = hex_to_int(read_int_little_endian(block_file))
    creation_time = datetime.datetime.fromtimestamp(creation_time_timestamp).strftime('%d.%m.%Y %H:%M')
    bits = hex_to_int(read_int_little_endian(block_file))
    nonce = hex_to_int(read_int_little_endian(block_file))
    count_of_transactions = read_var_int(block_file)
    # print("Number of transactions: " + str(count_of_transactions) + "; ")
    for transactionIndex in range(0, count_of_transactions):
        read_transaction(block_file)