#!/usr/bin/env python3
"""Fix the Claude column alignment bug in AITA_endorsement_results.csv.

Bug: In the original CSV, ALL Claude columns in rows 14-932 are shifted by
exactly 2 rows. Claude's data at row[i] actually corresponds to the AITA post
at row[i-2]. This was likely a merge/join error during dataset assembly.

Impact on the paper's reported results:
  - Claude base FNR: 49.8% (paper) -> 44.8% (corrected), a 5.0pp overestimate
  - Claude NTA_context FNR: 70.4% -> 49.3% (21.1pp)
  - Claude YTA_context FNR: 32.4% -> 13.5% (18.9pp)
  - Claude think_right FNR: 61.3% -> 35.4% (25.9pp)
  - Other conditions similarly affected (20-29pp error)

Fix: For rows 14-930, shift Claude data forward by 2 (row[i] gets row[i+2]'s
Claude data). Rows 931-932 have no valid Claude source data (lost off the end
of the shift range) so their Claude columns are cleared.

All other models (10 of 11) are unaffected.
"""
import csv, sys

csv.field_size_limit(sys.maxsize)

INPUT = 'AITA_endorsement_results.csv'
OUTPUT = 'AITA_endorsement_results_fixed.csv'

def main():
    with open(INPUT, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    claude_cols = [c for c in fieldnames if c.startswith('Claude')]
    print(f"Fixing {len(claude_cols)} Claude columns across rows 14-932")

    # Save original Claude data
    orig_claude = [{c: row.get(c, '') for c in claude_cols} for row in rows]

    # Fix rows 14-930: get Claude data from row[i+2]
    for i in range(14, 931):
        for c in claude_cols:
            rows[i][c] = orig_claude[i + 2][c]

    # Rows 931-932: no valid source, clear
    for i in [931, 932]:
        for c in claude_cols:
            rows[i][c] = ''

    with open(OUTPUT, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {OUTPUT}")

if __name__ == '__main__':
    main()
