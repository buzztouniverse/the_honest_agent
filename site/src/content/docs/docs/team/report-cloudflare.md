---
title: Host the report on Cloudflare
description: Publish the report on Cloudflare Pages, behind a Cloudflare Access sign-in.
---

:::caution[An example, not a security review]
This is one setup we tested, shown as an example. Don't copy it blindly: check each step
against your company's security policies, and adapt it before you use it with real data.
See [Your setup, your responsibility](/docs/team/#your-setup-your-responsibility).
:::

Cloudflare Pages hosts the report folder, and Cloudflare Access puts a sign-in in front
of it. It's free for up to 50 people, with sign-in by email code or SSO (Google, GitHub,
Entra, Okta, or any SAML or OIDC provider).

:::danger[Set up the sign-in before the first deploy]
A Pages site is public at `https://<project>.pages.dev` from its first deploy until
Access protects it.
:::

## 1. Create the project

This needs Node; `npx` fetches Cloudflare's `wrangler` tool.

```bash
npx wrangler login
npx wrangler pages project create honest-agent-report --production-branch main
```

This reserves `honest-agent-report.pages.dev` without deploying anything. "Branch" is
only a label for uploads like these: always deploy with `--branch main`, or wrangler
guesses it from git.

## 2. Turn on Zero Trust

Dashboard → Zero Trust (shown as "Cloudflare One"): pick the **Free** plan and a team
name. The team name appears in the sign-in address, `<team>.cloudflareaccess.com`.

## 3. Allow sign-in by email code

Integrations → Identity providers: add **One-time PIN** if it isn't listed. It may not be
on by default, and without it only people with a Cloudflare account can sign in.

## 4. Create the Access application

Access controls → Applications → Add an application → **Self-hosted and private**.

- **Destinations → Add public hostname,** twice, picking `honest-agent-report.pages.dev`
  from the Domain menu:
  - with the subdomain **empty**, for the site itself;
  - with the subdomain `*`, for preview deployments. Every deploy also gets its own
    preview address.
- Don't use the **Workers** destination: Pages projects aren't listed there, and the
  Workers it lists are other sites.
- Make sure no row uses one of your own domains: that would put a sign-in in front of
  that whole site.
- Leave "browser-based RDP, SSH, or VNC" off.
- **Policy:** Action Allow, Include → Emails → the people who may see the report (or an
  email domain, a GitHub organisation, or a group from your identity provider).
- **Authentication:** "Accept all available identity providers" is fine.

## 5. Check the protection

Before deploying anything real:

```bash
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" https://honest-agent-report.pages.dev/data/report.json
```

It must answer `302`, redirecting to `https://<team>.cloudflareaccess.com/...`. A `200`
means the site is public: stop and fix Access first.

## 6. Deploy

```bash
honest-agent report
npx wrangler pages deploy honest_agent_report --project-name honest-agent-report --branch main
```

Open the address in a private window: you should get the sign-in page, then the report.
A new deploy shows up on a normal reload: Pages serves every file with
`public, max-age=0, must-revalidate`.

To deploy after every run, see [GitHub Actions](/docs/team/ci/).
