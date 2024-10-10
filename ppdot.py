"""-------------------------------------------------------------------

   Copyright (C) 2019-2024, Andrew W. Steiner

   This neutron star plot is free software; you can redistribute it
   and/or modify it under the terms of the GNU General Public License
   as published by the Free Software Foundation; either version 3 of
   the License, or (at your option) any later version.
   
   This neutron star plot is distributed in the hope that it will be
   useful, but WITHOUT ANY WARRANTY; without even the implied warranty
   of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
   General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this neutron star plot. If not, see
   <http://www.gnu.org/licenses/>.
   
   -------------------------------------------------------------------

Death line from Zhang et al. APJL 631 (2000) 138
Pulsars from ATNF database
Magnetars from McGill
RRATs from WVU
Comparable p pdot diagram in Zhou et al. (2017) 1708.05494

XDINS From Rigoselli et al. (2019), ignoring J1605.3+3249 which doesn't
  have P and Pdot data

"""
import math
import matplotlib.pyplot as plot
import o2sclpy
import matplotlib.patches as patches

# Gauss in fm^{-2}
gauss_fm2=math.sqrt(3.16303e-36)

# x- and y-axis limits
xlo=1.0e-3
xhi=30.0
ylo=1.0e-22
yhi=1.0e-8

# Use 250 for higher dpi monitors and 100 for the default
final_dpi=250

rrats=[dict()]
index=0
f=open('ns_data/rratalog.txt')
for line in f:
    if index>0 and line[0]!='#':
        if 0:
            name=line[0:12].replace(' ','')
            P=line[16:21].replace(' ','')
            Pdot=line[25:30].replace(' ','')
            DM=line[33:37].replace(' ','')
            RA=line[41:49].replace(' ','')
            DEC=line[52:61].replace(' ','')
            l=line[65:71].replace(' ','')
            b=line[72:78].replace(' ','')
            Rate=line[81:86].replace(' ','')
        else:
            line=line.split()
            name=line[0]
            P=line[1]
            Pdot=line[2]
            DM=line[3]
            RA=line[4]
            DEC=line[5]
            l=line[6]
            b=line[7]
            Rate=line[8]
            logB=line[9]
            logts=line[10]
            Dhat=line[11]
            FluxD=line[12]
            Pulse_Width=line[13]
            Survey=line[14]
        dvalue={'name': name,
                'P': P,
                'Pdot': Pdot,
                'DM': DM,
                'RA': RA,
                'DEC': DEC,
                'l': l,
                'b': b,
                'Rate': Rate,
                'logB': logB,
                'logts': logts,
                'Dhat': Dhat,
                'FluxD': FluxD,
                'Pulse_Width': Pulse_Width,
                'Survey': Survey}
        if index!=1:
            rrats.append(dict())
        rrats[index-1]=dvalue
    index=index+1
f.close()
print('Read',len(rrats),'RRATs')

# Parse the database. The database is a list of dictionaries
# and subdictionaries. 
psrcat=[dict()]
f=open('ns_data/psrcat.db')
index=0
need_new=True
for line in f:
    # Skip comments and separators
    if line[0]!='#' and (line[0]!='@' or line[1]!='-'):
        # If necessary, add a new dictionary to the list
        if need_new:
            psrcat.append(dict())
            index=index+1
            need_new=False
        # First get the field name
        field=line[0:8].replace(' ','')
        if field=='ASSOC' or field=='SURVEY':
            value=line[9:].replace('\n',' ').replace(' ','')
            flag=''
            ref=''
            extra=''
            dvalue={'value': value}
        else:
            value=line[9:33].replace(' ','')
            flag=line[34:38].replace(' ','')
            ref=line[39:45].replace(' ','')
            extra=line[45:].replace('\n',' ').replace(' ','')
            dvalue={'value': value, 'flag': flag, 'ref': ref}
        #print('field',field,'value',value,'flag',flag,'ref',ref,'extra',
        #extra,'end')
        #print(dvalue)
        psrcat[index][field]=dvalue
        #txt=input("Next\n")
    elif line[0]=='@' and line[2]=='-':
        # We have reached a separator, so if there is more data
        # we need to add an entry to the list
        need_new=True
f.close()
print('Read',len(psrcat),'pulsar entries.')

magnetars=[]
f=open('ns_data/magnetar2.txt')
for line in f:
    line=line.split(' ')
    magnetars.append(line)
f.close()

# From Rigoselli et al. (2019), ignoring J1605.3+3249 which doesn't
# have P and Pdot data
xdins=[
    ['J0420.0-5022',3.45,2.76],
    ['J0720.4-3125',16.78,18.6],
    ['J0806.4-4123',11.37,5.6],
    ['J1308.6+2127',10.31,11.2],
    ['J1856.5-3754',7.06,2.98],
    ['J2143.0+0654',9.43,4.1],
    ['J0726.0-2612',3.44,29.3]
]

plot.rcParams['figure.dpi']=final_dpi

o2=o2sclpy.plot_base()

(fig,ax)=o2sclpy.default_plot(left_margin=0.16,bottom_margin=0.11,
                              right_margin=0.01,top_margin=0.02,
                              rt_ticks=True,ticks_in=True)
                              
ax.set_xscale('log')
ax.set_yscale('log')
plot.xlim([xlo,xhi])
plot.ylim([ylo,yhi])
plot.xlabel('$$ P~(\\mathrm{s}) $$',fontsize=16)
plot.ylabel('$$ \\dot{P} $$',fontsize=16)

x=[]
y=[]
x2=[]
y2=[]
for i in range(0,len(psrcat)):
    if 'P0' in psrcat[i] and 'P1' in psrcat[i]:
        if 'BINCOMP' in psrcat[i] or 'BINARY' in psrcat[i]:
            x2.append(float(psrcat[i]['P0']['value']))
            y2.append(float(psrcat[i]['P1']['value']))
        else:
            x.append(float(psrcat[i]['P0']['value']))
            y.append(float(psrcat[i]['P1']['value']))

plot.plot(x,y,marker='.',color='black',lw=0)
plot.plot(x2,y2,marker='o',mfc='white',color='black',lw=0)

x=[]
y=[]
for i in range(0,len(rrats)):
    if rrats[i]['P']!='--' and rrats[i]['Pdot']!='--':
        x.append(float(rrats[i]['P']))
        y.append(float(rrats[i]['Pdot'])*1.0e-15)
        #print(x[len(x)-1],y[len(y)-1])

plot.scatter(x,y,marker='*',color='blue')

x=[]
y=[]
for i in range(0,len(magnetars)):
    x.append(float(magnetars[i][2]))
    y.append(float(magnetars[i][4])*1.0e-11)
    #print(x[len(x)-1],y[len(y)-1])

plot.scatter(x,y,marker='s',color='red')

x=[]
y=[]
for i in range(0,len(xdins)):
    x.append(xdins[i][1])
    y.append(xdins[i][2]*1.0e-14)
    #print(x[len(x)-1],y[len(y)-1])

plot.scatter(x,y,marker='v',color='green')
        
for logB in range(8,16):
    xright=10.0
    yleft=(10.0**logB/3.3e19)**2.0/xlo
    plot.plot([xlo,xright],[yleft,
                             (10.0**logB/3.3e19)**2.0/xright],ls=':',
              color='black')
    if logB>8 and logB<13:
        ax.text(2.1e-3,yleft*0.78,'$$ 10^{'+str(logB)+'}~\\mathrm{G} $$',
                fontsize=12)
    elif logB==13:
        ax.text(2.1e-3,yleft*0.78,'$$ B=10^{'+str(logB)+'}~\\mathrm{G} $$',
                fontsize=12)
    elif logB==14:
        ax.text(1.5e-2,1.0e-9,'$$ 10^{'+str(logB)+'}~\\mathrm{G} $$',
                fontsize=12)
    elif logB==15:
        ax.text(1.05,1.0e-9,'$$ 10^{'+str(logB)+'}~\\mathrm{G} $$',
                fontsize=12)

for log_tau in range(2,12):
    line_left=xlo*10.0
    if log_tau>9:
        line_left=xlo
    text_x=14.0
    
    yright=0.5/(10.0**log_tau*31556926)*xhi
    plot.plot([line_left,xhi],[0.5/(10.0**log_tau*31556926)*line_left,
                             yright],ls=':',
              color='blue')
    if log_tau==10:
        ax.text(text_x*0.85,yright*0.9,'$$ 10^{'+str(log_tau)+'} $$',
                fontsize=12,color='blue')
    elif log_tau>3:
        ax.text(text_x,yright*0.9,'$$ 10^{'+str(log_tau)+'} $$',
                fontsize=12,color='blue')
    elif log_tau>2:
        ax.text(text_x*0.85,yright*1.0,
                '$$ 10^{'+str(log_tau)+'}~\\mathrm{yr} $$',
                fontsize=12,color='blue')

plot.plot([xlo,xhi*0.4],[10**(2.0*(-3.0)-16.52),
                         10**(2.0*math.log10(xhi*0.4)-16.52)],color='green')

# Legend
r=patches.Rectangle((0.2,2.0e-22),20.0,4.0e-19,
                    angle=0,lw=0,fc='white',fill=True,
                    zorder=20)
ax.add_patch(r)

top=1.0e-19
fact=5.0

plot.plot([0.3],[top],marker='s',mfc='red',mew=0,lw=0,zorder=21)
ax.text(0.4,top,
        '$$ \\mathrm{Magnetars} $$',
        fontsize=16,color='black',ha='left',va='center',zorder=21)

top=top/fact

plot.plot([0.3],[top],marker='*',mfc='blue',mew=0,lw=0,zorder=21)
ax.text(0.4,top,
        '$$ \\mathrm{RRATs} $$',
        fontsize=16,color='black',ha='left',va='center',zorder=21)

fact2=15.0
plot.plot([0.3*fact2],[top],marker='v',mfc='green',mew=0,lw=0,zorder=21)
ax.text(0.4*fact2,top,
        '$$ \\mathrm{XDINs} $$',
        fontsize=16,color='black',ha='left',va='center',zorder=21)

top=top/fact

plot.plot([0.3],[top],marker='.',mfc='black',mew=0,lw=0,zorder=21)
ax.text(0.4,top,
        '$$ \\mathrm{Pulsars} $$',
        fontsize=16,color='black',ha='left',va='center',zorder=21)

top=top/fact

plot.plot([0.3],[top],marker='o',mec='black',mew=1,lw=0,zorder=21,
          mfc='white')
ax.text(0.4,top,
        '$$ \\mathrm{Pulsars (binaries)} $$',
        fontsize=16,color='black',ha='left',va='center',zorder=21)

plot.savefig('ppdot.pdf')        
plot.savefig('ppdot.png')        
plot.show()


