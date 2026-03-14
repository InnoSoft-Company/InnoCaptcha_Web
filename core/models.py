from django.core.validators import EmailValidator, MinLengthValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models

User = get_user_model()

class ContactSubmission(models.Model):
  SUBJECT_CHOICES = [
    ('technical', 'Technical Support'),
    ('billing', 'Billing & Account'),
    ('sales', 'Sales Inquiry'),
    ('enterprise', 'Enterprise Plan'),
    ('partnership', 'Partnership Opportunity'),
    ('security', 'Security Concern'),
    ('feedback', 'Product Feedback'),
    ('other', 'Other'),
  ]
  STATUS_CHOICES = [
    ('pending', 'Pending Review'),
    ('in_progress', 'In Progress'),
    ('responded', 'Responded'),
    ('resolved', 'Resolved'),
    ('spam', 'Spam'),
  ]
  PRIORITY_CHOICES = [
    ('normal', 'Normal'),
    ('high', 'High Priority'),
    ('emergency', 'Emergency'),
  ]
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email = models.EmailField(max_length=255, validators=[EmailValidator()])
  company = models.CharField(max_length=200, blank=True, null=True)
  subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
  message = models.TextField(max_length=2000, validators=[MinLengthValidator(10)])
  is_priority = models.BooleanField(default=False)
  subscribe_newsletter = models.BooleanField(default=False)
  agreed_to_terms = models.BooleanField(default=True)
  submission_date = models.DateTimeField(auto_now_add=True)
  ip_address = models.GenericIPAddressField(null=True, blank=True)
  user_agent = models.TextField(blank=True, null=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
  priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
  assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_contacts')
  response_date = models.DateTimeField(null=True, blank=True)
  response_notes = models.TextField(blank=True, null=True)
  tags = models.ManyToManyField('ContactTag', blank=True)
  class Meta:
    ordering = ['-submission_date', 'priority']
    verbose_name = 'Contact Submission'
    verbose_name_plural = 'Contact Submissions'
    indexes = [models.Index(fields=['status', 'priority']), models.Index(fields=['email']), models.Index(fields=['submission_date']),]

  def __str__(self): return f"{self.first_name} {self.last_name} - {self.get_subject_display()} - {self.submission_date.strftime('%Y-%m-%d')}"
  @property
  def full_name(self): return f"{self.first_name} {self.last_name}"  
  @property
  def is_high_priority(self): return self.is_priority or self.priority in ['high', 'emergency']
  @property
  def response_time_hours(self): return (self.response_date - self.submission_date).total_seconds() / 3600 if self.response_date and self.submission_date else None

  def mark_as_responded(self, user=None):
    self.status = 'responded'
    self.response_date = timezone.now()
    if user: self.assigned_to = user
    self.save()

  def escalate_priority(self):
    if self.priority == 'normal': self.priority = 'high'
    elif self.priority == 'high': self.priority = 'emergency'
    self.save()

class ContactTag(models.Model):
  name = models.CharField(max_length=50, unique=True)
  color = models.CharField(max_length=7, default='#00d4ff', help_text='Hex color code (e.g., #00d4ff)')
  description = models.TextField(blank=True, null=True)
  class Meta: ordering = ['name']
  def __str__(self): return self.name

class ActivityLog(models.Model):
  ACTION_TYPES = (
    ('login', 'User Login'),
    ('logout', 'User Logout'),
    ('oauth_connect', 'OAuth Connection'),
    ('oauth_disconnect', 'OAuth Disconnect'),
    ('2fa_enable', '2FA Enabled'),
    ('2fa_disable', '2FA Disabled'),
    ('2fa_verify', '2FA Verification'),
    ('google_api', 'Google API Call'),
    ('github_api', 'GitHub API Call'),
    ('account_sync', 'Account Sync'),
    ('security_check', 'Security Check'),
    ('password_change', 'Password Changed'),
    ('profile_update', 'Profile Updated'),
  )
  SERVICE_TYPES = (
    ('google', 'Google'),
    ('github', 'GitHub'),
    ('authflowx', 'AuthFlowX'),
    ('system', 'System'),
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
  action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
  service = models.CharField(max_length=20, choices=SERVICE_TYPES, default='authflowx')
  description = models.TextField()
  account_email = models.CharField(max_length=255, blank=True, null=True)
  account_provider = models.CharField(max_length=50, default='AuthFlowX')
  ip_address = models.GenericIPAddressField(blank=True, null=True)
  user_agent = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  class Meta:
    ordering = ['-created_at']
    indexes = [
      models.Index(fields=['user', 'created_at']),
      models.Index(fields=['action_type', 'created_at']),
    ]
  def __str__(self): return f"{self.user.username} - {self.get_action_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
