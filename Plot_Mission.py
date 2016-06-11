# Plot_Mission.py
# 
# Created:  May 2015, E. Botero
# Modified: 

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    

import SUAVE
from SUAVE.Core import Units, Data
import numpy as np
import pylab as plt


# ----------------------------------------------------------------------
#   Plot Mission
# ----------------------------------------------------------------------

def plot_mission(results, show=True, line_style='bo-'):
    axis_font = {'fontname': 'Arial', 'size': '14'}
    folder = "output/graphs/"
    file_format = ".png"

    # ------------------------------------------------------------------
    #   Aerodynamics 
    # ------------------------------------------------------------------
    fig = plt.figure("Aerodynamic Coefficients", figsize=(8, 10))
    for segment in results.base.segments.values():
        time = segment.conditions.frames.inertial.time[:, 0] / Units.min
        CLift = segment.conditions.aerodynamics.lift_coefficient[:, 0]

        cl_inviscid = segment.conditions.aerodynamics.lift_breakdown.inviscid_wings_lift[:, 0]
        cl_compressible = segment.conditions.aerodynamics.lift_breakdown.compressible_wings[:, 0]

        CDrag = segment.conditions.aerodynamics.drag_coefficient[:, 0]
        # segment.conditions.freestream.velocity
        eta = segment.conditions.propulsion.throttle[:, 0]
        Drag = -segment.conditions.frames.wind.drag_force_vector[:, 0]

        # print segment.conditions.aerodynamics.lift_breakdown.keys() # ['inviscid_wings_lift', 'compressible_wings']
        # print segment.conditions.lift_curve_slope
        # print segment.conditions.frames.wind.lift_force_vector[:,0] #keys() # ['inertial', 'body', 'wind', 'planet']


        Thrust = segment.conditions.frames.body.thrust_force_vector[:, 0]
        Position = segment.conditions.frames.inertial.position_vector[:,
                   0]  # ['position_vector', 'velocity_vector', 'acceleration_vector', 'gravity_force_vector', 'total_force_vector', 'time']

        # print segment.conditions.frames.inertial.velocity_vector.keys()
        # print segment.conditions.frames.inertial.gravity_force_vector.keys()

        aoa = segment.conditions.aerodynamics.angle_of_attack[:, 0] / Units.deg
        body_angle = segment.unknowns.body_angle[:, 0] / Units.deg

        # vel segment.conditions.frames.wind.velocity_vector.keys()
        # print segment.conditions.frames.wind.lift_vector.keys()

        l_d = CLift / CDrag

        axes = fig.add_subplot(4, 1, 1)
        axes.plot(time, CLift, line_style)
        # axes.plot(time,cl_inviscid,'ro-')
        # axes.plot(time, cl_compressible, 'ro-')

        axes.set_ylabel('Lift Coefficient', axis_font)
        axes.grid(True)

        axes = fig.add_subplot(4, 1, 2)
        axes.plot(time, l_d, line_style)
        axes.set_ylabel('L/D', axis_font)
        axes.grid(True)

        axes = fig.add_subplot(4, 1, 3)
        axes.plot(time, eta, line_style)
        axes.set_ylabel('Throttle (%)', axis_font)
        axes.grid(True)

        axes = fig.add_subplot(4, 1, 4)
        axes.plot(time, aoa, line_style)
        axes.plot(time, body_angle, 'ro-')
        axes.set_xlabel('Time (min)', axis_font)
        axes.set_ylabel('AOA + body angle (deg)', axis_font)
        axes.grid(True)

    plt.savefig(folder + "fig1" + file_format, bbox_inches='tight')

    # ------------------------------------------------------------------
    #   Aerodynamics 2
    # ------------------------------------------------------------------
    fig = plt.figure("Drag Components", figsize=(8, 10))
    axes = plt.gca()
    for i, segment in enumerate(results.base.segments.values()):

        # print segment.conditions.aerodynamics.drag_breakdown.parasite['fuselage']

        time = segment.conditions.frames.inertial.time[:, 0] / Units.min
        drag_breakdown = segment.conditions.aerodynamics.drag_breakdown
        cdp = drag_breakdown.parasite.total[:, 0]
        cdi = drag_breakdown.induced.total[:, 0]
        cdc = drag_breakdown.compressible.total[:, 0]
        cdm = drag_breakdown.miscellaneous.total[:, 0]
        cd = drag_breakdown.total[:, 0]

        if line_style == 'bo-':
            axes.plot(time, cdp, 'ko-', label='CD parasite')
            axes.plot(time, cdi, 'bo-', label='CD induced')
            axes.plot(time, cdc, 'go-', label='CD compressibility')
            # axes.plot(time, cdm, 'yo-', label='CD miscellaneous')
            axes.plot(time, cd, 'ro-', label='CD total')
            if i == 0:
                axes.legend(loc='upper left')
        else:
            axes.plot(time, cdp, line_style)
            axes.plot(time, cdi, line_style)
            axes.plot(time, cdc, line_style)
            # axes.plot(time, cdm, line_style)
            axes.plot(time, cd, line_style)

    axes.set_xlabel('Time (min)')
    axes.set_ylabel('$C_D$')
    axes.grid(True)

    plt.savefig(folder + "fig2" + file_format, bbox_inches='tight')

    # ------------------------------------------------------------------
    #   Altitude, vehicle weight
    # ------------------------------------------------------------------

    fig = plt.figure("Altitude, Weight", figsize=(8, 10))
    i=0
    for i, segment in enumerate(results.base.segments.values()):
        time = segment.conditions.frames.inertial.time[:, 0] / Units.min
        CLift = segment.conditions.aerodynamics.lift_coefficient[:, 0]
        CDrag = segment.conditions.aerodynamics.drag_coefficient[:, 0]
        Drag = -segment.conditions.frames.wind.drag_force_vector[:, 0]
        Thrust = segment.conditions.frames.body.thrust_force_vector[:, 0]
        aoa = segment.conditions.aerodynamics.angle_of_attack[:, 0] / Units.deg
        l_d = CLift / CDrag
        mass = segment.conditions.weights.total_mass[:, 0]
        altitude = segment.conditions.freestream.altitude[:, 0]
        mdot = segment.conditions.weights.vehicle_mass_rate[:, 0]

        # spray_rate = segment.sprayer_rate
        thrust = segment.conditions.frames.body.thrust_force_vector[:, 0]
        sfc = mdot / thrust

        # if segment.conditions.

        fuel_burn = segment.conditions.weights.fuel_burn[:, 0]
        sprayed_weight = segment.conditions.weights.spray[:, 0]

        axes = fig.add_subplot(3, 1, 1)
        axes.plot(time, altitude, line_style)
        axes.set_ylabel('Altitude (m)', axis_font)
        axes.grid(True)

        axes = fig.add_subplot(3, 1, 2)
        axes.plot(time, mass, 'ro-', label='Aircraft mass')
        axes.plot(time, fuel_burn, line_style, label='Fuel burn')
        axes.plot(time, sprayed_weight, 'go-', label='Aerosol released')
        axes.set_ylabel('Weight (kg)', axis_font)
        axes.grid(True)
        if i==0:
            legend = axes.legend(loc='upper right', shadow=False)

        axes = fig.add_subplot(3, 1, 3)
        axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        axes.plot(time, sfc, line_style)
        axes.set_ylabel('Specific fuel consumption (kg/Ns)', axis_font)
        axes.grid(True)

        axes.set_xlabel('Time (min)')

    plt.savefig(folder + "fig3" + file_format, bbox_inches='tight')

    fig = plt.figure("Misc", figsize=(8, 10))
    for segment in results.base.segments.values():
        time = segment.conditions.frames.inertial.time[:, 0] / Units.min

        mach = segment.conditions.freestream.mach_number[:, 0]
        mdot = segment.conditions.weights.vehicle_mass_rate[:, 0]
        velocity = segment.conditions.freestream.velocity[:, 0]
        Drag = -segment.conditions.frames.wind.drag_force_vector[:, 0]
        Thrust = segment.conditions.frames.body.thrust_force_vector[:, 0]

        # print Thrust
        spray_rate = segment.conditions.weights.sprayer[:, 0]
        spray_rate_meter = segment.conditions.weights.sprayer[:, 0] / velocity

        # axes = fig.add_subplot(5, 1, 1)
        # axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        # axes.plot(time, Thrust, line_style)
        # axes.set_ylabel('Thrust [N]', axis_font)
        # axes.grid(True)

        axes = fig.add_subplot(5, 1, 1)
        axes.plot(time, mach, line_style)
        axes.set_ylabel('Mach (-)', axis_font)
        axes.grid(True)

        axes = fig.add_subplot(5, 1, 2)
        axes.plot(time, velocity, line_style)
        axes.set_ylabel('Velocity (m/s)', axis_font)
        axes.grid(True)

        axes = fig.add_subplot(5, 1, 3)
        axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        axes.plot(time, Drag, line_style)
        axes.plot(time, Thrust, 'ro-')
        # axes.plot(time, Lift, 'ro-')
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Drag and Thrust (N)')
        axes.grid(True)

        axes = fig.add_subplot(5, 1, 4)
        axes.plot(time, mdot, line_style)
        axes.plot(time, spray_rate, 'go-')
        axes.set_ylabel('Mass rate (kg/s)', axis_font)
        axes.grid(True)

        axes = fig.add_subplot(5, 1, 5)
        axes.plot(time, spray_rate_meter, 'go-')
        axes.set_ylabel('Mass rate (kg/m)', axis_font)
        axes.grid(True)

        axes.set_xlabel('Time (min)')

    plt.savefig(folder + "fig4" + file_format, bbox_inches='tight')

    fig = plt.figure("Velocities and accelerations", figsize=(8, 10))
    for segment in results.base.segments.values():
        time = segment.conditions.frames.inertial.time[:, 0] / Units.min

        acc_x = segment.conditions.frames.inertial.acceleration_vector[:, 0]
        acc_y = segment.conditions.frames.inertial.acceleration_vector[:, 1]
        acc_z = segment.conditions.frames.inertial.acceleration_vector[:, 2]

        # segment.conditions.frames.inertial

        vel_x = segment.conditions.frames.inertial.velocity_vector[:, 0]
        vel_y = segment.conditions.frames.inertial.velocity_vector[:, 1]  # airspeed is very different (earth is moving)
        vel_z = segment.conditions.frames.inertial.velocity_vector[:, 2]

        f_x = segment.conditions.frames.inertial.gravity_force_vector[:, 0]
        f_y = segment.conditions.frames.inertial.gravity_force_vector[:, 1]
        f_z = segment.conditions.frames.inertial.gravity_force_vector[:, 2]

        temp = segment.conditions.freestream.temperature[:, 0]

        # engine_power =  segment.conditions.energies.propulsion_power[:,0]

        net_acceleration = (f_x ** 2 + f_y ** 2 + f_z ** 2) ** (1. / 3.)

        Lift = -segment.conditions.frames.wind.lift_force_vector[:, 2]

        power = segment.conditions.output_power

        # power = segment.conditions.weights.out[:, 0]
        # print segment


        # axes = fig.add_subplot(5, 1, 1)
        # axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        # axes.plot(time, Thrust, line_style)
        # axes.set_ylabel('Thrust [N]', axis_font)
        # axes.grid(True)

        axes = fig.add_subplot(5, 1, 1)
        axes.plot(time, acc_x, line_style)
        # axes.plot(time, acc_y, line_style)
        # axes.plot(time, acc_z, line_style)
        # axes.plot(time,cl_inviscid,'ro-')
        # axes.plot(time, cl_compressible, 'ro-')

        axes.set_ylabel('Accelerations', axis_font)
        axes.grid(True)

        axes = fig.add_subplot(5, 1, 2)
        # axes.plot(time, acc_x, line_style)
        # axes.plot(time, acc_y, line_style)
        axes.plot(time, -vel_z, line_style)
        # axes.plot(time,cl_inviscid,'ro-')
        # axes.plot(time, cl_compressible, 'ro-')

        axes.set_ylabel('Climb rate ($-v_z$)', axis_font)
        axes.grid(True)

        axes = fig.add_subplot(5, 1, 3)
        axes.plot(time, Lift, line_style)
        axes.plot(time, net_acceleration, 'ro-')
        # axes.plot(time, acc_y, line_style)
        # axes.plot(time, -vel_z, line_style)
        # axes.plot(time,cl_inviscid,'ro-')
        # axes.plot(time, cl_compressible, 'ro-')

        axes.set_ylabel('(net?) Force vector / Lift [N]', axis_font)
        axes.grid(True)

        axes = fig.add_subplot(5, 1, 4)
        axes.plot(time, temp, line_style)
        # axes.plot(time, acc_y, line_style)
        # axes.plot(time, -vel_z, line_style)
        # axes.plot(time,cl_inviscid,'ro-')
        # axes.plot(time, cl_compressible, 'ro-')

        axes.set_ylabel('Temperature (K)', axis_font)
        axes.grid(True)

        axes = fig.add_subplot(5, 1, 5)
        axes.plot(time, power, line_style)
        # axes.plot(time, acc_y, line_style)
        # axes.plot(time, -vel_z, line_style)
        # axes.plot(time,cl_inviscid,'ro-')
        # axes.plot(time, cl_compressible, 'ro-')


        axes.set_ylabel('Engine Power (W)', axis_font)
        axes.grid(True)

        # print segment.conditions.freestream.keys()

        # positions?

        axes.set_xlabel('Time (min)')

    plt.savefig(folder + "fig5" + file_format, bbox_inches='tight')

    # aerosol disperion rate plot

    if show:
        plt.show()

    # pretty_print(segment) # print all the values in the dictionary
    # print segment.conditions.weights.weight_breakdown
    # print segment.conditions.energies.total_efficiency

    # print segment.conditions.freestream.gravity
    # print segment.conditions.freestream.reynolds_number


    return


if __name__ == '__main__':
    main()
    plt.show()
