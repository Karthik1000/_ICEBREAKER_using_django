from django.contrib import admin
from .models import GroupTable, MemberTable, CommentTable

admin.site.register(MemberTable)
admin.site.register(GroupTable)
admin.site.register(CommentTable)

