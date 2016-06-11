# Procedure.py
# 
# Created:  Mar 2016, M. Vegh
# Modified: 

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    

import SUAVE
from SUAVE.Core import Units, Data
import numpy as np
import copy
from SUAVE.Analyses.Process import Process
from SUAVE.Methods.Propulsion.turbofan_sizing import turbofan_sizing
from SUAVE.Methods.Geometry.Two_Dimensional.Cross_Section.Propulsion.compute_turbofan_geometry import \
    compute_turbofan_geometry
from SUAVE.Methods.Center_of_Gravity.compute_component_centers_of_gravity import compute_component_centers_of_gravity
from SUAVE.Methods.Center_of_Gravity.compute_aircraft_center_of_gravity import compute_aircraft_center_of_gravity
from SUAVE.Methods.Aerodynamics.Fidelity_Zero.Lift.compute_max_lift_coeff import compute_max_lift_coeff
from SUAVE.Methods.Performance import estimate_take_off_field_length
from SUAVE.Methods.Performance import estimate_landing_field_length
from SUAVE.Methods.Flight_Dynamics.Dynamic_Stability.Full_Linearized_Equations.longitudinal import longitudinal
from SUAVE.Input_Output.Results import print_parasite_drag, \
    print_compress_drag, \
    print_weight_breakdown
from print_engine_data import print_engine_data
from print_mission_breakdown import print_mission_breakdown

from SUAVE.Methods.Noise.Fidelity_One.Airframe import noise_airframe_Fink
from SUAVE.Methods.Noise.Fidelity_One.Engine import noise_SAE

from SUAVE.Methods.Noise.Fidelity_One.Noise_Tools import pnl_noise
from SUAVE.Methods.Noise.Fidelity_One.Noise_Tools import noise_tone_correction
from SUAVE.Methods.Noise.Fidelity_One.Noise_Tools import epnl_noise
from SUAVE.Methods.Noise.Fidelity_One.Noise_Tools import noise_certification_limits


def pretty_print(d, indent=0):  # recursive printer
    for key in d.keys():
        print '\t' * indent + str(key)
        v = d[key]
        if isinstance(v, Data):
            pretty_print(v, indent + 1)
        elif isinstance(v, (np.ndarray, np.generic)):
            continue
        else:
            print '\t' * (indent + 1) + str(v)


output_folder = "output/"


# ----------------------------------------------------------------------
#   Setup
# ----------------------------------------------------------------------   

def setup():
    # ------------------------------------------------------------------
    #   Analysis Procedure
    # ------------------------------------------------------------------ 

    # size the base config
    procedure = Data()
    procedure.simple_sizing = simple_sizing

    # find the weights
    procedure.weights = weight

    # AVL Analysis to create surrogate model

    # finalizes the data dependencies
    procedure.finalize = finalize

    # performance studies
    procedure.missions = Process()
    procedure.missions.design_mission = design_mission

    # # Noise evaluation
    # procedure.noise = Process()
    # procedure.noise.sideline_init = noise_sideline_init
    # procedure.noise.takeoff_init = noise_takeoff_init
    # procedure.noise.noise_sideline = noise_sideline
    # procedure.noise.noise_flyover = noise_flyover
    # procedure.noise.noise_approach = noise_approach

    # post process the results
    procedure.post_process = post_process

    # done!
    return procedure


# ----------------------------------------------------------------------        
#   Target Range Function
# ----------------------------------------------------------------------    

def find_target_range(nexus, mission):
    segments = mission.segments
    # cruise_altitude = mission.segments['climb_5'].altitude_end
    #
    # climb_1 = segments['climb_1']
    # climb_2 = segments['climb_2']
    # climb_3 = segments['climb_3']
    # climb_4 = segments['climb_4_final_outgoing']
    # climb_5 = segments['climb_5']
    #
    # descent_1 = segments['descent_1']
    # descent_2 = segments['descent_2']
    # # descent_3 = segments['descent_3']
    #
    # x_climb_1 = climb_1.altitude_end / np.tan(np.arcsin(climb_1.climb_rate / climb_1.air_speed))
    # x_climb_2 = (climb_2.altitude_end - climb_1.altitude_end) / np.tan(
    #     np.arcsin(climb_2.climb_rate / climb_2.air_speed))
    # x_climb_3 = (climb_3.altitude_end - climb_2.altitude_end) / np.tan(
    #     np.arcsin(climb_3.climb_rate / climb_3.air_speed))
    # x_climb_4 = (climb_4.altitude_end - climb_3.altitude_end) / np.tan(
    #     np.arcsin(climb_4.climb_rate / climb_4.air_speed))
    # x_climb_5 = (climb_5.altitude_end - climb_4.altitude_end) / np.tan(
    #     np.arcsin(climb_5.climb_rate / climb_5.air_speed))
    # x_descent_1 = (climb_5.altitude_end - descent_1.altitude_end) / np.tan(
    #     np.arcsin(descent_1.descent_rate / descent_1.air_speed))
    # x_descent_2 = (descent_1.altitude_end - descent_2.altitude_end) / np.tan(
    #     np.arcsin(descent_2.descent_rate / descent_2.air_speed))
    # # x_descent_3 = (descent_2.altitude_end - descent_3.altitude_end) / np.tan(
    # #    np.arcsin(descent_3.descent_rate / descent_3.air_speed))
    #
    # cruise_range = mission.design_range - (
    #     x_climb_1 + x_climb_2 + x_climb_3 + x_climb_4 + x_climb_5 + x_descent_1 + x_descent_2)  # + x_descent_3)
    # # some sort of a sum here?

    aerosol_sum = 0.
    payload = nexus.vehicle_configurations.base.mass_properties.payload
    for segment in segments:
        aerosol_sum += segment.aerosol_mass_initial

    for segment in segments:
        segment.aerosol_mass_initial = segment.aerosol_mass_initial * (payload / aerosol_sum) # scaling to account for possible changed payload


    # segments.aerosol_mass_initial

    # segments['cruise_2'].distance=cruise_range # FIXME need to add other cruises

    # print segments.cruise.distance
    # print cruise_range

    return nexus


def noise_sideline_init(nexus):
    # Update number of control points for noise
    mission = nexus.missions.sideline_takeoff
    results = nexus.results
    results.sideline_initialization = mission.evaluate()

    n_points = np.ceil(results.sideline_initialization.conditions.climb.frames.inertial.time[-1] / 0.5 + 1)

    nexus.npoints_sideline_sign = np.sign(n_points)
    nexus.missions.sideline_takeoff.segments.climb.state.numerics.number_control_points = np.minimum(200,
                                                                                                     np.abs(n_points))

    return nexus


def noise_takeoff_init(nexus):
    # Update number of control points for noise
    mission = nexus.missions.takeoff
    results = nexus.results
    results.takeoff_initialization = mission.evaluate()

    n_points = np.ceil(results.takeoff_initialization.conditions.climb.frames.inertial.time[-1] / 0.5 + 1)
    nexus.npoints_takeoff_sign = np.sign(n_points)

    nexus.missions.takeoff.segments.climb.state.numerics.number_control_points = np.minimum(200, np.abs(n_points))

    return nexus


def evaluate_field_length(configs, analyses, mission, results):
    # unpack
    airport = mission.airport

    takeoff_config = configs.takeoff
    landing_config = configs.landing

    # evaluate

    airport.atmosphere = analyses.base.atmosphere

    TOFL = estimate_take_off_field_length(takeoff_config, analyses, airport)
    LFL = estimate_landing_field_length(landing_config, analyses, airport)  # FIXME

    # pack
    field_length = SUAVE.Core.Data()
    field_length.takeoff = TOFL[0]
    field_length.landing = LFL[0]

    results.field_length = field_length
    return results


# ----------------------------------------------------------------------
#   Sideline noise
# ----------------------------------------------------------------------

def noise_sideline(nexus):
    mission = nexus.missions.sideline_takeoff
    nexus.analyses.takeoff.noise.settings.sideline = 1
    nexus.analyses.takeoff.noise.settings.flyover = 0
    results = nexus.results
    # results.sideline = mission.evaluate()
    # SUAVE.Input_Output.SUAVE.archive(results.sideline,'sideline.res')
    results.sideline = SUAVE.Input_Output.SUAVE.load('sideline.res')

    # Determine the x0
    x0 = 0.
    position_vector = results.sideline.conditions.climb.frames.inertial.position_vector
    degree = 3
    coefs = np.polyfit(-position_vector[:, 2], position_vector[:, 0], degree)
    for idx, coef in enumerate(coefs):
        x0 += coef * 304.8 ** (degree - idx)

    nexus.analyses.takeoff.noise.settings.mic_x_position = x0

    noise_segment = results.sideline.segments.climb
    SUAVE.Input_Output.SUAVE.archive(results.sideline, 'sideline.res')
    noise_config = nexus.vehicle_configurations.takeoff
    noise_analyse = nexus.analyses.takeoff
    noise_config.engine_flag = 1

    noise_config.print_output = 0
    noise_config.output_file = 'Noise_Sideline.dat'
    noise_config.output_file_engine = 'Noise_Sideline_Engine.dat'

    if nexus.npoints_sideline_sign == -1:
        noise_result_takeoff_SL = 500. + nexus.missions.sideline_takeoff.segments.climb.state.numerics.number_control_points
    else:
        noise_result_takeoff_SL = compute_noise(noise_config, noise_analyse, noise_segment)

    nexus.summary.noise = Data()
    nexus.summary.noise.sideline = noise_result_takeoff_SL

    return nexus


# ----------------------------------------------------------------------
#   Flyover noise
# ----------------------------------------------------------------------

def noise_flyover(nexus):
    mission = nexus.missions.takeoff
    nexus.analyses.takeoff.noise.settings.flyover = 1
    nexus.analyses.takeoff.noise.settings.sideline = 0
    results = nexus.results
    # results.flyover = mission.evaluate()
    # SUAVE.Input_Output.SUAVE.archive(results.flyover,'flyover.res')
    results.flyover = SUAVE.Input_Output.SUAVE.load('flyover.res')

    noise_segment = results.flyover.segments.climb
    noise_config = nexus.vehicle_configurations.takeoff
    noise_analyse = nexus.analyses.takeoff
    noise_config.engine_flag = 1

    noise_config.print_output = 0
    noise_config.output_file = 'Noise_Flyover_climb.dat'
    noise_config.output_file_engine = 'Noise_Flyover_climb_Engine.dat'

    if nexus.npoints_takeoff_sign == -1:
        noise_result_takeoff_FL_clb = 500. + nexus.missions.sideline_takeoff.segments.climb.state.numerics.number_control_points
    else:
        noise_result_takeoff_FL_clb = compute_noise(noise_config, noise_analyse, noise_segment)

    noise_segment = results.flyover.segments.cutback
    noise_config = nexus.vehicle_configurations.cutback
    noise_config.print_output = 0
    noise_config.engine_flag = 1
    noise_config.output_file = 'Noise_Flyover_cutback.dat'
    noise_config.output_file_engine = 'Noise_Flyover_cutback_Engine.dat'

    if nexus.npoints_takeoff_sign == -1:
        noise_result_takeoff_FL_cutback = 500. + nexus.missions.sideline_takeoff.segments.climb.state.numerics.number_control_points
    else:
        noise_result_takeoff_FL_cutback = compute_noise(noise_config, noise_analyse, noise_segment)

    noise_result_takeoff_FL = 10. * np.log10(
        10 ** (noise_result_takeoff_FL_clb / 10) + 10 ** (noise_result_takeoff_FL_cutback / 10))

    nexus.summary.noise.flyover = noise_result_takeoff_FL

    return nexus


# ----------------------------------------------------------------------
#   Approach noise
# ----------------------------------------------------------------------

def noise_approach(nexus):
    mission = nexus.missions.landing
    nexus.analyses.landing.noise.settings.approach = 1
    results = nexus.results
    # results.approach = mission.evaluate()
    # SUAVE.Input_Output.SUAVE.archive(results.approach,'approach.res')
    results.approach = SUAVE.Input_Output.SUAVE.load('approach.res')

    noise_segment = results.approach.segments.descent
    noise_config = nexus.vehicle_configurations.landing
    noise_analyse = nexus.analyses.landing

    noise_config.print_output = 0
    noise_config.output_file = 'Noise_Approach.dat'
    noise_config.output_file_engine = 'Noise_Approach_Engine.dat'

    noise_config.engine_flag = 1

    noise_result_approach = compute_noise(noise_config, noise_analyse, noise_segment)

    nexus.summary.noise.approach = noise_result_approach

    return nexus


# ----------------------------------------------------------------------
#   NOISE CALCULATION
# ----------------------------------------------------------------------
def compute_noise(config, analyses, noise_segment):
    turbofan = config.propulsors[0]

    outputfile = config.output_file
    outputfile_engine = config.output_file_engine
    print_output = config.print_output
    engine_flag = config.engine_flag  # remove engine noise component from the approach segment

    airframe_noise = noise_airframe_Fink(config, analyses, noise_segment, print_output, outputfile)

    engine_noise = noise_SAE(turbofan, noise_segment, config, analyses, print_output, outputfile_engine)

    noise_sum = 10. * np.log10(10 ** (airframe_noise[0] / 10) + (engine_flag) * 10 ** (engine_noise[0] / 10))

    return noise_sum


# ----------------------------------------------------------------------
#   Design Mission
# ----------------------------------------------------------------------    
def design_mission(nexus):
    mission = nexus.missions.base
    mission.design_range = 7000. * Units['km']
    find_target_range(nexus,mission)

    results = nexus.results
    results.base = mission.evaluate()

    return nexus


# ----------------------------------------------------------------------
#   Sizing
# ----------------------------------------------------------------------    

def simple_sizing(nexus):
    configs = nexus.vehicle_configurations
    base = configs.base

    # find conditions
    air_speed = nexus.missions.base.segments['cruise_2'].air_speed

    altitude = 18.5 * Units.km  # nexus.missions.base.segments['climb_8'].altitude_end #FIXME

    atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()

    freestream = atmosphere.compute_values(altitude)
    freestream0 = atmosphere.compute_values(6000. * Units.ft)  # cabin altitude

    diff_pressure = 0
    fuselage = base.fuselages['fuselage']
    fuselage.differential_pressure = diff_pressure

    # now size engine
    mach_number = air_speed / freestream.speed_of_sound

    # now add to freestream data object
    freestream.velocity = air_speed
    freestream.mach_number = mach_number
    freestream.gravity = 9.81

    conditions = SUAVE.Analyses.Mission.Segments.Conditions.Aerodynamics()  # assign conditions in form for propulsor sizing
    conditions.freestream = freestream
    # conditions.weights.vehicle_mass_rate = -200 * Units['kg/s']


    for config in configs:
        # config.wings.horizontal_stabilizer.areas.reference = (26.0 / 92.0) * config.wings.main_wing.areas.reference

        for wing in config.wings:
            wing = SUAVE.Methods.Geometry.Two_Dimensional.Planform.wing_planform(wing)

            wing.areas.exposed = 0.8 * wing.areas.wetted
            wing.areas.affected = 0.6 * wing.areas.reference

        fuselage = config.fuselages['fuselage']
        fuselage.differential_pressure = diff_pressure

        print config.tag
        # print mach_number, altitude
        # print config.propulsors.turbofan
        turbofan_sizing(config.propulsors['turbofan'], mach_number, altitude)
        compute_turbofan_geometry(config.propulsors['turbofan'], conditions)

        # engine_length, nacelle_diameter, areas.wette
        # diff the new data
        config.store_diff()

    # ------------------------------------------------------------------
    #   Landing Configuration
    # ------------------------------------------------------------------
    landing = nexus.vehicle_configurations.landing
    landing_conditions = Data()
    landing_conditions.freestream = Data()

    # landing weight
    # landing.mass_properties.landing = 0.85 * config.mass_properties.takeoff

    # Landing CL_max
    altitude = nexus.missions.base.segments[-1].altitude_end
    atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    p, T, rho, a, mu = atmosphere.compute_values(altitude)
    landing_conditions.freestream.velocity = nexus.missions.base.segments['descent_final'].air_speed
    landing_conditions.freestream.density = rho
    landing_conditions.freestream.dynamic_viscosity = mu / rho
    CL_max_landing, CDi = compute_max_lift_coeff(landing, landing_conditions)
    landing.maximum_lift_coefficient = CL_max_landing
    # diff the new data
    landing.store_diff()

    # Takeoff CL_max
    takeoff = nexus.vehicle_configurations.takeoff
    takeoff_conditions = Data()
    takeoff_conditions.freestream = Data()
    altitude = nexus.missions.base.airport.altitude
    atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    p, T, rho, a, mu = atmosphere.compute_values(altitude)
    takeoff_conditions.freestream.velocity = nexus.missions.base.segments.climb_1.air_speed
    takeoff_conditions.freestream.density = rho
    takeoff_conditions.freestream.dynamic_viscosity = mu / rho
    max_CL_takeoff, CDi = compute_max_lift_coeff(takeoff, takeoff_conditions)
    takeoff.maximum_lift_coefficient = max_CL_takeoff

    takeoff.store_diff()

    # Base config CL_max
    base = nexus.vehicle_configurations.base
    base_conditions = Data()
    base_conditions.freestream = Data()
    altitude = nexus.missions.base.airport.altitude
    atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    p, T, rho, a, mu = atmosphere.compute_values(altitude)
    base_conditions.freestream.velocity = nexus.missions.base.segments.climb_1.air_speed
    base_conditions.freestream.density = rho
    base_conditions.freestream.dynamic_viscosity = mu / rho
    max_CL_base, CDi = compute_max_lift_coeff(base, base_conditions)
    base.maximum_lift_coefficient = max_CL_base
    base.store_diff()

    # done!

    return nexus


# ----------------------------------------------------------------------
#   Weights
# ----------------------------------------------------------------------    

def weight(nexus):
    vehicle = nexus.vehicle_configurations.base

    # weight analysis
    weights = nexus.analyses.base.weights.evaluate()

    # print "nexus_rest"
    compute_component_centers_of_gravity(vehicle)
    nose_load_fraction = .06
    compute_aircraft_center_of_gravity(vehicle, nose_load_fraction)

    weights = nexus.analyses.cruise.weights.evaluate()
    # print weights # FIXME
    weights = nexus.analyses.landing.weights.evaluate()
    # print weights
    weights = nexus.analyses.takeoff.weights.evaluate()
    #    weights = nexus.analyses.short_field_takeoff.weights.evaluate()

    empty_weight = vehicle.mass_properties.operating_empty

    passenger_weight = 0

    for config in nexus.vehicle_configurations:
        # config.mass_properties.max_zero_fuel                = empty_weight+passenger_weight
        config.mass_properties.zero_fuel_center_of_gravity = vehicle.mass_properties.zero_fuel_center_of_gravity
        config.fuel = vehicle.fuel

    return nexus


# ----------------------------------------------------------------------
#   Finalizing Function (make part of optimization nexus)[needs to come after simple sizing doh]
# ----------------------------------------------------------------------    

def finalize(nexus):
    nexus.analyses.finalize()

    return nexus


# ----------------------------------------------------------------------
#   Post Process Results to give back to the optimizer
# ----------------------------------------------------------------------   

def post_process(nexus):
    # Unpack data
    vehicle = nexus.vehicle_configurations.base
    configs = nexus.vehicle_configurations
    results = nexus.results
    summary = nexus.summary
    missions = nexus.missions

    # pretty_print(results)

    # Static stability calculations
    CMA = -10.
    for segment in results.base.segments.values():
        max_CMA = np.max(segment.conditions.stability.static.cm_alpha[:, 0])
        # lamda with a min/max?
        if max_CMA > CMA:
            CMA = max_CMA

    # Dynamics stability calculations
    dyn_stab = np.zeros(6)
    # j=0
    # for element in results.base.segments.conditions.stability.dynamic.values():
    #
    #     max = np.max(element[:, 0])
    #     min = np.min(element[:, 0])
    #     avg = np.mean(element[:, 0])
    #



    # for derivative in

    # stability data structure:


    # stability
    #     static
    #         cm_alpha
    #         cn_beta
    #
    #
    #     dynamic
    #         cn_r
    #         cl_p
    #         0
    #         cl_beta
    #         0
    #         cm_q
    #         cm_alpha_dot
    #         cz_alpha


    #
    # summary.static_stability = CMA
    #
    results = evaluate_field_length(configs, nexus.analyses, missions.base, results)
    #
    summary.field_length_takeoff = results.field_length.takeoff
    # print summary.field_length_takeoff
    summary.field_length_landing = results.field_length.landing
    # print summary.field_length_landing
    #
    # #
    # pretty_print(nexus)
    # throttle in design mission
    max_throttle = 0
    min_throttle = 0
    for segment in results.base.segments.values():
        max_segment_throttle = np.max(segment.conditions.propulsion.throttle[:, 0])
        min_segment_throttle = np.min(segment.conditions.propulsion.throttle[:, 0])
        if max_segment_throttle > max_throttle:
            max_throttle = max_segment_throttle
        if min_segment_throttle < min_throttle:
            min_throttle = min_segment_throttle

    summary.max_throttle = max_throttle
    summary.min_throttle = min_throttle

    # short_w_n, short_zeta, phugoid_w_n, phugoid_zeta = longitudinal(velocity, density, S_gross_w, mac, Cm_q, Cz_alpha, mass, Cm_alpha, Iy, Cm_alpha_dot, Cz_u, Cz_alpha_dot, Cz_q, Cw, Theta, Cx_u, Cx_alpha):


    # Fuel margin and base fuel calculations

    vehicle.mass_properties.operating_empty += 6e3  # FIXME hardcoded wing mass correction # area scaling?

    operating_empty = vehicle.mass_properties.operating_empty
    payload = vehicle.mass_properties.payload  # TODO fuel margin makes little sense when ejecting aerosol
    design_landing_weight = results.base.segments[-1].conditions.weights.total_mass[-1]
    design_takeoff_weight = vehicle.mass_properties.takeoff
    max_takeoff_weight = nexus.vehicle_configurations.takeoff.mass_properties.max_takeoff
    zero_fuel_weight = payload + operating_empty

    # pretty_print(nexus.vehicle_configurations)
    clmax = 0
    for segment in results.base.segments.values():
        cl = np.max(segment.conditions.aerodynamics.lift_coefficient[:, 0])
        if cl>clmax:
            clmax=cl

    summary.clmax = clmax


    for i in range(1, len(results.base.segments)):  # make fuel burn and sprayer continuous
        # print i
        results.base.segments[i].conditions.weights.fuel_burn[:, 0] += \
            results.base.segments[i - 1].conditions.weights.fuel_burn[-1]


        results.base.segments[i].conditions.weights.spray[:, 0] += \
            results.base.segments[i - 1].conditions.weights.spray[-1]

    summary.op_empty = operating_empty
    summary.max_zero_fuel_margin = (
                                       design_landing_weight - operating_empty) / operating_empty  # used to be (design_landing_weight - zero_fuel_weight) / zero_fuel_weight changed because of aerosol ejection
    summary.base_mission_fuelburn = results.base.segments[-1].conditions.weights.fuel_burn[
        -1]  # esults.base.segments[i].conditions.weights.fuel_burn0#results.base.segments.conditions.weights.fuel_burn                         #design_takeoff_weight - results.base.segments['descent_3'].conditions.weights.total_mass[-1] # - results.base.segments['cruise'].conditions.sprayer_rate
    summary.base_mission_sprayed = results.base.segments[-1].conditions.weights.spray[-1]

    summary.cruise_range = 0  # missions.base.segments.cruise_2.distance # assume we're flying straight
    summary.empty_range = results.base.segments['cruise_outgoing'].conditions.frames.inertial.position_vector[:, 0][
                              -1] / 1000.
    summary.mission_range = results.base.segments['cruise_final'].conditions.frames.inertial.position_vector[:, 0][
                                -1] / 1000.  # Assuming mission ends at cruise altitude
    summary.spray_range = summary.mission_range - summary.empty_range

    summary.total_range = results.base.segments[-1].conditions.frames.inertial.position_vector[:, 0][-1] / 1000.

    summary.main_mission_time = (results.base.segments['descent_final'].conditions.frames.inertial.time[-1] -
                                 results.base.segments[0].conditions.frames.inertial.time[0])
    summary.total_mission_time = (results.base.segments[-1].conditions.frames.inertial.time[-1] -
                                  results.base.segments[0].conditions.frames.inertial.time[0])

    summary.MTOW_delta = zero_fuel_weight + summary.base_mission_fuelburn - vehicle.mass_properties.takeoff

    # summary.power_draw = results.base.segments.

    # summary.engine_weight =

    # print results.base.segments.keys()
    # print summary.engine_weight

    print "zero fuel weight: ", zero_fuel_weight, "kg  i.e. (", payload, "+", operating_empty, ")"
    print "MTOW selected: ", vehicle.mass_properties.takeoff, "kg, MTOW calculated: ", zero_fuel_weight + summary.base_mission_fuelburn
    # FIXME Fuel burn doesn't change when the operating empty weight changes!
    print "Max/Min throttle: ", summary.max_throttle, ", ", summary.min_throttle
    print "Take-off field length: ", summary.field_length_takeoff[0], "m"
    print "Landing field length: ", summary.field_length_landing[0], "m"
    print "Mission Range (must be at least 7000km): ", summary.mission_range, " km"
    print "Non-spraying range (must be at least 3500km): ", summary.empty_range, " km"
    print "Spraying Range (must be at least 3500km): ", summary.spray_range, " km"
    print "Total Range: ", summary.total_range, " km", "(+", summary.total_range - summary.mission_range, ")"
    print "Mission time: ", summary.main_mission_time[0] * Units['s'] / Units.h, "hours (main) +", \
        (summary.total_mission_time - summary.main_mission_time)[0] * Units['s'] / Units.h, "hours (diversion)"
    summary.nothing = 0.0
    print 'Fuel burn: ', summary.base_mission_fuelburn, " Fuel margin: ", summary.max_zero_fuel_margin
    print "CL_max: ", summary.clmax
    # print 'fuel margin=', problem.all_constraints()

    gt_engine = nexus.vehicle_configurations.base.propulsors.turbofan

    # print thrust
    # FIXME move that to printing/results section
    print "Turbofan thrust:", gt_engine.sealevel_static_thrust, " x ", int(
        gt_engine.number_of_engines), "engines (tot: ", gt_engine.sealevel_static_thrust * gt_engine.number_of_engines, " N)"
    print "Thrust required: ", gt_engine.design_thrust, "N"

    print "Estimated engine length: ", gt_engine.engine_length, ", diameter: ", gt_engine.nacelle_diameter, ", wetted area: ", gt_engine.areas.wetted

    # FXI

    print "Aerosol released: ", summary.base_mission_sprayed[0], " kg\n\n"

    # print vehicle.wings.main_wing.chords.root, vehicle.wings.main_wing.spans.projected, vehicle.wings.main_wing.areas.reference

    # print "cruise range: ",problem.summary.cruise_range/1000., " km"


    hf = vehicle.fuselages.fuselage.heights.at_wing_root_quarter_chord
    wf = vehicle.fuselages.fuselage.width
    Lf = vehicle.fuselages.fuselage.lengths.total
    Sw = vehicle.wings.main_wing.areas.reference
    cw = vehicle.wings.main_wing.chords.mean_aerodynamic
    b = vehicle.wings.main_wing.spans.projected
    Sh = vehicle.wings.horizontal_stabilizer.areas.reference
    Sv = vehicle.wings.vertical_stabilizer.areas.reference
    lh = vehicle.wings.horizontal_stabilizer.origin[0] + vehicle.wings.horizontal_stabilizer.aerodynamic_center[0] - \
         vehicle.mass_properties.center_of_gravity[0]
    lv = vehicle.wings.vertical_stabilizer.origin[0] + vehicle.wings.vertical_stabilizer.aerodynamic_center[0] - \
         vehicle.mass_properties.center_of_gravity[0]

    # when you run want to output results to a file
    unscaled_inputs = nexus.optimization_problem.inputs[:, 1]  # use optimization problem inputs here
    input_scaling = nexus.optimization_problem.inputs[:, 3]
    scaled_inputs = unscaled_inputs / input_scaling
    problem_inputs = []

    # SEGMENTS: need to loop it and add all segments
    output_array_segments = np.zeros(4).reshape(4, 1)
    for i in range(1, len(results.base.segments)):
        # print results.base.segments[i].conditions.aerodynamics.lift_coefficient[:, 0]
        # print results.base.segments[i].conditions.aerodynamics.angle_of_attack[:, 0] / Units.deg
        # print results.base.segments[i].conditions.freestream.dynamic_viscosity[:,0]
        # print results.base.segments[i].conditions.freestream.density[:,0]
        output_array_i = np.vstack((results.base.segments[i].conditions.aerodynamics.lift_coefficient[:, 0],
                                    results.base.segments[i].conditions.aerodynamics.angle_of_attack[:, 0] / Units.deg,
                                    results.base.segments[i].conditions.freestream.dynamic_viscosity[:, 0],
                                    results.base.segments[i].conditions.freestream.density[:, 0]))
        output_array_segments = np.hstack((output_array_segments, output_array_i))

    output_segment_indices = ["CL", "alpha", "dynamic_visc", "air_density"]

    # print output_array_segments[segment_output_indexes.index("CL")]

    # print         vehicle.wings.main_wing.areas.wetted + vehicle.wings.horizontal_stabilizer.areas.wetted +\
    #    vehicle.wings.vertical_stabilizer.areas.wetted + vehicle.fuselages.fuselage.areas.wetted

    output_array = np.array([
        vehicle.wings.main_wing.aspect_ratio,
        vehicle.wings.main_wing.areas.reference,
        vehicle.wings.main_wing.sweep,
        vehicle.wings.main_wing.taper,
        vehicle.wings.main_wing.chords.root,
        vehicle.wings.main_wing.spans.projected,
        vehicle.fuselages.fuselage.effective_diameter,
        vehicle.fuselages.fuselage.lengths.total,
        vehicle.wings.main_wing.chords.mean_aerodynamic,
        2. * vehicle.fuselages.fuselage.origin[1],

        configs.takeoff.maximum_lift_coefficient,
        configs.landing.maximum_lift_coefficient,
        vehicle.maximum_lift_coefficient,
        missions.base.segments['descent_final'].air_speed,
        missions.base.segments['cruise_1'].air_speed,

        gt_engine.number_of_engines,
        gt_engine.mass_properties.mass / gt_engine.number_of_engines,  # PER ENGINE
        gt_engine.mass_properties.mass / 1.6 / gt_engine.number_of_engines,  # PER ENGINE DRY WEIGHT
        gt_engine.nacelle_diameter,

        summary.base_mission_fuelburn,
        zero_fuel_weight + summary.base_mission_fuelburn,
        operating_empty,
        design_landing_weight,
        vehicle.weight_breakdown.wing,
        vehicle.weight_breakdown.fuselage,
        vehicle.weight_breakdown.landing_gear,
        payload,

        820.,  # Fuel density

        vehicle.wings.horizontal_stabilizer.sweep,
        vehicle.wings.horizontal_stabilizer.spans.projected,
        vehicle.wings.horizontal_stabilizer.chords.root,

        vehicle.wings.vertical_stabilizer.sweep,
        vehicle.wings.vertical_stabilizer.taper,
        vehicle.wings.vertical_stabilizer.chords.root,

        vehicle.wings.main_wing.areas.wetted + vehicle.wings.horizontal_stabilizer.areas.wetted + \
        vehicle.wings.vertical_stabilizer.areas.wetted + vehicle.fuselages.fuselage.areas.wetted

        # Oswald
        # Wetted area

        # QUESTIONABLE: CL_alpha, CM_alpha, Lift distribution, CM_delta, CL_delta
    ])

    output_indices = ["A",
                      "S",
                      "sweep",
                      "taper",
                      "c_r",
                      "b",
                      "d_fus",
                      "l_fus",
                      "c_mac",
                      "y_fuselages",
                      "CL_max_TO",
                      "CL_max_landing",
                      "CL_max_clean",
                      "v_landing",
                      "v_cr",
                      "N_engines",
                      "m_engine_wet",
                      "m_engine_dry",
                      "d_engine",
                      "m_fuel",
                      "MTOW",
                      "OEW",
                      "m_landing",
                      "m_wing",
                      "m_fus",
                      "m_landing_gear",
                      "m_payload",
                      "rho_fuel",
                      "sweep_h",
                      "b_h",
                      "c_r_h",
                      "sweep_v",
                      "taper_v",
                      "c_r_v",
                      "S_wet"
                      ]
    fuel_burn_sec = np.zeros(1)
    for i in range(1, len(results.base.segments)):
        fuel_burn_sec = np.hstack((fuel_burn_sec,results.base.segments[i - 1].conditions.weights.fuel_burn[-1]))

    wing_loading = (operating_empty + summary.base_mission_fuelburn - fuel_burn_sec)*9.81/vehicle.wings.main_wing.areas.reference
    # print wing_loading
    # print output_array[output_indexes.index("c_r_v")]
    # print output_array[-1]

    # print vehicle.weight_breakdown
    np.save(output_folder + "wing_loading.npy", wing_loading)
    np.save(output_folder + "output_array.npy", output_array)
    np.save(output_folder + "output_indices.npy", output_indices)
    np.save(output_folder + "output_array_segments.npy", output_array_segments)
    np.save(output_folder + "output_segment_indices.npy", output_segment_indices)

    for value in unscaled_inputs:
        problem_inputs.append(value)

    file_out = open(output_folder + 'results.txt', 'ab')

    file_out.write('fuel weight = ')
    file_out.write(str(summary.base_mission_fuelburn))

    file_out.write(', inputs = ')
    file_out.write(str(problem_inputs))

    file_out.write('\n')
    file_out.close()

    print_weight_breakdown(nexus.vehicle_configurations.base, filename=output_folder + 'weight_breakdown.dat')
    #
    # # print engine data into file
    print_engine_data(nexus.vehicle_configurations.base, filename=output_folder + 'engine_data.dat')
    #
    # # print parasite drag data into file
    # # define reference condition for parasite drag
    ref_condition = Data()
    ref_condition.mach_number = 0.7  # FIXME
    ref_condition.reynolds_number = 7e6  # FIXME
    Analyses = Data()
    Analyses.configs = nexus.analyses

    print_parasite_drag(ref_condition, nexus.vehicle_configurations.cruise, Analyses,
                        filename=output_folder + 'parasite_drag.dat')
    #
    # print compressibility drag data into file

    # print Analyses
    print_compress_drag(nexus.vehicle_configurations.cruise, Analyses, filename=output_folder + 'compress_drag.dat')

    # print mission breakdown
    print_mission_breakdown(nexus.results.base,
                            filename=output_folder + 'mission_breakdown.dat')  # FIXME fuel weight adds aerosol = wrong!!!!!

    return nexus
