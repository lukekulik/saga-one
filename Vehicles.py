# Vehicles.py
# 
# Created:  Feb. 2016, M. Vegh
# Modified: 

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    

import SUAVE
from SUAVE.Core import Units, Data
import numpy as np
from engine import engine_caluclations


# ----------------------------------------------------------------------
#   Define the Vehicle
# ----------------------------------------------------------------------

def setup():
    base_vehicle = base_setup()
    configs = configs_setup(base_vehicle)

    return configs


def base_setup():



    # ------------------------------------------------------------------
    #   Initialize the Vehicle
    # ------------------------------------------------------------------

    vehicle = SUAVE.Vehicle()
    vehicle.tag = 'SAGA_One'

    # important design parameters exported out for clarity:

    twin = "OFF"
    vehicle.thrust_total = 0e3 * Units.N  # defined in Optimize.py
    num_engine = 4 # move to main -> how to guarantee these parameters when not optimized for??? - selected at the top and entered in inputs from there?
    bypass = 7.5

    # design sizing conditions
    altitude = 19. * Units.km
    mach_number = 0.68



    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------

    # mass properties
    vehicle.mass_properties.max_takeoff = 0  # selected in Optimize.py
    vehicle.mass_properties.takeoff = 0  # selected in Optimize.py
    vehicle.mass_properties.max_payload = 40000. * Units.kg  # selected in Optimize.py
    vehicle.mass_properties.payload = 40000. * Units.kg  # selected in Optimize.py

    # vehicle.mass_properties.operating_empty           = 65000.   # kg

    # vehicle.mass_properties.max_zero_fuel             = 105000. #60899.3  # kg
    # vehicle.mass_properties.cargo                     = 0.0 * Units.kg

    # vehicle.mass_properties.max_fuel                  = 30000.

    # vehicle.mass_properties.center_of_gravity = [18., 0, 0]
    # vehicle.mass_properties.moments_of_inertia.tensor = [[10 ** 5, 0, 0], [0, 10 ** 6, 0, ],
    #                                                      [0, 0, 10 ** 7]]  # Not Correct

# envelope properties
    vehicle.envelope.ultimate_load = 3.75
    vehicle.envelope.limit_load = 2.5

    # basic parameters
    vehicle.reference_area = 0  # selected in Optimize.py
    vehicle.passengers = 0
    vehicle.systems.control = "fully powered"
    vehicle.systems.accessories = "long range"

    # # ------------------------------------------------------------------
    # #  Airfoil
    # # ------------------------------------------------------------------
    #
    # airfoil = SUAVE.Components.Wings.Airfoils.Airfoil()
    # airfoils = SUAVE.Components.Wings.Airfoils.load_airfoils(
    #     "/Users/lkulik/Dropbox/Shared/DSE Conceptual Design/suave_saga/")

    # ------------------------------------------------------------------
    #   Main Wing
    # ------------------------------------------------------------------

    wing = SUAVE.Components.Wings.Main_Wing()
    wing.tag = 'main_wing'

    # wing.airfoil = airfoils["sc3"]

    wing.span_efficiency = 0.75
    wing.areas.reference = 0  # selected in Optimize.py

    wing.aspect_ratio = 0  # selected in Optimize.py

    wing.sweep = 0.0 * Units.deg

    wing.thickness_to_chord = 0.12
    wing.taper = 0.55
    wing.spans.projected = np.sqrt(wing.aspect_ratio * wing.areas.reference)

    wing.chords.root = 2*wing.spans.projected/(wing.aspect_ratio*(1+wing.taper))
    wing.chords.tip = wing.chords.root*wing.taper
    # wing.chords.mean_aerodynamic = 3.680

    wing.areas.wetted = 2.0 * wing.areas.reference
    wing.areas.exposed = 0.8 * wing.areas.wetted
    wing.areas.affected = 0.6 * wing.areas.reference

    wing.twists.root = 2.0 * Units.degrees
    wing.twists.tip = 0.0 * Units.degrees

    wing.origin = [13.2, 0, 0]  # Need to fix
    # wing.aerodynamic_center      = [3,0,0] # Need to fix  ---> MUST INCLUDE A SIZING CALL, TO GENERATE PLANFORM

    wing.vertical = False
    wing.symmetric = True

    wing.high_lift = True
    wing.high_mach = True
    wing.flaps.type = "double_slotted"
    wing.flaps.chord = 1.0  # FIXME

    wing.dynamic_pressure_ratio = 1.0

    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------
    #  Horizontal Stabilizer
    # ------------------------------------------------------------------

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'horizontal_stabilizer'

    wing.aspect_ratio = 5.5
    wing.sweep = 34.5 * Units.deg
    wing.thickness_to_chord = 0.11
    wing.taper = 0.11
    wing.span_efficiency = 0.9

    wing.chords.root = 3.030
    wing.chords.tip = 0.883
    wing.chords.mean_aerodynamic = 2.3840

    wing.areas.reference = 115
    wing.areas.wetted = 2.0 * wing.areas.reference
    wing.areas.exposed = 0.8 * wing.areas.wetted
    wing.areas.affected = 0.6 * wing.areas.reference

    wing.spans.projected = np.sqrt(wing.aspect_ratio * wing.areas.reference)

    wing.twists.root = 2.0 * Units.degrees
    wing.twists.tip = 2.0 * Units.degrees

    wing.origin = [31., 0, 0]  # need to fix
    # wing.aerodynamic_center      = [3,0,0] # Need to fix  ---> MUST INCLUDE A SIZING CALL, TO GENERATE PLANFORM

    wing.vertical = False
    wing.symmetric = True

    wing.dynamic_pressure_ratio = 0.9

    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------
    #   Vertical Stabilizer
    # ------------------------------------------------------------------

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'vertical_stabilizer'

    wing.aspect_ratio = 1.7  #
    wing.sweep = 35 * Units.deg
    wing.thickness_to_chord = 0.11
    wing.taper = 0.31
    wing.span_efficiency = 0.9

    wing.chords.root = 4.70
    wing.chords.tip = 1.45
    wing.chords.mean_aerodynamic = 3.36

    wing.areas.reference = 81.0  #

    wing.spans.projected = np.sqrt(wing.aspect_ratio * wing.areas.reference)

    wing.areas.wetted = 2.0 * wing.areas.reference
    wing.areas.exposed = 0.8 * wing.areas.wetted
    wing.areas.affected = 0.6 * wing.areas.reference

    wing.twists.root = 0.0 * Units.degrees
    wing.twists.tip = 0.0 * Units.degrees

    wing.origin = [29.5, 0, 0]
    # wing.aerodynamic_center      = [3,0,0] # Need to fix  ---> MUST INCLUDE A SIZING CALL, TO GENERATE PLANFORM

    wing.vertical = True
    wing.symmetric = False

    wing.dynamic_pressure_ratio = 1.0

    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------
    #  Fuselage (Right)
    # ------------------------------------------------------------------

    fuselage = SUAVE.Components.Fuselages.Fuselage()
    fuselage.tag = 'fuselage'
    fuselage.origin = [0, 0, 0]  # yeyesyesyes
    fuselage.number_coach_seats = vehicle.passengers
    fuselage.seats_abreast = 0
    # fuselage.seat_pitch            = 0.7455

    fuselage.fineness.nose = 2.5
    fuselage.fineness.tail = 2.5

    fuselage.lengths.nose = 5.0
    fuselage.lengths.tail = 5.0
    fuselage.lengths.cabin = 40.0
    fuselage.lengths.total = 50.0 # FIXME add a formula
    fuselage.lengths.fore_space = 0.
    fuselage.lengths.aft_space = 0.

    fuselage.width = 1.4

    fuselage.heights.maximum = 1.4
    fuselage.heights.at_quarter_length = 1.4
    fuselage.heights.at_three_quarters_length = 1.4
    fuselage.heights.at_wing_root_quarter_chord = 1.4

    fuselage.areas.side_projected = 8.
    fuselage.areas.wetted = 21.05
    fuselage.areas.front_projected = 0.78

    fuselage.effective_diameter = 1.4

    fuselage.differential_pressure = 0 * Units.pascal  # Maximum differential pressure

    # add to vehicle
    vehicle.append_component(fuselage)

    if twin == "ON":
        # ------------------------------------------------------------------
        #  Fuselage (Left)
        # ------------------------------------------------------------------
        print "Twin-fuselage activated"
        fuselage = SUAVE.Components.Fuselages.Fuselage()
        fuselage.tag = 'fuselage2'
        fuselage.origin = [0, -10, 0]  # yeyesyesyes
        fuselage.number_coach_seats = vehicle.passengers
        fuselage.seats_abreast = 0
        # fuselage.seat_pitch            = 0.7455

        fuselage.fineness.nose = 2.5
        fuselage.fineness.tail = 2.5

        fuselage.lengths.nose = 1.0
        fuselage.lengths.tail = 1.0
        fuselage.lengths.cabin = 6
        fuselage.lengths.total = 8
        fuselage.lengths.fore_space = 0.
        fuselage.lengths.aft_space = 0.

        fuselage.width = 1.4

        fuselage.heights.maximum = 1.4
        fuselage.heights.at_quarter_length = 1.4
        fuselage.heights.at_three_quarters_length = 1.4
        fuselage.heights.at_wing_root_quarter_chord = 1.4

        fuselage.areas.side_projected = 8.
        fuselage.areas.wetted = 21.05
        fuselage.areas.front_projected = 0.78

        fuselage.effective_diameter = 1

        fuselage.differential_pressure = 0 * Units.pascal  # Maximum differential pressure

        # add to vehicle
        vehicle.append_component(fuselage)

    # ------------------------------------------------------------------
    #  Turbofan Network
    # ------------------------------------------------------------------


    gt_engine = engine_caluclations(altitude, bypass, mach_number, num_engine, vehicle.thrust_total)

    # print"vehicles: gt_engine"
    # print gt_engine

    # add gas turbine network gt_engine to the vehicle
    vehicle.append_component(gt_engine)

    # now add weights objects
    landing_gear = SUAVE.Components.Landing_Gear.Landing_Gear()
    vehicle.landing_gear = landing_gear

    control_systems = SUAVE.Components.Physical_Component()
    vehicle.control_systems = control_systems

    electrical_systems = SUAVE.Components.Physical_Component()
    vehicle.electrical_systems = electrical_systems

    avionics = SUAVE.Components.Energy.Peripherals.Avionics()
    vehicle.avionics = avionics

    passengers = SUAVE.Components.Physical_Component()
    vehicle.passenger_weights = passengers

    furnishings = SUAVE.Components.Physical_Component()
    vehicle.furnishings = furnishings

    air_conditioner = SUAVE.Components.Physical_Component()
    vehicle.air_conditioner = air_conditioner

    fuel = SUAVE.Components.Physical_Component()
    vehicle.fuel = fuel

    apu = SUAVE.Components.Physical_Component()
    vehicle.apu = apu

    hydraulics = SUAVE.Components.Physical_Component()
    vehicle.hydraulics = hydraulics

    optionals = SUAVE.Components.Physical_Component()
    vehicle.optionals = optionals

    rudder = SUAVE.Components.Physical_Component()
    vehicle.wings['vertical_stabilizer'].rudder = rudder

    # ------------------------------------------------------------------
    #   Vehicle Definition Complete
    # ------------------------------------------------------------------

    return vehicle


# ----------------------------------------------------------------------
#   Define the Configurations
# ---------------------------------------------------------------------

def configs_setup(vehicle):
    # ------------------------------------------------------------------
    #   Initialize Configurations
    # ------------------------------------------------------------------

    configs = SUAVE.Components.Configs.Config.Container()

    base_config = SUAVE.Components.Configs.Config(vehicle)
    base_config.tag = 'base'
    configs.append(base_config)

    # ------------------------------------------------------------------
    #   Cruise Configuration
    # ------------------------------------------------------------------

    config = SUAVE.Components.Configs.Config(base_config)
    config.tag = 'cruise'

    config.maximum_lift_coefficient = 1.4

    configs.append(config)

    # ------------------------------------------------------------------
    #   Takeoff Configuration
    # ------------------------------------------------------------------

    config = SUAVE.Components.Configs.Config(base_config)
    config.tag = 'takeoff'

    config.wings['main_wing'].flaps.angle = 20. * Units.deg
    config.wings['main_wing'].slats.angle = 25. * Units.deg

    config.V2_VS_ratio = 1.21
    config.maximum_lift_coefficient = 2.2

    configs.append(config)

    # ------------------------------------------------------------------
    #   Landing Configuration
    # ------------------------------------------------------------------

    config = SUAVE.Components.Configs.Config(base_config)
    config.tag = 'landing'

    config.wings['main_wing'].flaps_angle = 30. * Units.deg
    config.wings['main_wing'].slats_angle = 25. * Units.deg

    config.Vref_VS_ratio = 1.23
    config.maximum_lift_coefficient = 2.2

    configs.append(config)

    # ------------------------------------------------------------------
    #   Short Field Takeoff Configuration
    # ------------------------------------------------------------------ 

    config = SUAVE.Components.Configs.Config(base_config)
    config.tag = 'short_field_takeoff'

    config.wings['main_wing'].flaps.angle = 20. * Units.deg
    config.wings['main_wing'].slats.angle = 25. * Units.deg

    config.V2_VS_ratio = 1.21
    config.maximum_lift_coefficient = 2.

    configs.append(config)

    # ------------------------------------------------------------------
    #   High-lift initial payload Configuration
    # ------------------------------------------------------------------

    config = SUAVE.Components.Configs.Config(base_config)
    config.tag = 'high_lift_cruise'

    config.wings['main_wing'].flaps.angle = 10. * Units.deg
    # config.wings['main_wing'].slats.angle = 10. * Units.deg

    # config.V2_VS_ratio = 1.21
    config.maximum_lift_coefficient = 2.

    # payload?

    configs.append(config)

    # done!
    return configs
