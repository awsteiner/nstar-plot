import matplotlib.pyplot as plot
import o2sclpy

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

o2=o2sclpy.plotter()

(fig,ax)=o2sclpy.default_plot(left_margin=0.14,bottom_margin=0.11,
                              right_margin=0.01,
                              top_margin=0.02,rt_ticks=True,ticks_in=True)
ax.set_xscale('log')
ax.set_yscale('log')
plot.xlim([1.0e-3,20.0])
plot.ylim([1.0e-22,1.0e-8])
plot.xlabel('$$ P~(\mathrm{s}) $$',fontsize=16)
plot.ylabel('$$ \dot{P} $$',fontsize=16)

x=[]
y=[]
for i in range(0,len(psrcat)):
    if 'P0' in psrcat[i] and 'P1' in psrcat[i]:
        x.append(float(psrcat[i]['P0']['value']))
        y.append(float(psrcat[i]['P1']['value']))

plot.scatter(x,y,marker='.',color='black')

x=[]
y=[]
for i in range(0,len(rrats)):
    if rrats[i]['P']!='--' and rrats[i]['Pdot']!='--':
        x.append(float(rrats[i]['P']))
        y.append(float(rrats[i]['Pdot'])*1.0e-15)
        print(x[len(x)-1],y[len(y)-1])

plot.scatter(x,y,marker='s',color='blue')

for logB in range(8,16):
    yleft=(10.0**logB/3.3e19)**2.0/1.0e-3
    plot.plot([1.0e-3,20.0],[yleft,
                             (10.0**logB/3.3e19)**2.0/20.0],ls=':',
              color='black')
    if logB>8 and logB<14:
        ax.text(1.6e-3,yleft*0.9,'$$ 10^{'+str(logB)+'}~\mathrm{G} $$',
                fontsize=12)

for log_tau in range(2,12):
    yright=0.5/(10.0**log_tau*31556926)*20.0
    plot.plot([1.0e-3,20.0],[0.5/(10.0**log_tau*31556926)*1.0e-3,
                             yright],ls=':',
              color='blue')
    if log_tau>1:
        ax.text(7.0,yright*1.0,'$$ 10^{'+str(log_tau)+'}~\mathrm{yr} $$',
                fontsize=12,color='blue')

plot.savefig('ppdot.pdf')        
plot.show()


