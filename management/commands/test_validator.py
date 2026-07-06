"""Demo command: `python manage.py test_validator`.

Creates three entries that exercise the happy path and the two main failure paths,
then prints what the AI decided. Because saving an OTJEntry fires the post_save
signal, the AI runs automatically on create — we just read the results back.

Place this file at: <your_app>/management/commands/test_validator.py
"""

import datetime

from django.core.management.base import BaseCommand

# '...' walks up: commands -> management -> your app package.
from ...models import OTJEntry, KSB


# A handful of KSBs to judge against, seeded only if the table is empty.
SEED_KSBS = [
    ("K1", "Understands the principles of relational databases and how data is structured."),
    ("K2", "Understands version control and why teams use it to manage changing code."),
    ("S3", "Can write clear technical documentation for a non-technical audience."),
    ("S4", "Can debug software by forming and testing hypotheses about a fault."),
    ("B1", "Communicates clearly and adapts explanations to the listener."),
    ("B2", "Reflects on their own work and identifies what they would improve."),
]

# (entry_id, ksbs, activity_description) — one per scenario.
SCENARIOS = [
    # 1. Good: real new learning, reflection, clearly tied to the claimed KSBs.
    ("E001", "K2,S4", (
        "I hit a bug where our app showed stale data after an edit. I'd never used "
        "git bisect before, so I learned how it binary-searches commits and used it to "
        "find the commit that broke caching. I formed a hypothesis that the cache key "
        "ignored the updated timestamp, tested it by logging the key, and confirmed it. "
        "I now understand why we invalidate caches on write, which I hadn't grasped before."
    )),
    # 2. Vague: just 'did my usual tasks', no learning described -> Manual review.
    ("E002", "K1", "Did my usual daily tasks and helped out around the office as normal."),
    # 3. Mismatch: text is about spreadsheets but claims a communication behaviour.
    ("E003", "B1", (
        "I spent the afternoon tidying a spreadsheet, fixing broken VLOOKUP formulas "
        "and reformatting the columns so the totals lined up correctly."
    )),
]


class Command(BaseCommand):
    help = "Create demo OTJ entries and print the AI validation results."

    def handle(self, *args, **options):
        # Seed KSBs so the AI has descriptions to judge against.
        if not KSB.objects.exists():
            for code, description in SEED_KSBS:
                KSB.objects.create(code=code, description=description)
            self.stdout.write(f"Seeded {len(SEED_KSBS)} KSBs.")

        for entry_id, ksbs, description in SCENARIOS:
            # Start clean so the demo is repeatable.
            OTJEntry.objects.filter(entry_id=entry_id).delete()

            # Creating the entry fires the post_save signal, which runs the AI.
            entry = OTJEntry.objects.create(
                entry_id=entry_id,
                student_id="S12345",
                activity_date=datetime.date.today(),
                start_time=datetime.time(9, 0),
                end_time=datetime.time(10, 0),
                activity_description=description,
                within_contracted_hours="Yes",
                funding_eligible="Yes",
                ksbs=ksbs,
            )
            # Re-read to be sure we see the values the signal saved.
            entry.refresh_from_db()

            self.stdout.write("")
            self.stdout.write(f"{entry.entry_id}  (claimed {entry.ksbs})")
            self.stdout.write(f"  decision   : {entry.ai_decision}")
            self.stdout.write(f"  confidence : {entry.ai_confidence}")
            self.stdout.write(f"  detail     : {entry.ai_detail}")
