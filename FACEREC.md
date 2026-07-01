# Local face analysis (InsightFace)

Installed: **InsightFace** with the **buffalo_l** model pack (ArcFace recognition
+ RetinaFace detection + gender/age), running on CPU via `onnxruntime`. Fully
local — no cloud API, no account.

## The one thing to understand

This tool has **no database of people** and **no internet search**. It cannot
tell you who a stranger is. It can only:

- **detect** faces in an image you give it, and
- **compare** a face against other faces **you** provide.

That is the fundamental difference from PimEyes/Clearview, which work by having
scraped billions of labeled faces off the web. Nothing open-source ships that
gallery, and I did not build one.

## Usage

```bash
# How many faces, where, and rough age/sex estimate
.venv/bin/python facerec.py detect photo.jpg

# Are these two photos the same person? (1:1 verification)
.venv/bin/python facerec.py verify me_2020.jpg me_2024.jpg

# Rank a folder of labeled photos by similarity to a probe (1:N against
# a gallery YOU assembled — e.g. your own photo library)
.venv/bin/python facerec.py search probe.jpg ./my_gallery/
```

`verify`/`search` use cosine similarity of 512-d ArcFace embeddings.
Rule of thumb with buffalo_l: `>0.5` likely same person, `>0.6` strong,
`<0.4` likely different. Always eyeball the actual images — embeddings give
false matches, especially across age, lighting, and look-alikes.

## Acceptable use

Face recognition pointed at people is high-impact. Use this only for:

- your **own** photos (dedup, organize, verify it's the same you across pics),
- identity checks **with the consent** of the person pictured,
- research/testing on public benchmark datasets.

Do **not** use it to identify, track, or profile people without their consent.
I won't help extend this into a web-scraping or stranger-identification
pipeline — that's the part that harms people, and it's also illegal in a
growing number of places (BIPA, GDPR, etc.).

## Files / storage

- `facerec.py` — the CLI.
- Model weights live in `~/.insightface/models/buffalo_l/` (~280 MB, auto-
  downloaded once; not in this repo).
- The `.venv/` holds insightface + onnxruntime + opencv (git-ignored).
