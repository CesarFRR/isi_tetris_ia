from Classifier import Classifier
from Framer import Framer


fr = Framer()

class NextManager:
    def __init__(self):
        self.next = None
        self.cls = Classifier()
        self.fr = Framer()

    def get_next(self, next):
        return self.next
    
    def load_next(self, next):
        self.next = next

    def handle(self, request):
        if self.next:
            self.next.handle(request)

class HoldManager:
    def __init__(self):
        self.hold = None
        self.cls = Classifier()
        self.fr = Framer()

    def get_hold(self, hold):
        return self.hold
    
    def load_hold(self, hold):
        self.hold = hold

    def handle(self, request):
        if self.hold:
            self.hold.handle(request)

class GridManager:
    def __init__(self):
        self.grid = None
        self.cls = Classifier()
        self.fr = Framer()

    def get_grid(self, grid):
        return self.grid
    
    def load_grid(self, grid):
        self.grid = grid

    def handle(self, request):
        if self.grid:
            self.grid.handle(request)