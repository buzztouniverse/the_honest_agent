---
title: Host the report on AWS
description: Publish the report from a private S3 bucket, through CloudFront with a Cognito sign-in.
---

:::caution[An example, not a security review]
This is one setup we tested, shown as an example. Don't copy it blindly: check each step
against your company's security policies, and adapt it before you use it with real data.
See [Your setup, your responsibility](/docs/team/#your-setup-your-responsibility).
:::

The report sits in a private S3 bucket and is served through CloudFront, which checks a
Cognito sign-in at its edge before every request. AWS publishes the whole setup as one
template,
[`cloudfront-authorization-at-edge`](https://github.com/aws-samples/cloudfront-authorization-at-edge).
It creates the report bucket (separate from any results bucket), the CloudFront
distribution, a Cognito user pool, and small Lambda@Edge functions that check each
request. Cognito can be connected to your identity provider.

:::caution[Know what you're deploying]
It's an AWS sample, not a supported product. Its last published version (2.3.2,
September 2024) runs on Node.js 20, which no longer gets security patches; the
repository's `main` branch has moved on but isn't released. For production, consider
deploying a pinned commit of `main` with the SAM CLI. The template also shows the
Cognito client secret as a plain stack output: limit who in your AWS account can read
CloudFormation stacks.
:::

## 1. Deploy the template

Pick your region; the template adds the Lambda@Edge functions in us-east-1 itself, as AWS
requires. With the AWS CLI:

```bash
aws serverlessrepo create-cloud-formation-change-set --region <region> \
  --application-id arn:aws:serverlessrepo:us-east-1:520945424137:applications/cloudfront-authorization-at-edge \
  --semantic-version 2.3.2 --stack-name honest-agent-report-auth \
  --capabilities CAPABILITY_IAM CAPABILITY_RESOURCE_POLICY \
  --parameter-overrides file://params.json
# review the change set (all "Add"), then run it:
aws cloudformation execute-change-set --region <region> \
  --stack-name serverlessrepo-honest-agent-report-auth --change-set-name <name>
```

The parameters, in `params.json` as a list of `{"Name": ..., "Value": ...}`:

- **`EnableSPAMode` = `false`:** login cookies are HTTP-only, and Cognito uses a client
  secret. The report doesn't need JavaScript access to the tokens.
- **`RewritePathWithTrailingSlashToIndex` = `true`:** `/evals/` serves
  `/evals/index.html`.
- **`EmailAddress`:** the first person's email. Cognito sends them a temporary password.
  Only an admin can add people; nobody can sign up on their own.
- **`HttpHeaders`:** the template's default content security policy blocks the report's
  bundled icons (`data:` images). Pass this one, which matches the report's own:
  `default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; base-uri 'none'; form-action 'none'; object-src 'none'; frame-ancestors 'none'`

It takes about 10 minutes; check that the stack reaches `CREATE_COMPLETE`. Its outputs
give the address (`WebsiteUrl`) and the bucket (`S3Bucket`).

## 2. Check the protection

Before uploading anything:

```bash
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" https://<id>.cloudfront.net/data/report.json
```

It must answer `307`, redirecting to your `*.amazoncognito.com` sign-in. The bucket
itself must refuse direct access (`403`).

## 3. Upload the report

```bash
REPORT_BUCKET=s3://<bucket from the stack outputs>
aws s3 sync honest_agent_report/ "$REPORT_BUCKET"/ --delete --exclude "index.html" --exclude "data/*"
aws s3 cp honest_agent_report/index.html "$REPORT_BUCKET"/index.html --cache-control no-cache
aws s3 cp honest_agent_report/data/ "$REPORT_BUCKET"/data/ --recursive --cache-control no-cache
```

`--delete` removes the template's sample page and old report files. `no-cache` on the
page and its data makes CloudFront fetch them fresh on every load, so a new report shows
up right away. The files in `assets/` have hashed names and can be cached.

:::danger[Check the bucket before `sync --delete`]
Run against the results bucket with an admin login, `sync --delete` would delete your
results.
:::

## 4. Add and remove people

People live in the stack's Cognito user pool, and only an admin can add them: Cognito →
User pools → Users → Create user (email invitation, email marked as verified, generated
password), or:

```bash
aws cognito-idp admin-create-user --region <region> --user-pool-id <pool id> \
  --username person@example.com \
  --user-attributes Name=email,Value=person@example.com Name=email_verified,Value=true \
  --desired-delivery-mediums EMAIL
```

To remove someone, sign them out everywhere first, then disable them. Disabling alone
leaves their open sessions refreshable for up to 30 days.

```bash
aws cognito-idp admin-user-global-sign-out --region <region> --user-pool-id <pool id> --username person@example.com
aws cognito-idp admin-disable-user --region <region> --user-pool-id <pool id> --username person@example.com
```

For a company, connect Cognito to your identity provider (Google Workspace, Entra ID,
Okta, SAML or OIDC), so access follows your directory. Then limit who gets in: assign
the app to specific people or groups in the provider, or use the template's
`UserPoolGroupName` so only one Cognito group can sign in. Otherwise everyone in the
directory can.

## Removing it

Delete the stack. Deleting the Lambda@Edge part can fail for a few hours while
CloudFront clears its copies; retry later.

To deploy after every run, see [GitHub Actions](/docs/team/ci/#variant-report-on-aws).
