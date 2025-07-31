import sys
from cefpython3 import cefpython as cef
from engine import AI_move, GameEngine
import os

DIR = os.getcwd()

class startgame:
    def __init__(self) -> None:
        self.AI_move = AI_move()
        self.engine = GameEngine()
        cef.Initialize()
        self.define_bindings()
        cef.MessageLoop()
        del self.browser
        # cef.Shutdown()

    def define_bindings(self):
        self.browser = cef.CreateBrowserSync(url=f'file:///{DIR}/tic.html',
                                        window_title="Tic Tac Toe",)
        
        self.browser.ToggleFullscreen() # make game fullscreen
        bindings = cef.JavascriptBindings()
        bindings.SetFunction("py_exit", self.py_exit)
        bindings.SetFunction("py_reset", self.py_reset)
        bindings.SetFunction("py_set_difficulty", self.py_set_difficulty)
        bindings.SetFunction("py_ai_move", self.py_ai_move)
        bindings.SetFunction("py_player_move", self.py_player_move)
        bindings.SetFunction("py_start_new", self.py_start_new)
        bindings.SetFunction("py_cv_value", self.py_cv_value)
        self.browser.SetJavascriptBindings(bindings)

    def py_exit(self):
        cef.Shutdown()

    def py_set_difficulty(self, value, js_set_difficulty):
        print(value)
        if 0 <= value <= 2:
            self.AI_move.difficulty = value
            js_set_difficulty.Call(True)
        else:
            js_set_difficulty.Call(False)

    def py_start_new(self,js_start_new):
        js_start_new.Call(self.AI_move.start_new())

    def py_ai_move(self,js_ai_move):
        js_ai_move.Call(self.AI_move.process_AI())

    def py_player_move(self,move,js_player_move):
        js_player_move.Call(self.AI_move.process_player(move))

    def py_reset(self, js_reset):
        del self.AI_move

        self.AI_move = AI_move()
        
        js_reset.Call(self.AI_move.reset())

    def py_cv_value(self,js_fingers):
        js_fingers.Call(self.engine.send_value())

if __name__ == '__main__':
    startgame()