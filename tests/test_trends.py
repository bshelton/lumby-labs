import unittest
from datetime import datetime, timezone
from trends import record, render, PLUGIN

class TrendsTest(unittest.TestCase):
    def test_collection_and_rerun(self):
        now=datetime(2026,10,29,tzinfo=timezone.utc)
        rows=record([], {PLUGIN:6}, now)
        self.assertEqual(record(rows,{PLUGIN:10},now),rows)
        self.assertEqual(record(rows,{PLUGIN:0},datetime(2026,10,30,tzinfo=timezone.utc))[-1]['count'],0)

    def test_bad_responses_do_not_become_zero(self):
        for payload in ({}, {PLUGIN:None}, {PLUGIN:True}, {PLUGIN:-1}, {PLUGIN:'6'}, []):
            with self.assertRaises(ValueError):
                record([],payload,datetime.now(timezone.utc))

    def test_render_single_and_missing_days(self):
        rows=record([],{PLUGIN:6},datetime(2026,10,29,tzinfo=timezone.utc))
        self.assertIn('first snapshot',render(rows))
        rows=record(rows,{PLUGIN:9},datetime(2026,10,31,tzinfo=timezone.utc))
        self.assertNotIn('class="chart-line"',render(rows))
        self.assertIn('+3 since',render(rows))
        rows=record(rows,{PLUGIN:4},datetime(2026,11,1,tzinfo=timezone.utc))
        self.assertEqual(render(rows).count('class="chart-line"'),1)

    def test_zero_counts_render(self):
        rows=record([],{PLUGIN:0},datetime(2026,10,29,tzinfo=timezone.utc))
        self.assertIn('0 active installs',render(rows))
