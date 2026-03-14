from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject_display',  'status_display', 'priority_display', 'submission_date']
    list_filter = ['status', 'priority', 'subject', 'submission_date']
    search_fields = ['first_name', 'last_name', 'email', 'message']
    readonly_fields = ['submission_date', 'ip_address', 'user_agent']
    actions = ['mark_as_responded', 'escalate_priority']
    fieldsets = (('Personal Information', {'fields': ('first_name', 'last_name', 'email', 'company')}), ('Inquiry Details', {'fields': ('subject', 'message', 'is_priority', 'subscribe_newsletter')}), ('Processing Information', {'fields': ('status', 'priority', 'assigned_to', 'tags')}), ('Response Tracking', {'fields': ('response_date', 'response_notes'), 'classes': ('collapse',)}), ('Technical Information', {'fields': ('submission_date', 'ip_address', 'user_agent'), 'classes': ('collapse',)}),)
    def subject_display(self, obj): return obj.get_subject_display()
    subject_display.short_description = 'Subject'
    def status_display(self, obj):
        color_map = {'pending': 'orange', 'in_progress': 'blue', 'responded': 'green', 'resolved': 'gray', 'spam': 'red'}
        color = color_map.get(obj.status, 'black')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.get_status_display())
    status_display.short_description = 'Status'
    def priority_display(self, obj):
        color_map = {
            'normal': 'green',
            'high': 'orange',
            'emergency': 'red'
        }
        color = color_map.get(obj.priority, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_display.short_description = 'Priority'
    
    def mark_as_responded(self, request, queryset):
        for submission in queryset:
            submission.mark_as_responded(request.user)
        self.message_user(request, f"{queryset.count()} submissions marked as responded.")
    mark_as_responded.short_description = "Mark selected as responded"
    
    def escalate_priority(self, request, queryset):
        for submission in queryset:
            submission.escalate_priority()
        self.message_user(request, f"{queryset.count()} submissions escalated in priority.")
    escalate_priority.short_description = "Escalate priority of selected"


@admin.register(ContactTag)
class ContactTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_display', 'description_short']
    search_fields = ['name', 'description']
    def color_display(self, obj): return format_html('<div style="background-color: {}; width: 20px; height: 20px; border-radius: 3px;"></div>', obj.color)
    color_display.short_description = 'Color'
    def description_short(self, obj): return obj.description[:50] + '...' if obj.description else ''
    description_short.short_description = 'Description'

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
  list_display = ['user', 'action_type', 'created_at']
  list_filter = ['action_type', 'created_at']
  search_fields = ['user__username', 'action_type']
