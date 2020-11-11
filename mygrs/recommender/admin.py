from django.contrib import admin
from .models import RepoTypes, GithubUsers, User_Repo_Type_Contribution, Users_Repos, Languages, Following

admin.site.register(RepoTypes)
admin.site.register(User_Repo_Type_Contribution)
admin.site.register(Users_Repos)
admin.site.register(Languages)
admin.site.register(Following)
admin.site.register(GithubUsers)
# Register your models here.
