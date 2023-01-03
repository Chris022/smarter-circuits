class Vertex:
    
    def __init__(self,color="black",label="",attr={}) -> None:
        self.id = None
        self.color = color
        self.label = label
        self.attr = dict(attr)

    def __setId__(self,id):
        self.id = id

    def __repr__(self) -> str:
        return "   Vector: [" + str(self.id) + " " + str(self.color) + " " + str(self.attr) + " ]   "