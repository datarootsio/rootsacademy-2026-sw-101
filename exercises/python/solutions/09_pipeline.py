"""Case study: the sales job that runs at 02:00.

Yesterday's export arrives as rows of text. Add VAT, convert to euros, total
per country – and account for every row you could not use.

The rules the job is judged on:

* a row that cannot be used is **reported**, never silently dropped;
* the logic takes the clock and the rate service as arguments, so it gives the
  same answer on any day, on any machine, with the network unplugged;
* a new input format is a new function, not an edit to a working one.

A raw row is ``order_id,day,amount,currency,country``. A rejection reason is
one of ``"wrong number of fields"``, ``"bad date"``, ``"bad amount"``,
``"unknown country"`` – the assertions check the exact string.

Reference solution for 09_pipeline.py.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from json import loads


class PipelineError(Exception):
    """Base for everything this module raises."""


class UnknownCountry(PipelineError):
    """No VAT rate is configured for this country."""


class UnsupportedFormat(PipelineError):
    """No reader is registered for this file extension."""


@dataclass(frozen=True)
class Sale:
    order_id: str
    day: date
    amount: Decimal
    currency: str
    country: str


@dataclass(frozen=True)
class Rejected:
    line: int
    raw: str
    reason: str


@dataclass(frozen=True)
class Result:
    totals: dict
    rejected: list


VAT_RATES = {
    "BE": Decimal("0.21"),
    "NL": Decimal("0.21"),
    "LU": Decimal("0.21"),
    "FR": Decimal("0.20"),
}

RAW_ROWS = [
    "ORD-1,2026-01-05,100.00,EUR,BE",
    "ORD-2,2026-01-04,999.00,EUR,BE",
    "ORD-3,05/01/2026,50.00,EUR,BE",
    "ORD-4,2026-01-04,10.00,EUR,NL",
    "ORD-5,2026-01-05,ten,EUR,BE",
]

MORE_ROWS = [
    "ORD-6,2026-01-05,100.00,EUR,ZZ",
    "ORD-7,2026-01-05,100.00",
    "ORD-8,2026-01-05,100.00,USD,NL",
]


# ───────────────────────────── 1. the boundary ─────────────────────────────


def parse_row(line, raw):
    """A raw row -> a Sale, or a Rejected carrying the line number and reason.

    This function never raises and never returns None. Country codes come back
    uppercased.
    """
    fields = [field.strip() for field in raw.split(",")]
    if len(fields) != 5:
        return Rejected(line, raw, "wrong number of fields")

    order_id, raw_day, raw_amount, currency, country = fields
    try:
        day = date.fromisoformat(raw_day)
    except ValueError:
        return Rejected(line, raw, "bad date")
    try:
        amount = Decimal(raw_amount)
    except InvalidOperation:
        return Rejected(line, raw, "bad amount")

    return Sale(order_id, day, amount, currency.upper(), country.upper())


# ────────────────────────────── 2. the rules ───────────────────────────────


def vat_for(country):
    """The VAT rate for a country code. Raises UnknownCountry."""
    try:
        return VAT_RATES[country.upper()]
    except KeyError:
        raise UnknownCountry(country) from None


def net_to_gross(sale, rates):
    """The sale in euros, VAT included, using rates.eur(currency)."""
    return sale.amount * rates.eur(sale.currency) * (1 + vat_for(sale.country))


# ───────────────────────────── 3. the pipeline ─────────────────────────────


def run(rows, rates, today):
    """Fold raw rows into totals per country plus the rows that were rejected.

    Only rows dated `today` are counted; rows from another day are neither
    counted nor rejected. `rows` may be any iterable, including a generator.
    """
    totals = defaultdict(Decimal)
    rejected = []

    for line, raw in enumerate(rows, 1):
        parsed = parse_row(line, raw)
        if isinstance(parsed, Rejected):
            rejected.append(parsed)
            continue
        if parsed.day != today:
            continue
        try:
            gross = net_to_gross(parsed, rates)
        except UnknownCountry:
            rejected.append(Rejected(line, raw, "unknown country"))
            continue
        totals[parsed.country] += gross

    return Result(dict(totals), rejected)


# ──────────────────────────────── 4. a fake ────────────────────────────────


class FixedRates:
    """A stand-in for the rate service: 1 for EUR, the given value otherwise."""

    def __init__(self, value):
        self.value = Decimal(value)

    def eur(self, currency):
        return Decimal("1") if currency == "EUR" else self.value


# ──────────────────────────── 5. a second format ───────────────────────────


def read_csv_rows(text):
    """Yield the non-empty lines of a CSV export."""
    for line in text.splitlines():
        if line.strip():
            yield line.strip()


def read_jsonl_rows(text):
    """One JSON object per line -> the same comma-separated rows as the CSV.

    Keys: order_id, day, amount, currency, country.
    """
    fields = ("order_id", "day", "amount", "currency", "country")
    for line in text.splitlines():
        if line.strip():
            record = loads(line)
            yield ",".join(str(record[field]) for field in fields)


READERS = {".csv": read_csv_rows, ".jsonl": read_jsonl_rows}


def read_rows(suffix, text):
    """Dispatch only. A new format is a new entry in READERS, never an edit here."""
    try:
        reader = READERS[suffix]
    except KeyError:
        raise UnsupportedFormat(suffix) from None
    return reader(text)


if __name__ == "__main__":
    import inspect

    sale = parse_row(1, "ORD-1,2026-01-05,100.00,EUR,be")
    assert sale == Sale("ORD-1", date(2026, 1, 5), Decimal("100.00"), "EUR", "BE")
    assert parse_row(3, "ORD-3,05/01/2026,50.00,EUR,BE") == Rejected(
        3, "ORD-3,05/01/2026,50.00,EUR,BE", "bad date"
    )
    assert parse_row(5, "ORD-5,2026-01-05,ten,EUR,BE").reason == "bad amount"
    assert parse_row(7, "ORD-7,2026-01-05,100.00").reason == "wrong number of fields"
    print("1 parse_row ok – no exceptions, no silent skips")

    assert vat_for("BE") == Decimal("0.21")
    assert vat_for("fr") == Decimal("0.20"), "country codes arrive in any case"
    try:
        vat_for("ZZ")
    except UnknownCountry:
        pass
    else:
        raise AssertionError("an unknown country must raise UnknownCountry")
    assert net_to_gross(sale, FixedRates("0.90")) == Decimal("121.00")
    print("2 rules ok")

    result = run(RAW_ROWS, FixedRates("0.90"), today=date(2026, 1, 5))
    assert result.totals == {"BE": Decimal("121.00")}, result.totals
    assert [r.line for r in result.rejected] == [3, 5]
    assert result.rejected[0].reason == "bad date"
    print("3 run ok – one day counted, every bad row accounted for")

    other = run(MORE_ROWS, FixedRates("0.90"), today=date(2026, 1, 5))
    assert other.totals == {"NL": Decimal("108.90")}, other.totals
    assert [r.reason for r in other.rejected] == [
        "unknown country",
        "wrong number of fields",
    ]
    print("4 run ok – an unknown country is a rejected row, not a crash")

    parameters = inspect.signature(run).parameters
    assert "rates" in parameters and "today" in parameters
    assert run(RAW_ROWS, FixedRates("0.50"), today=date(2026, 1, 5)).totals == {
        "BE": Decimal("121.00")
    }, "EUR rows must not be converted"
    assert run(MORE_ROWS, FixedRates("0.50"), today=date(2026, 1, 5)).totals == {
        "NL": Decimal("60.50")
    }
    print("5 FixedRates ok – the same answer on any day, with no network")

    csv_text = "ORD-9,2026-01-05,10.00,EUR,BE\n"
    json_text = (
        '{"order_id": "ORD-9", "day": "2026-01-05", "amount": "10.00",'
        ' "currency": "EUR", "country": "BE"}\n'
    )
    expected = {"BE": Decimal("12.10")}
    for suffix, text in ((".csv", csv_text), (".jsonl", json_text)):
        rows = read_rows(suffix, text)
        assert run(rows, FixedRates("0.90"), date(2026, 1, 5)).totals == expected
    try:
        read_rows(".parquet", "")
    except UnsupportedFormat:
        pass
    else:
        raise AssertionError("an unregistered format must raise UnsupportedFormat")
    assert "json" not in inspect.getsource(read_rows), (
        "OCP: you extended the dispatcher by editing it"
    )
    print("6 readers ok – a second format touched no working code")

    def endless():
        yield "ORD-1,2026-01-05,1.00,EUR,BE"
        while True:
            yield "ORD-X,2026-01-05,1.00,EUR,BE"

    from itertools import islice

    streamed = run(islice(endless(), 3), FixedRates("0.90"), date(2026, 1, 5))
    assert streamed.totals == {"BE": Decimal("3.63")}, "run must accept any iterable"
    print("7 bonus ok – it streams, so the file size stops mattering")

    print("\nAll pipeline exercises pass.")
