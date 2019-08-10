class Cat:
    def __init__(self, io):
        self.io=io

    def transact(self, op, param = None, nresp=0):
        if param is None:
            param = [0]*4;
        self.io.write(param+[op])
        if nresp > 0:
            return self.io.read(nresp)
        return []
