#!/bin/sh
# po każdej turze: walidacja, build, commit, push
cd "$(dirname "$0")/.." && python3 skills/validate.py && python3 build_pwa.py | head -1 && rm -rf __pycache__ skills/__pycache__ market/__pycache__ && cd .. && git add -A && git commit -qm "Umiejętności: tura $1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PLQZBunFy7GoD4f66ZyxfW" && git push -q origin HEAD:main && git log --oneline -1
