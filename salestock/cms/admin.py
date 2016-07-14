from django.contrib import admin

# Register your models here.

class ContentManageableAdmin(object):
    """
    auto populate creator, created, last_modified_by, updated date from admin interface
    """

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
        else:
            obj.last_modified_by = request.user
        return super(ContentManageableAdmin, self).save_model(request, obj, form, change)


    def get_readonly_fields(self, request, obj=None):
        fields = list(super(ContentManageableAdmin, self).get_readonly_fields(request, obj))
        return fields + ['created', 'updated', 'creator', 'last_modified_by']

    def get_list_filter(self, request):
        fields = list(super(ContentManageableAdmin, self).get_list_filter(request))
        return fields + ['created', 'updated']

    def get_list_display(self, request):
        fields = list(super(ContentManageableAdmin, self).get_list_display(request))
        return fields + ['created', 'updated']

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ContentManageableAdmin, self).get_fieldsets(request, obj)
        for name, fieldset in fieldsets:
            for f in ('created', 'updated', 'creator', 'last_modified_by'):
                if f in fieldset['fields']:
                    fieldset['fields'].remove(f)

        return fieldsets + [("metadata", {
            'fields': [('creator', 'created'), ('last_modified_by', 'updated')],
            'classes': ('collapse', ),
        })]


class ContentManageableModelAdmin(ContentManageableAdmin, admin.ModelAdmin):
    pass