import lib.components.patterns.capacitor    as CapacitorPattern
import lib.components.patterns.resistor     as ResistorPattern
import lib.components.patterns.ground       as GroundPattern
import lib.components.patterns.voltage      as VoltagePattern

import lib.components.components.capacitor  as Capacitor
import lib.components.components.resistor   as Resistor
import lib.components.components.inductor   as Inductor
import lib.components.components.ground     as Ground
import lib.components.components.voltage    as Voltage


PATTERNS = {
    1: ResistorPattern.Resistor(),
    2: CapacitorPattern.Capacitor(),
    3: GroundPattern.Ground(),
    4: VoltagePattern.Voltage()
}

CLASS_OBJECTS = {
    "resistor":Resistor.Resistor(),
    "inductor":Inductor.Inductor(),
    "capacitor":Capacitor.Capacitor(),
    "ground":Ground.Ground(),
    "voltage":Voltage.Voltage()
}