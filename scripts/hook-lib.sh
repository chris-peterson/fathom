# Shared by fathom's hooks: read the session id from the hook's stdin, and list
# the records that session wrote, from the ledger `fathom` keeps (see
# `fathom --help`). Pure shell, so a hook that has nothing to do costs nothing.

# The hook payload's session_id, or nothing.
session_id() {
  sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([A-Za-z0-9-]*\)".*/\1/p' | head -n 1
}

# Each record directory the session wrote to that still holds a record, once.
touched_records() {
  local state="${FATHOM_STATE:-${XDG_STATE_HOME:-$HOME/.local/state}/fathom}"
  local ledger="$state/sessions/$1.jsonl"
  [ -n "$1" ] && [ -f "$ledger" ] || return 0
  sed -n 's/^{"record": "\([^"]*\)".*/\1/p' "$ledger" | awk '!seen[$0]++' | while IFS= read -r dir; do
    [ -f "$dir/record.jsonl" ] && printf '%s\n' "$dir"
  done
}
