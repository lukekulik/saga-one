# Missions.py
# 
# Created:  Mar 2016, M. Vegh
# Modified: 


# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    

import SUAVE
from SUAVE.Core import Units
from sprayer import update_weights_sprayer

import numpy as np

# ----------------------------------------------------------------------
#   Define the Mission
# ----------------------------------------------------------------------
    
def setup(analyses):
    
    # the mission container
    missions = SUAVE.Analyses.Mission.Mission.Container()

    # ------------------------------------------------------------------
    #   Base Mission
    # ------------------------------------------------------------------
    base_mission = base(analyses)
    missions.base = base_mission 
 

    



    return missions  

    
def base(analyses):
    
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------

    mission = SUAVE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'the_mission'

    #airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude   =  0.0  * Units.ft
    airport.delta_isa  =  0.0
    airport.atmosphere =  SUAVE.Analyses.Atmospheric.US_Standard_1976

    mission.airport = airport    

    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments

    # base segment
    base_segment = Segments.Segment()
    atmosphere=SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    planet = SUAVE.Attributes.Planets.Earth()
    
    # ------------------------------------------------------------------
    #   First Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate()
    segment.tag = "climb_1"

    # connect vehicle configuration
    segment.analyses.extend( analyses.base )

    # define segment attributes
    segment.atmosphere     = atmosphere
    segment.planet         = planet
    # segment.battery_energy = 10 #Charge the battery to start


    segment.altitude_start = 0.0   * Units.km
    segment.altitude_end   = 3.048 * Units.km
    segment.air_speed      = 118.0 * Units['m/s']
    segment.climb_rate     = 15. * Units['m/s']

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate()
    segment.tag = "climb_2"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet

    segment.altitude_end = 3.657 * Units.km
    segment.air_speed    = 148.0 * Units['m/s']
    segment.climb_rate   = 13. * Units['m/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Climb Segment: Constant Speed, Constant Climb Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate()
    segment.tag = "climb_3"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet

    segment.altitude_end = 11. * Units.km
    segment.air_speed    = 180.0  * Units['m/s']
    segment.climb_rate   = 10. * Units['m/s']

    # add to mission
    mission.append_segment(segment)
    
     # ------------------------------------------------------------------
    #   Fourth Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate()
    segment.tag = "climb_4"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet

    segment.altitude_end = 15. * Units.km
    segment.air_speed    = 200.0* Units['m/s']
    segment.climb_rate   = 8. * Units['m/s']

    # add to mission
    mission.append_segment(segment)   
    
    # ------------------------------------------------------------------
    #   Fifth Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate()
    segment.tag = "climb_5"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet

    segment.altitude_end = 65600. * Units.ft
    segment.air_speed    = 210.0  * Units['m/s']
    segment.climb_rate   = 7.   * Units['m/s']

    # add to mission
    mission.append_segment(segment)    
    
    
    # ------------------------------------------------------------------
    #   First Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude()
    segment.tag = "cruise"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet     = planet

    segment.air_speed  = 684. * Units['km/h']
    segment.distance   = 3400. * Units.km

    # segment.conditions.weights.vehicle_mass_rate = 2 * Units['kg/s']

    segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.sprayer_rate = 1.2 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   First Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate()
    segment.tag = "descent_1"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet

    segment.altitude_end = 15.8  * Units.km
    segment.air_speed    = 684. * Units['km/h']
    segment.descent_rate = 2600. * Units['ft/min']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude()
    segment.tag = "cruise_2"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet     = planet

    segment.air_speed  = 684. * Units['km/h']
    segment.distance   = 3300. * Units.km

    # add to mission
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Second Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate()
    segment.tag = "descent_2"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet

    segment.altitude_end = 3.657 * Units.km
    segment.air_speed    = 365.0 * Units.knots
    segment.descent_rate = 2300. * Units['ft/min']

    # append to mission
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Third Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate()
    segment.tag = "descent_3"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet

    segment.altitude_end = 0.0   * Units.km
    segment.air_speed    = 250.0 * Units.knots
    segment.descent_rate = 1500. * Units['ft/min']

    # append to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Mission definition complete    
    # ------------------------------------------------------------------
    
    #
    #
    # #------------------------------------------------------------------
    # ###         Reserve mission
    # #------------------------------------------------------------------
    #
    # # ------------------------------------------------------------------
    # #   First Climb Segment: constant Mach, constant segment angle
    # # ------------------------------------------------------------------
    #
    # # ------------------------------------------------------------------
    # #   First Climb Segment: Constant Speed, Constant Throttle
    # # ------------------------------------------------------------------
    #
    # segment = Segments.Climb.Constant_Speed_Constant_Rate()
    # segment.tag = "reserve_climb"
    #
    # # connect vehicle configuration
    # segment.analyses.extend( analyses.base )
    #
    # # define segment attributes
    # segment.atmosphere     = atmosphere
    # segment.planet         = planet
    #
    # segment.altitude_start = 0.0    * Units.km
    # segment.altitude_end   = 15000. * Units.ft
    # segment.air_speed      = 138.0  * Units['m/s']
    # segment.climb_rate     = 3000.  * Units['ft/min']
    #
    # # add to misison
    # mission.append_segment(segment)
    #
    #
    #
    # # ------------------------------------------------------------------
    # #   Cruise Segment: constant speed, constant altitude
    # # ------------------------------------------------------------------
    #
    # segment = Segments.Cruise.Constant_Mach_Constant_Altitude(base_segment)
    # segment.tag = "reserve_cruise"
    #
    # segment.analyses.extend( analyses.cruise )
    #
    # segment.mach      = 0.5
    # segment.distance  = 140.0 * Units.nautical_mile
    # mission.append_segment(segment)
    #
    # # ------------------------------------------------------------------
    # #   Loiter Segment: constant mach, constant time
    # # ------------------------------------------------------------------
    #
    # segment = Segments.Cruise.Constant_Mach_Constant_Altitude_Loiter(base_segment)
    # segment.tag = "reserve_loiter"
    #
    # segment.analyses.extend( analyses.cruise )
    #
    # segment.mach = 0.5
    # segment.time = 30.0 * Units.minutes
    #
    # mission.append_segment(segment)
    #
    #
    # # ------------------------------------------------------------------
    # #  Final Descent Segment: consant speed, constant segment rate
    # # ------------------------------------------------------------------
    #
    # segment = Segments.Descent.Linear_Mach_Constant_Rate(base_segment)
    # segment.tag = "reserve_descent_1"
    #
    # segment.analyses.extend( analyses.landing )
    # analyses.landing.aerodynamics.settings.spoiler_drag_increment = 0.00
    #
    #
    # segment.altitude_end = 0.0   * Units.km
    # segment.descent_rate = 3.0   * Units['m/s']
    #
    #
    # segment.mach_end    = 0.24
    # segment.mach_start  = 0.3
    #
    # append to mission
    # mission.append_segment(segment)
    
    #------------------------------------------------------------------
    ###         Reserve mission completed
    #------------------------------------------------------------------
    

    return mission





# ----------------------------------------------------------------------        
#   Call Main
# ----------------------------------------------------------------------    

if __name__ == '__main__':
    import vehicles
    import analyses
    
    vehicles = vehicles.setup()
    analyses = analyses.setup(vehicles)
    missions = setup(analyses)
    
    vehicles.finalize()
    analyses.finalize()
    missions.finalize()
    
    missions.base.evaluate()