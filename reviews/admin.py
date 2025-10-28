from django.contrib import admin
from django.utils.html import format_html
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'status_badge', 'review_preview', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('name', 'role', 'text')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    actions = ['approve_reviews', 'reject_reviews']

    def status_badge(self, obj):
        """Colored badge for approval status."""
        color = '#10B981' if obj.is_approved else '#EF4444'
        text = 'Approved' if obj.is_approved else 'Pending'
        return format_html(
            '<span style="color: white; background-color: {}; padding: 4px 10px; border-radius: 8px; font-size: 12px;">{}</span>',
            color, text
        )
    status_badge.short_description = 'Status'

    def review_preview(self, obj):
        """Short preview of review text."""
        return (obj.text[:60] + '...') if len(obj.text) > 60 else obj.text
    review_preview.short_description = 'Review Preview'

    @admin.action(description='✅ Approve selected reviews')
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} review(s) approved successfully.")

    @admin.action(description='❌ Reject selected reviews')
    def reject_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} review(s) rejected successfully.")
