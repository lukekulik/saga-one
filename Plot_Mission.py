# Plot_Mission.py
# 
# Created:  May 2015, E. Botero
# Modified: 

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    

import SUAVE
from SUAVE.Core import Units

import pylab as plt

# ----------------------------------------------------------------------
#   Plot Mission
# ----------------------------------------------------------------------

def plot_mission(results,line_style='bo-'):
    
    axis_font = {'fontname':'Arial', 'size':'14'}    
    folder = "/Users/lkulik/Dropbox/Shared/DSE Conceptual Design/graphs/"
    file_format = ".jpg"

    # ------------------------------------------------------------------
    #   Aerodynamics 
    # ------------------------------------------------------------------
    fig = plt.figure("Aerodynamic Coefficients",figsize=(8,10))
    for segment in results.base.segments.values():

        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        CLift  = segment.conditions.aerodynamics.lift_coefficient[:,0]
        CDrag  = segment.conditions.aerodynamics.drag_coefficient[:,0]
        # segment.conditions.freestream.velocity
        Drag   = -segment.conditions.frames.wind.drag_force_vector[:,0]
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0]
        Position = segment.conditions.frames.inertial.position_vector[:,0]
        aoa = segment.conditions.aerodynamics.angle_of_attack[:,0] / Units.deg
        l_d = CLift/CDrag


        axes = fig.add_subplot(4,1,1)
        axes.plot( time , CLift , line_style )
        axes.set_ylabel('Lift Coefficient',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(4,1,2)
        axes.plot( time , l_d , line_style )
        axes.set_ylabel('L/D',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(4,1,3)
        axes.plot( time , Thrust , line_style )
        axes.set_ylabel('Thrust [N]',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(4,1,4)
        axes.plot( time , aoa , 'ro-' )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('AOA (deg)',axis_font)
        axes.grid(True)

    plt.savefig(folder+"fig1"+file_format)

    # ------------------------------------------------------------------
    #   Aerodynamics 2
    # ------------------------------------------------------------------
    fig = plt.figure("Drag Components",figsize=(8,10))
    axes = plt.gca()
    for i, segment in enumerate(results.base.segments.values()):

        # print segment.conditions.aerodynamics.drag_breakdown.parasite['fuselage']

        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        drag_breakdown = segment.conditions.aerodynamics.drag_breakdown
        cdp = drag_breakdown.parasite.total[:,0]
        cdi = drag_breakdown.induced.total[:,0]
        cdc = drag_breakdown.compressible.total[:,0]
        cdm = drag_breakdown.miscellaneous.total[:,0]
        cd  = drag_breakdown.total[:,0]

        if line_style == 'bo-':
            axes.plot( time , cdp , 'ko-', label='CD parasite' )
            axes.plot( time , cdi , 'bo-', label='CD induced' )
            axes.plot( time , cdc , 'go-', label='CD compressibility' )
            axes.plot( time , cdm , 'yo-', label='CD miscellaneous' )
            axes.plot( time , cd  , 'ro-', label='CD total'   )
            if i == 0:
                axes.legend(loc='upper center')            
        else:
            axes.plot( time , cdp , line_style )
            axes.plot( time , cdi , line_style )
            axes.plot( time , cdc , line_style )
            axes.plot( time , cdm , line_style )
            axes.plot( time , cd  , line_style )            

    axes.set_xlabel('Time (min)')
    axes.set_ylabel('CD')
    axes.grid(True)

    plt.savefig(folder+"fig2"+file_format)

    # ------------------------------------------------------------------
    #   Altitude, vehicle weight
    # ------------------------------------------------------------------

    fig = plt.figure("Altitude, Weight",figsize=(8,10))
    for segment in results.base.segments.values():

        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        CLift  = segment.conditions.aerodynamics.lift_coefficient[:,0]
        CDrag  = segment.conditions.aerodynamics.drag_coefficient[:,0]
        Drag   = -segment.conditions.frames.wind.drag_force_vector[:,0]
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0]
        aoa    = segment.conditions.aerodynamics.angle_of_attack[:,0] / Units.deg
        l_d    = CLift/CDrag
        mass   = segment.conditions.weights.total_mass[:,0]
        altitude = segment.conditions.freestream.altitude[:,0]
        mdot   = segment.conditions.weights.vehicle_mass_rate[:,0]

        # spray_rate = segment.sprayer_rate
        thrust =  segment.conditions.frames.body.thrust_force_vector[:,0]
        sfc    = mdot  / thrust

        # if segment.conditions.

        fuel_burn = segment.conditions.weights.fuel_burn[:,0]
        sprayed_weight = segment.conditions.weights.spray[:,0]




        axes = fig.add_subplot(3,1,1)
        axes.plot( time , altitude , line_style )
        axes.set_ylabel('Altitude (m)',axis_font)
        axes.grid(True)

 

        axes = fig.add_subplot(3,1,2)
        axes.plot( time , mass , 'ro-' )
        axes.plot( time , fuel_burn , line_style )
        axes.plot( time , sprayed_weight , 'go-' )
        axes.set_ylabel('Weight (kg)',axis_font)
        axes.grid(True)



        axes = fig.add_subplot(3,1,3)
        axes.plot( time , sfc , line_style )
        axes.set_ylabel('Specific fuel consumption (N/Ns)',axis_font)
        axes.grid(True)
        
        axes.set_xlabel('Time (min)')
    plt.savefig(folder+"fig3"+file_format)

    fig = plt.figure("Misc",figsize=(8,10))
    for segment in results.base.segments.values():

        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        eta  = segment.conditions.propulsion.throttle[:,0]
        mach = segment.conditions.freestream.mach_number[:,0]
        mdot   = segment.conditions.weights.vehicle_mass_rate[:,0]
        velocity  = segment.conditions.freestream.velocity[:,0]
        Drag   = -segment.conditions.frames.wind.drag_force_vector[:,0]
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0]
        spray_rate=segment.conditions.weights.sprayer[:,0]

        axes = fig.add_subplot(5,1,1)
        axes.plot( time , eta , line_style )
        axes.set_ylabel('Throttle (%)',axis_font)
        axes.grid(True)



        axes = fig.add_subplot(5,1,2)
        axes.plot( time , mach , 'ro-' )
        axes.set_ylabel('Mach (-)',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(5,1,3)
        axes.plot( time , velocity , 'ro-' )
        axes.set_ylabel('Velocity (m/s)',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(5,1,4)
        axes.plot( time , mdot , line_style )
        axes.plot( time , spray_rate , 'go-' )
        axes.set_ylabel('Mass rate (kg/s)',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(5,1,5)
        axes.plot( time , Drag   , line_style )
        axes.plot( time , Thrust , 'ro-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Drag and Thrust (N)')
        axes.grid(True)

        axes.set_xlabel('Time (min)')

    plt.savefig(folder+"fig4"+file_format)


    # aerosol disperion rate plot

    # plt.show()


    return

if __name__ == '__main__': 
    main()    
    plt.show()