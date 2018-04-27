"""
-------------------------------------------------------------------

Copyright (C) 2016-2018, Andrew W. Steiner

This python code utilizes the superconducting material properties data
compiled by P.J. Ray at
http://dx.doi.org/10.6084/m9.figshare.2075680.v2 (see below)

This program is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

-------------------------------------------------------------------

"""
import matplotlib.pyplot as plot

# Material, original time coordinate, original temperature coordinate,
# from P.J. Ray at
#
# @MastersThesis{PJRay2015, author = {Pia Jensen Ray}, title =
# {{Structural investigation of La(2-x)Sr(x)CuO(4+y) - Following staging
# as a function of temperature}}, school = {Niels Bohr Institute, Faculty
# of Science, University of Copenhagen}, address = {Copenhagen, Denmark},
# year = {2015}, month = {November}, doi =
# {10.6084/m9.figshare.2075680.v2}, url = {http://fys.bozack.dk/docs/master}}
#
# Fourth and fifth columns are used for label positioning
# 
def time(x):
    if (x<2):
        yr=1900+40*x
    else:
        yr=1970+5*x
    return yr

def tptr(x):
    if (x<125):
        tptr=x*0.4
    else:
        tptr=x*2-200
    return tptr

dat=[
# BCS superconductors
    ['Hg',0.299320,10.859729,1,1,1,0],
    ['Pb',0.353741,18.099548,1,1,1,0],
    ['Nb',0.829932,23.981900,1,1,1,0],
    ['NbN',1.034014,41.628959,1,1,1,0],
    [r'V_3Si',1.319728,43.891403,1,1,1,0],
    [r'Nb_3Sn',1.346939,46.606335,1,1,1,0],
    [r'Nb_3Ge',1.809524,59.728507,1,1,1,0],
    ['BKBO',3.687075,77.828054,1,1,1,0],
    [r'YbPd2B$_2$C',4.870748,59.276018,1,1,1,0],
    [r'MgB_2',6.217687,103.167421,1,1,1,0],
# Heavy fermion superconductors
    [r'CeCu$_2$Si$_2$',1.931973,2.262443,2,1,1,0],
    [r'UBe_{13}',2.707483,2.262443,2,1,1,0],
    [r'UPt_3',2.911565,2.262443,2,1,1,0],
    [r'UPd_2Al_3',4.285714,5.429864,2,1,1,0],
    [r'CeCoIn_5',6.231293,5.882353,2,1,1,0],
    [r'PuCoGa_5',6.421769,48.416290,2,1,1,0],
    [r'PuRhGa_5',6.612245,22.624434,2,1,1,0],
# Cuprates
    ['LaBaCuO',3.306122,77.375566,3,1,1,0],
    ['YBaCuO',3.496599,154.298643,3,1,1,0],
    ['BiSrCaCuO',3.687075,166.515837,3,1,1,0],
    ['TlBaCaCuO',3.700680,169.230769,3,1,1,0],
    ['HgBaCaCuO',4.666667,172.398190,3,1,1,0],
    ['HgTlBaCaCuO',4.870748,185.067873,3,1,1,0],
    ['HgBaCaCuO @ 30~GPa',5.047619,173.755656,3,0.985,1.1,1],
    ['LaSrCuO',3.350000,90,3,1,1,0],
# Fullerenes
    [r'K_3C_{60}',4.272109,48.868778,4,1,1,0],
    [r'RbCsC_{60}',4.272109,84.615385,4,1,1,0],
    [r'Cs$_3$C$_{60}$ @ 1.4~GPa',5.061224,102.262443,4,1,1.25,1],
# Carbon nanotubes and diamonds
    ['CNT',6.217687,0.904977,5,1,1,0],
    ['diamond',6.816327,11.764706,5,1,1,0],
    ['CNT',7.197279,31.221719,5,1,1,0],
# Iron-based superconductors
     ['LaOFeP',7.200000,8.750000,6,1,1,0],
     ['LaOFFeAs',7.600000,62.500000,6,1,1,0],
     ['SrFFeAs',7.800000,132.579186,6,1,1,0],
     ['FeSe film',9,150,6,1,1,0],
     ['SmOFFeAs',7.600000,107.500000,6,1,1,0],
# BCS superconductors at high pressure
     ['Li @ 33~GPa',6.421769,41.628959,7,0.99,0.95,1],
     [r'H$_2$S @ 155~GPa',9,203,7,1,1.25,1]
]

# Initial figure setup

lmar=0.14
bmar=0.12
rmar=0.04
tmar=0.04

plot.rc('text',usetex=True)
plot.rc('font',family='serif')
plot.rcParams['lines.linewidth']=0.5
fig=plot.figure(1,figsize=(6.0,6.0))
fig.set_facecolor('white')
ax=plot.axes([lmar,bmar,1.0-lmar-rmar,1.0-tmar-bmar])
ax.minorticks_on()
ax.tick_params('both',length=12,width=1,which='major')
ax.tick_params('both',length=5,width=1,which='minor')
plot.grid(False)

# First plot

y_scale=1.25
x_scale=1.0

plot.xlim([1900,2040])
plot.ylim([2.0e-1,4.0e2])
        
for i in range(0,len(dat)):
    if dat[i][6]==0:
        if dat[i][3]==1:
            plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                          marker='o',mfc='blue',mew=0)
        elif dat[i][3]==2:
            plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                          marker='o',mfc='salmon',mew=0)
        elif dat[i][3]==3:
            plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                          marker='o',mfc='gold',mew=0)
        elif dat[i][3]==4:
            plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                          marker='o',mfc='cyan',mew=0)
        elif dat[i][3]==5:
            plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                          marker='o',mfc='dimgray',mew=0)
        elif dat[i][3]==6:
            plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                          marker='o',mfc='red',mew=0)
        elif dat[i][3]==7:
            plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                      marker='o',mfc='blue',mew=0)
        if i<3:
            ax.text(time(dat[i][1])*x_scale*dat[i][4],
                    tptr(dat[i][2])*y_scale*dat[i][5],dat[i][0],
                    fontsize=12,va='center',ha='center',color='blue')

ax.text(0.1,0.55,'BCS',transform=ax.transAxes,
        fontsize=12,va='center',ha='center',color='blue')
ax.text(0.55,0.25,'Heavy fermion',transform=ax.transAxes,
        fontsize=12,va='center',ha='center',color='salmon')
ax.text(0.53,0.85,'Cuprates',transform=ax.transAxes,
        fontsize=12,va='center',ha='center',color='gold')
ax.text(0.6,0.54,'Fullerenes',transform=ax.transAxes,
        fontsize=12,va='center',ha='center',color='cyan')
ax.text(0.86,0.1,'Carbon-based',transform=ax.transAxes,
        fontsize=12,va='center',ha='center',color='dimgray')
ax.text(0.88,0.7,'Iron-based',transform=ax.transAxes,
        fontsize=12,va='center',ha='center',color='red')

ax.text(0.5,-0.1,'Discovery year',
        transform=ax.transAxes,
        fontsize=12,va='center',ha='center')
ax.text(-0.1,0.5,r'$T_C$ (K)',rotation=90,
        transform=ax.transAxes,
        fontsize=12,va='center',ha='center')
plot.savefig('sfluid1.png')        
#plot.show()

plot.clf()

# Second plot

y_scale=1.0
x_scale=1.0

ax=plot.axes([lmar,bmar,1.0-lmar-rmar,1.0-tmar-bmar])
ax.minorticks_on()
ax.tick_params('both',length=12,width=1,which='major')
ax.tick_params('both',length=5,width=1,which='minor')

plot.xlim([1900,2040])
plot.ylim([2.0e-1,4.0e2])

for i in range(0,len(dat)):
    if dat[i][6]==1:
        if dat[i][3]==3:
            ax.text(time(dat[i][1])*x_scale*dat[i][4],
                    tptr(dat[i][2])*y_scale*dat[i][5],dat[i][0],
                    fontsize=12,va='center',ha='center',color='black')
        elif dat[i][3]==4:
            ax.text(time(dat[i][1])*x_scale*dat[i][4],
                    tptr(dat[i][2])*y_scale*dat[i][5],dat[i][0],
                    fontsize=12,va='center',ha='center',color='black')
        elif dat[i][3]==7:
            ax.text(time(dat[i][1])*x_scale*dat[i][4],
                    tptr(dat[i][2])*y_scale*dat[i][5],dat[i][0],
                    fontsize=12,va='center',ha='center',color='black')
    if dat[i][3]==1:
        plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                      marker='o',mfc='blue',mew=0)
    elif dat[i][3]==2:
        plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                      marker='o',mfc='salmon',mew=0)
    elif dat[i][3]==3:
        plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                      marker='o',mfc='gold',mew=0)
    elif dat[i][3]==4:
        plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                      marker='o',mfc='cyan',mew=0)
    elif dat[i][3]==5:
        plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                      marker='o',mfc='dimgray',mew=0)
    elif dat[i][3]==6:
        plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                      marker='o',mfc='red',mew=0)
    elif dat[i][3]==7:
        if i==len(dat)-1:
            plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                          marker='o',mfc='none',mew=1,mec='blue')
        else:
            plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                          marker='o',mfc='blue',mew=0)

ax.text(0.1,0.55,'BCS',transform=ax.transAxes,
        fontsize=12,va='center',ha='center',color='blue')
ax.text(0.55,0.25,'Heavy fermion',transform=ax.transAxes,
        fontsize=12,va='center',ha='center',color='salmon')
ax.text(0.53,0.85,'Cuprates',transform=ax.transAxes,
        fontsize=12,va='center',ha='center',color='gold')
ax.text(0.6,0.54,'Fullerenes',transform=ax.transAxes,
        fontsize=12,va='center',ha='center',color='cyan')
ax.text(0.86,0.1,'Carbon-based',transform=ax.transAxes,
        fontsize=12,va='center',ha='center',color='dimgray')
ax.text(0.88,0.7,'Iron-based',transform=ax.transAxes,
        fontsize=12,va='center',ha='center',color='red')

ax.text(0.5,-0.1,'Discovery year',
        transform=ax.transAxes,
        fontsize=12,va='center',ha='center')
ax.text(-0.1,0.5,r'$T_C$ (K)',rotation=90,
        transform=ax.transAxes,
        fontsize=12,va='center',ha='center')

plot.savefig('sfluid2.png')        
#plot.show()

plot.clf()

# Third plot

ax=plot.axes([lmar,bmar,1.0-lmar-rmar,1.0-tmar-bmar])
ax.minorticks_on()
ax.tick_params('both',length=12,width=1,which='major')
ax.tick_params('both',length=5,width=1,which='minor')

plot.xlim([1900,2040])
plot.ylim([2.0e-1,4.0e11])

for i in range(0,len(dat)):
    if dat[i][3]==1:
        plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                      marker='o',mfc='blue',mew=0)
    elif dat[i][3]==2:
        plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                      marker='o',mfc='salmon',mew=0)
    elif dat[i][3]==3:
        plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                      marker='o',mfc='gold',mew=0)
    elif dat[i][3]==4:
        plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                      marker='o',mfc='cyan',mew=0)
    elif dat[i][3]==5:
        plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                      marker='o',mfc='dimgray',mew=0)
    elif dat[i][3]==6:
        plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                      marker='o',mfc='red',mew=0)
    elif dat[i][3]==7:
        if i==len(dat)-1:
            plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                          marker='o',mec='blue',mew=1,mfc='none')
        else:
            plot.semilogy(time(dat[i][1]),tptr(dat[i][2]),
                          marker='o',mfc='blue',mew=0)

x_scale=1.004
y_scale=1.0
        
plot.semilogy(2009,1.2e10,marker='o',mfc='green',mew=0)
ax.text(2009*x_scale,1.2e10*y_scale,r'$^{1}S_0$ n',
        fontsize=12,va='center',ha='center')
plot.semilogy(2009,4.0e9,marker='o',mfc='green',mew=0)
ax.text(2009*x_scale,4.0e9*y_scale,r'$^{1}S_0$ p',
        fontsize=12,va='center',ha='center')
plot.semilogy(2009,5.0e8,marker='o',mfc='green',mew=0)
ax.text(2009*x_scale,5.0e8*y_scale,r'$^{3}P_2$ n',
        fontsize=12,va='center',ha='center')
plot.semilogy(1958,3.5e10,marker='o',mfc='green',mew=0)
ax.text(1960*x_scale,3.0e10*y_scale,r'(Z,N)',
        fontsize=12,va='center',ha='center')
plot.semilogy(1977,1.6e10,marker='o',mec='purple',mfc='none',mew=1)
ax.text(1977*x_scale,1.6e10*y_scale,r'uds',
        fontsize=12,va='center',ha='center')

ax.text(1965,7.5e10,'Bohr and Mottelson (1957)',
        fontsize=12,va='center',ha='right')
ax.text(2007,7.0e9,'Brown and Cumming (2009)',
        fontsize=12,va='center',ha='right')
ax.text(2007,3.4e10,'Barrois (1977)',
        fontsize=12,va='center',ha='right')
ax.text(2010,1.3e9,'Page et al. (2009)',
        fontsize=12,va='center',ha='right')

ax.text(0.5,-0.1,'Discovery year',
        transform=ax.transAxes,
        fontsize=12,va='center',ha='center')
ax.text(-0.1,0.5,r'$T_C$ (K)',rotation=90,
        transform=ax.transAxes,
        fontsize=12,va='center',ha='center')

plot.savefig('sfluid3.png')        
#plot.show()

