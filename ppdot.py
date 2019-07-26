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
