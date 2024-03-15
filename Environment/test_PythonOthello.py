from PythonOthello import ReversiBoard
from PythonOthello import BOARD_SIZE
from PythonOthello import WHITE
from PythonOthello import BLACK
from PythonOthello import YOU
from PythonOthello import COM

class TestReversiBoard:
     def test_initialization(self):
          rb = ReversiBoard()
          assert sum([len(item) for item in rb.cells]) == BOARD_SIZE * BOARD_SIZE
          assert rb.cells[3][3] == WHITE
          assert rb.cells[3][4] == BLACK
          assert rb.cells[4][3] == BLACK
          assert rb.cells[4][4] == WHITE

     def test_input_board(self):
          rb = ReversiBoard()
          assert rb.input_board() == "0000000000000000000000000002100000012000000000000000000000000000"

     def test_put_disk_石を配置してTrueを返す(self, mocker):
          rb = ReversiBoard()
          mocker.patch("PythonOthello.ReversiBoard.list_flippable_disks", return_value=[[1, 0]])
          assert rb.put_disk(1, 0, YOU)

     def test_put_disk_既に石が配置されているためFalseを返す(self, mocker):
          rb = ReversiBoard()
          rb.cells[0][1] = WHITE
          mocker.patch("PythonOthello.ReversiBoard.list_flippable_disks", return_value=[[1, 0]])
          assert not rb.put_disk(1, 0, YOU)

     def test_put_disk_石を配置する場所がないのでFalseを返す(self, mocker):
          rb = ReversiBoard()
          mocker.patch("PythonOthello.ReversiBoard.list_flippable_disks", return_value=[])
          assert not rb.put_disk(1, 0, YOU)