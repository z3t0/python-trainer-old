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

    def _input(self, key):
        if key in self.input_handlers:
            self.input_handlers[key]()
            return True

    def handle_input(self, term):
        with term.cbreak():
            while not self.quit:
                key = term.inkey().lower()
                self._input(key);


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


        print(render_string)

    def register_input_handlers(self):
        Screen.register_input_handlers(self)

        def _install():
            ps = PromptScreen("Enter the git repository", self.screen_manager)
            self.screen_manager.next_screen(ps)
            
       
        self.input_handlers['i'] = _install

class PromptScreen(Screen):
    def __init__(self, prompt, screen_manager):
        Screen.__init__(self, screen_manager)

        if not prompt:
            raise Exception("Missing arguments")

        self.prompt = prompt

    def render(self, term):
        render_string = f"{self.prompt}: "

        print(render_string)

    def _input(self, key):
        if not Screen._input(self, key):
            print(key, end="", flush=True)
        
        
