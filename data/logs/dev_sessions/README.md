# Development Session Logs

All session logs are stored as UTF-8 encoded JSON files, with filenames indicating the session start and end times (e.g., session_YYYY-MM-DDTHHMMSS_to_YYYY-MM-DDTHHMMSS.json). Each log contains:
- Session metadata (start/end, participants, notes, encoding)
- An array of prompt/response history entries, each with a timestamp, role (user/assistant), and content

**Format Example:**
```json
{
	"session_metadata": {
		"start": "2026-02-08T00:00:00",
		"end": "2026-02-08T23:59:59",
		"participants": ["Andy Turner", "GitHub Copilot"],
		"encoding": "UTF-8",
		"notes": "Session log is a partial, human-curated record of prompt/response and key actions. Not all development steps or context are captured."
	},
	"history": [ ... ]
}
```

Use GitHub LFS for large files. Reference specific logs in documentation or JOSS submission as needed.

## Session Log Summaries

| Filename | Start | End | Participants | Notes |
|----------|-------|-----|--------------|-------|
| session_2026-02-08T000000_to_2026-02-08T235959.json | 2026-02-08T00:00:00 | 2026-02-08T23:59:59 | Andy Turner, GitHub Copilot | Example session log for 2026-02-08 |

Add a row for each session log as it is created. This table provides a quick reference and summary for the archive.
