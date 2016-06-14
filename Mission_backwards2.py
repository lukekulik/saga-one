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

    missions.takeoff = takeoff_mission_setup(analyses)

    # Sideline Takeoff mission
    missions.sideline_takeoff = sideline_mission_setup(analyses)

    # Landing mission
    missions.landing = landing_mission_setup(analyses)

    return missions


def base(analyses):
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------

    mission = SUAVE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'the_mission'

    # airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude = 0.0 * Units.km
    airport.delta_isa = 0.0
    airport.atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976

    mission.airport = airport

    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments

    # base segment
    base_segment = Segments.Segment()
    base_segment.process.iterate.conditions.weights = update_weights_sprayer
    # ADD A RANGE HERE?

    atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976(temperature_deviation=0.0)
    planet = SUAVE.Attributes.Planets.Earth()

    climb_throttle = 0.925  # Constant throttle for all climb segments
    climb_air_speed = 210. * Units['m/s']

    # CLIMB PHASES START HERE:

    # ------------------------------------------------------------------
    #  Take off phase
    # ------------------------------------------------------------------

    # segment = Segments.Ground.Takeoff(base_segment)
    # segment.tag = "take_off"
    #
    # # connect vehicle configuration
    # segment.analyses.extend(analyses.takeoff)
    #
    # # define segment attributes
    # segment.atmosphere     = atmosphere
    # segment.planet         = planet
    #
    # segment.velocity_start = 0.0
    # segment.velocity_end = 118. * Units['m/s']
    # segment.friction_coefficient = 0.04
    # segment.throttle = 1.0
    # segment.ground_incline = 0.
    #
    # # segment.process.iterate.conditions.weights = update_weights_sprayer
    # segment.sprayer_rate = 0 * Units['kg/s']
    # segment.aerosol_mass_initial = 0. * Units.kg
    #
    # # add to misison
    # mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   First Climb Segment: Constant Throttle
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "climb_1"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # define segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.altitude_start = 0.0 * Units.km
    segment.altitude_end = 3.0 * Units.km
    segment.air_speed = 118.0 * Units['m/s']
    segment.throttle = climb_throttle

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.sprayer_rate = 0 * Units['kg/s']
    segment.aerosol_mass_initial = 0. * Units.kg

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
    segment.air_speed = (climb_air_speed - 10.) * Units['m/s']
    segment.climb_rate = 15. * Units['m/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment
    segment.sprayer_rate = 0 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fourth Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "final_outgoing"

    # Initial conditions
    ones_row = segment.state.ones_row
    segment.state.unknowns.body_angle = ones_row(1) * 7.0 * Units.deg
    segment.state.unknowns.wind_angle = ones_row(1) * 5.0 * Units.deg

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.altitude_start = 11. * Units.km
    segment.altitude_end = 15. * Units.km
    segment.air_speed = climb_air_speed * Units['m/s']
    segment.throttle = climb_throttle

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment
    segment.sprayer_rate = 0 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    # CRUISE WITH THE AEROSOL ON BOARD

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_outgoing"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.air_speed = 200 * Units.m / Units.s
    # segment.altitude_start = 15. * Units.km
    # segment.angle_of_attack = 2. * Units.deg
    segment.distance = 3367. * Units.km
    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.sprayer_rate = 0 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fifth Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "climb_5"

    # Set initial values of the climb unknowns to ensure convergence
    ones_row = segment.state.ones_row
    segment.state.unknowns.body_angle = ones_row(1) * 7.0 * Units.deg
    segment.state.unknowns.wind_angle = ones_row(1) * 5.0 * Units.deg

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    # segment.altitude_start = 15. * Units.km
    segment.altitude_end = 17 * Units.km
    segment.air_speed = climb_air_speed * Units['m/s']
    segment.throttle = climb_throttle
    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment
    segment.sprayer_rate = 0 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Sixth Climb Segment: Constant Throttle
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)

    # Set initial values of the climb unknowns to ensure convergence
    ones_row = segment.state.ones_row
    segment.state.unknowns.body_angle = ones_row(1) * 7.0 * Units.deg
    segment.state.unknowns.wind_angle = ones_row(1) * 5.0 * Units.deg
    segment.tag = "climb_6"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    # define segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet
    # segment.battery_energy = 10 #Charge the battery to start


    # segment.altitude_start = 17 * Units.km
    segment.altitude_end = 18.5 * Units.km
    segment.air_speed = climb_air_speed * Units['m/s']
    segment.throttle = climb_throttle + 0.05

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.sprayer_rate = 0 * Units['kg/s']
    segment.aerosol_mass_initial = 0. * Units.kg

    # add to misison
    mission.append_segment(segment)

    # CRUISE STARTS HERE!!

    # ------------------------------------------------------------------
    #  First Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_1"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise_spraying)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.air_speed = 210. * Units['m/s']
    segment.distance = 1000 * Units.km

    # segment.conditions.weights.vehicle_mass_rate = 2 * Units['kg/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 12500 * Units.kg  # mass to be sprayed in this segment

    # segment.sprayer_rate = aerosol_mass_initial / (segment.distance / segment.air_speed ) #* Units['kg/s'] #1.2121 * Units['kg/s']
    # print segment.sprayer_rate # delegate rate to a method which will calculate live rate?
    #  2.4706 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #  Intermediate climb 1: Constant throttle, constant speed
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)

    # Set initial conditions
    ones_row = segment.state.ones_row
    segment.state.unknowns.body_angle = ones_row(1) * 8.0 * Units.deg
    segment.state.unknowns.wind_angle = ones_row(1) * 6.0 * Units.deg

    segment.tag = "climb_2_1"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise_spraying)

    # define segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet
    # segment.battery_energy = 10 #Charge the battery to start


    segment.altitude_end = 19 * Units.km
    segment.air_speed = climb_air_speed * Units['m/s']
    segment.throttle = climb_throttle

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    # segment.sprayer_rate = 0 * Units['kg/s']

    segment.aerosol_mass_initial = 1450. * Units.kg  # mass to be sprayed in this segment

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #  First Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_2"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise_spraying)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.air_speed = 210. * Units['m/s']
    segment.distance = 1150 * Units.km

    # segment.conditions.weights.vehicle_mass_rate = 2 * Units['kg/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 14250 * Units.kg  # mass to be sprayed in this segment

    # FIXME add iteration which roughly equalizes the mass flow kg/m for all phases

    # segment.sprayer_rate = aerosol_mass_initial / (segment.distance / segment.air_speed ) #* Units['kg/s'] #1.2121 * Units['kg/s']
    # print segment.sprayer_rate # delegate rate to a method which will calculate live rate?
    #  2.4706 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #  Intermediate climb 2: Constant throttle, constant speed
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "climb_2_2"

    # Set initial conditions
    ones_row = segment.state.ones_row
    segment.state.unknowns.body_angle = ones_row(1) * 7.0 * Units.deg
    segment.state.unknowns.wind_angle = ones_row(1) * 5.0 * Units.deg

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise_spraying)

    # define segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet
    # segment.battery_energy = 10 #Charge the battery to start


    segment.altitude_end = 19.5 * Units.km
    segment.air_speed = climb_air_speed * Units['m/s']
    segment.throttle = climb_throttle

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    # segment.sprayer_rate = 0 * Units['kg/s']
    segment.aerosol_mass_initial = 800. * Units.kg  # mass to be sprayed in this segment

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #  Third Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_final"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise_spraying)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.air_speed = 210. * Units['m/s']
    segment.distance = 900 * Units.km

    # segment.conditions.weights.vehicle_mass_rate = 2 * Units['kg/s']

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.aerosol_mass_initial = 11000 * Units.kg  # mass to be sprayed in this segment

    # segment.sprayer_rate = aerosol_mass_initial / (segment.distance / segment.air_speed ) #* Units['kg/s'] #1.2121 * Units['kg/s']
    # print segment.sprayer_rate # delegate rate to a method which will calculate live rate?
    #  2.4706 * Units['kg/s']

    # add to mission
    mission.append_segment(segment)

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

    segment.altitude_end = 18 * Units.km
    segment.air_speed = 210. * Units['m/s']
    segment.descent_rate = 1000. * Units['ft/min']
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
    segment.air_speed = 200. * Units['m/s']
    segment.descent_rate = 6.6 * Units['m/s']

    segment.aerosol_mass_initial = 0 * Units.kg  # mass to be sprayed in this segment

    # segment.process.iterate.conditions.weights = update_weights_sprayer
    segment.sprayer_rate = 0 * Units['kg/s']

    # append to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_final"

    # connect vehicle configuration
    segment.analyses.extend(analyses.landing)

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet = planet

    segment.altitude_end = 0.0 * Units.km
    segment.air_speed = 80. * Units['m/s']
    landing_gradient = 3. * Units.deg
    # segment.descent_rate = -8. * Units['m/s']
    segment.descent_rate = segment.air_speed * np.sin(landing_gradient) * Units['m/s']
    # print segment.descent_rate

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
    segment.altitude_end = 10 * Units.km
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
    segment.descent_rate = 6.0 * Units['m/s']

    segment.sprayer_rate = 0 * Units['kg/s']

    segment.mach_end = 0.24
    segment.mach_start = 0.4

    # append to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    ###         Reserve mission completed
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    #  Landing phase
    # ------------------------------------------------------------------
    #
    # segment = Segments.Ground.Landing(base_segment)
    # segment.tag = "landing"
    #
    # # connect vehicle configuration
    # segment.analyses.extend(analyses.landing)
    #
    # # define segment attributes
    # segment.atmosphere     = atmosphere
    # segment.planet         = planet
    #
    # segment.velocity_start = 80 * Units['m/s']
    # segment.velocity_end = 0.0
    # segment.friction_coefficient = 0.4
    # segment.throttle = 0.0
    #
    # # segment.process.iterate.conditions.weights = update_weights_sprayer
    # segment.sprayer_rate = 0 * Units['kg/s']
    # segment.aerosol_mass_initial = 0. * Units.kg
    #
    # # add to misison
    # mission.append_segment(segment)


    return mission


def takeoff_mission_setup(analyses):
    # ------------------------------------------------------------------
    #   Initialize the Mission segment for takeoff
    # ------------------------------------------------------------------
    mission = SUAVE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'takeoff'

    # airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude = 0.0 * Units.ft
    airport.delta_isa = 0.0
    airport.atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    mission.airport = airport

    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments

    # base segment
    base_segment = Segments.Segment()

    # Climb Segment: Constant throttle, constant speed
    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "climb"
    segment.analyses.extend(analyses.takeoff)
    segment.altitude_start = 35. * Units.fts
    segment.altitude_end = 304.8 * Units.meter
    segment.air_speed = 85.4 * Units['m/s']
    segment.throttle = 1.
    segment.state.numerics.number_control_points = 10
    # segment.state.numerics.discretization_method = SUAVE.Methods.Utilities.Chebyshev.linear_data
    mission.append_segment(segment)

    # Cutback Segment: Constant speed, constant segment angle
    segment = Segments.Climb.Constant_Speed_Constant_Angle_Noise(base_segment)
    segment.tag = "cutback"
    segment.analyses.extend(analyses.takeoff)
    segment.air_speed = 85.4 * Units['m/s']
    segment.climb_angle = 2.86 * Units.degrees
    # segment.state.numerics.discretization_method = SUAVE.Methods.Utilities.Chebyshev.linear_data
    mission.append_segment(segment)

    return mission



def sideline_mission_setup(analyses):
    # ------------------------------------------------------------------
    #   Initialize the Mission segment for takeoff
    # ------------------------------------------------------------------
    mission = SUAVE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'sideline_takeoff'

    # airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude = 0.0 * Units.ft
    airport.delta_isa = 0.0
    airport.atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    mission.airport = airport

    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments

    # base segment
    base_segment = Segments.Segment()

    # Climb Segment: Constant throttle, constant speed
    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "climb"
    segment.analyses.extend(analyses.takeoff)
    segment.altitude_start = 35. * Units.fts
    segment.altitude_end = 1600 * Units.fts
    segment.air_speed = 123 * Units['m/s']#85.4 * Units['m/s']
    segment.throttle = 0.7
    segment.state.numerics.number_control_points = 10
    # segment.state.numerics.discretization_method = SUAVE.Methods.Utilities.Chebyshev.linear_data
    mission.append_segment(segment)

    return mission


def takeoff_mission_initialization(analyses):
    # ------------------------------------------------------------------
    #   Initialize the Mission segment for takeoff
    # ------------------------------------------------------------------
    mission = SUAVE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'takeoff_initialization'

    # airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude = 0.0 * Units.ft
    airport.delta_isa = 0.0
    airport.atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    mission.airport = airport

    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments

    # base segment
    base_segment = Segments.Segment()

    # Climb Segment: Constant speed, constant segment angle
    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "climb"
    segment.analyses.extend(analyses.takeoff)
    segment.altitude_start = 35. * Units.fts
    segment.altitude_end = 300. * Units.meter
    segment.air_speed = 85.4 * Units['m/s']
    segment.throttle = 1.
    segment.state.numerics.number_control_points = 5
    mission.append_segment(segment)

    return mission


def landing_mission_setup(analyses):
    # ------------------------------------------------------------------
    #   Initialize the Mission segment for landing
    # ------------------------------------------------------------------
    mission = SUAVE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'landing'

    # airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude = 0.0 * Units.ft
    airport.delta_isa = 0.0
    airport.atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    mission.airport = airport

    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments

    # base segment
    base_segment = Segments.Segment()
    # ------------------------------------------------------------------
    #   Descent Segment: Constant speed, constant segment angle
    # ------------------------------------------------------------------
    segment = Segments.Descent.Constant_Speed_Constant_Angle_Noise(base_segment)
    segment.tag = "descent"
    segment.analyses.extend(analyses.landing)

    segment.air_speed = 67. * Units['m/s']
    segment.descent_angle = 3.0 * Units.degrees
    # segment.state.numerics.discretization_method = SUAVE.Methods.Utilities.Chebyshev.linear_data
    mission.append_segment(segment)

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
