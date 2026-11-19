#!/usr/bin/env bash
# DOCUMENTATION: Before a conversation compaction, asks the summary to carry the reasoning behind each record this session wrote.
# PreCompact: no model turn happens before the summary, but this hook's stdout
# becomes instructions for writing it. Use that to carry, for each record this
# session wrote, the reasoning a compaction pass needs and the summary would
# otherwise drop: why facts changed, which keys are the same thing, why the
# lede says what it says. Silent when the session wrote no record.
set -u
. "$(dirname "$0")/../scripts/hook-lib.sh"
records=$(session_id | { read -r sid; touched_records "${sid:-}"; })
[ -n "$records" ] || exit 0
cat <<MSG
This session kept fathom records, which a compaction pass will clean up right after this summary:
$(printf '%s\n' "$records" | sed 's/^/- /')
For each record, keep in the summary what the record itself can't hold: each fact found wrong (its key, the evidence against it), each set of keys that describe the same thing and which one should survive, each contradiction still unsettled (both values and both sources), and why the lede says what it says. Leave out the facts themselves; they are in the record.
MSG
