
#
# オセロ（リバーシ） 6x6
#

N = 6  # 大きさ

EMPTY = 0  # 空
BLACK = 1  # 黒
WHITE = 2  # 白
STONE = ['□', '●', '○']  #石の文字

#
# board = [0] * (N*N)
#

def xy(p):    # 1次元から2次元へ
  return p % N, p // N
#文字盤の数字を座標で表示


def p(x, y):    # 2次元から1次元へ
  return x + y * N


# リバーシの初期画面を生成する

def init_board():
  board = [EMPTY] * (N*N)
  c = N//2 #3
  board[p(c, c)] = BLACK
  board[p(c-1, c-1)] = BLACK
  board[p(c, c-1)] = WHITE
  board[p(c-1, c)] = WHITE
  return board

# リバーシの画面を表示する

def show_board(board):
  counts = [0, 0, 0]
  for y in range(N):
    for x in range(N):
      stone = board[p(x, y)]
      counts[stone] += 1 #石が置かれたら０(空)から１(黒)　さらに置かれたら2(白)になる
      print(STONE[stone], end='') #数字を記号で表示,改行しない
    print()
  print()
  for pair in zip(STONE, counts): #(石,石の数)
    print(pair, end=' ')
  print()
#最後に空のprint()があるのは、for文で最後の一個表示した後にまた次をprintしようとすると、さらに上書きしてしまう為です。
#空のprintを入れる事で、そのまま改行をしているという仕組みです。


# (x,y) が盤面上か判定する
def on_borad(x, y):
  return 0 <= x < N and 0 <= y < N

# (x,y)から(dx,dy)方向をみて反転できるか調べる
def try_reverse(board, x, y, dx, dy, color):
  if not on_borad(x, y) or board[p(x, y)] == EMPTY:
    return False
  if board[p(x, y)] == color: #とりあえず色がついていたら(Emptyでないものなら)
    return True
  if try_reverse(board, x+dx, y+dy, dx, dy, color):
    board[p(x, y)] = color
    return True
  return False

# 相手（反対）の色を返す
def opposite(color):
  if color == BLACK:
    return WHITE
  return BLACK

# (x,y) が相手（反対）の色かどうか判定 

def is_oposite(board, x, y, color):
  return on_borad(x, y) and board[p(x, y)] == opposite(color) #相手の色ならTrue

#自分の周辺
DIR = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),         (1, 0),
    (-1, 1), (0, 1), (1, 1),
]

def put_and_reverse(board, position, color):
  if board[position] != EMPTY:
  	return False
  board[position] = color

  x, y = xy(position) #座標に変換
  turned = False
  for dx, dy in DIR:
    nx = x + dx
    ny = y + dy
    if is_oposite(board, nx, ny, color): #相手の色
      if try_reverse(board, nx, ny, dx, dy, color): #ひっくり返せる環境
        turned = True
  if not turned: #どんな状況？
    board[position] = EMPTY
  return turned

# プレイが継続できるか？ 
# つまり、まだ石を置けるところが残っているか調べる？
def can_play(board, color):
  board = board[:] # コピーしてボードを変更しないようにする
  for position in range(0, N*N):
    if put_and_reverse(board, position, color):
      return True
  return False


def game(player1, player2):
	board = init_board() #初期画面
	show_board(board) #画面表示
	on_gaming = True  # 　ゲームが続行できるか？
	while on_gaming:
		on_gaming = False  # 　いったん、ゲーム終了にする
		if can_play(board, BLACK):
			# player1 に黒を置かせる
			position = player1(board[:], BLACK) #なぜ引数を持ってこられるのか？
			show_board(board)
			# 黒が正しく置けたら、ゲーム続行
			on_gaming = put_and_reverse(board, position, BLACK) #空でないならFalse=置く場所がなければ終了
		if can_play(board, WHITE):
			# player1 に白を置かせる
			position = player2(board[:], WHITE)
			show_board(board)
			# 白が置けたらゲーム続行
			on_gaming = put_and_reverse(board, position, WHITE)
	show_board(board)  # 最後の結果を表示!

# AI 用のインターフェース
  
import random
def Simple_AI(board,color):
  for _ in range(100):
    l=[i for i in range(0,N*N)]
    w=[5,2,3,3,2,5,2,1,4,4,1,2,3,4,0,0,4,3,3,4,0,0,4,3,2,1,4,4,1,2,5,2,3,3,2,5] #重りをつける
    position=random.choices(l,weights=w)
    position=position[0]
    if put_and_reverse(board,position,color):
      return position
  return 0
