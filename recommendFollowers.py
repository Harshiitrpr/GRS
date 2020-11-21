f=open("/home/captain/GRS/userFollowingData.txt", 'r')
lines=f.read().splitlines()

similar=open('/home/captain/GRS/values4.txt', 'r')
s=similar.read().splitlines()

followee={}
for line in lines:
    users=line.split()
    followee[users[0]]=users[1:]

filee=open('/home/captain/GRS/followersrecommended.txt', 'a')

fileuser=open('/home/captain/GRS/users.txt', 'r')
fileusers=fileuser.read().splitlines()


for counter in range(len(lines)):
    
    line=lines[counter]
    users=line.split()
    filee.write(users[0]+' ')
    count=0
    for user in users[1:]:
        if(user in followee.keys()):
            for x in followee[user]:
                if x not in users[1:]:
                    count+=1
                    filee.write(user+'/'+x+' ')
    
    lst=s[counter].split()
    for x in range(1965):
        if(fileusers[x]==users[0]):
            continue
        if(count>20):
            break
        check=0
        try:
            check=float(lst[x])
        except:
            continue
        if(check>5.0):
            filee.write('similar/'+fileusers[x]+'/'+lst[x]+' ')
            count+=1
    
    for x in range(1965):
        if(fileusers[x]==users[0]):
            continue
        if(count>20):
            break
        check=0
        try:
            check=float(lst[x])
        except:
            continue
        if(check>3.0 and check<=5.0):
            filee.write('similar/'+fileusers[x]+'/'+lst[x]+' ')
            count+=1
    
    for x in range(1965):
        if(fileusers[x]==users[0]):
            continue
        if(count>20):
            break
        check=0
        try:
            check=float(lst[x])
        except:
            continue
        if(check>2.0 and check<=3.0):
            filee.write('similar/'+fileusers[x]+'/'+lst[x]+' ')
            count+=1
    filee.write('\n')
filee.close()