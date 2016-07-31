# Jet A1
#
# Created:  Unk 2013, SUAVE TEAM
# Modified: Apr 2015, SUAVE TEAM
#           Feb 2016, M.Vegh
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from SUAVE.Attributes.Propellants.Propellant import Propellant


# ----------------------------------------------------------------------
#  Jet_A1 Propellant Class
# ----------------------------------------------------------------------

class Jet_JP7(Propellant):
    """ Physical properties of Jet A-1; reactant = O2 """

    def __defaults__(self):
        self.tag = 'JP-7'
        self.reactant = 'O2'
        self.density = 790.0  # kg/m^3 (15 C, 1 atm)
        self.specific_energy = 43.682e6  # J/kg
        self.energy_density = 39700e6  # J/m^3
        self.max_mass_fraction = {'Air': 0.0633, 'O2': 0.3022}  # kg propellant / kg oxidizer
        self.temperatures.flash = 334  # K
        self.temperatures.autoignition = 514  # K
        self.temperatures.freeze = 229.7  # K
        self.temperatures.boiling = 200
