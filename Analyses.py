# Analyses.py
# 
# Created:  Mar. 2016, M. Vegh
# Modified: 

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    

import SUAVE

from Optimize import AVL_analysis
from supporting.empty_saga import empty
from supporting.stability_saga import Fidelity_Zero


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

    # takeoff_analysis
    analyses.takeoff.aerodynamics.settings.drag_coefficient_increment = 0.0000

    # landing analysis
    aerodynamics = analyses.landing.aerodynamics

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
    weights.settings.empty_weight_method = empty
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    if not AVL_analysis:  # Run zero-fidelity method
        aerodynamics = SUAVE.Analyses.Aerodynamics.Fidelity_Zero()
        aerodynamics.geometry = vehicle

        aerodynamics.settings.drag_coefficient_increment = 0.0000
        analyses.append(aerodynamics)

    # AVL-based analysis
    else:
        # aerodynamics.process.compute.lift = aerodynamics_avl
        # aerodynamics = SUAVE.Analyses.Aerodynamics.Fidelity_Zero()
        # aerodynamics.geometry = vehicle
        # aerodynamics.settings.drag_coefficient_increment = 0.0000
        # aerodynamics_avl = SUAVE.Analyses.Aerodynamics.Surrogates.AVL()
        # aerodynamics_avl.features = vehicle
        # aerodynamics_avl.geometry = vehicle
        # aerodynamics_avl.training.angle_of_attack = np.array([-5.,0.,15.]) * Units.deg
        #
        # aerodynamics.process.compute.lift = aerodynamics_avl

        # aerodynamics_avl.process.compute.lift.aerodynamics_avl = aerodynamics_avl
        # aerodynamics.initialize()

        # aerodynamics_avl.lift.total

        # aerodynamics_avl.finalized = False
        # print aerodynamics_avl

        aerodynamics = SUAVE.Analyses.Aerodynamics.AVL()
        aerodynamics.geometry = vehicle
        aerodynamics.features = vehicle
        analyses.append(aerodynamics)

    # # ------------------------------------------------------------------
    # #  Stability Analysis
    # stability = Fidelity_Zero()#SUAVE.Analyses.Stability.Fidelity_Zero()
    # stability.geometry = vehicle
    # analyses.append(stability)

    #  Noise Analysis
    noise = SUAVE.Analyses.Noise.Fidelity_One()
    noise.geometry = vehicle
    analyses.append(noise)

    # ------------------------------------------------------------------
    #  Energy
    energy = SUAVE.Analyses.Energy.Energy()
    energy.network = vehicle.propulsors  # what is called throughout the mission (at every time step))
    analyses.append(energy)
    #

    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = SUAVE.Analyses.Planets.Planet()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976(temperature_deviation=30.0)
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)

    # done!
    return analyses
