import pickle
import os


class Node:
    def __init__(self, char, left=None, right=None):
        self.char = char
        self.left = left
        self.right = right


def decompress(file_name):
    compressed_file = open(file_name+".cmp", 'rb')
    letters_frequencies = pickle.load(compressed_file)
    root = Node("")
    for key, value in letters_frequencies.items():
        t = root
        for i in value:
            if i == '0':
                if t.left == None:
                    newNode = Node("")
                    t.left = newNode
                t = t.left
            if i == '1':
                if t.right == None:
                    newNode = Node("")
                    t.right = newNode
                t = t.right
        t.char = key
    decompressed_file = open(file_name+".txt", 'w')
    t = root
    num_extra_bits = int(compressed_file.read(1).hex(), 16)
    byte = compressed_file.read(1)
    while byte:
        index = 8
        if not compressed_file.read(1):
            index = 8 - num_extra_bits
        else:
            compressed_file.seek(-1, os.SEEK_CUR)

        byteString = "{:08b}".format(int(byte.hex(), 16))
        for i in range(index):
            if byteString[i] == '1':
                t = t.right
            if byteString[i] == '0':
                t = t.left
            if t.left == None and t.right == None:
                decompressed_file.write(t.char)
                t = root
        byte = compressed_file.read(1)
    compressed_file.close()
    decompressed_file.close()
