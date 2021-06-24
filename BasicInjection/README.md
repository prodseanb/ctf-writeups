# Basic Injection
### Challenge:
See if you can leak the whole database using what you know about SQL Injections.<br /> [Link](https://web.ctflearn.com/web4/)
### Extra resource:
[SQL Injection Part 1](https://ctflearn.com/lab/sql-injection-part-1)
### Solution:
Seems like we have a vulnerable input field that we can exploit to display contents of the database.
![basicinjection](https://user-images.githubusercontent.com/59718043/123304546-0d469800-d4ed-11eb-8791-9f566b81fc02.png)
Checking out the source code, there seems to be a hint in this comment:
```
<!-- Try some names like Hiroki, Noah, Luke -->
```
When I entered 'Luke', the output shows:
```
Name: Luke
Data: I made this problem.
```
Going back to our extra resource lab, we need to construct an SQL query that displays all the rows. 
```sql
select * from dogs where dog_name = 'irrelevant' or  '1'  = '1';
```
Since the field is already set up so that the query looks up `$input`, we need to inject only the last part, <br />i.e., `'irrelevant' or  '1'  = '1'`.
<br />So I decided to enter:<br />
![injection_input](https://user-images.githubusercontent.com/59718043/123306577-762f0f80-d4ef-11eb-880b-81280c1a0c5d.png)<br />
Note that the single quotations are positioned accordingly because we want to fit the `'$input'` query. This returns the flag somewhere in the output.<br />
![injection_flag](https://user-images.githubusercontent.com/59718043/123307167-2f8de500-d4f0-11eb-930c-da9639da1cb5.png)
