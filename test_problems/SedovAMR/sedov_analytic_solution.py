# Calculates analytic solution for Sedov blast, creates text file sedov.in
# (contains radius, density, pressure, velocity, temperature, and internal
# energy)

import numpy as na

time   = 0.07       # problem time 
npoints= 200
nu     = 2.0       # cylindrical symmetry       
gamma  = 1.4       # adiabatic index                                                                                                      
alpha  = 1.0       # alpha(gamma, nu), see p. 231                                                                      
                   # alpha(1.4, 3) = 0.851                                                       
                   # alpha(1.4, 2) = 1.0 (an approximate                                                            
                   # value taken from a plot in Sedov 1959)                                                            
                   # alpha(1.4, 1) = 1.1 (also an approximation)                                                                   

E_0    = 10.0      # explosion energy [per unit length (area) if nu=2 (=1)]                                                      
E      = E_0/alpha # dimensional constant #1                                                                                   
rho1   = 1.0       # ambient density (dimensional const #2)                                                                      

endpoints = 50

# useful combinations involving gamma and nu                                                                                      

gm1    = gamma - 1.
gp1    = gamma + 1.
nup2   = nu + 2.

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;                                                              

#; shock wave position and velocity [Sedov 1959, p. 213, eqs (11.3)]                                                              

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;                                                              

r2     = (E/rho1)**(1./nup2)*time**(2./nup2)
v_shock= 2./nup2*(E/rho1)**(1./nup2)*time**(-nu/nup2)

# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;                                                      

#; conditions on the shock front (exact within 5% for an intense explosion)                                                       

#; [Sedov 1959, p. 212, eqs (11.2)]                                                                                               

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;                                                      

v2     = 2./gp1*v_shock           # velocity                                                                                     
rho2   = gp1/gm1*rho1             # density
p2     = 2./gp1*rho1*v_shock**2    # pressure 
t2     = p2/rho2                  # temperature       

#;;;;;;;;;;;;;;;;;;;;;;;                                                                                                          

# self-similar solution                                                                                                          

#;;;;;;;;;;;;;;;;;;;;;;;                                                                                                          

Vmin   = 2./nup2/gamma  # explosion center  0.36 
Vmax   = 4./nup2/gp1    # shock front       0.42      
nbins  = npoints - 1
V      = na.zeros(npoints, dtype='double')
V      = na.arange(npoints)*(Vmax-Vmin)/(npoints-1.)
V      = V + Vmin

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;                                                                                 

#; power indices [Sedov 1959, p. 219, eq. (11.16)]                                                                               

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;                                                                                

alpha2 = -1.*gm1/(2.*gm1+nu)
alpha1 = nup2*gamma/(2.0+nu*gm1)*(2.*nu*(2.0-gamma)/(gamma*nup2**2) - alpha2)
alpha3 = nu/(2.*gm1+nu)
alpha4 = alpha1*nup2/(2.-gamma)
alpha5 = 2./(gamma-2.)
alpha6 = gamma/(2.*gm1+nu)
alpha7 = (2.+nu*gm1)*alpha1/(nu*(2.-gamma))
alpha8 = -2./nup2
alpha9 = 2.*nu/nup2

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;                                                                          
 
#; analytical solution [Sedov 1959, p. 219, eq. (11.15)]                                                                          
 
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;                                                                         
 

rr2    = (nup2*gp1*V/4.)**alpha8*(gp1/gm1*(nup2*gamma*V/2.-1.))**(-alpha2)*(nup2*gp1/(nup2*gp1-2.*(2.+nu*gm1))*(1.-(2.+nu*gm1)/2.*V))**(-alpha1)


r0r2   = (nup2*gp1*V/4.)**alpha8*(gp1/gm1*(nup2*gamma*V/2.-1.))**alpha6*(nup2*gp1/(nup2*gp1-2.*(2.+nu*gm1))*(1.-(2.+nu*gm1)/2.*V))**alpha7*(gp1/gm1*(1.-nup2/2.*V))**(-alpha6-alpha7-2./nup2)

vv2    = nup2*gp1*V*rr2/4.

rhorho2= (gp1/gm1*(nup2*gamma/2.*V-1.))**alpha3*(gp1/gm1*(1.-nup2*V/2.))**alpha5*((nup2*gp1/(nup2*gp1-2.*(2.+nu*gm1)))*(1.-(2.+nu*gm1)*V/2.))**alpha4

pp2    = (nup2*gp1*V/4.0)**alpha9*(gp1/gm1*(1.0-nup2/2.0*V))**(alpha5+1.0)*((nup2*gp1/(nup2*gp1-2.0*(2.0+nu*gm1)))*(1.0-(2.0+nu*gm1)*V/2.0))**(alpha4-2.0*alpha1)

tt2    = na.zeros(npoints, dtype="float64")
tt2[0] = 300.0
tt2[1:nbins] = pp2[1:nbins]/rhorho2[1:nbins]


#;;;;;;;;;;;;;;;;;;;                                                                                                              
#; write a file                                                                                                                   
#;;;;;;;;;;;;;;;;;;;;                                                                                                             

f = open("sedov.in", 'w')

print >> f, "%s\t%s" % ("#", nbins)
print >> f, "%s\t%s" % ("#", "r    vel   rho   temp    internalenergy    p ")

for i in range(nbins):
    print >> f, "%f\t%f\t%f\t%f\t%f\t%f" % (rr2[i]*r2, vv2[i]*v2, rhorho2[i]*rho2, tt2[i]*t2, tt2[i]*t2/gm1, pp2[i]*p2)

f.close()
