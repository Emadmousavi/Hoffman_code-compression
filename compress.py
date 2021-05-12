import os
import pickle


class node:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.left = None
        self.right = None


class Compress:
    def __init__(self, path):
        self.path = path
        self.letter_repeat = dict()  # stores repeats of each letter in txt file
        self.letter_hofman_code = dict()  # stores Hofman_code of each letter
        self.queue = []  # Hofman operation will be done with this queue
        self.tree = None  # final Hofman tree is stored in it

    def extract_info(self):  # valuate self.letter_repeated
        file = open(self.path+".txt")
        while(True):
            char = file.read(1)
            if(not char):
                break

            try:
                self.letter_repeat[char] += 1
            except:
                self.letter_repeat[char] = 1

        file.close()

    def set_hofman_code(self, node, code):  # valuate self.letter_hofman_code
        if(node.left == None and node.right == None):
            self.letter_hofman_code[node.name] = code
            return
        if node.left != None:
            self.set_hofman_code(node.left, code+'0')
        if node.right != None:
            self.set_hofman_code(node.right, code+'1')

    def hofman(self):
        for letter in self.letter_repeat:
            self.queue.append(node(letter, self.letter_repeat[letter]))
        if len(self.queue) == 1:
            root = node("", 0)
            root.right = self.queue[0]
            self.tree = root
            self.set_hofman_code(self.tree, "")
            return
        while(len(self.queue) != 1):
            self.queue.sort(key=lambda x: x.number)
            new_node = node(self.queue[0].name + self.queue[1].name,
                            self.queue[0].number + self.queue[1].number)
            new_node.left = self.queue[0]
            new_node.right = self.queue[1]
            self.queue.pop(0)
            self.queue.pop(0)
            self.queue.append(new_node)

        self.tree = self.queue.pop()
        self.set_hofman_code(self.tree, "")

    def create_cmp_file(self):
        file = open(self.path+".txt")
        content = ""

        while(True):
            char = file.read(1)
            if(not char):
                break

            content += char

        cmp_content = ""
        for letter in content:
            cmp_content += self.letter_hofman_code[letter]

        file.close()
        file = open(self.path+".cmp", 'wb')
        pickle.dump(self.letter_hofman_code, file,
                    protocol=pickle.HIGHEST_PROTOCOL)
        data = cmp_content[:]
        zero_to_add = len(cmp_content) % 8
        b = bytearray()

        added_bit_in_binary = bin(8-zero_to_add)[2:]
        a = len(added_bit_in_binary) % 8
        added_bit_in_binary = (8-zero_to_add)*'0' + added_bit_in_binary
        b.append(int(added_bit_in_binary, 2))

        data += (8-zero_to_add)*'0'
        for i in range(0, len(data), 8):
            b.append(int(data[i:i+8], 2))

        file.write(b)
        file.close()

        with open(self.path+'_compressed_info.txt', 'w') as f:
            _o = os.path.getsize(self.path+".txt")
            _c = os.path.getsize(self.path+".cmp")
            f.write(f'Original file: {_o} bytes\n')
            f.write(f'Compressed file: {_c} bytes\n')
            f.write('Compressed file size  reduced about {}% \n\n'.format(
                round((((_o-_c)/_o)*100), 0)))
            f.write('character codes:\n')
            f.write(str(self.letter_hofman_code))
            f.write(f'\n\nThe encoded text:\n')
            f.writelines(cmp_content)

        added_bit_in_binary = bin(8-zero_to_add)[2:]
        a = len(added_bit_in_binary) % 8
        added_bit_in_binary = (8-zero_to_add)*'0' + added_bit_in_binary
        b.append(int(added_bit_in_binary, 2))
        return bytes(b)


def compress(file_name):
    file = Compress(file_name)
    file.extract_info()
    file.hofman()
    file.create_cmp_file()
