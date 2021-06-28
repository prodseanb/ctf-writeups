# 07601
### Challenge:
https://mega.nz/#!CXYXBQAK!6eLJSXvAfGnemqWpNbLQtOHBvtkCzA7-zycVjhHPYQQ I think I lost my flag in there. Hopefully, it won't get attacked...
### Solution:
This one involves the use of `strings` and `grep`. It's a simple steganography task where there is hidden data within a PNG file. First, we're going to need
to install ["foremost"](https://en.wikipedia.org/wiki/Foremost_(software)), a forensic tool that analyzes internal data structures within files. This is best used
for analyzing PNG files.
```bash
sudo apt-get install foremost
```
Then, we need to run the command and specify the file with `i`:
```bash
foremost -i AGT.png
```
This creates an `output` directory. Within one of the subdirectories occupy 3 zip files. After a comprehensive search, I found the flag in one of the extracted
files called 'I Warned You.jpeg'. The command I used:
```bash
strings -a 'I Warned You.jpeg' | grep CTF
```
Output:
```bash
ABCTF{Du$t1nS_D0jo}1r
```
![07601_flag](https://user-images.githubusercontent.com/59718043/123576944-e44e2d80-d7a0-11eb-97bc-1fc206929b5c.png)
