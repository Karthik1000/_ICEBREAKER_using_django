from django.contrib import admin
from .models import Profile,Temp
# Register your models here.
'''
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','status')
    list_filter = ('status','created','updated')
    search_fields = ('author__username','title')
    prepopulated_fields  = {'slug':('title',)}
    list_editable = ('status',)
    date_hierarchy = ('created')
'''
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','dob','photo','github_link')

#admin.site.register(post, PostAdmin)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Temp)
