# GitHub Copilot and Copilot Chat Required URLs

This document lists the URLs that need to be accessible for GitHub Copilot and GitHub Copilot Chat to function correctly, especially when behind a firewall or proxy server.

**Source:** [Configuring your proxy server or firewall for Copilot - GitHub Docs](https://docs.github.com/en/copilot/managing-copilot/managing-github-copilot-in-your-organization/configuring-your-proxy-server-or-firewall-for-copilot)

---

## Public URLs

These URLs are for the public version of GitHub.

- `https://github.com/login/*`
- `https://api.github.com/user`
- `https://api.github.com/copilot_internal/*`
- `https://copilot-telemetry.githubusercontent.com/telemetry`
- `https://default.exp-tas.com`
- `https://copilot-proxy.githubusercontent.com`
- `https://origin-tracker.githubusercontent.com`
- `https://*.githubcopilot.com`
- `https://*.individual.githubcopilot.com`
- `https://*.business.githubcopilot.com`
- `https://*.enterprise.githubcopilot.com`

## GitHub Enterprise Related URLs

If you are using GitHub Enterprise, you will also need to allow these URLs. Replace `YOUR-ENTERPRISE` with your actual enterprise name.

- `https://github.com/YOUR-ENTERPRISE/*`
- `https://github.com/YOUR-ENTERPRISE?*`
- `https://github.com/enterprises/YOUR-ENTERPRISE/*`
