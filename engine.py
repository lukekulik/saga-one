import SUAVE
from Turbofan_thr import Turbofan
import Turbine_saga
from SUAVE.Methods.Propulsion.turbofan_sizing import turbofan_sizing
from SUAVE.Methods.Geometry.Two_Dimensional.Cross_Section.Propulsion import compute_turbofan_geometry
from Generator import Generator
from Jet_JP7 import Jet_JP7

def engine_caluclations(altitude, bypass, mach_number, num_engine, thrust_total):
    # initialize the gas turbine network

    gt_engine = Turbofan()
    gt_engine.tag = 'turbofan'
    gt_engine.number_of_engines = num_engine
    gt_engine.bypass_ratio = bypass
    # gt_engine.engine_length = 5.2
    gt_engine.nacelle_diameter = 3.5

    # set the working fluid for the network
    working_fluid = SUAVE.Attributes.Gases.Air

    # add working fluid to the network
    gt_engine.working_fluid = working_fluid

    # Component 1 : ram,  to convert freestream static to stagnation quantities
    ram = SUAVE.Components.Energy.Converters.Ram()
    ram.tag = 'ram'
    # add ram to the network
    gt_engine.ram = ram

    # Component 2 : inlet nozzle
    inlet_nozzle = SUAVE.Components.Energy.Converters.Compression_Nozzle()
    inlet_nozzle.tag = 'inlet nozzle'
    inlet_nozzle.polytropic_efficiency = 0.98
    inlet_nozzle.pressure_ratio = 0.98  # turbofan.fan_nozzle_pressure_ratio     = 0.98     #0.98
    # add inlet nozzle to the network
    gt_engine.inlet_nozzle = inlet_nozzle

    # Component 3 :low pressure compressor
    low_pressure_compressor = SUAVE.Components.Energy.Converters.Compressor()
    low_pressure_compressor.tag = 'lpc'
    low_pressure_compressor.polytropic_efficiency = 0.90
    low_pressure_compressor.pressure_ratio = 1.5
    # add low pressure compressor to the network
    gt_engine.low_pressure_compressor = low_pressure_compressor

    # Component 4 :high pressure compressor
    high_pressure_compressor = SUAVE.Components.Energy.Converters.Compressor()
    high_pressure_compressor.tag = 'hpc'
    high_pressure_compressor.polytropic_efficiency = 0.90  # FIXME
    high_pressure_compressor.pressure_ratio = 14
    # add the high pressure compressor to the network
    gt_engine.high_pressure_compressor = high_pressure_compressor

    # Component 5 :low pressure turbine
    low_pressure_turbine = Turbine_saga.Turbine()
    low_pressure_turbine.tag = 'lpt'
    low_pressure_turbine.mechanical_efficiency = 0.99
    low_pressure_turbine.polytropic_efficiency = 0.89
    # add low pressure turbine to the network
    gt_engine.low_pressure_turbine = low_pressure_turbine

    # Component 5 :high pressure turbine
    high_pressure_turbine = Turbine_saga.Turbine()
    high_pressure_turbine.tag = 'hpt'
    high_pressure_turbine.mechanical_efficiency = 0.99
    high_pressure_turbine.polytropic_efficiency = 0.89
    # add the high pressure turbine to the network
    gt_engine.high_pressure_turbine = high_pressure_turbine

    # Component 6 :combustor
    combustor = SUAVE.Components.Energy.Converters.Combustor()
    combustor.tag = 'Comb'
    combustor.efficiency = 0.995
    combustor.alphac = 1.0
    combustor.turbine_inlet_temperature = 1450
    combustor.pressure_ratio = 0.96
    combustor.fuel_data = Jet_JP7()
    # combustor.fuel_data = SUAVE.Attributes.Propellants.Jet_A()
    # add the combustor to the network
    gt_engine.combustor = combustor

    # Component 7 :core nozzle
    core_nozzle = SUAVE.Components.Energy.Converters.Expansion_Nozzle()
    core_nozzle.tag = 'core nozzle'
    core_nozzle.polytropic_efficiency = 0.95
    core_nozzle.pressure_ratio = 0.99
    # add the core nozzle to the network
    gt_engine.core_nozzle = core_nozzle

    # Component 8 :fan nozzle
    fan_nozzle = SUAVE.Components.Energy.Converters.Expansion_Nozzle()
    fan_nozzle.tag = 'fan nozzle'
    fan_nozzle.polytropic_efficiency = 0.95
    fan_nozzle.pressure_ratio = 0.99
    # add the fan nozzle to the network
    gt_engine.fan_nozzle = fan_nozzle

    # Component 9 : fan
    fan = SUAVE.Components.Energy.Converters.Fan()
    fan.tag = 'fan'
    fan.polytropic_efficiency = 0.89
    fan.pressure_ratio = 1.5
    # add the fan to the network
    gt_engine.fan = fan

    # Component 10 : Payload power draw

    generator = Generator()
    generator.tag = 'generator'
    generator.power_draw = 1 / gt_engine.number_of_engines
    gt_engine.generator = generator

    # Define OPR
    OPR = fan.pressure_ratio * high_pressure_compressor.pressure_ratio * low_pressure_compressor.pressure_ratio

    # Component 10 : thrust (to compute the thrust)
    thrust = SUAVE.Components.Energy.Processes.Thrust()

    thrust.tag = 'compute_thrust'
    # total design thrust (includes all the engines)
    thrust.total_design = thrust_total  # should be just a pointer not a number
    # add thrust to the network
    gt_engine.thrust = thrust
    gt_engine.OPR = OPR
    # print thrust
    # size the turbofan
    turbofan_sizing(gt_engine, mach_number, altitude)

    compute_turbofan_geometry(gt_engine, None)

    return gt_engine
