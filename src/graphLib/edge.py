class Edge:
    color = None
    label = None
    attr = {}

    def __init__(self,color="black",label="",attr={}) -> None:
        self.color = color
        self.label = label
        self.attr = dict(attr)

    def __setId__(self,id):
        self.id = id