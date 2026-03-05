# ghstack Workflow Guide

## Setup

```bash
# Install ghstack
uv tool install ghstack

# Configure ~/.ghstackrc
cat > ~/.ghstackrc << 'EOF'
[ghstack]
github_url = github.com
github_oauth = <your_github_token>
github_username = <your_username>
EOF
```

You need a GitHub personal access token with `repo` scope. Generate one at
**Settings → Developer Settings → Personal Access Tokens**.

---

## Daily Workflow

### 1. Start a new feature stack

Work on `main` (or any branch tracking `origin/main`). Each commit becomes its
own PR.

```bash
git checkout main
git pull

# Make your first change
vim calculator.py
git add -A && git commit -m "Add input validation"

# Make your second change (builds on the first)
vim calculator.py
git add -A && git commit -m "Add logging for operations"

# Push the whole stack as separate PRs
ghstack
```

ghstack creates one PR per commit. The output shows the PR URLs:

```
 - Created https://github.com/ORG/repo/pull/10
 - Created https://github.com/ORG/repo/pull/11
```

### 2. Add a new commit on top of the stack

Just commit and re-run `ghstack`. It will create a new PR for the new commit
and leave existing PRs untouched.

```bash
# You're already at the top of your stack
vim cli.py
git add -A && git commit -m "Add CLI help text"

ghstack
```

Output:

```
 - Updated https://github.com/ORG/repo/pull/10
 - Updated https://github.com/ORG/repo/pull/11
 - Created https://github.com/ORG/repo/pull/12   <-- new PR
```

### 3. Fix a commit in the middle of the stack

This is the most common operation. Use interactive rebase.

**Example:** your stack has 3 commits and you need to fix commit 2.

```
$ git log --oneline
ccc3333 [3/3] Add CLI help text
bbb2222 [2/3] Add logging for operations    <-- need to fix this one
aaa1111 [1/3] Add input validation
```

#### Option A: `git rebase -i` (most flexible)

```bash
# Rebase onto the parent of the commit you want to edit
# Use the number of commits in your stack
git rebase -i HEAD~3
```

Your editor opens:

```
pick aaa1111 Add input validation
pick bbb2222 Add logging for operations      <-- change "pick" to "edit"
pick ccc3333 Add CLI help text
```

Change the line for commit 2 from `pick` to `edit`, save, and close.

Git stops at that commit. Make your fix:

```bash
vim calculator.py                # make your changes
git add -A
git commit --amend --no-edit     # amend the stopped commit
git rebase --continue            # replay the rest of the stack
```

If there are conflicts during `--continue`, resolve them and run:

```bash
git add -A
git rebase --continue
```

Then push the updated stack:

```bash
ghstack
```

All affected PRs are updated automatically.

#### Option B: `git commit --fixup` + `git rebase --autosquash`

If you prefer not to interrupt your flow:

```bash
# Make the fix right now, at the top of the stack
vim calculator.py
git add -A

# Create a fixup commit targeting the broken commit
git commit --fixup bbb2222

# Squash it into the right place
git rebase -i --autosquash HEAD~4
# Just save and close the editor — git reorders automatically

ghstack
```

#### Option C: Fix the top commit (simplest case)

If the commit you need to fix is the latest one:

```bash
vim calculator.py
git add -A
git commit --amend --no-edit

ghstack
```

---

## Quick Reference

| I want to...                        | Commands                                                                |
|-------------------------------------|-------------------------------------------------------------------------|
| Push my stack as PRs                | `ghstack`                                                               |
| Add a new commit on top             | `git commit` then `ghstack`                                             |
| Fix the latest commit               | `git commit --amend` then `ghstack`                                     |
| Fix a commit in the middle          | `git rebase -i HEAD~N`, mark `edit`, fix, `--amend`, `--continue`, `ghstack` |
| Reorder commits                     | `git rebase -i HEAD~N`, reorder lines, `ghstack`                        |
| Drop a commit/PR from the stack     | `git rebase -i HEAD~N`, delete the line, `ghstack`                      |
| Rebase onto latest main             | `git rebase origin/main` then `ghstack`                                 |
| Land (merge) the bottom PR          | `ghstack land <PR_URL>`                                                 |
| Check out a stack on another machine| `ghstack checkout <PR_URL>`                                             |

---

## Important Notes

- **Always rebase, never merge.** `git rebase origin/main` is correct.
  `git merge origin/main` will break ghstack.
- **Don't use the GitHub merge button.** Use `ghstack land <PR_URL>` instead,
  because ghstack PRs have synthetic base branches, not `main`.
- **Each commit = one PR.** Write clear, self-contained commit messages.
  The first line becomes the PR title.
- **Re-run `ghstack` after any change.** Whether you amend, rebase, add, or
  remove commits, always re-run `ghstack` to sync your PRs.
