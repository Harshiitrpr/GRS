with open("userRepoTypeInfo.txt") as f:
    users = f.read().splitlines() 

anss = []
iter = 0

val = open("values3.txt", 'a')

for User1 in users:
    for User2 in users:
        if(User1==User2):
            continue
        # print(User1, User2)
        user1 = User1.split()
        user2 = User2.split()
        lang1 = user1[1:]
        lang1_num = []
        lang1_type = []
        lang2 = user2[1:]
        lang2_num = []
        lang2_type = []
        ans = 0
        # print(lang1, lang2)
        for lang in lang1:
            i = 0
            while(lang[i]!='-'):
                i+=1

            lang1_num.append(int(lang[i+1:]))
            lang1_type.append(int(lang[:i]))
        
        # print(lang1_num, lang1_type)

        for lang in lang2:
            i = 0
            while(lang[i]!='-'):
                i+=1

            lang2_num.append(int(lang[i+1:]))
            lang2_type.append(int(lang[:i]))

        # print(lang2_num, lang2_type)

        for i in range(len(lang1_type)):
            if lang1_type[i] in lang2_type:
                ind = lang2_type.index(lang1_type[i])
                if(lang1_num[i]<lang2_num[ind]):
                    ans+=float(lang1_num[i])/lang2_num[ind]
                else:
                    ans+=float(lang2_num[ind])/lang1_num[i]
    
        ans = round(ans, 4)
        val.write(str(ans)+" ")
        anss.append(ans)
        iter+=1
        print("iter:",iter)

        # print("similarity index of ", user1[0], user2[0], " = ", ans)