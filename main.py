import os
from compress import compress
from decompress import decompress
file_name = input("Enter the file name to compress or decompress: ")
if os.path.exists(file_name + ".txt"):
    print("compressing "+file_name+".txt ...")
    compress(file_name)
elif os.path.exists(file_name + ".cmp"):
    print("decompressing "+file_name+".cmp ...")
    decompress(file_name)
else:
    print("No file exists with the specified name to compress or decompress")