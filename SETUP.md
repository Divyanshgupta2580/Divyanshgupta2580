# Setup and verification

This archive contains a GitHub profile README package, not a copy of your complete Git repository.

## Contents
- `README.md` — profile README source.
- `assets/hero-laptop.png` — extracted hero illustration from the approved visual reference.
- `assets/approved-design-reference.png` — full approved reference image.
- `.github/workflows/waka-readme.yml` — optional WakaTime updater workflow.

## Before publishing
1. Copy `README.md` and the `assets/` folder into `Divyanshgupta2580/Divyanshgupta2580`.
2. Verify the RevenueOS repository URL and replace its fallback link with the exact repository URL.
3. Verify the JanSetu repository URL and replace it if the project lives under a different owner/repository.
4. The Resume badge currently points to your portfolio because no resume PDF was supplied with this request. Once you add a PDF, upload it (for example, `assets/Divyansh-Gupta-Resume.pdf`) and update the badge link to that path.
5. Confirm the `WAKATIME_API_KEY` secret exists in the profile repository's Actions secrets.
6. Enable GitHub Actions and run the WakaTime workflow once.

## Important limitations
- GitHub README does not execute arbitrary JavaScript or custom CSS. The typing animation uses a hosted SVG service.
- Contribution and GitHub stats images are provided by third-party endpoints and may occasionally be unavailable.
- WakaTime numbers populate only after the workflow runs successfully and the WakaTime account has tracked editor activity.
- The visual reference is a design target. GitHub's Markdown renderer does not support exact pixel-level reproduction of a web page.

## Safety
No API keys, access tokens, or other secrets are included in this archive.
