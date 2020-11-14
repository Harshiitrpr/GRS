with open("users.txt") as user:
    user = user.read().splitlines()

with open("values3.txt") as values:
    values = values.read().splitlines()
    values = values[0].split()

user1 = input("Enter first user : ")
user2 = input("Enter second user : ")

id1 = user.index(user1)
id2 = user.index(user2)

total = len(user)

fId = total*id1 + id2
similarity = float(values[fId])
if(similarity > 0.5):
    with open("DataCorrect.txt") as repos:
        repos = repos.read().splitlines()
        user1Repos = repos[id1].split()[1:]
        user2Repos = repos[id2].split()[1:]
    
    print("Recommended for ", user1, " are ", user2Repos)
    print("Recommended for ", user2, " are ", user1Repos)

else:
    print("oops!!! they are not similar.")