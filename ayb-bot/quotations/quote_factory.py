class QuoteFactory:
    def __init__(self, quotes):
        self.quotes = quotes
        self.index = -1

    def next(self):
        self.index = (self.index + 1) % len(self.quotes)
        return self.quotes[self.index]
