# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x.x   | yes       |

## Reporting a Vulnerability

Please do not open a public GitHub issue for security vulnerabilities.

Email devneatharva@gmail.com with:
- A description of the vulnerability
- Steps to reproduce
- Potential impact

You will receive a response within 48 hours. Confirmed vulnerabilities will be patched and released promptly.

## Input Validation

All API endpoints validate inputs via FastAPI/Pydantic. Ticker symbols are normalised to uppercase. Hours parameters are bounded between 1 and 720.

## CORS Policy

By default the API allows all origins (`*`). In production, set `CORS_ORIGINS` in `.env` to restrict to known domains.

## Secrets Management

Never commit `.env` files. Use the provided `env.example` as a template. Rotate all secrets immediately if accidentally exposed.

## Dependency Security

Run `pip-audit` or `safety` regularly:
```bash
pip install pip-audit
pip-audit -r requirements.txt
```
