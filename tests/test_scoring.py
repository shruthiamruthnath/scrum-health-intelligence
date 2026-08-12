import unittest
from datetime import date

from scrum_health.dependencies import exposure, ranked_dependencies
from scrum_health.fixtures import sample_dataset
from scrum_health.scoring import health_index, score_health
from scrum_health.service import snapshot


class ScoringTests(unittest.TestCase):
    def test_dimensions_are_bounded_and_explainable(self):
        items, deps, goal = sample_dataset()
        dimensions = score_health(items, deps, goal)
        self.assertEqual(4, len(dimensions))
        self.assertTrue(all(0 <= d.health <= 100 for d in dimensions))
        self.assertTrue(all(d.signals for d in dimensions))
        self.assertTrue(0 <= health_index(dimensions) <= 100)

    def test_negative_slack_increases_dependency_exposure(self):
        _, deps, _ = sample_dataset()
        ranked = ranked_dependencies(deps)
        self.assertLess(ranked[0]["slackDays"], 0)
        self.assertGreater(ranked[0]["exposure"], ranked[-1]["exposure"])

    def test_snapshot_contract(self):
        data = snapshot()
        self.assertIn("healthIndex", data)
        self.assertIn("risks", data)
        self.assertIn("brief", data)
        self.assertTrue(data["brief"]["evidence"])


if __name__ == "__main__": unittest.main()

