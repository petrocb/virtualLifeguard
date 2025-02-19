class Always:
    def __init__(self):
        self.x = 0

    def step(self):
        #create a better alter here!!!!!!!!!!!!!!!!!!!!!!!!
        self.x += 1
        if self.x == 100:
            return True

        return False