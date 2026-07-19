# IMAP-Based Gmail Scanner (OAuth Bypass)

Create a new IMAP-based Gmail scanner using Python's built-in `imaplib` to scan email metadata for `amd949609@gmail.com` using a Google App Password, bypassing the problematic OAuth/browser flow. Ingest the metadata directly into the existing BigQuery table `gmail_index`.

## User Review Required
> [!IMPORTANT]
> The scanner will require a Google App Password for `amd949609@gmail.com`. You must set the environment variable `GMAIL_APP_PASSWORD` on your system before running the script, or provide it at the runtime prompt.

## Open Questions
- None. We will proceed with the standard table schema and insert flow.

## Proposed Changes

### Forensic Scanner Component

#### [NEW] [scan_gmail_imap.py](file:///c:/Users/HP/OneDrive/Documents/OsintNeoAi/agent/scan_gmail_imap.py)
- Establish connection to `imap.gmail.com` via SSL.
- Log in using `amd949609@gmail.com` and the App Password.
- Iterate and fetch header fields (`Message-ID`, `From`, `To`, `Subject`, `Date`, `Snippet`) from all or selected mailboxes.
- Format metadata records to match the `gmail_index` schema.
- Stream metadata into BigQuery: `project-743aab84-f9a5-4ec7-954.national_audits.gmail_index`.

## Verification Plan
- Run the script locally in dry-run mode (printing headers without BQ upload).
- Run the script to ingest a small batch of messages and verify counts in BigQuery.
