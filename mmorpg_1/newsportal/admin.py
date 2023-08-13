from django.contrib import admin

from .forms import EmailCampaignForm
from .models import Post, Category, EmailCampaign


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at', 'categories')
    search_fields = ('title', 'content_text')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)


class EmailCampaignAdmin(admin.ModelAdmin):
    form = EmailCampaignForm
    list_display = ['title', 'sent']
    actions = ['send_selected_campaigns']

    def send_selected_campaigns(self, request, queryset):
        for campaign in queryset:
            if not campaign.sent:
                campaign.send_emails()
                campaign.sent = True
                campaign.save()

    send_selected_campaigns.short_description = "Send Selected Campaigns"

admin.site.register(EmailCampaign, EmailCampaignAdmin)





