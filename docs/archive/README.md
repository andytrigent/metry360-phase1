# Archived documentation

These documents are **historical** — they describe earlier iterations of the project (Flask/SQLite local setup, pre-fix deployment claims, old email drafts, RCA investigations) and do NOT reflect the current system.

Important corrections relative to what these files claim:
- There is no Flask backend or SQLite database; the backend is AWS Lambda + S3 + DynamoDB (see root `README.md`).
- Before 2026-07-10 the upload pipeline did not actually work (no API Gateway route, upload page sent only file names, Lambda upload was a mock). Claims of "dynamic data loading" before that date were not accurate.
- The current architecture, API reference, deploy procedure, and honest feature status live in the root `README.md` and the parent `CLAUDE.md`.
