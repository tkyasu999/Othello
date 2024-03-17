import subprocess
import time
import tkinter
import tkinter.messagebox
import threading

WHITE = 0
BLACK = 1
BOARD_SIZE = 8

CANVAS_SIZE = 400
BOARD_COLOR = 'green'
YOUR_COLOR = 'black'
COM_COLOR = 'white'

YOU = 1
COM = 2

class ReversiBoard(object):
    def __init__(self):
        # 2次元リストを生成する
        # 各要素の初期値はNone
        self.cells = []
        for i in range(BOARD_SIZE):
            self.cells.append([None for i in range(BOARD_SIZE)])

        # 4つの石を初期配置する
        self.cells[3][3] = WHITE
        self.cells[3][4] = BLACK
        self.cells[4][3] = BLACK
        self.cells[4][4] = WHITE

    def put_disk(self, x, y, player):
        # 既にほかの石があれば置くことができない
        if self.cells[y][x] is not None:
            return False

        # 獲得できる石がない場合も置くことができない
        flippable = self.list_flippable_disks(x, y, player)
        if flippable == []:
            return False

        # 実際に石を置く処理
        self.cells[y][x] = player
        for x,y in flippable:
            self.cells[y][x] = player

        return True

    def list_flippable_disks(self, x, y, player):
        PREV = -1
        NEXT = 1
        DIRECTION = [PREV, 0, NEXT]
        flippable = []

        for dx in DIRECTION:
            for dy in DIRECTION:
                if dx == 0 and dy == 0:
                    continue

                tmp = []
                depth = 0
                while(True):
                    depth += 1

                    # 方向 × 深さ(距離)を要求座標に加算し直線的な探査をする
                    rx = x + (dx * depth)
                    ry = y + (dy * depth)

                    # 調べる座標(rx, ry)がボードの範囲内ならば
                    if 0 <= rx < BOARD_SIZE and 0 <= ry < BOARD_SIZE:
                        request = self.cells[ry][rx]

                        # Noneを獲得することはできない
                        if request is None:
                            break

                        if request == player:  # 自分の石が見つかったとき
                            if tmp != []:      # 探査した範囲内に獲得可能な石があれば
                                flippable.extend(tmp) # flippableに追加
                            break

                        # 相手の石が見つかったとき
                        else:
                            # 獲得可能な石として一時保存
                            tmp.append((rx, ry))
                    else:
                        break
        return flippable

    def show_board(self):
        print("--" * 20)
        for i in self.cells:
            for cell in i:
                if cell == WHITE:
                    print("2", end=" ")
                elif cell == BLACK:
                    print("1", end=" ")
                else:
                    print("0", end=" ")
            print("\n", end="")

    def input_board(self):
        in_str = ""
        for i in self.cells:
            for cell in i:
                if cell == WHITE:
                    in_str += "2"
                elif cell == BLACK:
                    in_str += "1"
                else:
                    in_str += "0"
        
        return in_str

    def list_possible_cells(self, player):
        possible = []
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.cells[y][x] is not None:
                    continue
                if self.list_flippable_disks(x, y, player) == []:
                    continue
                else:
                    possible.append((x, y))
        return possible

class Game(ReversiBoard):
    DRAW = -1

    def __init__(self, turn=0, start_player=BLACK):
        super().__init__()
        self.player = start_player
        self.turn = turn
        self.winner = None
        self.was_passed = False
        self.disks = {}

    def is_finished(self):
        return self.winner is not None

    def list_possible_cells(self):
        return super().list_possible_cells(self.player)

    def get_color(self, player):
        if player == WHITE:
            return "WHITE"
        if player == BLACK:
            return "BLACK"
        else:
            return "DRAW"

    def get_current_player(self):
        return self.player

    def get_next_player(self):
        return WHITE if self.player == BLACK else BLACK

    def shift_player(self):
        self.player = self.get_next_player()

    def put_disk(self, x, y):
        if super().put_disk(x, y, self.player):
            self.was_passed = False
            self.player = self.get_next_player()
            self.turn += 1
        else:
            return False
        
    def next_disk(self):
        self.was_passed = False
        self.player = self.get_next_player()
        self.turn += 1

    def pass_moving(self):
        if self.was_passed:
            return self.finish_game()

        self.was_passed = True
        self.shift_player()

    def show_score(self):
        """それぞれのプレイヤーの石の数を表示する"""
        print("{}: {}".format("BLACK", self.disks[BLACK]))
        print("{}: {}".format("WHITE", self.disks[WHITE]))

    def get_disk_map(self):
        disks = {}
        disks[WHITE] = 0
        disks[BLACK] = 0
        for i in self.cells:
            for cell in i:
                if cell == WHITE:
                    disks[WHITE] += 1
                elif cell == BLACK:
                    disks[BLACK] += 1
        return disks
    
    def finish_game(self):
        self.disks = self.get_disk_map()
        white = self.disks[WHITE]
        black =self.disks[BLACK]

        if white < black:
            self.winner = BLACK
        elif black < white:
            self.winner = WHITE
        else:
            self.winner = self.on_draw()

        return self.winner

    def on_draw(self):
        return self.DRAW

class BoardUI(ReversiBoard):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.color = {
            YOU: YOUR_COLOR,
            COM: COM_COLOR
        }
        self.createWidgets()
        self.initOthello()

    def createWidgets(self):
        self.canvas = tkinter.Canvas(
            self.master,
            bg=BOARD_COLOR,
            width=CANVAS_SIZE+1,
            height=CANVAS_SIZE+1,
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)

    def initOthello(self):
        self.square_size = CANVAS_SIZE // BOARD_SIZE

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                xs = x * self.square_size
                ys = y * self.square_size
                xe = (x + 1) * self.square_size
                ye = (y + 1) * self.square_size

                tag_name = 'square_' + str(x) + '_' + str(y)
                self.canvas.create_rectangle(
                    xs, ys,
                    xe, ye,
                    tag=tag_name
                )
        
        self.update(self.input_board())
 
    def drawDisk(self, x, y, color):
        center_x = (x + 0.5) * self.square_size
        center_y = (y + 0.5) * self.square_size

        xs = center_x - (self.square_size * 0.8) // 2
        ys = center_y - (self.square_size * 0.8) // 2
        xe = center_x + (self.square_size * 0.8) // 2
        ye = center_y + (self.square_size * 0.8) // 2

        tag_name = 'disk_' + str(x) + '_' + str(y)
        self.canvas.create_oval(
            xs, ys,
            xe, ye,
            fill=color,
            tag=tag_name
        )
    
    def update(self, cells):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if int(cells[y*BOARD_SIZE+x]) == 2:
                    self.drawDisk(x, y, self.color[COM])
                elif int(cells[y*BOARD_SIZE+x]) == 1:
                    self.drawDisk(x, y, self.color[YOU])
        self.canvas.update()

class GUI():
    def __init__(self, objTk, bui, game):
        self.objTk = objTk
        self.bui = bui
        self.game = game
        self.buftime = time.time()
        self.timeEvent()

    def timeEvent(self):
        tmp = time.time()
        if(tmp - self.buftime) >= 1:
            data = self.game.input_board()
            th = threading.Thread(target=self.update, args=(data,))
            th.start()
            self.buftime = tmp
        self.objTk.after(1, self.timeEvent)

    def update(self, data):
        self.bui.update(data)
        self.objTk.update()

def startTk(game):
    objTk = tkinter.Tk()
    bui = BoardUI(objTk)
    objTk.title("othello")
    GUI(objTk, bui, game)
    objTk.mainloop()

if __name__ == "__main__":
    game = Game()

    thd = threading.Thread(target=startTk, args=(game,))
    thd.start()
    
    while(True):
        possible = game.list_possible_cells()
        player_name = game.get_color(game.get_current_player())

        if game.is_finished():
            game.show_board()
            game.show_score()
            print("Winner: {}".format(game.get_color(game.winner)))
            break

        if possible == []:
            print("player {} can not puts.".format(player_name))
            game.pass_moving()
            continue

        game.show_board()
        print("player: " + player_name)
        print("put to: " + str(possible))

        print("input_board=" + game.input_board())
        if(player_name == "BLACK"):
            user_input = subprocess.run(["othello_cpu_black.exe", "-b", game.input_board()], capture_output=True, text=True)
        else:
            user_input = subprocess.run(["othello_cpu_white.exe", "-w", game.input_board()], capture_output=True, text=True)

        print("stdout=" + user_input.stdout)
        if user_input.stdout != "pass\n":
            my_tuple = tuple(map(int, user_input.stdout.split(",")))
            index = possible.index(my_tuple)
            game.put_disk(*possible[index])
        else:
            game.next_disk()

        time.sleep(1)