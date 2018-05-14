from functools import partial
from lib import install
from data import get_lesson_books_lst

echo = partial(print, end='', flush=True)

class Screen():
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.input_handlers = {}

        self.quit = False

        self.register_input_handlers()


    def register_input_handlers(self):
        def quit():
            import sys
            sys.exit()

        self.input_handlers['q'] = quit

    def render(self, term):
        pass

    def _input(self, key, term=None):
        key = key.lower()

        if key in self.input_handlers:
            self.input_handlers[key]()
            return True

    def handle_input(self, term):
        with term.cbreak():
            while not self.quit:
                key = term.inkey()
                self._input(key, term);


class WelcomeScreen(Screen):

    def __init__(self, screen_manager):
        Screen.__init__(self, screen_manager)

    def render(self, term):
        render_string = f"""Welcome to Python Trainer

    {term.bold}[B]{term.normal}egin Learning

    {term.bold}[I]{term.normal}nstall Lesson Repository
    {term.bold}[D]{term.normal}elete Lesson Repository
    {term.bold}[Q]{term.normal}uit
"""

        echo(render_string)

    def register_input_handlers(self):
        Screen.register_input_handlers(self)

        def _install():
            ps = PromptScreen("Enter the git repository", self.screen_manager)
            self.screen_manager.next_screen(ps)

        def _begin():
            lesson_books = get_lesson_books_lst()

            bs = ListSelectScreen(lesson_books, self.screen_manager)
            self.screen_manager.next_screen(bs)
            
       
        self.input_handlers['i'] = _install
        self.input_handlers['b'] = _begin

class PromptScreen(Screen):
    def __init__(self, prompt, screen_manager):
        Screen.__init__(self, screen_manager)

        if not prompt:
            raise Exception("Missing arguments")

        self.prompt = prompt
        self.input_log = ""

    def render(self, term=None):
        render_string = f"{self.prompt}: {self.input_log}"

        echo(render_string)

    def install(self):
        install(self.input_log)

    def _input(self, key, term):
        if not Screen._input(self, key):

            if key.name == 'KEY_DELETE':
                self.input_log = self.input_log[:-1]
            elif key.name == 'KEY_ENTER':
                self.install()
            else:
                self.input_log += key

            self.screen_manager.render()

class ListSelectScreen(Screen):
    def __init__(self, lst, screen_manager):
        Screen.__init__(self, screen_manager)
        from remote_pdb import RemotePdb
        RemotePdb('localhost', 4444).set_trace()


        if not lst or len(lst) < 0:
            raise Exception("Please check lst")

        self.lst = lst
        self.selected = 0
        self.length = len(lst)

    def render(self, term):
        for idx, val in enumerate(self.lst):
            if idx == self.selected:
                echo(term.standout)
                print(val['string'])
                echo(term.no_standout)
            else:
                print(val['string'])

    def _input(self, key, term):
        if not Screen._input(self, key):

            if key.name == 'KEY_DOWN':
                self.selected = min(self.selected + 1, self.length)
            elif key.name == 'KEY_UP':
                self.selected = max(self.selected - 1, 0)
            elif key.name == 'KEY_ENTER':
                pass

            self.screen_manager.render()
