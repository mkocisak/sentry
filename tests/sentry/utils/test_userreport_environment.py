from __future__ import absolute_import

from sentry.testutils import UserReportEnvironmentTestCase
from sentry.models import GroupStatus, UserReport
from sentry.utils.userreport_environment import backfill_environment_in_userreport


class BackfillEnvironmentReportTest(UserReportEnvironmentTestCase):
    def setUp(self):
        self.project = self.create_project()
        self.env1 = self.create_environment(self.project, 'production')
        self.env2 = self.create_environment(self.project, 'staging')

        self.group = self.create_group(project=self.project, status=GroupStatus.UNRESOLVED)

        self.env1_events = self.create_events_for_environment(self.group, self.env1, 5)
        self.env2_events = self.create_events_for_environment(self.group, self.env2, 5)

        self.env1_userreports = self.create_user_report_for_events(
            self.project, self.group, self.env1_events, None)
        self.env2_userreports = self.create_user_report_for_events(
            self.project, self.group, self.env2_events, None)

    def test_simple(self):
        assert UserReport.objects.filter(environment__isnull=True)
        backfill_environment_in_userreport()
        assert not UserReport.objects.filter(environment__isnull=True)
        reports = UserReport.objects.all()
        for report in reports:
            if report in self.env1_userreports:
                assert report.environment == self.env1
            else:
                assert report.environment == self.env2
