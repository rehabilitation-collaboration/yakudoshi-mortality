"""CrossRef API reference verification pipeline.

Parses references from manuscript.md and verifies each against the
CrossRef API, reporting matches, mismatches, and missing entries.
"""

import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import requests

CROSSREF_API = "https://api.crossref.org/works"
USER_AGENT = "YakudoshiPaper/1.0 (mailto:rehabilitation.collaboration@gmail.com)"
REQUEST_DELAY = 1.0  # seconds between API calls (polite pool)
MANUSCRIPT_PATH = Path(__file__).parent / "manuscript.md"
OUTPUT_PATH = Path(__file__).parent / "output" / "reference_verification.json"


@dataclass
class Reference:
    """Parsed reference from manuscript."""

    number: int
    raw_text: str
    authors: str = ""
    title: str = ""
    journal: str = ""
    year: str = ""
    volume: str = ""
    pages: str = ""
    doi: str = ""
    url: str = ""


@dataclass
class VerificationResult:
    """Result of CrossRef verification for one reference."""

    ref_number: int
    status: str = ""  # MATCH, MISMATCH, NOT_FOUND, URL_ONLY
    raw_text: str = ""
    mismatched_fields: list = field(default_factory=list)
    manuscript_data: dict = field(default_factory=dict)
    crossref_data: dict = field(default_factory=dict)
    crossref_doi: str = ""
    crossref_score: float = 0.0
    corrected_citation: str = ""


def parse_references(manuscript_path: Path) -> list[Reference]:
    """Extract numbered references from manuscript.md."""
    text = manuscript_path.read_text(encoding="utf-8")

    ref_section_match = re.search(
        r"^## References\s*\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not ref_section_match:
        print("ERROR: References section not found in manuscript.")
        sys.exit(1)

    ref_text = ref_section_match.group(1)
    # Match lines like "1. Author..."
    raw_refs = re.findall(r"^(\d+)\.\s+(.+?)(?=\n\d+\.|\Z)", ref_text, re.MULTILINE | re.DOTALL)

    references = []
    for num_str, body in raw_refs:
        ref = Reference(number=int(num_str), raw_text=body.strip())
        _parse_reference_fields(ref)
        references.append(ref)

    return references


def _parse_reference_fields(ref: Reference) -> None:
    """Best-effort parsing of reference fields from raw text."""
    text = ref.raw_text

    # Check if this is a URL-only reference (database, protocol doc, etc.)
    if "Available at:" in text or "https://" in text:
        url_match = re.search(r"https?://\S+", text)
        if url_match:
            ref.url = url_match.group(0).rstrip(".")

    # Extract year: prefer "Journal. YEAR;" pattern over year in title
    # Look for year followed by semicolon (standard citation format)
    year_match = re.search(r"\.\s*((?:19|20)\d{2})[;.]", text)
    if not year_match:
        # Fall back to "Accessed YEAR" for URL references
        year_match = re.search(r"Accessed\s+((?:19|20)\d{2})", text)
    if not year_match:
        # Last resort: last 4-digit year in the text
        all_years = re.findall(r"\b((?:19|20)\d{2})\b", text)
        if all_years:
            ref.year = all_years[-1]
    if year_match:
        ref.year = year_match.group(1)

    # Extract authors (everything before the title, which starts after a period)
    # Pattern: "Authors. Title. Journal..."
    parts = text.split(". ", 2)
    if len(parts) >= 2:
        ref.authors = parts[0].strip()
        # Title is the second segment
        ref.title = parts[1].strip().rstrip(".")

    # Extract journal, volume, pages from the remainder
    # Common pattern: "Journal. Year;Vol:Pages" or "Journal. Year;Vol(Issue):Pages"
    journal_match = re.search(
        r"(?:^|\.)\s*([A-Z][A-Za-z\s&]+?)\.\s*\d{4}",
        text,
    )
    if journal_match:
        ref.journal = journal_match.group(1).strip()

    vol_match = re.search(r"\d{4};(\d+)", text)
    if vol_match:
        ref.volume = vol_match.group(1)

    pages_match = re.search(r":(\d+[-–]\d+|e\d+)", text)
    if pages_match:
        ref.pages = pages_match.group(1)


def query_crossref(ref: Reference) -> dict | None:
    """Query CrossRef API for a reference. Returns best matching result or None."""
    # Build query from title (most reliable field)
    query = ref.title
    if not query or len(query) < 10:
        # Fall back to raw text if title parsing failed
        query = ref.raw_text[:200]

    params = {
        "query.bibliographic": query,
        "rows": 5,
    }

    headers = {"User-Agent": USER_AGENT}

    try:
        resp = requests.get(CROSSREF_API, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        items = resp.json().get("message", {}).get("items", [])
        if not items:
            return None

        # Select best candidate: prefer items where author/year/volume match
        return _select_best_candidate(items, ref)
    except requests.RequestException as e:
        print(f"  WARNING: API error for ref [{ref.number}]: {e}")
        return None


def _select_best_candidate(items: list[dict], ref: Reference) -> dict:
    """From multiple CrossRef results, pick the one that best matches the reference."""
    if len(items) == 1:
        return items[0]

    best = items[0]
    best_score = 0

    for item in items:
        score = 0
        cr = _extract_crossref_fields(item)

        # Year match
        if ref.year and cr["year"] and ref.year == cr["year"]:
            score += 3

        # Volume match
        if ref.volume and cr["volume"] and ref.volume == cr["volume"]:
            score += 2

        # Pages match
        if ref.pages and cr["page"]:
            ref_p = ref.pages.replace("–", "-")
            cr_p = cr["page"].replace("–", "-")
            if ref_p == cr_p:
                score += 2

        # First author surname match
        if ref.authors and cr["authors"]:
            ref_s = _normalize(ref.authors.split(",")[0].split()[0]) if ref.authors.split(",")[0].split() else ""
            cr_s = _normalize(cr["authors"].split(",")[0].split()[0]) if cr["authors"].split(",")[0].split() else ""
            if ref_s and cr_s and ref_s == cr_s:
                score += 2

        # Title word overlap
        if ref.title and cr["title"]:
            ref_words = set(_normalize(ref.title).split())
            cr_words = set(_normalize(cr["title"]).split())
            overlap = len(ref_words & cr_words) / max(len(ref_words | cr_words), 1)
            score += overlap * 3

        if score > best_score:
            best_score = score
            best = item

    return best


def _normalize(s: str) -> str:
    """Normalize a string for comparison."""
    s = s.lower().strip()
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s


def _journals_match(abbrev: str, full: str) -> bool:
    """Check if a journal abbreviation matches the full name.

    Handles cases like "BMJ" vs "BMJ", "Soc Sci Med" vs "Social Science & Medicine",
    "N Engl J Med" vs "New England Journal of Medicine".
    """
    a = _normalize(abbrev)
    f = _normalize(full)

    # Exact match
    if a == f:
        return True

    # Check if abbreviation words are prefixes of full name words
    a_words = a.split()
    f_words = f.split()

    # Remove stop words from full name
    stop = {"the", "of", "and", "in", "for", "a", "an"}
    f_words_filtered = [w for w in f_words if w not in stop]

    if len(a_words) == len(f_words_filtered):
        matches = sum(
            1 for aw, fw in zip(a_words, f_words_filtered)
            if fw.startswith(aw) or aw.startswith(fw) or aw == fw
        )
        if matches == len(a_words):
            return True

    # Check if all abbreviated words appear as prefixes somewhere in full name
    if a_words and f_words_filtered:
        matched = 0
        f_remaining = list(f_words_filtered)
        for aw in a_words:
            for i, fw in enumerate(f_remaining):
                if fw.startswith(aw) or aw.startswith(fw):
                    matched += 1
                    f_remaining.pop(i)
                    break
        if matched >= len(a_words) * 0.7:
            return True

    return False


def _extract_crossref_authors(item: dict) -> str:
    """Extract author string from CrossRef item."""
    authors = item.get("author", [])
    if not authors:
        return ""
    parts = []
    for a in authors:
        family = a.get("family", "")
        given = a.get("given", "")
        if family:
            initials = "".join(w[0] for w in given.split() if w) if given else ""
            parts.append(f"{family} {initials}".strip())
    return ", ".join(parts)


def _extract_crossref_fields(item: dict) -> dict:
    """Extract comparable fields from a CrossRef result."""
    title_list = item.get("title", [])
    title = title_list[0] if title_list else ""

    container = item.get("container-title", [])
    journal = container[0] if container else ""

    year = ""
    date_parts = (
        item.get("published-print", {}).get("date-parts")
        or item.get("published-online", {}).get("date-parts")
        or item.get("issued", {}).get("date-parts")
    )
    if date_parts and date_parts[0]:
        year = str(date_parts[0][0])

    volume = item.get("volume", "")
    page = item.get("page", "")
    article_number = item.get("article-number", "")
    doi = item.get("DOI", "")
    authors = _extract_crossref_authors(item)

    return {
        "title": title,
        "journal": journal,
        "year": year,
        "volume": volume,
        "page": page or article_number,
        "doi": doi,
        "authors": authors,
    }


def _format_corrected_citation(cr: dict, ref_number: int) -> str:
    """Format a corrected citation string from CrossRef data."""
    parts = []
    if cr["authors"]:
        parts.append(cr["authors"])
    if cr["title"]:
        parts.append(cr["title"])
    journal_part = cr["journal"]
    if cr["year"]:
        journal_part += f". {cr['year']}"
    if cr["volume"]:
        journal_part += f";{cr['volume']}"
    if cr["page"]:
        journal_part += f":{cr['page']}"
    parts.append(journal_part)
    if cr["doi"]:
        parts.append(f"doi:{cr['doi']}")
    return ". ".join(parts) + "."


def verify_reference(ref: Reference) -> VerificationResult:
    """Verify a single reference against CrossRef."""
    result = VerificationResult(ref_number=ref.number, raw_text=ref.raw_text)
    result.manuscript_data = {
        "authors": ref.authors,
        "title": ref.title,
        "journal": ref.journal,
        "year": ref.year,
        "volume": ref.volume,
        "pages": ref.pages,
    }

    # Skip URL-only references (databases, protocols, data sources)
    if ref.url and ("Available at:" in ref.raw_text or "Accessed" in ref.raw_text):
        result.status = "URL_ONLY"
        return result

    item = query_crossref(ref)
    if not item:
        result.status = "NOT_FOUND"
        return result

    cr = _extract_crossref_fields(item)
    result.crossref_data = cr
    result.crossref_doi = cr["doi"]
    result.crossref_score = item.get("score", 0)
    result.corrected_citation = _format_corrected_citation(cr, ref.number)

    # Compare fields
    mismatches = []

    # Title comparison (fuzzy)
    if ref.title and cr["title"]:
        ref_title_norm = _normalize(ref.title)
        cr_title_norm = _normalize(cr["title"])
        # Check if one contains the other or significant overlap
        if ref_title_norm not in cr_title_norm and cr_title_norm not in ref_title_norm:
            # Word overlap check
            ref_words = set(ref_title_norm.split())
            cr_words = set(cr_title_norm.split())
            overlap = len(ref_words & cr_words) / max(len(ref_words | cr_words), 1)
            if overlap < 0.5:
                mismatches.append("title")

    # Year comparison (exact)
    if ref.year and cr["year"] and ref.year != cr["year"]:
        mismatches.append("year")

    # Journal comparison (abbreviation-aware)
    if ref.journal and cr["journal"]:
        if not _journals_match(ref.journal, cr["journal"]):
            mismatches.append("journal")

    # Volume comparison (exact)
    if ref.volume and cr["volume"] and ref.volume != cr["volume"]:
        mismatches.append("volume")

    # Pages comparison (normalize dashes)
    # Skip if CrossRef has no page info (incomplete metadata, not a mismatch)
    if ref.pages and cr["page"]:
        ref_p = ref.pages.replace("–", "-")
        cr_p = cr["page"].replace("–", "-")
        # Also handle first-page-only from CrossRef (e.g., "1673-1673")
        cr_p_start = cr_p.split("-")[0] if "-" in cr_p else cr_p
        ref_p_start = ref_p.split("-")[0] if "-" in ref_p else ref_p
        if ref_p != cr_p and ref_p_start != cr_p_start:
            mismatches.append("pages")

    # Author comparison: check first author surname
    if ref.authors and cr["authors"]:
        # Extract first author surname from manuscript (e.g., "Panesar SS" -> "panesar")
        ref_author_part = ref.authors.split(",")[0].strip()
        ref_surname = _normalize(ref_author_part.split()[0]) if ref_author_part.split() else ""
        # Extract first author surname from CrossRef
        cr_author_part = cr["authors"].split(",")[0].strip()
        cr_surname = _normalize(cr_author_part.split()[0]) if cr_author_part.split() else ""
        if ref_surname and cr_surname and ref_surname != cr_surname:
            mismatches.append("first_author")
        # Also flag if initials differ (catches Panesar SS vs Panesar NS)
        # But tolerate CrossRef returning fewer initials (e.g., "C" vs "CH")
        elif ref_surname and cr_surname and ref_surname == cr_surname:
            ref_initials = _normalize("".join(w for w in ref_author_part.split()[1:]))
            cr_initials = _normalize("".join(w for w in cr_author_part.split()[1:]))
            if ref_initials and cr_initials:
                # If CrossRef has fewer initials, check prefix match
                shorter, longer = sorted([ref_initials, cr_initials], key=len)
                if not longer.startswith(shorter):
                    mismatches.append("author_initials")

    result.mismatched_fields = mismatches
    result.status = "MISMATCH" if mismatches else "MATCH"

    return result


def print_report(results: list[VerificationResult]) -> None:
    """Print human-readable verification report."""
    print("\n" + "=" * 70)
    print("REFERENCE VERIFICATION REPORT")
    print("=" * 70)

    status_counts = {"MATCH": 0, "MISMATCH": 0, "NOT_FOUND": 0, "URL_ONLY": 0}
    for r in results:
        status_counts[r.status] = status_counts.get(r.status, 0) + 1

    print(f"\nTotal: {len(results)} references")
    for status, count in status_counts.items():
        if count > 0:
            icon = {"MATCH": "OK", "MISMATCH": "!!", "NOT_FOUND": "??", "URL_ONLY": "--"}
            print(f"  [{icon[status]}] {status}: {count}")

    print("\n" + "-" * 70)
    for r in results:
        icon = {"MATCH": "OK", "MISMATCH": "!!", "NOT_FOUND": "??", "URL_ONLY": "--"}[r.status]
        print(f"\n[{icon}] Ref [{r.ref_number}]: {r.status}")
        if r.status == "URL_ONLY":
            print(f"    (URL/database reference, skipped)")
            continue
        if r.status == "NOT_FOUND":
            print(f"    Manuscript: {r.raw_text[:100]}...")
            continue

        if r.mismatched_fields:
            print(f"    Mismatched fields: {', '.join(r.mismatched_fields)}")
            for field_name in r.mismatched_fields:
                ms_val = r.manuscript_data.get(field_name, "")
                cr_val = r.crossref_data.get(field_name, "")
                if field_name in ("first_author", "author_initials"):
                    ms_val = r.manuscript_data.get("authors", "").split(",")[0]
                    cr_val = r.crossref_data.get("authors", "").split(",")[0]
                print(f"      {field_name}:")
                print(f"        manuscript: {ms_val}")
                print(f"        crossref:  {cr_val}")

        if r.crossref_doi:
            print(f"    DOI: {r.crossref_doi}")
        if r.crossref_score:
            print(f"    Score: {r.crossref_score:.1f}")
        if r.status == "MISMATCH":
            print(f"    Suggested: {r.corrected_citation}")


def save_results(results: list[VerificationResult], output_path: Path) -> None:
    """Save results as JSON."""
    data = []
    for r in results:
        data.append({
            "ref_number": r.ref_number,
            "status": r.status,
            "raw_text": r.raw_text,
            "mismatched_fields": r.mismatched_fields,
            "manuscript_data": r.manuscript_data,
            "crossref_data": r.crossref_data,
            "crossref_doi": r.crossref_doi,
            "crossref_score": r.crossref_score,
            "corrected_citation": r.corrected_citation,
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nResults saved to: {output_path}")


def main():
    manuscript_path = Path(sys.argv[1]) if len(sys.argv) > 1 else MANUSCRIPT_PATH
    print(f"Verifying references in: {manuscript_path}")

    refs = parse_references(manuscript_path)
    print(f"Found {len(refs)} references\n")

    results = []
    for ref in refs:
        print(f"  Checking ref [{ref.number}]: {ref.title[:60] if ref.title else ref.raw_text[:60]}...")
        result = verify_reference(ref)
        results.append(result)
        if result.status != "URL_ONLY":
            time.sleep(REQUEST_DELAY)

    print_report(results)
    save_results(results, OUTPUT_PATH)


if __name__ == "__main__":
    main()
