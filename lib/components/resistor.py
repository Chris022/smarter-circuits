from lib.components.baseComponent import BaseComponent

#        |-------------|
# #0-----|             |--------#1
#        |-------------|
class Resistor(BaseComponent):

    @staticmethod
    def connect(rotation,intersectionVertices):
        #get lowest Y and X coordinate
        for intersectionVertex in intersectionVertices:
            pass