from django.contrib import admin
from .models import User

# admin.site.register(PendingUser)

# فلتر مخصص لعرض الزبائن أو المدراء فقط
class UserFilter(admin.SimpleListFilter):
    title = 'User Type'  # عنوان الفلتر
    parameter_name = 'user_type'  # اسم المعامل في URL

    def lookups(self, request, model_admin):
        # القيم التي ستظهر في الفلتر
        return (
            ('client', 'Clients'),           # عرض العملاء
            ('admin', 'Admins'),             # عرض المدراء
            ('exclude_clients', 'Exclude Clients'),  # الجميع ما عدا العملاء
        )

    def queryset(self, request, queryset):
        # تنفيذ الفلتر بناءً على القيم المحددة
        value = self.value()
        if value == 'client':
            return queryset.filter(is_client=True)  # العملاء فقط
        elif value == 'admin':
            return queryset.filter(is_superuser=True)  # المدراء فقط
        elif value == 'exclude_clients':
            return queryset.exclude(is_client=True)  # الجميع ما عدا العملاء
        return queryset  # إذا لم يتم تحديد قيمة، عرض الجميع

# تسجيل المستخدم في واجهة الإدارة مع إضافة الفلتر
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active')
    list_filter = (UserFilter, 'is_active')
    search_fields = ('username', 'email')

    # لا يمكن تعديل is_client من الادمن
    readonly_fields = ('is_client',)

    def get_readonly_fields(self, request, obj=None):
        # is_client دائماً readonly، ونجعل username/email/password readonly بعد الإنشاء فقط
        base_readonly = list(self.readonly_fields)
        if obj:
            base_readonly += ['username', 'email', 'password']
        return base_readonly

    def get_fields(self, request, obj=None):
        # عند الإضافة: الاسم، الايميل، كلمة المرور، is_staff، is_superuser (is_staff إجباري)
        # عند التعديل: كل شيء عدا is_client (readonly)
        if not obj:
            return ['username', 'email', 'password', 'is_staff', 'is_superuser']
        else:
            # لا تعرض is_client في التعديل (أو اجعلها readonly)
            fields = ['username', 'email', 'password', 'is_staff', 'is_superuser', 'is_active']
            # إضافة جدول السماحيات إذا لم يكن المستخدم عميل
            if not getattr(obj, 'is_client', False):
                fields += ['user_permissions', 'groups']
            return fields

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            # عند الإضافة، اجعل is_staff إجباري
            form.base_fields['is_staff'].required = True
            # عند الإضافة، اجعل is_superuser اختياري (افتراضي False)
            if 'is_superuser' in form.base_fields:
                form.base_fields['is_superuser'].required = False
            # لا تعرض is_client في الفورم
            if 'is_client' in form.base_fields:
                form.base_fields['is_client'].widget = admin.widgets.AdminHiddenInput()
        return form

    def save_model(self, request, obj, form, change):
        # عند الإضافة، اجعل is_client دائماً False
        if not change:
            obj.is_client = False
        super().save_model(request, obj, form, change)
