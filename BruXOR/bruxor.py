import re

x = "q{vpln'bH_varHuebcrqxetrHOXEj"

with open('bruxor.txt', 'a') as file:
    for i in range(256):
        output = (i, ''.join([chr(ord(char) ^ i) for char in x]))
        file.write(str(output) + '\n')

# next section not necessary, you can use grep
pattern = "flag"

file = open('bruxor.txt', 'r')
for line in file:
    if re.search(pattern, line):
        print(line)