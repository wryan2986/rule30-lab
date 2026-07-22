# Publication Audit Report

**Date:** 2026-07-22
**Repository:** `.`
**Auditor:** Automated (opencode)

## Scope

This audit covers the full Git history (77 commits, main branch) and the
current working tree for secrets, private information, generated files, and
content unsuitable for public publication.

## Tools Used

- **gitleaks v8.21.2** — full repository scan (77 commits)
- **Manual grep/ripgrep** — pattern search for API keys, tokens, passwords,
  private keys, credentials, personal paths, email addresses, private IPs
- **git log --diff-filter=D** — inspection of deleted historical files
- **git ls-files** — inspection of tracked file sizes and types
- **git count-objects** — repository object size audit

## Findings

### Secrets and Credentials

| Category | Result |
|----------|--------|
| API keys (GitHub, OpenAI, Anthropic, AWS, Google) | **None found** |
| Access tokens / JWTs | **None found** |
| SSH private keys | **None found** |
| Passwords / client secrets | **None found** |
| .env files tracked | **None found** |
| Cloud credentials | **None found** |
| Webhook URLs | **None found** |
| Private network details | **None found** |

**gitleaks result:** 0 leaks found across 77 commits.

### Personal Information

| Category | Result |
|----------|--------|
| Email addresses | **None found** |
| Home addresses | **None found** |
| Personal domain names | **None found** |
| Windows user paths (C:\Users\...) | **None found** |

**Local path references:** The username `wryan` and checkout path
`/home/wryan/rule30-lab` appear in:
- Documentation files (README.md, various docs/*.md) — these are generic
  project documentation references to the canonical checkout path, not
  personal information. The GitHub username `wryan2986` is intentionally
  public.
- Experiment record JSON files (results/runs/*.record.json) — these contain
  local executable paths as experiment metadata. These files are already
  excluded by .gitignore rules but were tracked before the rules were added.
  They will be untracked as part of publication preparation.
- Result JSON files (results/benchmarks/*.json, results/problem*/**.json) —
  these contain experiment parameters including the local checkout path.
  This is standard provenance metadata for reproducible research.

### Deleted Historical Files

Only `.gitkeep` placeholder files were deleted in history. No sensitive files
were added and subsequently removed.

## Conclusion

**The repository is safe to publish.** No live secrets, credentials, or
private information requiring history rewrite were found. The local path
references (`/home/wryan/rule30-lab`) are acceptable for a public research
repository as they document the canonical checkout location.

### Actions Taken

1. Record JSON files in `results/runs/` will be untracked (already in
   .gitignore but previously tracked).
2. README will be updated to remove "private" language.
3. Documentation path references will be updated to use relative or generic
   paths where practical.
