import csv

with open("users.txt") as users:
    users = users.read().splitlines()

with open("values4.txt") as values:
    values = values.read().splitlines()

with open("userRepoTypeInfo.txt") as userInfo:
    userInfo = userInfo.read().splitlines()

repoInfo = []
with open('lang.csv', 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        repoInfo.append(row[0].split(','))

f = open("reposBasedOnSimilarity.txt", "a")
iter = 0

for i in range(len(values)):
    values[i] = values[i].split()

user = 0
maxsim = []
for value in values:
    f.write(users[user])
    if(user+12 < len(values)):
        maxsim = [[float(value[user+1]), user+1],
                  [float(user+2), user+2], [float(user+3), user+3]]
    else:
        maxsim = [[float(value[user-1]), user-1],
                  [float(user-2), user-2], [float(user-3), user-3]]
    maxsim.sort(key=lambda x: x[0])
    for i in range(len(value)):
        if(users[user] == users[i]):
            continue
        if(float(value[i]) > maxsim[0][0]):
            l = [float(value[i]), i]
            maxsim.append(l)
            maxsim.sort()
            maxsim = maxsim[1:]

    newUserInfo = (userInfo[user].split())[1:]
    userTypes = [0]*400

    for lang in newUserInfo:
        i = 0
        while(lang[i] != '-'):
            i += 1
        userTypes[int(lang[:i])] = int(lang[i+1:])

    reposScore = {}
    for i in range(3):
        for repo in repoInfo:
            if(repo[0] == users[maxsim[i][1]]):
                if(len(repo) > 2):
                    reposScore[repo[0]+"/"+repo[1]] = 0
                    for types in repo[2:]:
                        reposScore[repo[0]+"/"+repo[1]] += userTypes[int(types)]

    reposScore = sorted(reposScore.items(), key=lambda kv: (
        kv[1], kv[0]), reverse=True)
    j = 0
    for i in reposScore:
        f.write(" "+i[0])
        j += 1
        if(j == 10):
            break
    f.write("\n")
    user += 1
    print(user)
