#!/usr/bin/env python3
"""Print the interesting part of a Jam build log and report it as annotations."""

import re
import sys
from pathlib import Path

# Compiler, linker and Jam diagnostics we want to see first.
ERROR_PATTERN = re.compile(
	r"error:|Error \d|fatal error|undefined reference|cannot find|"
	r"No such file or directory|not found|BUILD FAILURE|failed updating",
	re.IGNORECASE)

CONTEXT = 6
MAX_ANNOTATION_CHARS = 3000
TAIL_LINES = 120


def escape(text):
	# Workflow command escaping for annotation payloads.
	return (text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A"))


def main():
	if len(sys.argv) != 2:
		print("usage: report_build_errors.py <build log>")
		return 1

	log = Path(sys.argv[1])
	if not log.is_file():
		print(f"no build log at {log}")
		return 1

	lines = log.read_text(errors="replace").splitlines()

	hits = [i for i, line in enumerate(lines) if ERROR_PATTERN.search(line)]
	selected = []
	for index in hits[:20]:
		start = max(0, index - CONTEXT)
		end = min(len(lines), index + CONTEXT + 1)
		selected.extend(lines[start:end])
		selected.append("...")

	print("=== build diagnostics ===")
	diagnostics = "\n".join(selected) if selected else "\n".join(lines[-TAIL_LINES:])
	print(diagnostics)

	print(f"=== last {TAIL_LINES} log lines ===")
	print("\n".join(lines[-TAIL_LINES:]))

	message = diagnostics[:MAX_ANNOTATION_CHARS]
	if message:
		print(f"::error title=Build failure::{escape(message)}")

	return 0


if __name__ == "__main__":
	sys.exit(main())
