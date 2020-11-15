with open("userRepoTypeInfo.txt") as f:
    f = f.read().splitlines()

users = open("users.txt", "a")

for line in f:
    line = line.split()
    user = line[0]
    users.write(user)
    users.write("\n")