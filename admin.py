"""Django admin for the OTJ entries — this is the uni worker's review queue.

The "manual review queue" is simply: open the admin, filter ai_decision = "Manual review".
The AI's fields are read-only here; humans edit final_status (and their own notes), not
the machine's output.
"""

from django.contrib import admin

from .models import OTJEntry


@admin.register(OTJEntry)
class OTJEntryAdmin(admin.ModelAdmin):
    list_display = ("entry_id", "student_id", "ai_decision", "ai_confidence", "final_status")
    # Filter to ai_decision="Manual review" to get the queue of entries needing a human.
    list_filter = ("ai_decision", "final_status")
    # The AI writes these; a human must not hand-edit them, so show them read-only.
    readonly_fields = ("ai_decision", "ai_confidence", "ai_detail")
