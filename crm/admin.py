from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from crm.models import UserProfile


class CustomUserAdmin(UserAdmin):
    change_form_template = 'admin/user_change_form.html'

    def user_profile_link(self, obj):
        content_type = ContentType.objects.get_for_model(UserProfile)
        return '<a href="%s">Профиль</a>' % (
            reverse('admin:{}_{}_change'.format(content_type.app_label, content_type.model), args=(obj.profile.id,))
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if User.objects.filter(id=object_id).exists():
            extra_context['user_profile_link'] = self.user_profile_link(User.objects.get(id=object_id))
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def has_add_permission(self, request, obj=None):
        return False

    user_profile_link.allow_tags = True
    user_profile_link.short_description = 'Профиль'


class UserProfileAdmin(ModelAdmin):
    change_form_template = 'admin/user_profile_change_form.html'

    def user_link(self, obj):
        content_type = ContentType.objects.get_for_model(User)
        return '<a href="%s">Базовые поля пользователя</a>' % (
            reverse('admin:{}_{}_change'.format(content_type.app_label, content_type.model), args=(obj.user.id,))
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if UserProfile.objects.filter(id=object_id).exists():
            extra_context['user_link'] = self.user_link(UserProfile.objects.get(id=object_id))
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    user_link.allow_tags = True
    user_link.short_description = 'Профиль'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
