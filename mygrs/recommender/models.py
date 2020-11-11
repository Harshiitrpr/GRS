from django.db import models

# Create your models here.
class GithubUsers(models.Model):
    username=models.CharField(unique=True, max_length=60)
    class Meta:
        verbose_name_plural = 'GitHubUser'
    
    def __str__(self):
        return str(self.username)
    
class Languages(models.Model):
    lang_name=models.CharField(max_length=60, unique=True)
    associated_number=models.IntegerField(unique=True)
    class Meta:
        verbose_name_plural = 'Languages'
    
    def __str__(self):
        return str(self.lang_name)

class User_Repo_Type_Contribution(models.Model):
    username=models.CharField(max_length=60)
    repo=models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='RepoType')
    contribution_count=models.IntegerField()
    class Meta:
        verbose_name_plural = 'User_Repo_Type_Contribution_Count'
    
    def __str__(self):
        return str(self.username)

class RepoTypes(models.Model):
    reponame=models.CharField(max_length=100, unique=True)
    repotype1=models.IntegerField()
    repotype2=models.IntegerField()
    repotype3=models.IntegerField()
    class Meta:
        verbose_name_plural = 'RepoTypes'
    
    def __str__(self):
        return str(self.reponame)

class Users_Repos(models.Model):
    username=models.CharField(max_length=60)
    repo=models.ForeignKey(RepoTypes, on_delete=models.CASCADE, related_name='user_repo')
    class Meta:
        verbose_name_plural = 'User_Repos'
    
    def __str__(self):
        return str(self.username)

class Following(models.Model):
    githubuser=models.ForeignKey(GithubUsers, on_delete=models.CASCADE, related_name='concerned_person')
    followee=models.CharField(max_length=60)
    class Meta:
        verbose_name_plural = 'Following'
    
    def __str__(self):
        return str(self.githubuser)



