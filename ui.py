from blessed import Terminal
import queue

# from lib import install
from screens import WelcomeScreen, PromptScreen

class ScreenManager():
    def __init__(self):
        self.state = queue.LifoQueue()
        self.current = None
        self.term = None

    def render(self):
        if self.current:
            self.term = Terminal()
            print(self.term.clear())
            self.current.render(self.term)
            self.current.handle_input(self.term)

    def next_screen(self, screen):
        self.state.put(screen)
        self.current = screen
        self.render()

    def prev_screen(self):
        if not self.state.empty():
            return self.state.get()

        


def handle_input(term):
    sm.handle_input(term)
    
sm = ScreenManager()

ws = WelcomeScreen(sm)
sm.next_screen(ws)

sm.render()
