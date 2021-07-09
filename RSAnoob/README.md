# RSA Noob
### Challenge:
These numbers were scratched out on a prison wall. Can you help me decode them? https://mega.nz/#!al8iDSYB!s5olEDK5zZmYdx1LZU8s4CmYqnynvU_aOUvdQojJPJQ
### Solution:
Reference: [Noxtal writeup](https://writeups.noxtal.com/posts/2020-05-28-ctflearn120.html)<br />
Python code:
```python
import binascii

output = hex(9327565722767258308650643213344542404592011161659991421)[2:]
#print(output)

result = binascii.unhexlify('61626374667b6233747465725f75705f793075725f657d')
print(result)
```
Output:
```
b'abctf{b3tter_up_y0ur_e}'
```
