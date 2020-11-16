from django.http import HttpResponse
from django.shortcuts import render
from .models import GithubUsers, Languages, User_Repo_Type_Contribution, RepoTypes, Users_Repos, Following
import csv
import json

def home(request):
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
    return render(request, 'recommender/userEntered.html', {'userdata':file_sent})

def follow(request):
    return render(request, 'recommender/follow.html')


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
