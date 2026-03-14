from rest_framework import serializers
from .models import (
    ContactSubmission, ContactTag, SupportAgent,
    ContactSettings, FAQ, FAQCategory
)

class ContactSubmissionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating contact submissions
    """
    class Meta:
        model = ContactSubmission
        fields = [
            'first_name', 'last_name', 'email', 'company',
            'subject', 'message', 'is_priority', 'subscribe_newsletter'
        ]
    
    def validate_message(self, value):
        settings_obj = ContactSettings.objects.first()
        if settings_obj:
            min_length = settings_obj.min_message_length
            max_length = settings_obj.max_message_length
            
            if len(value) < min_length:
                raise serializers.ValidationError(
                    f"Message must be at least {min_length} characters long."
                )
            if len(value) > max_length:
                raise serializers.ValidationError(
                    f"Message cannot exceed {max_length} characters."
                )
        return value
    
    def validate_subject(self, value):
        valid_subjects = [choice[0] for choice in ContactSubmission.SUBJECT_CHOICES]
        if value not in valid_subjects:
            raise serializers.ValidationError(
                f"Invalid subject. Must be one of: {', '.join(valid_subjects)}"
            )
        return value


class ContactSubmissionSerializer(serializers.ModelSerializer):
    """
    Full serializer for contact submissions (read/admin use)
    """
    full_name = serializers.ReadOnlyField()
    subject_display = serializers.CharField(source='get_subject_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    response_time_hours = serializers.ReadOnlyField()
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True)
    
    class Meta:
        model = ContactSubmission
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'company',
            'subject', 'subject_display', 'message',
            'is_priority', 'subscribe_newsletter',
            'status', 'status_display', 'priority', 'priority_display',
            'submission_date', 'response_date', 'response_notes',
            'assigned_to', 'assigned_to_email', 'tags',
            'ip_address', 'user_agent', 'response_time_hours'
        ]
        read_only_fields = [
            'id', 'submission_date', 'response_date',
            'ip_address', 'user_agent'
        ]


class ContactTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactTag
        fields = ['id', 'name', 'color', 'description']


class SupportAgentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = SupportAgent
        fields = [
            'id', 'user', 'user_email', 'user_full_name',
            'department', 'specializations', 'max_assigned_tickets',
            'is_available', 'average_response_time', 'resolved_count',
            'emergency_contact', 'working_hours'
        ]


class ContactSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSettings
        fields = '__all__'
        read_only_fields = ['updated_at']


class FAQSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = FAQ
        fields = [
            'id', 'question', 'answer', 'category', 'category_name',
            'order', 'is_active', 'views_count', 'helpful_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['views_count', 'helpful_count', 'created_at', 'updated_at']


class FAQCategorySerializer(serializers.ModelSerializer):
    faq_count = serializers.SerializerMethodField()
    
    class Meta:
        model = FAQCategory
        fields = ['id', 'name', 'description', 'icon', 'order', 'faq_count']
    
    def get_faq_count(self, obj):
        return obj.faqs.filter(is_active=True).count()
