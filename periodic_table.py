"""
   -------------------------------------------------------------------

   Copyright (C) 2015-2024, Andrew W. Steiner

   This periodic table plot is free software; you can redistribute it
   and/or modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation; either version 3 of the
   License, or (at your option) any later version.
   
   This periodic table plot is distributed in the hope that it will be
   useful, but WITHOUT ANY WARRANTY; without even the implied warranty
   of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
   General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this periodic table plot. If not, see
   <http://www.gnu.org/licenses/>.
   
   -------------------------------------------------------------------
   
   Note that the matplotlib output is a bit different on OSX and
   Ubuntu.

"""

# Imports
import numpy as np
import matplotlib.pyplot as plot
import matplotlib.patches as patches
import os

# ----------------------------------------------------------------
# Options 

# If true, then output a nucleosynthesis table. If false, output a
# standard periodic table. As of 10/10/24, the nsynth_mode=False
# version still needed a bit of work. 
nsynth_mode=True

# Use 250 for higher dpi monitors and 100 for the default
final_dpi=250

# RGB color definitions
unstable_color=(0.9,0.9,0.9)
BBN_color=(0.9,1.0,0.9)
cosmic_ray_color=(1.0,0.9,0.9)
Star_color=(1.0,0.8,0.8)
SNe_color=(0.9,0.9,1.0)
WD_color=(0.8,1.0,0.8)
r_proc_color=(1.0,1.0,0.9)
s_proc_color=(1.0,0.9,1.0)

# If true, report errors as +/- 0.00001 instead of (1)
long_errors=False

debug=False

# ----------------------------------------------------------------

def box(x,y,Z,abbrev,name,mass,ax,af,lf):
    """Create a box for the specified element with atomic number
    ``Z`` at location ``(x,y)``, using the nucleosynthetic fractions
    specified in ``af``.
    """
    #fill_color=(1.0-x/40,0.5+x/40,1.0)
    fill_color=(1.0,1.0,1.0)
    if nsynth_mode:
        bbn_frac=float(af[int(Z)][2])
        cr_frac=float(af[int(Z)][3])
        star_frac=float(af[int(Z)][4])
        sne_frac=float(af[int(Z)][5])
        wd_frac=float(af[int(Z)][6])
        r_frac=float(af[int(Z)][7])
        s_frac=float(af[int(Z)][8])
        total=bbn_frac+cr_frac+star_frac+sne_frac+wd_frac+r_frac+s_frac
        if total<1.0e-4:
            punstable=patches.Rectangle((x-0.5,y-0.5),1,1,fill=True,lw=0.5,
                                        color=unstable_color)
            ax.add_patch(punstable)
        else:
            y0=1
            y1=1-bbn_frac
            y2=1-bbn_frac-cr_frac
            y3=1-bbn_frac-cr_frac-star_frac
            y4=1-bbn_frac-cr_frac-star_frac-sne_frac
            y5=1-bbn_frac-cr_frac-star_frac-sne_frac-wd_frac
            y6=1-bbn_frac-cr_frac-star_frac-sne_frac-wd_frac-r_frac
            y7=0
            p0=patches.Rectangle((x-0.5,y-0.5+y1),1,y0-y1,fill=True,lw=0.5,
                                color=BBN_color)
            ax.add_patch(p0)
            p1=patches.Rectangle((x-0.5,y-0.5+y2),1,y1-y2,fill=True,lw=0.5,
                                color=cosmic_ray_color)
            ax.add_patch(p1)
            p2=patches.Rectangle((x-0.5,y-0.5+y3),1,y2-y3,fill=True,lw=0.5,
                                color=Star_color)
            ax.add_patch(p2)
            p3=patches.Rectangle((x-0.5,y-0.5+y4),1,y3-y4,fill=True,lw=0.5,
                                color=SNe_color)
            ax.add_patch(p3)
            p4=patches.Rectangle((x-0.5,y-0.5+y5),1,y4-y5,fill=True,lw=0.5,
                                color=WD_color)
            ax.add_patch(p4)
            p5=patches.Rectangle((x-0.5,y-0.5+y6),1,y5-y6,fill=True,lw=0.5,
                                color=r_proc_color)
            ax.add_patch(p5)
            p6=patches.Rectangle((x-0.5,y-0.5+y7),1,y6-y7,fill=True,lw=0.5,
                                color=s_proc_color)
            ax.add_patch(p6)
    else:
        p=patches.Rectangle((x-0.5,y-0.5),1,1,fill=True,lw=0.5,
                            color=fill_color)
        ax.add_patch(p)
    poutline=patches.Rectangle((x-0.5,y-0.5),1,1,fill=False,lw=0.5)
    ax.add_patch(poutline)

    # Output atomic number
    if int(Z)>99:
        ax.text(x-0.23,y+0.35,Z,ha='center',va='center',
                fontsize=7)
    else:
        ax.text(x-0.30,y+0.35,Z,ha='center',va='center',
                fontsize=7)

    # Output element abbreviation
    ax.text(x,y+0.08,abbrev,ha='center',va='center',
            fontsize=15)
    
    # Output element name
    if len(name)>10 or name=='Molybdenum':
        ax.text(x,y-0.2,name,ha='center',va='center',
                fontsize=4)
    elif len(name)>8:
        ax.text(x,y-0.2,name,ha='center',va='center',
                fontsize=5)
    else:
        ax.text(x,y-0.2,name,ha='center',va='center',
                fontsize=6)
        
    if nsynth_mode==True:
        if abbrev=='H':
            ax.text(x,y-0.4,'12',ha='center',va='center',
                    fontsize=5)
        else:
            for i in range(0,83):
                if lf[i][0]==abbrev:
                    abund=r'$ '+lf[i][1]+'{\\pm}'+lf[i][2]+' $'
                    if len(abund)>17:
                        ax.text(x,y-0.4,abund,ha='center',va='center',
                                fontsize=3)
                    elif len(abund)>16:
                        ax.text(x,y-0.4,abund,ha='center',va='center',
                                fontsize=4)
                    else:
                        ax.text(x,y-0.4,abund,ha='center',va='center',
                                fontsize=5)
    else:
        if name=='Hydrogen' or name=='Magnesium':
            ax.text(x,y-0.4,mass,ha='center',va='center',
                    fontsize=5)
        else:
            ax.text(x,y-0.4,mass,ha='center',va='center',
                    fontsize=7)
    
# ----------------------------------------------------------------
# Read data

df=np.genfromtxt('ciaaw_edit.txt',dtype='str')
af=np.genfromtxt('abund2.txt',dtype='str')
lf=np.genfromtxt('lodders03b.txt',dtype='str')

# ----------------------------------------------------------------
# Parse the 'ciaaw_edit.txt' file for atomic weights

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
            wgt_arr.append(df[i][7]+' $ \\pm $ '+df[i][8]+'$^g$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='gr':
        if df[i][8][0]!='(' and float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \\pm $ '+df[i][8]+'$^{gr}$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='gm':
        if df[i][8][0]!='(' and float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \\pm $ '+df[i][8]+'$^{gm}$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='m':
        if df[i][8][0]!='(' and float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \\pm $ '+df[i][8]+'$^{m}$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='r':
        if df[i][8][0]!='(' and float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \\pm $ '+df[i][8]+'$^r$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='s':
        if df[i][8][0]!='(' and float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \\pm $ '+df[i][8]+'$^s$')
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
            wgt_arr.append(df[i][7]+' $ \\pm $ '+df[i][8])
        else:
            wgt_arr.append(df[i][7])
    if debug:
        print('weight:',wgt_arr[i])
        print('')

# ----------------------------------------------------------------
# Determine (x,y) coordinates from atomic number

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

# ------------------------------------------------------------------
# Construct figure and axes objects

plot.rc('text',usetex=True)
#plot.rc('font',family='serif')
plot.rcParams['lines.linewidth']=0.5

# 8x6 is the same as 10x7.5 and thus is perfect for 8.5 x 11 paper
# with 1/2 inch margins on all four sides

fig=plot.figure(1,figsize=(8.0,6.0),dpi=final_dpi)

fig.set_facecolor('white')
ax=plot.axes([0.04,0.04,0.92,0.92])
ax.minorticks_on()
ax.tick_params('both',length=12,width=1,which='major')
ax.tick_params('both',length=5,width=1,which='minor')

plot.grid(False)
plot.xlim([0,19])
plot.ylim([0,10.5])
plot.axis('off')

# ------------------------------------------------------------------
# Plot all of the individual element boxes

for i in range(0,len(name_arr)):
    box(px_cent[i],py_cent[i],str(Z_arr[i]),abbrev_arr[i],name_arr[i],
        wgt_arr[i],ax,af,lf)

# ------------------------------------------------------------------
# Title

ax.text(2,10.5,'Origin of the Elements',
        ha='left',va='center',fontsize=20)

# ------------------------------------------------------------------
# Column and other labels

if nsynth_mode==False:
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
    for i in range(0,1):
        ax.text(i+3,2.65,str(i+3),
                ha='center',va='center',fontsize=10,color=group_color)

    ax.text(3,9.9,('$^g$ Some geologic samples have isotopic'+
                   ' compositions which vary outside quoted errors'),
            ha='left',va='center',fontsize=7)
    ax.text(3,9.7,('$^m$ Some commerical samples have isotopic comp'+
                   'ositions which have large deviations from quoted range'),
            ha='left',va='center',fontsize=7)
    ax.text(3,9.5,('$^r$ Precision limited by large isotopic range in'+
                   ' normal terrestrial material'),
            ha='left',va='center',fontsize=7)
    ax.text(3,9.3,('$^b$ CIAAW bracket has been converted to '+
                   'central value and error'),
            ha='left',va='center',fontsize=7)

# ----------------------------------------------------------------
# Create the notes at the top

notes_x=2.8
ax.text(notes_x,9.7,(r'The bottom number gives the $\mathrm{log}_{10} $ '+
                     'of the solar system abundance shifted to 12 for H '+
                     '(Lodders 2003).'),
        ha='left',va='center',fontsize=7)
ax.text(notes_x,9.5,('r-process to s-process ratios are from '+
                     'Simmerer et al. (2004)'),
        ha='left',va='center',fontsize=7)
ax.text(notes_x,9.3,('Inspired by previous versions from Jennifer '+
                     'Johnson, Inese Ivans, and Anna Frebel'),
        ha='left',va='center',fontsize=7)
ax.text(notes_x+0.2,9.1,('(see http://blog.sdss.org/2017/01/09/origin'+
                         '-of-the-elements-in-the-solar-system/ '),
        ha='left',va='center',fontsize=7)
ax.text(notes_x+0.2,8.9,('and http://www.cosmic-origins.org/ ).'),
        ha='left',va='center',fontsize=7)
ax.text(notes_x,8.7,'This version by Andrew W. Steiner, awsteiner@utk.edu,',
        ha='left',va='center',fontsize=7)
ax.text(notes_x+0.2,8.5,(r'python code (GPLv3) at https://github.com/'+
                         r'awsteiner/nstar-plot/periodic\_table.py'),
        ha='left',va='center',fontsize=7)
ax.text(notes_x,8.3,('There are significant uncertainties in some values '+
                     'that are not shown here.'),
        ha='left',va='center',fontsize=7)
ax.text(notes_x,8.1,('The origin of some elements is strongly '+
                     'isotope-dependent.'),
        ha='left',va='center',fontsize=7)

# ----------------------------------------------------------------
# Construct the legend at the bottom

ns_legend_x=[1,3.5,6,8.5,11,13.5,16,18.5]
ns_legend_color=[BBN_color,cosmic_ray_color,Star_color,SNe_color,WD_color,
                 r_proc_color,s_proc_color,unstable_color]
ns_legend_text=['big bang','cosmic rays','stellar evolution',
                'supernovae','white dwarfs',
                'r-process','s-process','unstable']

for i in range(0,7):
    leg1a=patches.Rectangle((ns_legend_x[i],0.01),0.4,0.4,fill=True,lw=0.5,
                            color=ns_legend_color[i])
    ax.add_patch(leg1a)
    leg1b=patches.Rectangle((ns_legend_x[i],0.01),0.4,0.4,fill=False,lw=0.5)
    ax.add_patch(leg1b)
    ax.text(ns_legend_x[i]+0.5,0.225,ns_legend_text[i],
            ha='left',va='center',fontsize=7)
    
print('Generating pdf.')
plot.savefig('periodic_table.pdf')

# AWS, 10/10/24: I have previously found it better to generate the
# .png using Imagemagick rather than trying to save it directly to PNG
# using matplotlib.
print('Coverting pdf to png (takes a few minutes).')    
os.system('convert -density 300 periodic_table.pdf periodic_table.png')

plot.show()
    

