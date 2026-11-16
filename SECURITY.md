# Security Policy

Last updated: 14 November 2026. Web version: https://radova.org/latest/security/policy/

This policy explains how to report a security vulnerability in Radova Linux privately, what is in scope, and what you can expect from us.

## Report a vulnerability

Email [security@example.org](mailto:security@example.org) with the details. Please report privately: do not open a public issue, pull request, or discussion, and do not share the details publicly until a fix or advisory is out.

Include as much of the following as you can:

- What is affected: the Radova Linux version, the application (Memora, Evrocks, Coretez, or Linkers), or the web page.
- Steps to reproduce, or a proof of concept.
- The impact you observed or expect.
- How we can reach you, and whether you would like to be credited in the advisory.

## Scope

In scope:

- Radova Linux and the packages and configuration it ships.
- Memora, Evrocks, Coretez, and Linkers as shipped in Radova Linux.
- The radova.org websites, including Radova Latest.

Out of scope:

- Vulnerabilities in upstream software that Radova Linux ships unchanged. Please report those to the upstream project; we are happy to help coordinate.
- Denial-of-service or load testing against radova.org.
- Social engineering, phishing, and physical attacks.
- Reports from automated scanners without a demonstrated impact.

## What to expect

- We acknowledge your report within 3 business days.
- We send an initial assessment, including whether we can reproduce the issue and its severity, within 10 business days.
- We keep you updated at least every 14 days until the issue is resolved.

## Coordinated disclosure

We ask that you give us up to 90 days from your report to release a fix before you disclose the issue publicly. We agree the publication date with you, and may publish earlier if the vulnerability is being actively exploited.

Once a fix or mitigation is available, we publish an advisory on [Radova Latest: Security](https://radova.org/latest/security/) with its advisory ID, severity, affected and patched versions, and credit for the reporter if they want it.

## Good-faith research

We will not pursue legal action against research done in good faith that follows this policy: report privately, avoid privacy violations and data destruction, and do not degrade our services.
