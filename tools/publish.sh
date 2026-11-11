#!/usr/bin/env bash
# Publish only generated files; preserve the deployment branch history.
set -euo pipefail
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
output_dir="$project_dir/public"
repository='git@github.com:EssieYiu/EssieYiu.github.io.git'
branch='gh-pages'
test -s "$output_dir/index.html"
staging_dir="$(mktemp -d)"
trap 'rm -rf -- "$staging_dir"' EXIT
git init --quiet "$staging_dir"
git -C "$staging_dir" remote add origin "$repository"
if git ls-remote --exit-code --heads "$repository" "refs/heads/$branch" >/dev/null; then
  git -C "$staging_dir" fetch --quiet --depth=1 origin "$branch"
  git -C "$staging_dir" checkout --quiet -b "$branch" FETCH_HEAD
else
  status=$?
  if [ "$status" -ne 2 ]; then exit "$status"; fi
  git -C "$staging_dir" checkout --quiet --orphan "$branch"
fi
python - "$output_dir" "$staging_dir" <<'PY_COPY'
from pathlib import Path
import shutil
import sys
source, target = map(Path, sys.argv[1:])
for entry in target.iterdir():
    if entry.name == '.git':
        continue
    if entry.is_dir() and not entry.is_symlink():
        shutil.rmtree(entry)
    else:
        entry.unlink()
for entry in source.iterdir():
    if entry.name == '.git':
        raise SystemExit('Refusing to publish Git metadata')
    destination = target / entry.name
    if entry.is_dir():
        shutil.copytree(entry, destination)
    else:
        shutil.copy2(entry, destination)
PY_COPY
touch "$staging_dir/.nojekyll"
git -C "$staging_dir" add --all
if git -C "$staging_dir" diff --cached --quiet; then
  echo 'Generated site is unchanged.'
  exit 0
fi
revision="$(git -C "$project_dir" rev-parse --short HEAD)"
git -C "$staging_dir" -c user.name='github-actions[bot]' -c user.email='41898282+github-actions[bot]@users.noreply.github.com' commit --quiet -m "Deploy blog from blog_source@$revision"
git -C "$staging_dir" push origin "HEAD:refs/heads/$branch"
if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then
  echo 'Published generated files to EssieYiu/EssieYiu.github.io, branch gh-pages. Pages must use gh-pages / (root). Site: https://essieyiu.github.io/' >> "$GITHUB_STEP_SUMMARY"
fi
