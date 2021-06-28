# Hextroadinary
### Challenge:


Meet ROXy, a coder obsessed with being exclusively the worlds best hacker. She specializes in short cryptic hard to decipher secret codes. The below hex values for example, she did something with them to generate a secret code, can you figure out what? Your answer should start with 0x.

0xc4115 0x4cf8
### Solution: 
The hint here is the name ROXy. We need to calculate the XOR of these 2 hex represented values. Pythonic approach:
```python
hex1 = 0xc4115
hex2 = 0x4cf8

output = hex(hex1 ^ hex2)

print(output)
```
Output:
```bash
0xc0ded
```
Notice how the challenge requires our answer to start with 0x. It's also peculiar how this string subtly means "coded". 
This means that this XOR-calculated result is the deciphered code.<br />
![hex_xor_flag](https://user-images.githubusercontent.com/59718043/123580155-3b570100-d7a7-11eb-8ec9-c79051e2dd43.png)
