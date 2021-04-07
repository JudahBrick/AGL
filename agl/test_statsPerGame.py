import unittest
import leagueDocs.agl.StatsPerGame as StatsPerGame


class TestStatsPerGame(unittest.TestCase):

    def test_wins_and_losses(self):
        stats = StatsPerGame.StatsPerGame("test game", [])
        stats.add_result(True, "")
        stats.add_result(True, "")
        stats.add_result(True, "")
        stats.add_result(False, "")
        stats.add_result(False, "")
        stats.add_result(False, "")
        stats.add_result(False, "")
        self.assertEqual(stats.get_win_loss_string(), "3-4")


    def test_vanilla_basketball(self):
        stats = StatsPerGame.StatsPerGame("Basketball", [])
        stats.add_result(False, "105-100")
        stats.add_result(True, "50-49")
        self.assertEqual(stats.avg_score, (100 + 50) / 2)
        self.assertEqual(stats.high_score, 100)
        self.assertEqual(stats.lowest_score, 50)
        self.assertEqual(stats.avg_win_differential, 1)
        self.assertEqual(stats.total_ots, 0)
        self.assertEqual(stats.win_percentage, 50.0)

    def test_basketball_with_ots(self):
        stats = StatsPerGame.StatsPerGame("Basketball", [])
        stats.add_result(True, "100-100:103-101")
        stats.add_result(True, "50-49")
        self.assertEqual(stats.avg_score, (100 + 103 + 50) / 3)
        self.assertEqual(stats.high_score, 103)
        self.assertEqual(stats.lowest_score, 50)
        self.assertEqual(stats.avg_win_differential, (2 + 1) / 2)
        self.assertEqual(stats.total_ots, 1)

    def test_vanilla_cup_pong(self):
        stats = StatsPerGame.StatsPerGame("Cup Pong", [])
        stats.add_result(False, "10")
        stats.add_result(True, "5")
        stats.add_result(True, "2")
        self.assertEqual(stats.avg_score, (-10 + 5 + 2) / 3)
        self.assertEqual(stats.high_score, 5)
        self.assertEqual(stats.lowest_score, -10)
        self.assertEqual(stats.avg_win_differential, (5 + 2) / 2)
        self.assertEqual(stats.total_ots, 0)

    def test_cup_pong_with_ots(self):
        stats = StatsPerGame.StatsPerGame("Cup Pong", [])
        stats.add_result(False, "10")
        stats.add_result(True, "5")
        stats.add_result(True, "1 OT 2")
        self.assertEqual(stats.avg_score, (-10 + 5 + 2) / 3)
        self.assertEqual(stats.high_score, 5)
        self.assertEqual(stats.lowest_score, -10)
        self.assertEqual(stats.avg_win_differential, (5 + 2) / 2)
        self.assertEqual(stats.total_ots, 1)


if __name__ == '__main__':
    unittest.main()
