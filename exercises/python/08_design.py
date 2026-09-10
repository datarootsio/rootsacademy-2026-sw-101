"""Design principles: DRY, KISS, SRP, OCP, LSP, DIP.

Six refactorings. Most of the code below already works – the exercise is to
change its shape, not its answers.

Several assertions test the *design* rather than the result. One fails while a
business rule is still written in three places; one fails if you add a format
by editing the dispatcher; one fails while a dependency is still hard-coded.
Read the message on the assertion: it names the principle you owe.

The reference solution is in solutions/08_design.py – look there only after you
have tried.
"""

from __future__ import annotations

import inspect
from datetime import date
from decimal import ROUND_CEILING, Decimal

# ────────────────────────────── 1. DRY ──────────────────────────────
# "Luxembourg charges 21% VAT" is one fact about the business. Right now it is
# written in three places, and one copy is already stale.
#
# Put the fact in VAT_RATES, make vat_for read it, and make the other two use
# vat_for. The tax office should need one edit.

VAT_RATES = {}  # TODO country code -> rate, as Decimal


def vat_for(country):
    """The VAT rate for a country code; zero for countries we do not charge."""
    if country in ("BE", "NL", "LU"):
        return Decimal("0.21")
    if country == "FR":
        return Decimal("0.20")
    return Decimal("0")


def invoice_total(amount, country):
    """Amount including VAT."""
    if country in ("BE", "NL", "LU"):
        return amount * Decimal("1.21")
    if country == "FR":
        return amount * Decimal("1.20")
    return amount


def quote_total(amount, country):
    """A quote: VAT included, then rounded up to whole euros."""
    if country in ("BE", "LU"):  # someone forgot the Netherlands
        amount = amount * Decimal("1.21")
    return amount.to_integral_value(rounding=ROUND_CEILING)


# ────────────────────────────── 2. KISS ─────────────────────────────
# status_clever works. Nobody can read it, and nobody dares change it.
# Write status() so that it gives the same answer and needs no explanation.


def status_clever(score):
    return ["fail", "warn", "ok"][(score > 50) + (score > 90)]


def status(score):
    """'ok' above 90, 'warn' above 50, otherwise 'fail'."""
    raise NotImplementedError("your turn")


# ────────────────────────────── 3. SRP ──────────────────────────────
# One function, four reasons to change: the line format, the definition of a
# billable row, the aggregation, and the report layout.
#
# Split it into the four stages it already contains, then rebuild report() out
# of them. Each stage must be usable on its own.

RAW_LINES = ["BE,100.00", "NL,50.00", "BE,-10.00", "FR,oops", "BE,25.00"]


def load_and_clean_and_report(lines):
    """The original. Leave it here to compare against."""
    totals = {}
    for line in lines:
        country, raw = line.split(",")
        try:
            amount = Decimal(raw)
        except ArithmeticError:
            continue
        if amount <= 0:
            continue
        totals[country] = totals.get(country, Decimal("0")) + amount
    return "\n".join(f"{c}: {t:.2f}" for c, t in sorted(totals.items()))


def parse_line(line):
    """'BE,100.00' -> ('BE', Decimal('100.00')). None if it is not a row."""
    raise NotImplementedError("your turn")


def is_billable(row):
    """A parsed row we should count."""
    raise NotImplementedError("your turn")


def totals_by_country(rows):
    """Sum the amounts per country code."""
    raise NotImplementedError("your turn")


def format_report(totals):
    """'BE: 125.00\\nFR: 0.00', sorted by country."""
    raise NotImplementedError("your turn")


def report(lines):
    """The same output as load_and_clean_and_report, built from the stages."""
    raise NotImplementedError("your turn")


# ────────────────────────────── 4. OCP ──────────────────────────────
# Add a jsonl reader. read_rows already knows how to dispatch, so it must not
# change – the assertion below checks that you did not touch it.


class UnsupportedFormat(Exception):
    """No reader is registered for this format."""


def read_csv_text(text):
    """'a,1\\nb,2' -> [{'code': 'a', 'value': '1'}, ...]"""
    rows = []
    for line in text.splitlines():
        if line.strip():
            code, value = line.split(",")
            rows.append({"code": code, "value": value})
    return rows


def read_jsonl_text(text):
    """'{"code": "a", "value": "1"}' per line -> the same list of dicts."""
    raise NotImplementedError("your turn")


READERS = {"csv": read_csv_text}
# TODO register the jsonl reader here


def read_rows(fmt, text):
    """Do not edit this function. That is the whole point of the exercise."""
    try:
        reader = READERS[fmt]
    except KeyError:
        raise UnsupportedFormat(fmt) from None
    return reader(text)


# ────────────────────────────── 5. LSP ──────────────────────────────
# LoggingCache is used everywhere a Cache is, but it raises where its parent
# returned a default – so lookup_all() breaks for that one subclass.
# Fix the subclass. Do not touch lookup_all or Cache.


class Cache:
    def __init__(self, data=None):
        self._data = dict(data or {})

    def get(self, key, default=None):
        return self._data.get(key, default)


class LoggingCache(Cache):
    """A Cache that remembers which keys were asked for."""

    def __init__(self, data=None):
        super().__init__(data)
        self.asked = []

    def get(self, key, default=None):
        self.asked.append(key)
        if key not in self._data:
            raise KeyError(key)
        return self._data[key]


def lookup_all(cache, keys):
    """Do not edit. Written against Cache, so it must work for every Cache."""
    return [cache.get(key, "n/a") for key in keys]


# ────────────────────────────── 6. DIP ──────────────────────────────
# daily_total_hardcoded reaches out for the clock and the rate service, so it
# cannot be tested at all. Write daily_total(rows, rates, today) instead, and
# a four-line FixedRates to test it with.
#
# A row is (day, amount, currency).

ROWS = [
    (date(2026, 1, 5), Decimal("100"), "EUR"),
    (date(2026, 1, 5), Decimal("100"), "USD"),
    (date(2026, 1, 4), Decimal("999"), "EUR"),
]


class LiveRates:
    """The real one: euros per unit of currency, over the network."""

    def eur(self, currency):
        raise RuntimeError("no network in a test")


def daily_total_hardcoded(rows):
    """The original."""
    today = date.today()
    rate = LiveRates().eur("USD")
    return sum(
        amount * (rate if currency == "USD" else Decimal("1"))
        for day, amount, currency in rows
        if day == today
    )


class FixedRates:
    """A stand-in for the rate service: 1 for EUR, the given value otherwise."""

    def __init__(self, value):
        raise NotImplementedError("your turn")

    def eur(self, currency):
        raise NotImplementedError("your turn")


def daily_total(rows, rates, today):
    """One day's rows, converted with rates.eur(currency). No clock, no network."""
    raise NotImplementedError("your turn")


if __name__ == "__main__":
    assert vat_for("NL") == Decimal("0.21")
    assert invoice_total(Decimal("100"), "NL") == Decimal("121")
    assert quote_total(Decimal("100"), "NL") == invoice_total(Decimal("100"), "NL"), (
        "DRY: the quote still uses its own stale copy of the rule"
    )
    assert quote_total(Decimal("100.10"), "BE") == Decimal("122"), (
        "a quote still rounds up – share the fact, not the behaviour"
    )
    VAT_RATES["ES"] = Decimal("0.21")
    try:
        assert vat_for("ES") == Decimal("0.21"), "DRY: vat_for does not read VAT_RATES"
        assert invoice_total(Decimal("100"), "ES") == Decimal("121"), (
            "DRY: invoice_total does not go through vat_for"
        )
        assert quote_total(Decimal("100"), "ES") == Decimal("121"), (
            "DRY: quote_total does not go through vat_for"
        )
    finally:
        del VAT_RATES["ES"]
    print("1 DRY ok – one edit changes every caller")

    for score in range(-10, 111):
        assert status(score) == status_clever(score), f"different answer for {score}"
    print("2 KISS ok – same answers, and you can read it")

    assert parse_line("BE,100.00") == ("BE", Decimal("100.00"))
    assert parse_line("FR,oops") is None
    assert is_billable(("BE", Decimal("10"))) is True
    assert is_billable(("BE", Decimal("-10"))) is False
    assert totals_by_country([("BE", Decimal("10")), ("BE", Decimal("5"))]) == {
        "BE": Decimal("15")
    }
    assert format_report({"FR": Decimal("2"), "BE": Decimal("1")}) == "BE: 1.00\nFR: 2.00"
    assert report(RAW_LINES) == load_and_clean_and_report(RAW_LINES)
    print("3 SRP ok – four stages, four tests, same output")

    assert read_rows("csv", "a,1\nb,2") == [
        {"code": "a", "value": "1"},
        {"code": "b", "value": "2"},
    ]
    assert read_rows("jsonl", '{"code": "a", "value": "1"}') == [
        {"code": "a", "value": "1"}
    ]
    try:
        read_rows("xml", "<rows/>")
    except UnsupportedFormat:
        pass
    else:
        raise AssertionError("an unknown format must raise UnsupportedFormat")
    assert "jsonl" not in inspect.getsource(read_rows), (
        "OCP: you extended the dispatcher by editing it"
    )
    print("4 OCP ok – a new format touched no working code")

    data = {"a": 1, "b": 2}
    logging_cache = LoggingCache(data)
    assert lookup_all(logging_cache, ["a", "zz"]) == lookup_all(Cache(data), ["a", "zz"])
    assert logging_cache.asked == ["a", "zz"], "the subclass must still do its own job"
    print("5 LSP ok – the subclass no longer surprises its callers")

    parameters = inspect.signature(daily_total).parameters
    assert "rates" in parameters and "today" in parameters, (
        "DIP: pass the rate service and the date in, do not reach for them"
    )
    assert daily_total(ROWS, FixedRates("0.90"), date(2026, 1, 5)) == Decimal("190.00")
    assert daily_total(ROWS, FixedRates("0.50"), date(2026, 1, 5)) == Decimal("150.00")
    assert daily_total(ROWS, FixedRates("0.90"), date(2026, 1, 4)) == Decimal("999")
    print("6 DIP ok – deterministic, and tested without a network")

    print("\nAll design exercises pass.")
