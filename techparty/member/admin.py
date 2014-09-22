#encoding=utf-8

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from techparty.member.models import User, UserLink


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User

    def clean_password(self):
        return self.initial["password"]


class UserLinkInline(admin.StackedInline):
    model = UserLink
    extra = 1


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id','username', 'first_name',  'is_superuser', 'is_lecturer')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', )}),
        (u'基本信息', {'fields': ('password',
                                'email',
                                'is_lecturer',
                                'description',
                                'company',
                                'title',
                                'tags',
                                'avatar',
                                )}),
        (u'用户权限', {
            'fields': ('is_superuser',
                       'is_staff',
                       'groups'),
            'classes': ('collapse',)
            }),
    )
    inlines = [UserLinkInline]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),
    )
    search_fields = ('username', 'first_name', 'email')
    ordering = ('username', )
    filter_horizontal = ()

admin.site.register(User, MyUserAdmin)
