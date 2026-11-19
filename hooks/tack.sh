#!/usr/bin/env bash
# DOCUMENTATION: Keeps a session record for a tack: creates it when a route binds, carries /goal into it, and renders its recap when /tack:end runs.
#
# fathom reacts to tack; tack knows nothing about fathom. One script, three triggers:
#   - `tack session <route> <session> --tack <tack>` ran (PostToolUse, Bash): start the
#     record <route>/<tack> of kind `session`, unless it exists, and say how to keep it.
#   - /goal <condition> was typed (UserPromptSubmit): the goal moved; record it.
#   - /tack:end was invoked, typed (UserPromptSubmit) or by the agent (PostToolUse,
#     Skill): render the recap before the retrospective, so the retro can link it.
# Every other event exits 0 silently: this runs on every prompt and every Bash call.
# Needs jq; without it the hook does nothing.
set -u
command -v jq >/dev/null 2>&1 || exit 0
here="$(cd "$(dirname "$0")" && pwd)"
. "$here/../scripts/hook-lib.sh"
input=$(cat)
field() { printf '%s' "$input" | jq -r "$1 // empty" 2>/dev/null; }

sid=$(field .session_id)
tool=$(field .tool_name)

# The session records this session wrote whose kind is `session`.
session_records() {
  touched_records "$sid" | while IFS= read -r dir; do
    head -n 1 "$dir/record.jsonl" | grep -q '"kind": *"session"' && printf '%s\n' "$dir"
  done
}

if [ "$tool" = "Bash" ]; then
  cmd=$(field .tool_input.command)
  binding=$(printf '%s' "$cmd" | sed -n 's/.*tack session \([a-z0-9][a-z0-9-]*\) [^ ]* --tack \([a-z0-9][a-z0-9-]*\).*/\1\/\2/p' | head -n 1)
  [ -n "$binding" ] || exit 0
  cwd=$(field .cwd)
  cd "${cwd:-.}" 2>/dev/null || exit 0
  out=$(CLAUDE_CODE_SESSION_ID="$sid" "$here/../scripts/fathom" init "$binding" --kind session 2>&1) || {
    case "$out" in *"already holds a record"*) ;; *) exit 0 ;; esac
  }
  sed "s|{record}|\`$binding\`|" "$here/../kinds/session/recording.md"
  exit 0
fi

skill=$(field .tool_input.skill)
prompt=""
if [ -z "$skill" ]; then
  prompt=$(field .prompt | head -n 1)
  skill=$(printf '%s' "$prompt" | sed -n 's|^[[:space:]]*/\([A-Za-z0-9:_-][A-Za-z0-9:_-]*\).*|\1|p')
fi

case "$skill" in
  goal)
    arg=$(printf '%s' "$prompt" | sed -n 's|^[[:space:]]*/goal[[:space:]]*||p')
    case "$arg" in ""|clear|stop|off|reset|none|cancel) exit 0 ;; esac
    records=$(session_records)
    [ -n "$records" ] || exit 0
    cat <<MSG
fathom: the goal moved. Record it as a new row of the \`goal\` key (set-by: /goal, statement: the condition as typed) in:
$(printf '%s\n' "$records" | sed 's/^/- /')
Then revise the lede if the new goal changes where the work stands against it.
MSG
    ;;
  tack:end|end)
    [ "$skill" = "end" ] && [ -z "$prompt" ] && exit 0  # a bare `end` skill from another plugin
    records=$(session_records)
    [ -n "$records" ] || exit 0
    cat <<MSG
fathom: before handing off the retrospective, close out each session record this session kept:
$(printf '%s\n' "$records" | sed 's/^/- /')
1. Record any outcome, decision, or open action still missing, and revise the lede to where the work now stands against its goal.
2. Render the \`recap\` brief (/fathom:render) as a polished page, save it, and publish it as an artifact.
3. Offer a PDF (/fathom:pdf) and, when the retrospective is written, a link to the recap from it.
MSG
    ;;
esac
exit 0
