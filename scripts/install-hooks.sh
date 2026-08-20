#!/usr/bin/env bash
# install-hooks.sh — arm the git-boundary guard in this clone.
#
# .git/hooks/ is NOT tracked, so a fresh clone ships with NO protection. This
# one-liner points git at the tracked hooks/ directory so the pre-commit and
# pre-push guards run. Run it once after cloning:
#
#     bash scripts/install-hooks.sh
#
# It sets core.hooksPath to the tracked hooks/ dir (single source of truth, no
# symlinks, survives new hooks being added). Use --uninstall to revert to the
# default .git/hooks path. Use --verify to confirm the guard is armed (exit 1 if not).
set -u

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$REPO_ROOT" ]; then
  echo "install-hooks: not inside a git work tree." >&2
  exit 1
fi
cd "$REPO_ROOT"

HOOKS_DIR="hooks"

case "${1:-}" in
  --uninstall)
    git config --unset core.hooksPath 2>/dev/null || true
    echo "install-hooks: core.hooksPath unset — reverted to default .git/hooks/."
    echo "install-hooks: the boundary guard is NO LONGER armed for commit/push."
    exit 0
    ;;
  --verify)
    current="$(git config --get core.hooksPath || echo "")"
    if [ "$current" = "$HOOKS_DIR" ]; then
      echo "install-hooks: armed — core.hooksPath=$current"
      exit 0
    else
      echo "install-hooks: NOT armed — core.hooksPath='$current' (expected '$HOOKS_DIR')." >&2
      echo "install-hooks: run 'bash scripts/install-hooks.sh' to arm it." >&2
      exit 1
    fi
    ;;
  --help|-h)
    grep -E '^#( |$)' "$0" | sed 's/^# \{0,1\}//'
    exit 0
    ;;
  "") : ;;
  *)
    echo "install-hooks: unknown argument '$1' (use --uninstall, --verify, or --help)." >&2
    exit 2
    ;;
esac

if [ ! -d "$HOOKS_DIR" ]; then
  echo "install-hooks: $HOOKS_DIR/ not found in repo root." >&2
  exit 1
fi

chmod +x "$HOOKS_DIR"/pre-commit "$HOOKS_DIR"/pre-push 2>/dev/null || true
git config core.hooksPath "$HOOKS_DIR"

echo "install-hooks: armed."
echo "  core.hooksPath -> $HOOKS_DIR"
echo "  pre-commit + pre-push now run scripts/check-git-boundary.sh"
echo ""
echo "Verify any time with: bash scripts/install-hooks.sh --verify"
