---
title: Store results in S3
description: Keep honest-agent's results file in a private S3 bucket.
---

:::caution[An example, not a security review]
This is one setup we tested, shown as an example. Don't copy it blindly: check each step
against your company's security policies, and adapt it before you use it with real data.
See [Your setup, your responsibility](/docs/team/#your-setup-your-responsibility).
:::

DuckDB can't write a database file that sits in S3, so the file is copied in before a
run and out after it, with the AWS CLI. In the config, `results_path` stays a local file
(the default, `honest_agent_results/results.duckdb`).

:::note[Other cloud storage]
honest-agent never talks to S3 itself: it only reads and writes the local file. So the
same approach works with Google Cloud Storage (`gcloud storage cp`) or Azure Blob Storage
(`az storage blob` or `azcopy`), following the same rules: a private bucket or container
with versioning, credentials that can only read and write the one file, a check that
tells a missing file from a permission error, and one run at a time. We've only tested S3.
:::

## 1. Create the bucket

S3 → Create bucket:

- **Name:** one you'll reuse below, like `acme-honest-agent`.
- **Block all public access:** on (the default).
- **Bucket Versioning:** enable it. Every upload replaces the whole file, so a bad upload
  could wipe your history; versions let you restore it.
- **Encryption:** the default (SSE-S3).

Keep the report out of this bucket: report viewers must never reach the results.

## 2. Add a lifecycle rule

So old versions don't pile up: bucket → Management → Create lifecycle rule.

- **Scope:** the prefix `results/`.
- **Permanently delete noncurrent versions:** after 7 days, keeping 10 newer versions.
- **Delete expired object delete markers or incomplete multipart uploads:** incomplete
  uploads after 7 days.
- **Don't** tick "Expire current versions": it deletes the live file.

## 3. Create a policy for the one file

IAM → Policies → Create → JSON. It allows reading and writing the results file, and
listing the bucket, nothing else:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadWriteResultsFile",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::<bucket>/results/results.duckdb.gz"
    },
    {
      "Sid": "ListResultsBucket",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::<bucket>"
    }
  ]
}
```

The listing lets a run tell "no results file yet" apart from a permission problem, so the
first run can start on its own.

## 4. Create a role with that policy

IAM → Roles → Create role → Custom trust policy. A role has two policies: the **trust
policy** says who may use it, and the **permissions policy** (step 3, attached on the
next screen) says what it can do.

To test from your machine first, trust your own account. The
[GitHub Actions recipe](/docs/team/ci/#1-let-github-actions-use-the-role) replaces this
with GitHub.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "LocalTestingRemoveBeforeCI",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::<account-id>:root" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Name it after what it does, like `honest-agent-results-writer`.

## 5. Test the role from your machine

Add a profile to `~/.aws/config` (not `~/.aws/credentials`):

```ini
[profile honest-agent-results-writer]
role_arn = arn:aws:iam::<account-id>:role/honest-agent-results-writer
source_profile = default
```

```bash
export AWS_PROFILE=honest-agent-results-writer
aws sts get-caller-identity       # shows assumed-role/honest-agent-results-writer
aws s3 ls s3://<bucket>/results/  # works: the role can list the bucket
aws s3 ls s3://<another-bucket>/  # must be denied
```

## 6. Every run

Save this as `get-results.sh` next to your config. It downloads the results file before a
run, and starts a new history only when the file doesn't exist yet:

```bash
#!/usr/bin/env bash
# Downloads the results file from S3. A missing file (404) starts a new history;
# any other error, like a permission problem (403), stops without touching anything.
set -euo pipefail
: "${RESULTS_S3:?set RESULTS_S3, e.g. s3://<bucket>/results/results.duckdb.gz}"
RESULTS_FILE=${RESULTS_FILE:-honest_agent_results/results.duckdb}

bucket=${RESULTS_S3#s3://}
key=${bucket#*/}
bucket=${bucket%%/*}

if found=$(aws s3api head-object --bucket "$bucket" --key "$key" 2>&1); then
  mkdir -p "$(dirname "$RESULTS_FILE")"
  aws s3 cp "$RESULTS_S3" "$RESULTS_FILE.gz"
  gunzip -t "$RESULTS_FILE.gz"
  gunzip -f "$RESULTS_FILE.gz"
elif [[ $found == *"(404)"* ]]; then
  echo "No results file in S3 yet: this run starts a new history."
else
  echo "$found" >&2
  exit 1
fi
```

Then each run downloads, runs and uploads. A DuckDB file is mostly reserved space and
JSON, so it's compressed for the upload: gzip shrinks it 25 to 100 times.

```bash
export RESULTS_S3=s3://<bucket>/results/results.duckdb.gz
bash get-results.sh
honest-agent run
test -f honest_agent_results/results.duckdb && gzip -c honest_agent_results/results.duckdb | aws s3 cp - "$RESULTS_S3"
```

The download replaces the local file only once the archive is complete. If anything
other than a missing file goes wrong, the script stops before the run, so a mistake never
overwrites your history.

:::note
The first run without a results file (the 404 branch) hasn't run in CI yet.
:::

:::caution[One run at a time]
If two runs overlap, each uploads its own copy, and the later one silently drops the
other's results. The [GitHub Actions recipe](/docs/team/ci/) prevents that with a
`concurrency` group.
:::
