class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return "<" + str(self.start) + " " + str(self.end) + ">"
