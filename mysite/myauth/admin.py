from django.contrib import admin

from myauth.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'short_bio', 'avatar']
    list_display_links = ['pk', 'user']
    ordering = ['pk']
    search_fields = 'pk', 'user__username',

    def get_queryset(self, request):
        return Profile.objects.select_related('user')

    def short_bio(self, obj: Profile) -> str:
        if len(obj.bio) < 48:
            return obj.bio
        else:
            return obj.bio[:48] + '...'