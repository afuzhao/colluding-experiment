# Branch catalog

Inventory checked on 2026-10-26. Branch tips can move; the pinned commits below identify the evidence used in the published report. See [branches.json](branches.json) for machine-readable references.

| Branch | Purpose | Where to start | Integration status |
|---|---|---|---|
| `main` | Reviewed report, study packages, audits, and navigation | [Final report](../papers/final_report/README.md) | Canonical reading and publication branch |
| `sumin/disruption` | Quantity-market disruption and talk/action comparisons | [E1-D audit on main](../studies/exp%205%20%28env1_disruption%29/README.md) | Audited derivatives and pinned links integrated; original source retained separately |
| `anay/apart-sprint-ring-study` | Other-market collusion and forged-message experiments | [Report source map](../papers/final_report/SOURCE_MAP.md) | Record-derived analyses integrated; separate market definitions retained |

## Pinned evidence

- [Sumin source](https://github.com/afuzhao/colluding-experiment/tree/a10db995c8d0e8206d4ae935118cf9b8727fc067): `a10db995c8d0e8206d4ae935118cf9b8727fc067`.
- [Anay primary report snapshot](https://github.com/afuzhao/colluding-experiment/tree/e3c0b8790cd2fb802251187faa72a71a6f98c767): `e3c0b8790cd2fb802251187faa72a71a6f98c767`.
- [Anay late-update snapshot](https://github.com/afuzhao/colluding-experiment/tree/07a92fc01832d131cb7d77970ea3ff0e73a53b55): `07a92fc01832d131cb7d77970ea3ff0e73a53b55`. The report records the claimed-value sweep qualification separately from its primary figures.
- [Published report baseline](https://github.com/afuzhao/colluding-experiment/tree/65c82a226f7765886bc73529ce0d19e63997446d/papers/final_report): `65c82a226f7765886bc73529ce0d19e63997446d`. Later navigation-only commits do not change the underlying experiment versions.

The two contributor branches contain overlapping historical package paths. Their files must not be copied over `main` indiscriminately. Branch names describe provenance, not additional independent replications. Other-market experiments on Anay's branch are not the unexecuted three-firm E2-D specification.

## Working with branches

Fetch without changing your checkout:

```sh
git fetch origin
git branch -r
```

Inspect a pinned file with `git show COMMIT:path/to/file`, or use its GitHub commit link. If isolated development is needed, use a separate worktree and a new descriptive branch. Retain existing contributor branches and commit history; no branches were renamed, deleted, or force-pushed during repository organization.

Future branches should follow the [contribution conventions](../CONTRIBUTING.md). Update this catalog when evidence is integrated, superseded, or archived. Do not label a contributor branch complete solely because a subset of its results was used in a report.
