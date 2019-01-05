from django.contrib import admin

# Register your models here.

from .models import Campaign, Faqs, Update, Post, comment, Backers, Reward ,RewardClaimed


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['campaign_Title', 'start_Date', 'end_Date', 'goal', 'campaign_status']
    list_editable = ['campaign_status']
    search_fields = ['campaign_status', 'campaign_Tagline']
    ordering = ['start_Date']


class BackersAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'amount', 'date_backed']
    list_filter = ['amount']


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Faqs)
admin.site.register(Update)
admin.site.register(Post)
admin.site.register(comment)
admin.site.register(Backers, BackersAdmin)
admin.site.register(Reward)
admin.site.register(RewardClaimed)
