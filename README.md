# Othello
Competitive Othello game environment and C language exercises.

# CPU
Program exercise to search for stone placement in C language.

## File type
- othello_cpu.c
    - Competitive CPU code for checking program exercises.
    - Weak due to random algorithm.
- othello_template.c
    - Template implementing input specifications. 
    - Under construction.

## Specification
- input
    - argv[1]
        - '-b' is black stone.
        - '-w' is white stone.
    - argv[2]
        - This is the data row of the current Othello board, and the rows are arranged in order from the top left to the right side.
        - It becomes a data string of 0, 1, 2 without spaces.
- output
    - the coordinates where you want to place the stone in xy, separated by ','.

# Envirnment
Displays and controls the Othello board, determines the winner, and also executes each CPU's exe in a competitive format to place stones.

## File type
- PythonOthello.py

## Specification
- file
    - Place the battle exe on the py file.
        - othello_cpu1.exe
        - othello_cpu1.exe
- input
    - the coordinates where you want to place the stone in xy, separated by ','.
- output
    - This is the data row of the current Othello board.

## Reference
1. https://katoh4u.hatenablog.com/entry/2018/03/22/130105