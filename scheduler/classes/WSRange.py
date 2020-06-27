

class WSRange():
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def getA1(self):
        return self.start.getA1() + ":" + self.end.getA1()