# CLI Patterns

Create:

```bash
python3 scripts/opportunity_manager.py create \
  --account "Accounts/CSG" \
  --organization "Organizations/CSG" \
  --primary-contact "Contacts/David-Ketley" \
  --name "CSG - PH Banking Advisory - 2026" \
  --opportunity-type advisory \
  --source manual
```

Advance stage:

```bash
python3 scripts/opportunity_manager.py set-stage \
  "Opportunities/CSG-PH-Banking-Advisory-2026" \
  --stage proposal \
  --probability 40
```

Update structure:

```bash
python3 scripts/opportunity_manager.py update \
  "Opportunities/CSG-PH-Banking-Advisory-2026" \
  --commercial-value 250000 \
  --close-date 2026-06-30 \
  --summary "Proposal delivered and awaiting budget confirmation."
```

Close lost:

```bash
python3 scripts/opportunity_manager.py mark-lost \
  "Opportunities/CSG-PH-Banking-Advisory-2026" \
  --reason "budget shifted" \
  --lost-date 2026-05-10
```
