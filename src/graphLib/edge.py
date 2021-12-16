class Edge:
    color = None
    label = None
    def __init__(self,color="black",label="") -> None:
        self.color = color
        self.label = label
    def __setId(self,id):
        self.id = id