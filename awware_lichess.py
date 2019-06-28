from selenium import webdriver
import re
import chess
from pystockfish import *
import win32api, win32con
import dictmoves
import keyboard
import time
from random import randint
from selenium.webdriver.chrome.options import Options

#SHIT CODE SIMULATION
#THX https://github.com/iacobcristi

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.4)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def rightClick(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    time.sleep(0.7)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)

def toggleBrowsec():
    click(1820, 52)
    time.sleep(1)
    click(1580, 390)

def reconnectBrowsec():
    click(1820, 52)
    time.sleep(1)
    click(1790, 465)
    time.sleep(1)
    click(1790, 465)

color = -1
#1820 52 -> BROWSEC
#1580 390 -> Browsec Protect
#1790 464 -> Reconnect

chrome_options = Options()
chrome_options.add_extension('Browsec/omghfjlpggmjjaagoclmmobgdodcjboh.crx')

chrome = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
chrome.maximize_window()
toggleBrowsec()
chrome.get('https://lichess.org/')

def click_square(square):
    if color == 1:
        x, y = dictmoves.blackdict[square]
    else:
        x, y = dictmoves.whitedict[square]
    print((x, y))
    click(int(x) + randint(-randint(4, 15), randint(4, 9)), int(y) + randint(-randint(4, 9), randint(4, 15)))

def rclick_square(square):
    if color == 1:
        x, y = dictmoves.blackdict[square]
    else:
        x, y = dictmoves.whitedict[square]
    print((x, y))
    rightClick(int(x) + randint(-randint(4, 15), randint(4, 9)), int(y) + randint(-randint(4, 9), randint(4, 15)))

def myColor():
    table_wrap = chrome.find_elements_by_css_selector(
        '#main-wrap > main > div.round__app.variant-standard > div.rclock.rclock-bottom')
    if len(table_wrap):
        table_wrap = table_wrap[0].get_attribute('innerHTML')
    else:
        return -1
    if 'white' in table_wrap:
        return 0
    return 1

def myColor2():
    if chrome.find_elements_by_css_selector('#main-wrap > main > div.puzzle__board.main-board > div.cg-board-wrap.orientation-black.manipulable'):
        return 1
    return 0

def myColor3():
    orient = chrome.find_element_by_xpath('/html/body/div[1]/main/div[1]/div[1]/div')
    if orient.get_attribute('class') == 'cg-wrap orientation-black manipulable':
        return 1
    return 0

def getFen():
    moves = chrome.find_elements_by_css_selector(
        '#main-wrap > main > div.round__app.variant-standard > div.rmoves > div.moves')
    PGNMoves = [re.sub('х', 'x', move) for move in moves[0].text.split() if not move.isdigit()]
    board = chess.Board()
    print(PGNMoves)
    for move in PGNMoves:
        board.push_san(move)
    fen = board.fen()
    print('GET FEN 1 - ', fen)
    return fen

def getFen2():
    moves = chrome.find_elements_by_css_selector(
        '#main-wrap > main > div.puzzle__tools > div.puzzle__moves.areplay > div.tview2.tview2-column')
    print(moves[0].text)
    PGNMoves = [re.sub('х', 'x', move) for move in moves[0].text.split() if not move.isdigit()]
    board = chess.Board()
    PGNMoves[:] = (value for value in PGNMoves if value != '✓')
    print(PGNMoves)
    for move in PGNMoves:
        board.push_san(move)
    fen = board.fen()
    print('GET FEN 2 - ', fen)
    return fen

def getBestStupidMove(fen):
    deep = Engine(depth=1)
    deep.setfenposition(fen)
    best = deep.bestmove()['move']
    print(best)
    return best

def getBestMoveRandom(fen):
    deep = Engine(depth=randint(1, 15))
    deep.setfenposition(fen)
    best = deep.bestmove()['move']
    print('Random depth -> ', deep.depth)
    return best

def getBestInTheBestMove(fen):
    deep = Engine(depth=15)
    deep.setfenposition(fen)
    best = deep.bestmove()['move']
    print('Best in the best -> ', best)
    return best

def getReasonablyMove(fen):
    deep = Engine(depth=5)
    deep.setfenposition(fen)
    best = deep.bestmove()['move']
    print('Reasonably -> ', best)
    return best

def stupidMove():
    global color
    color = myColor3()
    fen = getFen()
    best = getBestStupidMove(fen)
    click_square(best[:2])
    click_square(best[2:])

def bestMove():
    global color
    color = myColor3()
    print('color - ', color)
    fen = getFen()
    print('fen - ', fen)
    best = getBestInTheBestMove(fen)
    print('best ', best)
    click_square(best[:2])
    click_square(best[2:])

def reasonablyMove():
    global color
    color = myColor3()
    fen = getFen()
    best = getBestInTheBestMove(fen)
    click_square(best[:2])
    click_square(best[2:])

def predicate():
    global color
    color = myColor3()
    fen = getFen()
    best = getReasonablyMove(fen)
    rclick_square(best[:2])
    time.sleep(0.5)
    rclick_square(best[2:])

def RandomDepthMove():
    global color
    color = myColor3()
    fen = getFen()
    print('FEN IS - ', fen)
    if fen is None or fen is '':
        fen = getFen2()
    best = getBestMoveRandom(fen)
    print('best step - ', best)
    click_square(best[:2])
    click_square(best[2:])

print('Press W -> Depth 15\nPress Q -> Depth 1\nPress E -> Depth random\nPress R -> Reconnect browsec\nPress p -> Predicate move')

#inifiny loop
while True:
    try:
        if keyboard.is_pressed('q'):
            stupidMove()
        elif keyboard.is_pressed('w'):
            bestMove()
        elif keyboard.is_pressed('e'):
            RandomDepthMove()
        elif keyboard.is_pressed('r'):
            reconnectBrowsec()
        elif keyboard.is_pressed('p'):
            print('Predicating...')
            predicate()
        else:
            pass
    except Exception as e:
        print(e)
        pass
