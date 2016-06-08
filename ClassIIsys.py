def classIIsys(Nen,W_eng,V_fuel,V_tanks,N_tanks, Iy_SI,S_cstot,L_fus,l_nose,b,c_root,l_pylon,l_eng,OEW,Vmax):
    '----------Raymer and Roskam Stuff---------------------'
    Wen = W_eng/0.45359237 #lb
    Vt = V_fuel*264.172052#gallons
    Vi = V_fuel*2 #lbs
    Vp = 0. #this is for self-sealing fuel tanks
    Nt = 6. #number of tanks
    Iy = Iy_SI/(0.45359237*0.3048**2) #lbs ft^2
    Scs = S_cstot/0.3048**2 #ft^2 - total control surface area
    Nf = 5. # number of functions performed by the controls (range of  4-7)
    Nm = 1. #number of mechanical functions performed by controls (range 0-2)
    Lf = L_fus/0.3048 #ft
    Bw = b/0.3048 #ft
    Rkva = 2000. # system electical rating [kVA] --> coming form Iris
    Ngen = Nen+1.
    La = 0.15*b/0.3048
    Vp = 0. #this is for self-sealing fuel tanks
    Nt = 6. #number of tanks


    '---------System weights------------------'
    W_starter = 49.19*(Nen*Wen/1000)**0.541 *0.45359237 #kg
    #cg_starter = -(l_pylon-0.5*l_eng)
    W_fuelsys = 2.405* Vt**0.606* (1+Vi/Vt)**-1* (1+ Vp/Vt)* Nt**0.5 *0.45359237 #kg
    #cg_fuelsys = 0.5*c_root #ADJUST!
    W_fc = 145.9* Nf**0.554* (1+Nm/Nf)**-1* Scs**0.2* (Iy*10**-6)**0.07 *0.45359237 #kg
    #cg_fc = 0.85*c_root
    W_hyd = 0.2673* Nf* (Lf + Bw)**0.937*0.45359237 #kg
    #cg_hyd = 0.5*c_root
    W_el = 7.291*Rkva**0.782* La**0.346* Ngen**0.1*0.45359237 #kg
    #cg_el = 0.2*c_root
    W_ecs = 0.018*OEW # from Torenbeek Try to find relation from ROSKAM 1990 or later!!
    #cg_ecs = 0.3*c_root
    W_comms = 200 #kg - Assumption. After looking into the system, make a revision of this
    #cg_comms = -0.85*l_nose

    '''---------------Avionics------------------'''
    W_autopilot = 11*5*0.45359237*1.5*1*0.4 #kg
    W_ins = 2*5*0.45359237*1.5*2*0.1*3 #kg
    W_gps = 0.5*5*1.5*2*1 #kg - unit weight*redundancy factor*adjustment_weights
    W_processors = 600 #kg - assumption
    W_cameras = 4*2*0.5* (4*0.5 + 4*1) *0.45359237 #kg --> firrst three values are weights based on rugedness, performance, minituarisation
    W_recorders = 100*0.45359237#kg - assumption (this is for 200GB of recorder)
    W_atc = (3*(2.1+2*0.4) + 2*2.06)*0.45359237 #kg for transponders and radios
    W_ads = 1.2*(Vmax/0.5144444)*0.05*1.2*0.6*1.2*0.45359237 #kg Air Data System
    W_avionics = W_autopilot + W_ins + W_gps + W_processors + W_cameras + W_recorders + W_atc + W_ads
    #cg_avionics = -0.5*l_nose

    W_sys = W_starter + W_fuelsys + W_hyd + W_el + W_ecs + W_comms + W_avionics
    #cg_sys = (cg_starter*W_starter + cg_fuelsys*W_fuelsys + cg_hyd*W_hyd + cg_el*W_el + cg_ecs*W_ecs + cg_comms*W_comms + cg_avionics*W_avionics)/W_sys
    return W_starter, W_fuelsys, W_fc, W_hyd, W_el, W_ecs,W_comms,W_avionics,W_sys

def propgroup(Nen,W_eng,d_eng,l_eng,W_fuelsys):
    d_nacelle = 1.15*d_eng
    Ktr = 1.18 #If no thrust reversers --> Ktr = 1
    Wec = (W_eng/0.45359237)**0.901*Ktr #lb
    Nw = d_nacelle/0.3048 #ft - nacelle width
    Nlt = (0.7*l_eng)/0.3048 #ft - nacelle length
    #l_nacelle = Nlt*0.3048 #m - nacelle length
    Sn = np.pi*Nw*Nlt-2*np.pi/4*Nw**2 #ft**
    W_nacelle = 0.6724* Kng* Nlt**0.1* Nw**0.294* Nz**0.119* Wec**0.611* Nen**0.984* Sn**0.224 *0.45359237 #kg
    #cg_nacelle = -0.45*(l_pylon+0.4*l_nacelle) # the minus sign is because the nacelle is in front of the LE
    #cg_eng = -(l_pylon-0.5*l_eng) #same as for the nacelle
    W_propulsion = W_eng*Nen + W_nacelle + W_fuelsys
    return W_nacelle, W_propulsion
