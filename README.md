# Othello

Competitive Othello game environment and C language exercises.

# CPU

Program exercise to search for stone placement in C language.

- On the board
1  2  3  4  5  6  7  8
9  10 11 12 13 14 15 16
17 18 19 20 21 22 23 24
25 26 27 28 29 30 31 32
33 34 35 36 37 38 39 40
41 42 43 44 45 46 47 48
49 50 51 52 53 54 55 56
57 58 59 60 61 62 63 64

## File type

- othello_cpu.c
  - Competitive CPU code for checking program exercises.
  - Weak due to random algorithm.
- othello_cpu_smart.c
  - A program to determine the position with the highest number of flippable stones.
- othello_cpu_smart_evaluation.c
  - Determine the position to place a stone using an evaluation function.

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

## Build

- Run the command below

```
pyinstaller PythonOthello.py --onefile --clean
```

## Install multiple libraries for unit tests

```
pip install pytest
pip install pytest-mock
pip install pytest-cov
```

## Run unit tests

```
pytest -v --cov=. --cov-report=term-missing test_PythonOthello.py
```

## Coverage Memo

- Stmts: 実行対象コード全体の行数
- Miss: 網羅できなかった行数
- Cover: カバレッジ率

## Reference

1. https://katoh4u.hatenablog.com/entry/2018/03/22/130105
