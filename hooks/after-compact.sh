#!/usr/bin/env bash
# DOCUMENTATION: After a conversation compaction, starts /fathom:compact on the records this session wrote.
# SessionStart (compact): the summary is written, so ask for the compaction
# pass while its reasoning is still in the summary. Silent when the session
# wrote no record.
set -u
. "$(dirname "$0")/../scripts/hook-lib.sh"
records=$(session_id | { read -r sid; touched_records "${sid:-}"; })
[ -n "$records" ] || exit 0
cat <<MSG
fathom: the conversation was just compacted. Before the next task, run /fathom:compact on each record this session wrote, and on no other:
$(printf '%s\n' "$records" | sed 's/^/- /')
MSG
# The recording rule for a session record came in as context when the record
# started; the summary may have dropped it, so restate it for each.
printf '%s\n' "$records" | while IFS= read -r dir; do
  head -n 1 "$dir/record.jsonl" | grep -q '"kind": *"session"' || continue
  name=${dir##*/.fathom/}
  echo
  sed "s|{record}|\`$name\`|" "$(dirname "$0")/../kinds/session/recording.md"
done
