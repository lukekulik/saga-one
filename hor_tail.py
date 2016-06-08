def hor_tail(c_hor,taper_h,lh,Sel,Sh,Ah,Bhor,sweep_ht,MTOW,Nz):
    Kuht = 1. #1.143 for all moving tail
    Sht = Sh/(0.3048**2)
    c_hor_tip = c_hor*taper_h
    Fw = 0.6 #Change! Fuselage width at hor.tail intersection
    Ky = 0.3*lh/0.3048
    Lt = lh/0.3048
    Se = Sel/(0.3048**2)
    Bh = Bhor/(0.3048**2)
    W_htail = 0.83* 0.0379* Kuht * (1+Fw/Bh)**(-0.25)* MTOW**0.639* Nz**0.1* Sht**0.75* Lt**-1* Ky**0.704* np.cos(sweep_ht)**-1* Ah**0.166* (1+Se/Sht)**0.1 *0.45359237 #kg assuming composite
    #cg_htail = l_center - l_forwof_LE + l_tail - 0.58*(0.62*(c_hor-c_hor_tip)+c_hor_tip)
    return W_htail