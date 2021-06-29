# BruXOR
### Challenge
There is a technique called bruteforce. Message: q{vpln'bH_varHuebcrqxetrHOXEj No key! Just brute .. brute .. brute ... :D
### Solution:
This challenge requires us to perform XOR tests against the string provided. Pythonic approach:
```python
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
```
Output:
```bash
(23, 'flag{y0u_Have_bruteforce_XOR}')
```
![bruxor_flag](https://user-images.githubusercontent.com/59718043/123848199-6d6e7d00-d8e5-11eb-92cb-190c7cfaae67.png)
