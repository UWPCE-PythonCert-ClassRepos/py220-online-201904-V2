I removed all the lines that just show my file path.
My initial argument was 3. I began with a breakpoint at line nine and continued from there.

(Pdb) b 9
Breakpoint 1 at /home/jereamon/Documents/webDev/uwClass/py220-online-201904-V2/students/jeremy_monroe/lesson02/activity/recursive.py:9
(Pdb) cont
-> if n == 2:
(Pdb) disable 1
Disabled breakpoint 1 at /home/jereamon/Documents/webDev/uwClass/py220-online-201904-V2/students/jeremy_monroe/lesson02/activity/recursive.py:9
(Pdb) pp n
3
(Pdb) n
-> return my_fun(n / 2)
(Pdb) s
--Call--
-> def my_fun(n):
(Pdb) n
-> if n == 2:
(Pdb) pp n
1.5
(Pdb) n
-> return my_fun(n / 2)
(Pdb) s
--Call--
-> def my_fun(n):
(Pdb) n
-> if n == 2:
(Pdb) pp n
0.75
(Pdb) n
-> return my_fun(n / 2)
(Pdb) s
--Call--
-> def my_fun(n):
(Pdb) n
-> if n == 2:
(Pdb) pp n
0.375

