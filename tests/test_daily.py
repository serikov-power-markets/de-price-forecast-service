import pandas as pd

from dpfs.daily import target_day


def _now(s):
    return pd.Timestamp(s, tz="Europe/Berlin")


def test_evening_run_forecasts_tomorrow(tmp_path):
    assert target_day(_now("2026-11-18 20:30"), tmp_path) == pd.Timestamp("2026-11-19")


def test_run_delayed_past_midnight_forecasts_today(tmp_path):
    assert target_day(_now("2026-11-19 02:47"), tmp_path) == pd.Timestamp("2026-11-19")


def test_delayed_run_after_forecast_exists_moves_on(tmp_path):
    (tmp_path / "2026-11-19.csv").write_text("hour,q10,q50,q90\n", encoding="utf-8")
    assert target_day(_now("2026-11-19 02:47"), tmp_path) == pd.Timestamp("2026-11-20")


def test_morning_after_cutoff_forecasts_tomorrow(tmp_path):
    assert target_day(_now("2026-11-19 09:00"), tmp_path) == pd.Timestamp("2026-11-20")
