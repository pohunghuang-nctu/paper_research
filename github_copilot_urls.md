# GitHub Copilot Backend API URLs

This document lists the URLs that GitHub Copilot and Copilot Chat extensions for VSCode connect to for their backend services. This information is based on the official GitHub documentation and is useful for configuring firewalls or proxy servers.

## Main Copilot API Endpoints

These are the core URLs for Copilot's functionality:

- **Primary API Endpoint**:
  - `https://api.github.com/copilot_internal/*`

- **Copilot Services (including Chat)**:
  - `https://*.githubcopilot.com/*` (Wildcard domain for main services, especially Chat)
  - `https://copilot-proxy.githubusercontent.com/*`

- **Subscription-Specific Subdomains**:
  - `https://*.individual.githubcopilot.com/*` (For Personal plan)
  - `https://*.business.githubcopilot.com/*` (For Business plan)
  - `https://*.enterprise.githubcopilot.com/*` (For Enterprise plan)

- **Telemetry and Experimental Features**:
  - `https://copilot-telemetry.githubusercontent.com/telemetry/*`
  - `https://default.exp-tas.com/*` (For feature flags and A/B testing)

## Supporting GitHub URLs

Copilot also needs access to standard GitHub services for authentication and context:

- `https://api.github.com/*`
- `https://github.com/*`
- `https://avatars.githubusercontent.com/*`
- `https://raw.githubusercontent.com/*`

## Microsoft Authentication (if using Entra ID)
If your organization uses Microsoft Entra ID for authentication, these URLs are also required:

- `https://login.microsoftonline.com/*`
- `https://aadcdn.msauth.net/*`
- `https://login.live.com/*`
- `https://*.activedirectory.windowsazure.com/*`


## Reference

This list is compiled from the official GitHub documentation:
- [Configuring network settings for GitHub Copilot](https://docs.github.com/en/copilot/managing-copilot/managing-github-copilot-in-your-organization/configuring-your-proxy-server-or-firewall-for-copilot)
