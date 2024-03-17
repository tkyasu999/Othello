from PythonOthello import ReversiBoard
from PythonOthello import Game
from PythonOthello import BoardUI
from PythonOthello import BOARD_SIZE
from PythonOthello import WHITE
from PythonOthello import BLACK
from PythonOthello import YOU
from PythonOthello import COM
from PythonOthello import YOUR_COLOR
from PythonOthello import COM_COLOR
from PythonOthello import CANVAS_SIZE

class TestReversiBoard:
    def test_initialization(self):
        rb = ReversiBoard()
        assert sum([len(item) for item in rb.cells]) == BOARD_SIZE * BOARD_SIZE
        assert rb.cells[3][3] == WHITE
        assert rb.cells[3][4] == BLACK
        assert rb.cells[4][3] == BLACK
        assert rb.cells[4][4] == WHITE

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

    def test_list_flippable_disks_xとyがボードのサイズを超える場合はNullを返す(self):
        rb = ReversiBoard()
        result = rb.list_flippable_disks(BOARD_SIZE+2, BOARD_SIZE+2, WHITE)
        assert result == []

    def test_list_flippable_disks_xとyがボードのサイズより小さい場合はNullを返す(self):
        rb = ReversiBoard()
        result = rb.list_flippable_disks(-2, -2, WHITE)
        assert result == []

    def test_list_flippable_disks_xとyがNoneの場合はNullを返す(self):
        rb = ReversiBoard()
        result = rb.list_flippable_disks(0, 0, WHITE)
        assert result == []

    def test_list_flippable_disks_白石の番で黒石が獲得できる場合は1種類の座標を返す(self):
        rb = ReversiBoard()
        result = rb.list_flippable_disks(5, 3, WHITE)
        assert result == [(4, 3)]

    def test_list_flippable_disks_黒石の番で白石が獲得できる場合は1種類の座標を返す(self):
        rb = ReversiBoard()
        result = rb.list_flippable_disks(4, 5, BLACK)
        assert result == [(4, 4)]

    def test_list_flippable_disks_白石の番で黒石を斜めに獲得できる場合は複数の座標を返す(self):
        rb = ReversiBoard()
        rb.cells[4][4] = BLACK
        rb.cells[5][5] = BLACK
        result = rb.list_flippable_disks(6, 6, WHITE)
        assert result == [(5, 5), (4, 4)]

    def test_list_flippable_disks_黒石の番で白石を斜めに獲得できる場合は複数の座標を返す(self):
        rb = ReversiBoard()
        rb.cells[3][4] = WHITE
        rb.cells[2][5] = WHITE
        result = rb.list_flippable_disks(6, 1, BLACK)
        assert result == [(5, 2), (4, 3)]

    def test_list_flippable_disks_角の座標の場合はNullを返す(self):
        rb = ReversiBoard()
        rb.cells[0][0] = BLACK
        rb.cells[1][0] = WHITE
        result = rb.list_flippable_disks(1, 0, WHITE)
        assert result == []

    def test_show_board(self,capsys):
        rb = ReversiBoard()
        rb.show_board()
        captured = capsys.readouterr()
        assert captured.out == "----------------------------------------\n0 0 0 0 0 0 0 0 \n0 0 0 0 0 0 0 0 \n0 0 0 0 0 0 0 0 \n0 0 0 2 1 0 0 0 \n0 0 0 1 2 0 0 0 \n0 0 0 0 0 0 0 0 \n0 0 0 0 0 0 0 0 \n0 0 0 0 0 0 0 0 \n"

    def test_input_board(self):
        rb = ReversiBoard()
        assert rb.input_board() == "0000000000000000000000000002100000012000000000000000000000000000"

    def test_list_possible_cells_白石の番で黒石が獲得できる場合の座標を返す(self):
        rb = ReversiBoard()
        result = rb.list_possible_cells(WHITE)
        assert result == [(2, 4), (3, 5), (4, 2), (5, 3)]

    def test_list_possible_cells_黒石の番で白石が獲得できる場合の座標を返す(self):
        rb = ReversiBoard()
        result = rb.list_possible_cells(BLACK)
        assert result == [(2, 3), (3, 2), (4, 5), (5, 4)]

    def test_list_possible_cells_石が配置できない場合の座標を返す(self):
        rb = ReversiBoard()
        rb.cells[3][3] = None
        rb.cells[3][4] = None
        rb.cells[4][3] = None
        rb.cells[4][4] = None
        result = rb.list_possible_cells(BLACK)
        assert result == []

class TestGame:
    def test_initialization(self):
        gm = Game()
        assert gm.player == BLACK
        assert gm.turn == 0
        assert gm.winner is None
        assert not gm.was_passed
        assert gm.disks == {}

    def test_is_finished_勝者判定フラグがNoneの場合はFalseを返す(self):
        gm = Game()
        assert not gm.is_finished()

    def test_is_finished_勝者判定フラグがBlackの場合はTrueを返す(self):
        gm = Game()
        gm.winner = BLACK
        assert gm.is_finished()

    def test_is_finished_勝者判定フラグがWhiteの場合はTrueを返す(self):
        gm = Game()
        gm.winner = WHITE
        assert gm.is_finished()

    def test_list_possible_cells_座標を返す(self, mocker):
        gm = Game()
        mocker.patch("PythonOthello.ReversiBoard.list_possible_cells", return_value=[(1, 0)])
        assert gm.list_possible_cells() == [(1, 0)]

    def test_list_possible_cells_空の座標を返す(self, mocker):
        gm = Game()
        mocker.patch("PythonOthello.ReversiBoard.list_possible_cells", return_value=[])
        assert gm.list_possible_cells() == []

    def test_get_color_勝者がWHITEの場合にWHITE文字を返す(self):
        gm = Game()
        assert gm.get_color(WHITE) == "WHITE"

    def test_get_color_勝者がBLACKの場合にBLACK文字を返す(self):
        gm = Game()
        assert gm.get_color(BLACK) == "BLACK"

    def test_get_color_勝者がドローの場合にDRAW文字を返す(self):
        gm = Game()
        assert gm.get_color(gm.DRAW) == "DRAW"

    def test_get_current_player_黒石の場合(self):
        gm = Game()
        assert gm.get_current_player() == BLACK

    def test_get_current_player_白石の場合(self):
        gm = Game()
        gm.player = WHITE
        assert gm.get_current_player() == WHITE

    def test_get_next_player_次が黒石の場合(self):
        gm = Game()
        gm.player = WHITE
        assert gm.get_next_player() == BLACK

    def test_get_next_player_次が白石の場合(self):
        gm = Game()
        gm.player = BLACK
        assert gm.get_next_player() == WHITE

    def test_shift_player_次が黒石の場合(self, mocker):
        gm = Game()
        mocker.patch("PythonOthello.Game.get_next_player", return_value=BLACK)
        gm.shift_player()
        assert gm.player == BLACK

    def test_shift_player_次が白石の場合(self, mocker):
        gm = Game()
        mocker.patch("PythonOthello.Game.get_next_player", return_value=WHITE)
        gm.shift_player()
        assert gm.player == WHITE

    def test_put_disk_配置できて次の番が白石の場合(self, mocker):
        mocker.patch("PythonOthello.ReversiBoard.put_disk", return_value=True)
        gm = Game()
        mocker.patch("PythonOthello.Game.get_next_player", return_value=WHITE)
        gm.put_disk(1, 1)
        assert not gm.was_passed
        assert gm.player == WHITE
        assert gm.turn == 1

    def test_put_disk_配置できて次の番が黒石の場合(self, mocker):
        mocker.patch("PythonOthello.ReversiBoard.put_disk", return_value=True)
        gm = Game()
        mocker.patch("PythonOthello.Game.get_next_player", return_value=BLACK)
        gm.put_disk(1, 1)
        assert not gm.was_passed
        assert gm.player == BLACK
        assert gm.turn == 1

    def test_put_disk_配置できない場合(self, mocker):
        mocker.patch("PythonOthello.ReversiBoard.put_disk", return_value=False)
        gm = Game()
        assert not gm.put_disk(1, 1)

    def test_next_disk_次の番へ黒石の場合(self, mocker):
        gm = Game()
        mocker.patch("PythonOthello.Game.get_next_player", return_value=BLACK)
        gm.next_disk()
        assert not gm.was_passed
        assert gm.player == BLACK
        assert gm.turn == 1

    def test_next_disk_次の番へ白石の場合(self, mocker):
        gm = Game()
        mocker.patch("PythonOthello.Game.get_next_player", return_value=WHITE)
        gm.next_disk()
        assert not gm.was_passed
        assert gm.player == WHITE
        assert gm.turn == 1

    def test_pass_moving_パスしてゲーム終了でない場合(self, mocker):
        gm = Game()
        gm.was_passed = False
        mocker.patch("PythonOthello.Game.shift_player")
        gm.pass_moving()
        assert gm.was_passed

    def test_pass_moving_パスしてゲーム終了である場合(self, mocker):
        gm = Game()
        gm.was_passed = True
        mocker.patch("PythonOthello.Game.finish_game", return_value=BLACK)
        mocker.patch("PythonOthello.Game.shift_player")
        assert gm.pass_moving() == BLACK

    def test_show_score(self, capsys):
        gm = Game()
        gm.disks[BLACK] = 0
        gm.disks[WHITE] = 0
        gm.show_score()
        captured = capsys.readouterr()
        assert captured.out == "BLACK: 0\nWHITE: 0\n"

    def test_get_disk_map(self):
        gm = Game()
        disks = gm.get_disk_map()
        assert disks[BLACK] == 2
        assert disks[WHITE] == 2

    def test_finish_game_勝者が黒石の場合(self, mocker):
        gm = Game()
        disks = {}
        disks[BLACK] = 3
        disks[WHITE] = 2
        mocker.patch("PythonOthello.Game.get_disk_map", return_value=disks)
        assert gm.finish_game() == BLACK

    def test_finish_game_勝者が白石の場合(self, mocker):
        gm = Game()
        disks = {}
        disks[BLACK] = 2
        disks[WHITE] = 3
        mocker.patch("PythonOthello.Game.get_disk_map", return_value=disks)
        assert gm.finish_game() == WHITE

    def test_finish_game_ドローの場合(self, mocker):
        gm = Game()
        disks = {}
        disks[BLACK] = 2
        disks[WHITE] = 2
        mocker.patch("PythonOthello.Game.get_disk_map", return_value=disks)
        mocker.patch("PythonOthello.Game.on_draw", return_value=gm.DRAW)
        assert gm.finish_game() == gm.DRAW

    def test_on_draw(self):
        gm = Game()
        assert gm.on_draw() == gm.DRAW

class TestBoardUI:
    def test_initialize(self, mocker):
        mocker.patch("PythonOthello.BoardUI.createWidgets")
        mocker.patch("PythonOthello.BoardUI.initOthello")
        bui = BoardUI(mocker.Mock(spec=TK))
        assert bui.color[YOU] == YOUR_COLOR
        assert bui.color[COM] == COM_COLOR

    def test_getOval_XSとXEとYSとYEを比較する(self, mocker):
        mocker.patch("PythonOthello.BoardUI.createWidgets")
        mocker.patch("PythonOthello.BoardUI.initOthello")
        bui = BoardUI(mocker.Mock(spec=TK))
        assert bui.getInitXS(1, 50) == 50
        assert bui.getInitYS(1, 50) == 50
        assert bui.getInitXE(1, 50) == 100
        assert bui.getInitYE(1, 50) == 100
        assert bui.getInitTag(1, 2) == "square_1_2"

    def test_getOval_CenterXやCenterYやXSとXEとYSとYEを比較する(self, mocker):
        mocker.patch("PythonOthello.BoardUI.createWidgets")
        mocker.patch("PythonOthello.BoardUI.initOthello")
        bui = BoardUI(mocker.Mock(spec=TK))
        bui.square_size = CANVAS_SIZE // BOARD_SIZE
        assert bui.getOvalCenterX(0) == 25
        assert bui.getOvalCenterY(0) == 25
        assert bui.getOvalXS(25) == 5
        assert bui.getOvalYS(25) == 5
        assert bui.getOvalXE(25) == 45
        assert bui.getOvalYE(25) == 45
        assert bui.getOvalTag(1, 2) == "disk_1_2"

    def test_drawDisk(self, mocker):
        mocker.patch("PythonOthello.BoardUI.createWidgets")
        mocker.patch("PythonOthello.BoardUI.initOthello")
        bui = BoardUI(mocker.Mock(spec=TK))
        bui.square_size = CANVAS_SIZE // BOARD_SIZE
        bui.canvas = mocker.Mock(spec=Canvas)
        bui.drawDisk(0, 0, 2)

    def test_update(self, mocker):
        mocker.patch("PythonOthello.BoardUI.createWidgets")
        mocker.patch("PythonOthello.BoardUI.initOthello")
        mocker.patch("PythonOthello.BoardUI.drawDisk")
        bui = BoardUI(mocker.Mock(spec=TK))
        bui.canvas = mocker.Mock(spec=Canvas)
        cells = "0000000000000000000000000002100000012000000000000000000000000000"
        bui.update(cells)

class TK:
    pass

class Canvas:
    def create_oval(self):
        pass

    def update(self):
        pass