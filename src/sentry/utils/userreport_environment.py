"""
Script to backfill Environment into Userreports
"""
from __future__ import absolute_import

from sentry.models import Event, UserReport


def backfill_environment_in_userreport():
    for report in UserReport.objects.filter(
        environment__isnull=True,
    ):
        try:
            event = Event.objects.get(
                project_id=report.project_id,
                event_id=report.event_id,
            )
        except Event.DoesNotExist:
            continue
        else:
            report.update(environment=event.get_environment())
