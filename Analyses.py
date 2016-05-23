# Analyses.py
# 
# Created:  Mar. 2016, M. Vegh
# Modified: 

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    

import SUAVE
from SUAVE.Core import Units


# ----------------------------------------------------------------------
#   Setup Analyses
# ----------------------------------------------------------------------  

def setup(configs):
    analyses = SUAVE.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag, config in configs.items():
        analysis = base(config)
        analyses[tag] = analysis

    # adjust analyses for configs

    # aerosol-spreading analysis
    # print "test"
    # print analyses.cruise.weights.settings

    # takeoff_analysis
    analyses.takeoff.aerodynamics.settings.drag_coefficient_increment = 0.0000

    # landing analysis
    aerodynamics = analyses.landing.aerodynamics

    # -----------------------------------
    #   Battery Setup
    # -----------------------------------

    # required mission energy, chosen via guess and check
    #
    # # initialize the battery
    # battery = configs.base.energy_network['battery']
    # battery.specific_energy= 1000*Units.Wh/Units.kg
    # battery.specific_power = 1*Units.kW/Units.kg
    # Ereq=1000
    # Preq=1000
    # SUAVE.Methods.Power.Battery.Sizing.initialize_from_energy_and_power(battery,Ereq,Preq)
    # battery.current_energy= [battery.max_energy]
    # configs.base.store_diff()
    #
    # # Update all configs with new base data
    # for config in configs:
    #     config.pull_base()

    # mission.segments['cruise'].battery_energy=configs.base.energy_network.battery.max_energy


    return analyses


# ----------------------------------------------------------------------
#   Define Base Analysis
# ----------------------------------------------------------------------  

def base(vehicle):
    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = SUAVE.Analyses.Vehicle()

    # ------------------------------------------------------------------
    #  Basic Geometry Relations
    sizing = SUAVE.Analyses.Sizing.Sizing()
    sizing.features.vehicle = vehicle
    analyses.append(sizing)

    # ------------------------------------------------------------------
    #  Weights
    weights = SUAVE.Analyses.Weights.Weights()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics = SUAVE.Analyses.Aerodynamics.Fidelity_Zero()
    aerodynamics.geometry = vehicle

    aerodynamics.settings.drag_coefficient_increment = 0.0000
    analyses.append(aerodynamics)

    # ------------------------------------------------------------------
    #  Stability Analysis
    stability = SUAVE.Analyses.Stability.Fidelity_Zero()
    stability.geometry = vehicle
    analyses.append(stability)

    # ------------------------------------------------------------------
    #  Energy
    energy = SUAVE.Analyses.Energy.Energy()
    energy.network = vehicle.propulsors  # what is called throughout the mission (at every time step))
    analyses.append(energy)
    #
    # # ------------------------------------------------------------------
    # #  Energy - batteries
    # energy2= SUAVE.Analyses.Energy.Energy()
    # energy2.network = vehicle.energy_network #what is called throughout the mission (at every time step))
    # analyses.append(energy2)

    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = SUAVE.Analyses.Planets.Planet()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)

    # done!
    return analyses
