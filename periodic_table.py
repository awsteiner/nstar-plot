"""
-------------------------------------------------------------------

Copyright (C) 2015-2018, Andrew W. Steiner

This periodic table plot is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3 of
the License, or (at your option) any later version.

This periodic table plot is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this periodic table plot. If not, see
<http://www.gnu.org/licenses/>.

-------------------------------------------------------------------

"""
import numpy as np
import matplotlib.pyplot as plot
import matplotlib.patches as patches
from matplotlib.font_manager import FontProperties

# ----------------------------------------------------------------
# Note that the matplotlib output is significantly different on
# OSX and Ubuntu, and this code is currently designed to run on
# OSX.

# ----------------------------------------------------------------
# box

def box(x,y,Z,abbrev,name,mass,ax,font_abbrev,font_name,font_mass,font_Z):
    p=patches.Rectangle((x-0.5,y-0.5),1,1,fill=True,lw=0.5,
                        color=(1.0-x/40,0.5+x/40,1.0))
    ax.add_patch(p)
    p2=patches.Rectangle((x-0.5,y-0.5),1,1,fill=False,lw=0.5)
    ax.add_patch(p2)
    if int(Z)>99:
        ax.text(x-0.23,y+0.35,Z,ha='center',va='center',
                fontsize=7)
    else:
        ax.text(x-0.30,y+0.35,Z,ha='center',va='center',
                fontsize=7)
    ax.text(x,y+0.08,abbrev,ha='center',va='center',
            fontsize=15)
    if len(name)>10 or name=='Molybdenum':
        ax.text(x,y-0.2,name,ha='center',va='center',
                fontsize=4)
    elif len(name)>8:
        ax.text(x,y-0.2,name,ha='center',va='center',
                fontsize=5)
    else:
        ax.text(x,y-0.2,name,ha='center',va='center',
                fontsize=6)
    if name=='Hydrogen' or name=='Magnesium':
        ax.text(x,y-0.4,mass,ha='center',va='center',
                fontsize=5)
    else:
        ax.text(x,y-0.4,mass,ha='center',va='center',
                fontsize=7)
    
# ----------------------------------------------------------------
# Options 

# If true, report errors as +/- 0.00001 instead of (1)
long_errors=False

debug=True

# ----------------------------------------------------------------
# Read data

df=np.genfromtxt('ciaaw_edit.txt',dtype='str')

# ----------------------------------------------------------------
# Initial parse 

Z_arr=[]
name_arr=[]
wgt_arr=[]
abbrev_arr=[]

for i in range(0,len(df)):
    name_arr.append(df[i][0])
    abbrev_arr.append(df[i][3])
    Z_arr.append(int(df[i][4]))
    note=df[i][2]
    if debug:
        print('name:',name_arr[i],'Z:',Z_arr[i],'note:',note)
        print('old weight and error:',df[i][7],df[i][8])
    #
    if note!='b' and note!='bm' and note!='v':
        if long_errors:
            if df[i][8][0]=='(':
                last_digit=df[i][8][1]
                # Count digits after decimal
                dot_loc=df[i][7].find('.')
                ndigits=df[i][7]-dot_loc-1
                df[i][8]='0.'
                for i in range(0,ndigits-1):
                    df[i][8]+=' '
                df[i][8]+=last_digit
        else:
            if df[i][8][0]!='(' and float(df[i][8])>0.0:
                last_digit=df[i][8][len(df[i][8])-1]
                df[i][8]='('+last_digit+')'
    #
    if debug:
        print('new err:',df[i][8])
    if note=='v':
        wgt_arr.append('['+df[i][7]+','+df[i][8]+']')
    elif note=='u':
        wgt_arr.append('['+df[i][7]+']')
    elif note=='g':
        if df[i][8][0]!='(' and float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \pm $ '+df[i][8]+'$^g$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='gr':
        if df[i][8][0]!='(' and float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \pm $ '+df[i][8]+'$^{gr}$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='gm':
        if df[i][8][0]!='(' and float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \pm $ '+df[i][8]+'$^{gm}$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='m':
        if df[i][8][0]!='(' and float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \pm $ '+df[i][8]+'$^{m}$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='r':
        if df[i][8][0]!='(' and float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \pm $ '+df[i][8]+'$^r$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='s':
        if df[i][8][0]!='(' and float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \pm $ '+df[i][8]+'$^s$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='b':
        if long_errors:
            wgt_arr.append('['+df[i][7]+','+df[i][8]+']')
        else:
            avg=(float(df[i][7])+float(df[i][8]))/2
            diff=(float(df[i][8])-avg)*(1.0+1.0e-8)
            while diff<10:
                diff*=10.0
            digit=str(diff)[0]
            wgt_arr.append(str(avg)+'('+digit+')')
        print('Here2')
    elif note=='bm':
        if long_errors:
            wgt_arr.append('['+df[i][7]+','+df[i][8]+']$^m$')
        else:
            avg=(float(df[i][7])+float(df[i][8]))/2
            diff=(float(df[i][8])-avg)*(1.0+1.0e-8)
            while diff<10:
                diff*=10.0
            digit=str(diff)[0]
            wgt_arr.append(str(avg)+'('+digit+')$^m$')
    elif note=='n':
        if df[i][8][0]!='(' and float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \pm $ '+df[i][8])
        else:
            wgt_arr.append(df[i][7])
    if debug:
        print('weight:',wgt_arr[i])
        print('')

# ----------------------------------------------------------------
# Determine coordinates

px_cent=[Z_arr[i] for i in range(0,len(Z_arr))]
py_cent=[Z_arr[i] for i in range(0,len(Z_arr))]

ygap=0.5
xgap=2.5
height=1

for i in range(0,len(name_arr)):
    if Z_arr[i]>=89 and Z_arr[i]<=103:
        px_cent[i]=Z_arr[i]-88.5+xgap
        py_cent[i]=height
    if Z_arr[i]>=57 and Z_arr[i]<=71:
        px_cent[i]=Z_arr[i]-56.5+xgap
        py_cent[i]=height*2
    if Z_arr[i]>=87 and Z_arr[i]<=88:
        px_cent[i]=Z_arr[i]-86
        py_cent[i]=height*3+ygap
    if Z_arr[i]>=104 and Z_arr[i]<=118:
        px_cent[i]=Z_arr[i]-103+3
        py_cent[i]=height*3+ygap
    if Z_arr[i]>=55 and Z_arr[i]<=56:
        px_cent[i]=Z_arr[i]-54
        py_cent[i]=height*4+ygap
    if Z_arr[i]>=72 and Z_arr[i]<=86:
        px_cent[i]=Z_arr[i]-71+3
        py_cent[i]=height*4+ygap
    if Z_arr[i]>=37 and Z_arr[i]<=54:
        px_cent[i]=Z_arr[i]-36
        py_cent[i]=height*5+ygap
    if Z_arr[i]>=19 and Z_arr[i]<=36:
        px_cent[i]=Z_arr[i]-18
        py_cent[i]=height*6+ygap
    if Z_arr[i]>=11 and Z_arr[i]<=12:
        px_cent[i]=Z_arr[i]-10
        py_cent[i]=height*7+ygap
    if Z_arr[i]>=13 and Z_arr[i]<=18:
        px_cent[i]=Z_arr[i]-12+12
        py_cent[i]=height*7+ygap
    if Z_arr[i]>=3 and Z_arr[i]<=4:
        px_cent[i]=Z_arr[i]-2
        py_cent[i]=height*8+ygap
    if Z_arr[i]>=5 and Z_arr[i]<=10:
        px_cent[i]=Z_arr[i]-4+12
        py_cent[i]=height*8+ygap
    if Z_arr[i]==2:
        px_cent[i]=18
        py_cent[i]=height*9+ygap
    if Z_arr[i]==1:
        px_cent[i]=1
        py_cent[i]=height*9+ygap
    print('%15s %3i %20s %4s %4s'%(name_arr[i],Z_arr[i],wgt_arr[i],
                                   str(px_cent[i]),str(py_cent[i])))

plot.rc('text',usetex=True)
#plot.rc('font',family='serif')
plot.rcParams['lines.linewidth']=0.5

# ---------------------------------------------------------
# Create serif and sans-serif font objects

font_abbrev=FontProperties()
font_abbrev.set_family('serif')
font_abbrev.set_size('large')

font_name=font_abbrev.copy()
font_name.set_size('small')
font_name.set_family('sans-serif')

font_mass=font_name.copy()

font_Z=font_name.copy()

font_name.set_size('xx-small')
font_mass.set_size('xx-small')

# ---------------------------------------------------------

fig=plot.figure(1,figsize=(8.0,6.0))
fig.set_facecolor('white')
ax=plot.axes([0.04,0.04,0.92,0.92])
ax.minorticks_on()
ax.tick_params('both',length=12,width=1,which='major')
ax.tick_params('both',length=5,width=1,which='minor')

plot.grid(False)
plot.xlim([0,19])
plot.ylim([0,10.5])
plot.axis('off')

for i in range(0,len(name_arr)):
    box(px_cent[i],py_cent[i],str(Z_arr[i]),abbrev_arr[i],name_arr[i],
        wgt_arr[i],ax,font_abbrev,font_name,font_mass,font_Z)

ax.text(2,10.5,'Periodic Table',
        ha='left',va='center',fontsize=20)

group_color=(0.4,0.4,0.4)
ax.text(0.0,10.15,'Group:',
        ha='center',va='center',fontsize=10,color=group_color)
ax.text(1,10.15,'1',
        ha='center',va='center',fontsize=10,color=group_color)
ax.text(2,9.15,'2',
        ha='center',va='center',fontsize=10,color=group_color)
for i in range(0,10):
    ax.text(i+3,7.15,str(i+3),
            ha='center',va='center',fontsize=10,color=group_color)
ax.text(13,9.15,'13',
        ha='center',va='center',fontsize=10,color=group_color)
ax.text(14,9.15,'14',
        ha='center',va='center',fontsize=10,color=group_color)
ax.text(15,9.15,'15',
        ha='center',va='center',fontsize=10,color=group_color)
ax.text(16,9.15,'16',
        ha='center',va='center',fontsize=10,color=group_color)
ax.text(17,9.15,'17',
        ha='center',va='center',fontsize=10,color=group_color)
ax.text(18,10.15,'18',
        ha='center',va='center',fontsize=10,color=group_color)
for i in range(0,15):
    ax.text(i+3,2.65,str(i+3),
            ha='center',va='center',fontsize=10,color=group_color)

ax.text(3,9.9,('$^g$ Some geologic samples have isotopic'+
               ' compositions which vary outside quoted errors'),
        ha='left',va='center',fontsize=7)
ax.text(3,9.7,('$^m$ Some commerical samples have isotopic'+
               ' compositions which have large deviations from quoted range'),
        ha='left',va='center',fontsize=7)
ax.text(3,9.5,('$^r$ Precision limited by large isotopic range in'+
               ' normal terrestrial material'),
        ha='left',va='center',fontsize=7)
ax.text(3,9.3,'$^u$ unstable',
        ha='left',va='center',fontsize=7)
ax.text(3,9.1,'$^v$ unstable with two longest-lived isotopes',
        ha='left',va='center',fontsize=7)
ax.text(3,8.9,('$^b$ CIAAW bracket has been converted to '+
               'central value and error'),
        ha='left',va='center',fontsize=7)
ax.text(3,8.7,'Data taken from CIAAW',
        ha='left',va='center',fontsize=7)
ax.text(3,8.5,('Python code at https://github.com/awsteiner/'+
               'nstar-plot/periodic\_table.py'),
        ha='left',va='center',fontsize=7)

plot.savefig('pt.pdf')    
plot.show()
    
