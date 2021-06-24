# Forensics101 
### Challenge:
Think the flag is somewhere in there. Would you help me find it? https://mega.nz/#!OHohCbTa!wbg60PARf4u6E6juuvK9-aDRe_bgEL937VO01EImM7c<br />
### Solution:
Using `strings -a`, we can display all the printable characters present in a file.
```bash
strings -a 95f6edfb66ef42d774a5a34581f19052.jpg
```
The output should look similar to this:
```bash
JFIF
 , #&')*)
-0-(0%()(
((((((((((((((((((((((((((((((((((((((((((((((((((
L?~f
:UwR
y>2|
*'?-
yhH_&
Lmz'

...
```
The flag can be found somewhere in the output.
```bash
flag{wow!_data_is_cool}
```
![forensics](https://user-images.githubusercontent.com/59718043/123303348-b5f3f800-d4eb-11eb-9e75-84ff1c026fba.png)

