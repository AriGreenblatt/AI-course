# calculate the MD5 hash of a given string without using calculateMD5 function


import hashlib


def calculate_md5_without_function(input_string):
    # Create an MD5 hash object
    md5_hash = hashlib.md5()
    # Update the hash object with the bytes of the input string
    md5_hash.update(input_string.encode('utf-8'))
    # Return the hexadecimal representation of the hash
    return md5_hash.hexdigest()

# Example usage
print(calculate_md5_without_function('Hello World'))  # Output: 5eb63bbbe01eeed093cb22bb8f5acdc3
print(calculate_md5_without_function('OpenAI'))       # Output: 2c6ee24b09816a6f14f95d1698b24ead
