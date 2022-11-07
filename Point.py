class Point:
    def __init__(self, x, y) -> None:
       self.x = x
       self.y = y
    
    def display(self):
        print("("+str(self.x)+" ,"+str(self.y)+" )")

    def duplicate(self, A):
        if self.x == A.x and self.y == A.y:
          return True
        else:
          return False