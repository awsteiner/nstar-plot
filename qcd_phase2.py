import matplotlib.pyplot as plot
import o2sclpy
import numpy
import math

p=o2sclpy.plot_base()
p.fig_dict='fig_size_x=9.7,fig_size_y=6,left_margin=0.12,bottom_margin=0.16'
p.xlimits(0,2000)
p.ylimits(0,160)
p.font=28
p.xtitle(r'$ \mu_B = 3 \mu_Q~[\mathrm{MeV}]$')
p.ytitle(r'$ T~[\mathrm{MeV}]$')

nk=30

for k in range(0,nk):
    xmin=1100+k*300/(nk-1)
    xmax=2600-k*600/(nk-1)

    theta=numpy.arange(0,numpy.pi/2,numpy.pi/160)
    transition_x1=[(xmax-350)*math.cos(theta[i])+350 for i in
                   range(0,len(theta))]
    transition_y1=[143*math.sin(theta[i]) for i in range(0,len(theta))]
    transition_x2=[(xmin-350)*math.cos(theta[i])+350 for i in
                   range(0,len(theta))]
    transition_y2=[143*math.sin(theta[i]) for i in range(0,len(theta))]
    
    fill_region_x=[]
    fill_region_y=[]
    for i in range(0,len(transition_x1)):
        fill_region_x.append(transition_x1[i])
        fill_region_y.append(transition_y1[i])
    le=len(transition_x2)
    for i in range(0,le):
        fill_region_x.append(transition_x2[le-1-i])
        fill_region_y.append(transition_y2[le-1-i])
    fill_region_x.append(transition_x1[0])
    fill_region_y.append(transition_y1[0])

    color=[(nk-1-k/2.5)/(nk-1),(nk-1-k/2.5)/(nk-1),1.0]
    p.axes.fill(fill_region_x,fill_region_y,color=color,alpha=0.4)

for k in range(0,nk):
    merger_x1=[i*100 for i in range(0,21)]
    merger_x2=[i*100 for i in range(0,21)]
    merger_y1=[merger_x1[i]*merger_x1[i]*(130-60*k/float(nk-1))/(1800**2)
               for i in range(0,21)]
    merger_y2=[0.0 for i in range(0,21)]

    fill_region_x=[]
    fill_region_y=[]
    for i in range(0,len(merger_x1)):
        fill_region_x.append(merger_x1[i])
        fill_region_y.append(merger_y1[i])
    le=len(merger_x2)
    for i in range(0,le):
        fill_region_x.append(merger_x2[le-1-i])
        fill_region_y.append(merger_y2[le-1-i])
    fill_region_x.append(merger_x1[0])
    fill_region_y.append(merger_y1[0])

    color=[1,(nk-1-k)/(nk-1),(nk-1-k)/(nk-1)]
    p.axes.fill(fill_region_x,fill_region_y,color=color,alpha=0.03)
    
p.text(500,80,'hadrons')
p.ttext(0.9,0.9,'QGP')
p.text(700,30,'virial exp.')
p.text(940,10,'nuclei')
p.text(1400,10,'neutron stars')
p.text(1750,45,'mergers',color=[0.5,0,0])
p.ttext(0.05,0.6,'lattice QCD',rotation=90)
p.ttext(0.1,0.7,'RHIC',rotation=90)
p.ttext(500,20,'virial exp',rotation=90)
p.text(1250,90,'deconfinement',rotation=-50,color=[0,0,0.5])

p.font=22
p.text(180,150,'crossover')
p.line(350,143,0,143,lw=2,color=[0.5,0.5,0.5],ls=':')

p.save('qcd_phase2.png')
p.show()

