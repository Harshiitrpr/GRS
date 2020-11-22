from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import GithubUsers, Languages, User_Repo_Type_Contribution, RepoTypes, Users_Repos, Following, recommendedReposSimilarity, recommendedfollowing
import csv
import json

def home(request):
    # reposSimilarity()
    if(request.method == 'POST'):
        username = request.POST.get('username')
        return redirect('entered-user', username)
    return render(request, 'recommender/home.html')

def about(request):
    return render(request, 'recommender/about.html')

def userEntered(request, name):
    repos=User_Repo_Type_Contribution.objects.filter(username=name)
    if(len(repos)>0):
        file_sent=[]
        count=0
        for x in repos:
            file_sent.append([x.repo.lang_name, x.contribution_count])
            count+=x.contribution_count
        file_sent=sorted(file_sent, key=lambda x: x[1], reverse=True)
        file_sent=[[x[0], round(float(x[1])/count*100, 2)] for x in file_sent]
        file_sent=json.dumps(file_sent)
    else:
        file_sent='Error'
    return render(request, 'recommender/userEntered.html', {'userdata':file_sent, 'name' : name})

def follow(request):
    return render(request, 'recommender/follow.html')

def recommendedRepos(request, name):
    reposobj=recommendedReposSimilarity.objects.filter(user=name)
    return render(request, 'recommender/recommendedRepos.html', {'repos':reposobj})

def recommendedFollowers(request, name):
    recommendFollowee=recommendedfollowing.objects.filter(user=name)
    return render(request, 'recommender/recommendedFollowers.html', {'followee' : recommendFollowee})


# For database entries
def UserEntries():
    f=open('/home/captain/GRS/DataCorrect.txt', 'r')
    lines=f.read().splitlines()
    for line in lines:
        user=line.split()[0]
        check=GithubUsers.objects.filter(username=user)
        if(len(check)>0):
            continue
        a=GithubUsers(username=user)
        a.save()

def language_entries():
    f=open('/home/captain/GRS/languages.txt', 'r')
    lines=f.read().splitlines()
    for line in lines:
        lang=line.split()
        s=''
        for i in range(len(lang)-1):
            s+=lang[i]
            s+=' '
        a=Languages(lang_name=s, associated_number=int(lang[len(lang)-1]))
        a.save()

def user_repo_type_entries():
    with open("/home/captain/GRS/userRepoTypeInfo.txt") as f:
        lines = f.read().splitlines() 
    for line in lines:
        user = line.split()
        lang1 = user[1:]
        check=User_Repo_Type_Contribution.objects.filter(username=user[0])
        if(len(check)>0):
            continue
        for lang in lang1:
            i = 0
            while(lang[i]!='-'):
                i+=1
            if(int(lang[:i])<=1 or int(lang[:i])>191):
                continue
            language=Languages.objects.get(associated_number=int(lang[:i]))
            a=User_Repo_Type_Contribution(username=user[0], repo=language, contribution_count=int(lang[i+1:]))
            a.save()

def RepoTypesEntries():
    with open('/home/captain/GRS/lang.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if(len(row)<=1):
                continue
            if(len(RepoTypes.objects.filter(reponame=row[1]))>0):
                continue
            l=[-1, -1, -1]
            for i in range(2, min(5,len(row))):
                l[i-2]=int(row[i])
            a=RepoTypes(reponame=row[1], repotype1=l[0], repotype2=l[1], repotype3=l[2])
            a.save()
            line_count += 1
            print(line_count)
    print(f'Processed {line_count} lines.')

def UserReposEntries():
    with open('/home/captain/GRS/lang.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if(len(row)<=1):
                continue
            repo=RepoTypes.objects.get(reponame=row[1])
            check=Users_Repos.objects.filter(username=row[0], repo=repo)
            if(len(check)>0):
                continue
            a=Users_Repos(username=row[0], repo=repo)
            a.save()
            line_count += 1
        print(f'Processed {line_count} lines.')

def FollowingEntries():
    f=open('/home/captain/GRS/userFollowingData.txt', 'r')
    lines=f.read().splitlines()
    for line in lines:
        users=line.split()
        user=GithubUsers.objects.get(username=users[0])
        for i in range(1, len(users)):
            check=Following.objects.filter(githubuser=user, followee=users[i])
            if(len(check)>0):
                continue
            a=Following(githubuser=user, followee=users[i])
            a.save()

def reposSimilarity():
    f=open('/home/captain/GRS/reposBasedOnSimilarity1.txt', 'r')
    lines= f.read().splitlines()
    for line in lines:
        repos = line.split()
        user = repos[0]
        repos=repos[1:]
        for i in repos:
            x=i.split('/')
            check=recommendedReposSimilarity.objects.filter(user=user, reponame=x[1])
            if(len(check)>0):
                continue
            try:
                find = RepoTypes.objects.get(reponame=x[1])
            except:
                continue
            try:
                lang=Languages.objects.get(associated_number=find.repotype1)
            except:
                continue
            a = recommendedReposSimilarity(user = user, reponame=x[1],similaruser=x[0], repotype=lang, similarity=x[2])
            a.save()

def reposFollowing():
    f=open('/home/captain/GRS/Recommended-repos.txt', 'r')
    lines= f.read().splitlines()
    for line in lines:
        repos = line.split()
        user = repos[0]
        if(len(repos)<2):
            continue
        candidate=repos[1]
        repos = repos[2:]
        for i in repos:
            ch=len(i)-1
            a1=''
            a2=''
            while(i[ch]!='-'):
                a1+=i[ch]
                ch-=1
            for r in range(len(a1)-1, -1, -1):
                a2+=a1[r]
            a1=i[:ch]
            check=recommendedReposSimilarity.objects.filter(user=user, reponame=a1)
            if(len(check)>0):
                continue
            a = recommendedReposSimilarity(user = user, reponame=a1,similaruser=candidate, repotype=a2)
            a.save()
    
def followingSimilarity():
    f=open('/home/captain/GRS/followersrecommended.txt', 'r')
    lines= f.read().splitlines()
    for line in lines:
        repos = line.split()
        user = repos[0]
        repos = repos[1:]
        for i in repos:
            x = i.split('/')
            if(len(x) == 2): 
                check=recommendedfollowing.objects.filter(user=user, followee=x[1])
                if(len(check)>0):
                    continue
                a = recommendedfollowing(user = user, similar=0.0, followee=x[1], source=x[0])
                a.save()
            elif(len(x) == 3): 
                if(x[0]!='similar'):
                    continue
                check=recommendedfollowing.objects.filter(user=user, followee=x[1])
                if(len(check)>0):
                    continue
                a = recommendedfollowing(user = user, similar=float(x[2]), followee=x[1], source='none')
                a.save()