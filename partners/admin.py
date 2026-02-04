from django.contrib import admin
from django.utils.html import format_html
from .models import Partner, PartnerDocument, PartnerPayout, PartnerCommissionRate, PartnerNotification

class PartnerDocumentInline(admin.TabularInline):
    model = PartnerDocument
    extra = 0
    readonly_fields = ['uploaded_at']

class PartnerCommissionRateInline(admin.TabularInline):
    model = PartnerCommissionRate
    extra = 0

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = [
        'business_name', 
        'business_type', 
        'city', 
        'status_badge',
        'total_earnings', 
        'pending_payout',
        'registration_date'
    ]
    
    list_filter = ['status', 'business_type', 'city', 'is_verified']
    search_fields = ['business_name', 'contact_person', 'email', 'phone']
    readonly_fields = ['registration_date', 'updated_at', 'total_earnings', 'pending_payout', 'total_paid']
    inlines = [PartnerDocumentInline, PartnerCommissionRateInline]
    
    fieldsets = (
        ('Business Information', {
            'fields': ('user', 'business_name', 'business_type', 'registration_number', 'tax_id')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'phone', 'alternate_phone', 'email', 'website', 'address', 'city')
        }),
        ('Business Details', {
            'fields': ('description', 'year_established', 'employee_count')
        }),
        ('Payment Information', {
            'fields': ('commission_rate', 'payment_method', 'bank_name', 'bank_account', 
                      'bank_branch', 'mobile_money_provider', 'mobile_money_number')
        }),
        ('Status & Verification', {
            'fields': ('status', 'is_verified', 'verification_date', 'agreement_signed', 'agreement_date')
        }),
        ('Financial Summary', {
            'fields': ('total_earnings', 'pending_payout', 'total_paid'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('registration_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        color_map = {
            'approved': 'green',
            'pending': 'orange',
            'rejected': 'red',
            'suspended': 'gray'
        }
        color = color_map.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

@admin.register(PartnerPayout)
class PartnerPayoutAdmin(admin.ModelAdmin):
    list_display = ['partner', 'amount', 'net_amount', 'payout_method', 'status_badge', 'created_at']
    list_filter = ['status', 'payout_method', 'created_at']
    search_fields = ['partner__business_name', 'transaction_id', 'reference_number']
    readonly_fields = ['created_at', 'updated_at']
    
    def status_badge(self, obj):
        color_map = {
            'completed': 'green',
            'pending': 'orange',
            'processing': 'blue',
            'failed': 'red',
            'cancelled': 'gray'
        }
        color = color_map.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

@admin.register(PartnerNotification)
class PartnerNotificationAdmin(admin.ModelAdmin):
    list_display = ['partner', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['partner__business_name', 'title', 'message']
    readonly_fields = ['created_at']