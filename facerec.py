#!/usr/bin/env python3
"""
facerec.py — local face analysis with InsightFace (buffalo_l / ArcFace).

Three modes, all fully local. There is NO built-in database of people and NO
web access: this tool can only compare/search against faces YOU provide.

  detect  <image>                 Detect faces; print count, boxes, det score,
                                  and estimated age/gender per face.

  verify  <imageA> <imageB>       Are the largest face in A and B the same
                                  person? Prints cosine similarity + verdict.

  search  <probe> <gallery_dir>   Match the probe face against a folder of
                                  labeled images (one person per file/name).
                                  Ranks the gallery by similarity.

This does NOT identify strangers. To "recognize" someone you must already have
a labeled reference image of them in your gallery. Use only on your own photos
or with the consent of the people pictured.
"""
import sys, os, glob
import numpy as np
import cv2
from insightface.app import FaceAnalysis

# Cosine-similarity threshold for "same person" with buffalo_l / w600k_r50.
# ~0.6+ is a strong match, 0.4-0.6 possible, <0.4 likely different.
SAME_THRESHOLD = 0.5

_app = None
def app():
    global _app
    if _app is None:
        _app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
        _app.prepare(ctx_id=-1, det_size=(640, 640))
    return _app

def load(path):
    img = cv2.imread(path)
    if img is None:
        sys.exit(f"[!] Could not read image: {path}")
    return img

def largest_face(faces):
    if not faces:
        return None
    return max(faces, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))

def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def cmd_detect(path):
    faces = app().get(load(path))
    print(f"[*] {len(faces)} face(s) detected in {path}")
    for i, f in enumerate(sorted(faces, key=lambda f: f.bbox[0]), 1):
        x1, y1, x2, y2 = [int(v) for v in f.bbox]
        sex = 'M' if f.sex == 'M' else 'F'
        print(f"  face {i}: box=({x1},{y1})-({x2},{y2}) "
              f"score={f.det_score:.2f} est_age~{int(f.age)} est_sex={sex}")

def cmd_verify(a, b):
    fa = largest_face(app().get(load(a)))
    fb = largest_face(app().get(load(b)))
    if fa is None or fb is None:
        sys.exit("[!] No face found in one of the images.")
    sim = cosine(fa.normed_embedding, fb.normed_embedding)
    same = sim >= SAME_THRESHOLD
    print(f"[*] cosine similarity = {sim:.3f} (threshold {SAME_THRESHOLD})")
    print(f"[*] verdict: {'SAME person (likely)' if same else 'DIFFERENT people (likely)'}")

def cmd_search(probe, gallery_dir):
    fp = largest_face(app().get(load(probe)))
    if fp is None:
        sys.exit("[!] No face found in probe image.")
    files = [p for p in glob.glob(os.path.join(gallery_dir, '*'))
             if p.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp'))]
    if not files:
        sys.exit(f"[!] No images found in gallery: {gallery_dir}")
    scored = []
    for p in files:
        fg = largest_face(app().get(load(p)))
        if fg is None:
            continue
        scored.append((cosine(fp.normed_embedding, fg.normed_embedding), p))
    scored.sort(reverse=True)
    print(f"[*] probe: {probe}  vs  {len(scored)} gallery faces")
    for sim, p in scored[:10]:
        flag = ' <-- match' if sim >= SAME_THRESHOLD else ''
        print(f"  {sim:.3f}  {os.path.basename(p)}{flag}")

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    mode = sys.argv[1]
    if mode == 'detect' and len(sys.argv) == 3:
        cmd_detect(sys.argv[2])
    elif mode == 'verify' and len(sys.argv) == 4:
        cmd_verify(sys.argv[2], sys.argv[3])
    elif mode == 'search' and len(sys.argv) == 4:
        cmd_search(sys.argv[2], sys.argv[3])
    else:
        print(__doc__); sys.exit(1)

if __name__ == '__main__':
    main()
