from lib.components.capacitor import Capacitor
from lib.components.resistor import Resistor
from lib.components.ground import Ground

INTERSECTION_COLOR = "red"
END_COLOR = "blue"

CORNER_COLOR = "yellow"
COMPONENT_COLOR = "green"
CONNECTION_COLOR = "pink"
OTHER_NODE_COLOR = "white"
DEFAULT_EDGE_COLOR = "black"

OTHER_EDGE_COLOR = "green"

FOREGROUND = 0
BACKGROUND = 255

CLASS_NAMES = ['capacitor', 'ground', 'inductor', 'resistor', 'up', 'down', 'left', 'right']
CLASS_OBJECT_NAMES = {"cap":'capacitor', "gnd":'ground', "ind":'inductor', "res":'resistor'}
CLASS_OBJECTS = {"resistor":Resistor(),"ground":Ground(),"capacitor":Capacitor()}

POSSIBLE_ROTATIONS = [0,90,180,270]

ROTATION_DICT = {'right':0,'up':90,'left':180,'down':270}

INTERSECTION_COMBINATION_DIST = 3
