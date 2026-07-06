from pathlib import Path
import csv
import subprocess
import sys
import tempfile
import unittest


class PrototypeDailyTransitsTest(unittest.TestCase):
    def test_sample_counts_two_transits(self) -> None:
        repo = Path(__file__).resolve().parents[2]
        script = repo / "code" / "hormuz_tracker" / "prototype_daily_transits.py"
        sample = repo / "code" / "hormuz_tracker" / "sample_ais_positions.csv"
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "daily.csv"
            subprocess.run([sys.executable, str(script), "--input", str(sample), "--output", str(output)], check=True)
            with output.open() as f:
                rows = list(csv.DictReader(f))

        self.assertEqual(sum(int(row["transit_count"]) for row in rows), 2)
        self.assertEqual({row["vessel_class"] for row in rows}, {"crude_tanker", "lng_carrier"})
        self.assertEqual({row["coverage_flag"] for row in rows}, {"prototype_unvalidated"})


if __name__ == "__main__":
    unittest.main()
