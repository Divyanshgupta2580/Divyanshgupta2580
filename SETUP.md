# Setup and verification

## Contents

- `README.md` contains the public profile. [PROJECT-LINKS.md](./PROJECT-LINKS.md) records the featured project sources and verified demo links.
- `assets/systems-in-motion.jpg` and `assets/engineering-roles.svg` supply the profile artwork and animated role titles.
- `.github/workflows/snake.yml` refreshes the contribution snake on the `output` branch.
- `.github/workflows/profile-3d.yml` refreshes the 3D contribution chart at `profile-3d-contrib/profile-night-rainbow.svg`.
- `.github/workflows/waka-readme.yml` and `.github/scripts/update_waka.py` refresh WakaTime language reports for the last 7 days, 30 days, and year.

## Enable GitHub Actions

- Allow GitHub Actions to run in the [repository settings](https://github.com/Divyanshgupta2580/Divyanshgupta2580/settings/actions). The workflows request `contents: write` for the built-in `GITHUB_TOKEN`. Repository rules must permit the WakaTime and 3D chart workflows to update the default branch and the snake workflow to update `output`.
- The only custom Actions secret is `WAKATIME_API_KEY`. Set its value to the personal WakaTime OAuth token. A separate `GH_TOKEN` is unnecessary.
- Once the workflows are on the default branch, use [Generate Contribution Snake](https://github.com/Divyanshgupta2580/Divyanshgupta2580/actions/workflows/snake.yml) → **Run workflow** to refresh the SVGs immediately. The daily run is scheduled for midnight UTC.

## Enable the WakaTime language breakdown

1. Keep the API key configured in VS Code, Antigravity, and Sublime Text. Each editor sends activity to the same WakaTime account.
2. Sign in to the same account and copy your personal [WakaTime OAuth token](https://wakatime.com/oauth).
3. In [the profile repository’s Actions secrets](https://github.com/Divyanshgupta2580/Divyanshgupta2580/settings/secrets/actions), add or update `WAKATIME_API_KEY` with the OAuth token.
4. Once the workflow is on the default branch, open [Update WakaTime stats](https://github.com/Divyanshgupta2580/Divyanshgupta2580/actions/workflows/waka-readme.yml) and select **Run workflow**.

If the weekly request returns HTTP 401, replace the value of `WAKATIME_API_KEY` with a current personal OAuth token and run the workflow again. The API key configured in the editors is used to send activity.

Each period shows up to five languages ranked by time. Shares omit WakaTime’s `Other` category. When measured monthly or yearly data is unavailable, the updater uses the latest measured week to project 30 or 365 days at the same daily pace. The profile labels those tables as estimates and shows the source week’s end date. Measured figures take priority when WakaTime returns them.

## Rendering

GitHub renders the layout using Markdown and HTML. The artwork and role animation are stored in this repository. The skill badges and contribution graph use hosted image services.
