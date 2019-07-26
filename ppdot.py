import matplotlib.pyplot as plot
import o2sclpy

# Parse the database. The database is a list of dictionaries
# and subdictionaries. 
psrcat=[dict()]
f=open("psrcat/psrcat.db")
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
print('Read',len(psrcat),'entries.')

o2=o2sclpy.plotter()

x=[]
y=[]
for i in range(0,len(psrcat)):
    if 'P0' in psrcat[i] and 'P1' in psrcat[i]:
        x.append(float(psrcat[i]['P0']['value']))
        y.append(float(psrcat[i]['P1']['value']))

(fig,ax)=o2sclpy.default_plot(left_margin=0.14,bottom_margin=0.11,
                              right_margin=0.01,
                              top_margin=0.02,rt_ticks=True,ticks_in=True)
ax.set_xscale('log')
ax.set_yscale('log')
plot.xlim([1.0e-3,20.0])
plot.ylim([1.0e-22,1.0e-8])
plot.xlabel('$$ P~(\mathrm{s}) $$',fontsize=16)
plot.ylabel('$$ \dot{P} $$',fontsize=16)
plot.scatter(x,y,marker='.',color='black')

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


