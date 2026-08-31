"""Verification and Packaging Script for FinXCore Digital Banking Platform."""

import os
import zipfile
import requests
import json

zip_filename = 'Digital Banking Platform.zip'
if os.path.exists(zip_filename):
    try:
        os.remove(zip_filename)
    except Exception as e:
        print(f"Warning: {e}")

print(f"Packaging repository into: {zip_filename}...")
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk('.'):
        # Exclude temporary caches
        if '__pycache__' in root or '.pytest_cache' in root or '.vscode' in root:
            continue
        for f in files:
            if f == zip_filename or f.endswith('.zip') or f.endswith('.pyc') or f.endswith('.db-journal') or f.endswith('.sqlite3'):
                continue
            filepath = os.path.join(root, f)
            arcname = os.path.relpath(filepath, '.')
            zf.write(filepath, arcname)

size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
print(f"Zip archive created: {size_mb:.2f} MB")

print("Posting to TrainPlex Checker Bot: https://train-plex-checker-bot-1--ttejaswar1234.replit.app/api/check")
try:
    with open(zip_filename, 'rb') as f:
        res = requests.post(
            'https://train-plex-checker-bot-1--ttejaswar1234.replit.app/api/check',
            files={'file': (zip_filename, f, 'application/zip')},
            timeout=120
        )
    print(f"HTTP Status: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        tp = data.get('trainplex', {})
        summary = tp.get('summary', {})
        print("=" * 60)
        print(f"OVERALL STATUS: {summary.get('overall')}")
        print(f"COMPLIANCE SCORE: {summary.get('score')}%")
        print(f"PASSED: {summary.get('passed')}/{summary.get('total')}")
        print(f"FAILED: {summary.get('failed')}")
        print(f"WARNED: {summary.get('warned')}")
        print(f"LOC: {summary.get('loc')}")
        print(f"GIT COMMITS: {summary.get('git', {}).get('commits')}")
        print(f"GIT PRS: {summary.get('git', {}).get('prs')}")
        print("=" * 60)
        print("Detailed Checklist:")
        for c in tp.get('checks', []):
            st = c.get('status', '').upper()
            print(f" [{st}] {c.get('name')}: {c.get('details')} (Value: {c.get('value')}, Required: {c.get('required')})")
            if st != 'PASS':
                print(f"       Fix Hint: {c.get('fix')}")
    else:
        print("Checker error response:", res.text)
except Exception as e:
    print(f"Verification request error: {e}")
