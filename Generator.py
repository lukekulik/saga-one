# Payload.py
# 
# Created:  Jun 2014, E. Botero
# Modified: Feb 2016, T. MacDonald

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# suave imports
import SUAVE
from SUAVE.Components.Energy.Energy_Component import Energy_Component
import numpy as np


# ----------------------------------------------------------------------
#  Payload Class
# ----------------------------------------------------------------------  

class Generator(Energy_Component):
    def __defaults__(self):

        self.power_draw = 0.0
        self.reference_temperature = 288.15
        self.reference_pressure = 1.01325 * 10 ** 5
        self.compressor_nondimensional_massflow = 0.0

    def compute(self):
        """ The avionics input power
            
            Inputs:
                draw
               
            Outputs:
                power output
               
            Assumptions:
                This device just draws power
               
        """

        mdhc = self.inputs.mdhc

        Tref = self.reference_temperature
        Pref = self.reference_pressure

        total_temperature_reference = self.inputs.total_temperature_reference
        total_pressure_reference = self.inputs.total_pressure_reference

        self.outputs.power = self.power_draw

        mdot_core = mdhc * np.sqrt(Tref / total_temperature_reference) * (total_pressure_reference / Pref)

        if np.all(mdot_core) != 0:
            self.outputs.work_done = self.outputs.power / mdot_core
        else:
            self.outputs.work_done = 0
            # print mdot_core


            # print self.outputs.work_done

    __call__ = compute
