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

#have alternative mission files

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

    # airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude = 0.0 * Units.ft
    airport.delta_isa = 0.0
    airport.atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976

    mission.airport = airport

    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments

    # base segment
    base_segment = Segments.Segment()
    base_segment.process.iterate.conditions.weights = update_weights_sprayer

    atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    planet = SUAVE.Attributes.Planets.Earth()

    # Constant_Throttle_Constant_Speed


    # # ------------------------------------------------------------------
    # #   First Climb Segment: Constant Throttle
    # # ------------------------------------------------------------------
    #
    # segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    # segment.tag = "climb_1"
    #
    # # connect vehicle configuration
    # segment.analyses.extend( analyses.cruise )
    #
    # # define segment attributes
    # segment.atmosphere     = atmosphere
    # segment.planet         = planet
    # # segment.battery_energy = 10 #Charge the battery to start
    #
    #
    # segment.altitude_start = 0.0   * Units.km
    # segment.altitude_end   = 8 * Units.km
    # segment.air_speed      = 118.0 * Units['m/s']
    # segment.throttle     = 0.95 * Units['m/s']
    #
    # # segment.process.iterate.conditions.weights = update_weights_sprayer
    # segment.sprayer_rate = 0 * Units['kg/s']
    #
    # # add to misison
    # mission.append_segment(segment)
    #
    #
    # # ------------------------------------------------------------------
    # #   Second Climb Segment: Constant Throttle
    # # ------------------------------------------------------------------
    #
    # segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    # segment.tag = "climb_2"
    #
    # # connect vehicle configuration
    # segment.analyses.extend( analyses.cruise )
    #
    # # define segment attributes
    # segment.atmosphere     = atmosphere
    # segment.planet         = planet
    # # segment.battery_energy = 10 #Charge the battery to start
    #
    #
    # segment.altitude_start = 0.0   * Units.km
    # segment.altitude_end   = 8 * Units.km
    # segment.air_speed      = 168.0 * Units['m/s']
    # segment.throttle     = 0.95 * Units['m/s']
    #
    # # segment.process.iterate.conditions.weights = update_weights_sprayer
    # segment.sprayer_rate = 0 * Units['kg/s']
    #
    # # add to misison
    # mission.append_segment(segment)


    #CLIMB PHASES START HERE:


    # ------------------------------------------------------------------
    #   First Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_1"

    # connect vehicle configuration
    segment.analyses.extend(analyses.takeoff)

    # define segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet
    # segment.battery_energy = 10 #Charge the battery to start


    segment.altitude_start = 0.0 * Units.km
    segment.altitude_end = 3 * Units.km
    segment.air_speed = 118.0 * Units['m/s']
    segment.climb_rate = 40. * Units['m/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment
    segment.sprayer_rate = 0 * Units['kg/s']

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_2"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.altitude_end = 6 * Units.km
    segment.air_speed = 148.0 * Units['m/s']
    segment.climb_rate = 30. * Units['m/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment
    segment.sprayer_rate = 0 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Climb Segment: Constant Speed, Constant Climb Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_3"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.altitude_end = 11. * Units.km
    segment.air_speed = 180.0 * Units['m/s']
    segment.climb_rate = 15. * Units['m/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment
    segment.sprayer_rate = 0 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fourth Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_4"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.altitude_end = 15. * Units.km
    segment.air_speed = 200.0 * Units['m/s']
    segment.climb_rate = 10 * Units['m/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment
    segment.sprayer_rate = 0 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fifth Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_5"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.altitude_end = 18 * Units.km
    segment.air_speed = 210.0 * Units['m/s']
    segment.climb_rate = 3. * Units['m/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment
    segment.sprayer_rate = 0 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Sixth Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_6"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.altitude_end = 18.5 * Units.km
    segment.air_speed = 650.0 * Units['km/h']
    segment.climb_rate = 2. * Units['m/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment
    segment.sprayer_rate = 0 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

     # ------------------------------------------------------------------
     #   Seventh Climb Segment: Constant Speed, Constant Rate
     # ------------------------------------------------------------------
    #
    # segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    # segment.tag = "climb_7"
    #
    # # connect vehicle configuration
    # segment.analyses.extend( analyses.cruise )
    #
    # # segment attributes
    # segment.atmosphere   = atmosphere
    # segment.planet       = planet
    #
    # segment.altitude_end = 19.5 * Units.km
    # segment.air_speed    = 670.0  * Units['km/h']
    # segment.climb_rate   = 0.5   * Units['m/s']
    #
    # segment.sprayer_rate = 0 * Units['kg/s']
    #
    #  # segment.process.iterate.conditions.weights = update_weights_sprayer
    # segment.aerosol_mass_initial = 0 * Units.kg # mass to be sprayed in this segment
    # segment.sprayer_rate = 0 * Units['kg/s']
    #
    #
    # # add to mission
    # mission.append_segment(segment)
    #
    # # ------------------------------------------------------------------
    #  #   Eighth Climb Segment: Constant Speed, Constant Rate
    #  # ------------------------------------------------------------------
    #
    # segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    # segment.tag = "climb_8"
    #
    #  # connect vehicle configuration
    # segment.analyses.extend( analyses.cruise )
    #
    #  # segment attributes
    # segment.atmosphere   = atmosphere
    # segment.planet       = planet
    #
    # segment.altitude_end = 20. * Units.km
    # segment.air_speed    = 670.0  * Units['km/h']
    # segment.climb_rate   = 0.25   * Units['m/s']
    #
    # # segment.sprayer_rate = 0 * Units['kg/s']
    #
    # # segment.process.iterate.conditions.weights = update_weights_sprayer
    # # segment.aerosol_mass_initial = 2000 * Units.kg # mass to be sprayed in this segment
    # segment.sprayrate_override = 1  * Units['kg/s'] #1 for mission (3500km)
    #
    #
    # # add to mission
    # mission.append_segment(segment)


    # # ------------------------------------------------------------------
    #  #   Throttle Max Climb Segment: Constant Speed, Constant Rate
    #  # ------------------------------------------------------------------
    #
    # # ------------------------------------------------------------------
    # #   First Climb Segment: Constant Speed, Constant Rate
    # # ------------------------------------------------------------------
    #
    # segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    # segment.tag = "climb_1"
    #
    # # connect vehicle configuration
    # segment.analyses.extend(analyses.takeoff)
    #
    # # define segment attributes
    # segment.atmosphere = atmosphere
    # segment.planet = planet
    # # segment.battery_energy = 10 #Charge the battery to start
    #
    #
    # segment.altitude_start = 0.0 * Units.km
    # segment.altitude_end = 3 * Units.km
    # segment.air_speed = 118.0 * Units['m/s']
    # segment.climb_rate = 40. * Units['m/s']
    #
    # # segment.process.iterate.conditions.weights = update_weights_sprayer
    # segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment
    # segment.sprayer_rate = 0 * Units['kg/s']
    #
    # # add to misison
    # mission.append_segment(segment)
    #
    #
    # segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    # segment.tag = "climb_8"
    #
    #  # connect vehicle configuration
    # segment.analyses.extend( analyses.cruise )
    #
    #  # segment attributes
    # segment.atmosphere   = atmosphere
    # segment.planet       = planet
    #
    # segment.altitude_end = 18.5 * Units.km
    # segment.throttle = 1
    # segment.air_speed    = 700.0  * Units['km/h']
    # # segment.climb_rate   = 0.25   * Units['m/s']
    #
    # # segment.sprayer_rate = 0 * Units['kg/s']
    #
    # # segment.process.iterate.conditions.weights = update_weights_sprayer
    # # segment.aerosol_mass_initial = 2000 * Units.kg # mass to be sprayed in this segment
    # # segment.sprayrate_override = 1  * Units['kg/s'] #1 for mission (3500km)
    #
    #
    # # add to mission
    # mission.append_segment(segment)


    # # ------------------------------------------------------------------
    # #   First Cruise Segment: constant speed, constant altitude
    # # ------------------------------------------------------------------
    #
    # segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    # segment.tag = "cruise_highlift"
    #
    # # connect vehicle configuration
    # segment.analyses.extend( analyses.landing ) #FIXME
    #
    # # segment attributes
    # segment.atmosphere = atmosphere
    # segment.planet     = planet
    #
    # segment.air_speed  = 691. * Units['km/h']
    # segment.distance   = 900. * Units.km
    #
    # # segment.conditions.weights.vehicle_mass_rate = 2 * Units['kg/s']
    #
    # # segment.process.iterate.conditions.weights = update_weights_sprayer
    # # aerosol_mass = 40000 * Units.kg #- payload mass
    # # segment.sprayer_rate = 2.4706 #aerosol_mass / (segment.distance / segment.air_speed ) #* Units['kg/s'] #1.2121 * Units['kg/s']
    # # segment.aerosol_mass_initial = 0 * Units.kg # mass to be sprayed in this segment/
    # # print segment.sprayer_rate
    # segment.aerosol_mass_initial = 10060 * Units.kg
    #
    #
    # # add to mission
    # mission.append_segment(segment)



    # CRUISE STARTS HERE!!

    # ------------------------------------------------------------------
    #  Second Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_2"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.air_speed = 730. * Units['km/h']
    segment.distance = 1100 * Units.km

    # segment.conditions.weights.vehicle_mass_rate = 2 * Units['kg/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 13300 * Units.kg  # mass to be sprayed in this segment

    # segment.sprayer_rate = aerosol_mass_initial / (segment.distance / segment.air_speed ) #* Units['kg/s'] #1.2121 * Units['kg/s']
    # print segment.sprayer_rate # delegate rate to a method which will calculate live rate?
    #  2.4706 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_2_1"

    # connect vehicle configuration
    segment.analyses.extend(analyses.takeoff)

    # define segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet
    # segment.battery_energy = 10 #Charge the battery to start


    segment.altitude_end = 19.5 * Units.km
    segment.air_speed = 691.0 * Units['km/h']
    segment.climb_rate = 1.5 * Units['m/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment
    segment.sprayer_rate = 0 * Units['kg/s']

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #  Second Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_2_2"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.air_speed = 730. * Units['km/h']
    segment.distance = 1100 * Units.km

    # segment.conditions.weights.vehicle_mass_rate = 2 * Units['kg/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 13300 * Units.kg  # mass to be sprayed in this segment

    # segment.sprayer_rate = aerosol_mass_initial / (segment.distance / segment.air_speed ) #* Units['kg/s'] #1.2121 * Units['kg/s']
    # print segment.sprayer_rate # delegate rate to a method which will calculate live rate?
    #  2.4706 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_2_2"

    # connect vehicle configuration
    segment.analyses.extend(analyses.takeoff)

    # define segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet
    # segment.battery_energy = 10 #Charge the battery to start


    segment.altitude_end = 20.5 * Units.km
    segment.air_speed = 691.0 * Units['km/h']
    segment.climb_rate = 1.5 * Units['m/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment
    segment.sprayer_rate = 0 * Units['kg/s']

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #  Second Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_2_3"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.air_speed = 730. * Units['km/h']
    segment.distance = 1200 * Units.km

    # segment.conditions.weights.vehicle_mass_rate = 2 * Units['kg/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 13300 * Units.kg  # mass to be sprayed in this segment

    # segment.sprayer_rate = aerosol_mass_initial / (segment.distance / segment.air_speed ) #* Units['kg/s'] #1.2121 * Units['kg/s']
    # print segment.sprayer_rate # delegate rate to a method which will calculate live rate?
    #  2.4706 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)


    #
    # # ------------------------------------------------------------------
    # #   Climbing Cruise Segment (Alternative): constant speed, constant altitude
    # # ------------------------------------------------------------------
    #
    # segment = Segments.Climb.Constant_Mach_Constant_Angle(base_segment)
    # segment.tag = "cruise_2"#_climbing"
    #
    # # connect vehicle configuration
    # segment.analyses.extend( analyses.cruise )
    #
    # # segment attributes
    # segment.atmosphere = atmosphere
    # segment.planet     = planet
    #
    # segment.altitude_end  = 20.5 * Units['km']
    # segment.mach   = 0.71
    # segment.climb_angle =  (20.5-18.5)/(3400) * Units.rad/Units.deg  #np.arctan(1/3400) * Units.rad
    #
    # # segment.conditions.weights.vehicle_mass_rate = 2 * Units['kg/s']
    # segment.aerosol_mass_initial = 0 * Units.kg # mass to be sprayed in this segment
    #
    # # segment.process.iterate.conditions.weights = update_weights_sprayer
    # # aerosol_mass = 40000 * Units.kg
    # segment.sprayer_rate = 2.4706 * Units['kg/s'] #aerosol_mass / (segment.distance / segment.air_speed ) #* Units['kg/s'] #1.2121 * Units['kg/s']
    # # print segment.sprayer_rate
    #
    # # add to mission
    # mission.append_segment(segment)

    # Linear_Speed_Constant_Rate


    # self.altitude_start = None # Optional
    # self.altitude_end   = 10. * Units.km
    # self.climb_angle    = 3.  * deg
    # self.mach           = 0.7




    # ------------------------------------------------------------------
    #   First Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_1"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.altitude_end = 19.2 * Units.km
    segment.air_speed = 720. * Units['km/h']
    segment.descent_rate = 500. * Units['ft/min']
    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment
    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.sprayer_rate = 0 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_3"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.air_speed = 750. * Units['km/h']
    segment.distance = 1100. * Units.km
    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.sprayer_rate = 0 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_2"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.altitude_end = 3.657 * Units.km
    segment.air_speed = 400.0 * Units.knots
    segment.descent_rate = 2300. * Units['ft/min']

    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.sprayer_rate = 0 * Units['kg/s']

    # append to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_3"

    # connect vehicle configuration
    segment.analyses.extend(analyses.landing)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.altitude_end = 0.0 * Units.km
    segment.air_speed = 250.0 * Units.knots
    segment.descent_rate = 1500. * Units['ft/min']

    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.sprayer_rate = 0 * Units['kg/s']

    # append to mission
    mission.append_segment(segment)

    #  ------------------------------------------------------------------
    #   Mission definition complete
    # ------------------------------------------------------------------

    #
    #
    # ------------------------------------------------------------------
    ###         Reserve mission
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    #   First Climb Segment: constant Mach, constant segment angle
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    #   First Climb Segment: Constant Speed, Constant Throttle
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "reserve_climb"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # define segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.altitude_start = 0.0 * Units.km
    segment.altitude_end = 15000. * Units.ft
    segment.air_speed = 138.0 * Units['m/s']
    segment.climb_rate = 3000. * Units['ft/min']

    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment

    segment.sprayer_rate = 0 * Units['kg/s']

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Mach_Constant_Altitude(base_segment)
    segment.tag = "reserve_cruise"

    segment.analyses.extend(analyses.cruise)

    segment.mach = 0.5
    segment.distance = 1000.0 * Units.km  # 1000km for the most critical case

    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment

    segment.sprayer_rate = 0 * Units['kg/s']
    mission.append_segment(segment)
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

    # segment.sprayer_rate = 0 * Units['kg/s']
    #
    # mission.append_segment(segment)
    #

    # ------------------------------------------------------------------
    #  Final Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Linear_Mach_Constant_Rate(base_segment)
    segment.tag = "reserve_descent_1"

    segment.analyses.extend(analyses.landing)
    analyses.landing.aerodynamics.settings.spoiler_drag_increment = 0.00

    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment

    segment.altitude_end = 0.0 * Units.km
    segment.descent_rate = 3.0 * Units['m/s']

    segment.sprayer_rate = 0 * Units['kg/s']

    segment.mach_end = 0.24
    segment.mach_start = 0.3

    # append to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    ###         Reserve mission completed
    # ------------------------------------------------------------------


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
