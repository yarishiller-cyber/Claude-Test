# Sherlock OSINT setup

This repo has [**Sherlock**](https://github.com/sherlock-project/sherlock)
installed — the free, open-source OSINT tool that hunts a **username** across
~400 social networks and reports where an account with that handle exists.

## What it does / doesn't do

- ✅ Input a **username/handle** → get a list of social-media profiles using it.
- ❌ It does **not** take a photo and identify a person. That "upload a photo,
  I'll do the digging" product is a *separate, paid* app ("Sherlock AI"), not
  this tool, and is not installed here.

### How images fit in anyway

You can still hand me an **image that contains a username** (a screenshot of a
profile, a bio, a business card, etc.). I'll read the handle out of the image
and run Sherlock on it for you. So the workflow is:

> screenshot with a handle in it → I extract the handle → Sherlock → results

## Usage

First-time setup (already done in this environment):

```bash
./osint.sh --setup
```

Run it:

```bash
./osint.sh torvalds                       # single username, all sites
./osint.sh alice bob --csv                # multiple usernames, CSV output
./osint.sh someuser --site GitHub --site Instagram --print-all
```

Results are written to `./results/` (git-ignored). Full flag list:

```bash
.venv/bin/sherlock --help
```

## Notes / caveats

- **Sandbox network:** this environment's outbound access is restricted, so
  some sites return proxy errors instead of hits. Results here are partial —
  run the same command on an unrestricted machine for full coverage.
- **False positives:** a "found" result means a profile page exists at that URL
  for that handle; it does **not** prove it's the same person across sites.
  Always verify manually.
- **Use responsibly.** OSINT on public data is legal in most places, but use it
  only for authorized purposes (your own accounts, security research, consented
  investigations). Don't use it to harass, stalk, or dox.
