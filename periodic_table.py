import numpy as np

Z_arr=[]
name_arr=[]
wgt_arr=[]

df=np.genfromtxt('ciaaw_edit.txt',dtype='str')

for i in range(0,len(df)):
    print('h',i,df[i][4])
    name_arr.append(df[i][0])
    Z_arr.append(df[i][4])
    note=df[i][2]
    #
    if df[i][8][0]='(':
        last_digit=df[i][8][1]
        # Count digits after decimal
        
    #
    if note=='v':
        wgt_arr.append(df[i][7]+','+df[i][8])
    elif note=='u':
        wgt_arr.append('['+df[i][7]+']')
    elif note=='g':
        if float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \pm $ '+df[i][8]+'$^g$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='gr':
        if float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \pm $ '+df[i][8]+'$^{gr}$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='gm':
        if float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \pm $ '+df[i][8]+'$^{gm}$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='m':
        if float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \pm $ '+df[i][8]+'$^{m}$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='r':
        if float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \pm $ '+df[i][8]+'$^r$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='s':
        if float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \pm $ '+df[i][8]+'$^s$')
        else:
            wgt_arr.append(df[i][7])
    elif note=='b':
        wgt_arr.append('['+df[i][7]+' $ -- $ '+df[i][8]+']')
    elif note=='bm':
        wgt_arr.append('['+df[i][7]+' $ -- $ '+df[i][8]+'] $^m$')
    elif note=='n':
        if float(df[i][8])>0.0:
            wgt_arr.append(df[i][7]+' $ \pm $ '+df[i][8])
        else:
            wgt_arr.append(df[i][7])

print(len(name_arr),len(Z_arr),len(wgt_arr))
