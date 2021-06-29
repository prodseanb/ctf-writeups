# Reverse Polarity
### Challenge:
I got a new hard drive just to hold my flag, but I'm afraid that it rotted. What do I do? The only thing I could get off of it was this: 01000011010101000100011001111011010000100110100101110100010111110100011001101100011010010111000001110000011010010110111001111101
### Solution:
This is a simple binary to text convertion. Pythonic approach:
```python
x = "01000011010101000100011001111011010000100110100101110100010111110100011001101100011010010111000001110000011010010110111001111101"

def decode(bin):
    output = ''.join(chr(int(bin[i*8:i*8+8], 2)) for i in range(len(bin)//8))
    print(output)
    
decode(x)
```
The function takes each block of eight characters (a byte) from our variable, converts it into an integer, and finally converts it into a character with `chr()`.
There are also hundreds of tools on the internet to convert binary data into a readable string.<br />
Output:
```bash
CTF{Bit_Flippin}
```
![reverse_polarity_flag](https://user-images.githubusercontent.com/59718043/123842561-e9b19200-d8de-11eb-8308-f026032a82dd.png)
