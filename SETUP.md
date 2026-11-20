# Setup and verification

This archive contains a GitHub profile README package, not a copy of your complete Git repository.

## Contents
- `README.md` — profile README source.
- `assets/hero-laptop.png` — extracted hero illustration from the approved visual reference.
- `assets/approved-design-reference.png` — full approved reference image.
- `.github/workflows/waka-readme.yml` and `.github/scripts/update_waka.py` — daily WakaTime language reports for the last 7 days, 30 days, and year.

## Before publishing
1. Copy `README.md` and the `assets/` folder into `Divyanshgupta2580/Divyanshgupta2580`.
2. Verify the RevenueOS repository URL and replace its fallback link with the exact repository URL.
3. Verify the JanSetu repository URL and replace it if the project lives under a different owner/repository.
4. The Resume badge currently points to your portfolio because no resume PDF was supplied with this request. Once you add a PDF, upload it (for example, `assets/Divyansh-Gupta-Resume.pdf`) and update the badge link to that path.

## Enable the WakaTime language breakdown

1. Keep the API key configured in VS Code, Antigravity, and Sublime Text. Each editor sends activity to the same WakaTime account.
2. Sign in to the same account and copy your personal [WakaTime OAuth token](https://wakatime.com/oauth).
3. In [the profile repository’s Actions secrets](https://github.com/Divyanshgupta2580/Divyanshgupta2580/settings/secrets/actions), add or update `WAKATIME_API_KEY` with the OAuth token.
4. Once the workflow is on the default branch, open [Update WakaTime stats](https://github.com/Divyanshgupta2580/Divyanshgupta2580/actions/workflows/waka-readme.yml) and select **Run workflow**. The workflow uses the built-in `GITHUB_TOKEN` with `contents: write` to update the README. Repository rules must allow those updates.

Each period shows up to five languages ranked by tracked time. Shares use all identified language time in that period and omit WakaTime’s `Other` category. WakaTime may take longer to calculate the yearly range on the first request. The updater keeps that section until WakaTime has the result ready.

## Important limitations
- GitHub README does not execute arbitrary JavaScript or custom CSS. The typing animation uses a hosted SVG service.
- Contribution and GitHub stats images are provided by third-party endpoints and may occasionally be unavailable.
- The visual reference is a design target. GitHub's Markdown renderer does not support exact pixel-level reproduction of a web page.

## Safety
No API keys, access tokens, or other secrets are included in this archive.
