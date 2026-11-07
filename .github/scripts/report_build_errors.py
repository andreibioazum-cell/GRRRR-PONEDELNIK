#!/usr/bin/env python3
"""Print the interesting part of a Jam build log and report it as annotations."""

import re
import sys
from pathlib import Path

# Real diagnostics only - warning text can mention the word "error" too.
ERROR_PATTERN = re.compile(
	r"\berror:|^Error:|^\.\.\.failed|BUILD FAILURE|undefined reference|"
	r"cannot find|No such file or directory|command not found|"
	r"Segmentation fault|Permission denied|Operation not supported")

CONTEXT = 8
SOLVER_CONTEXT = 30
MAX_ANNOTATION_CHARS = 2800
TAIL_LINES = 100

# Package dependency problems are reported as a problem/solution list.
SOLVER_PATTERN = re.compile(
	r"nothing provides|Cannot install|problem \d|solution \d|"
	r"conflicting requests|does not belong to a distupgrade repository|"
	r"Failed to (?:open|resolve|install)|ERROR:", re.IGNORECASE)


def escape(text):
	# Workflow command escaping for annotation payloads.
	return (text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A"))


def annotate(message):
	message = message.strip()[:MAX_ANNOTATION_CHARS]
	if message:
		print(f"::error title=Build failure::{escape(message)}")


def main():
	if len(sys.argv) != 2:
		print("usage: report_build_errors.py <build log>")
		return 1

	log = Path(sys.argv[1])
	if not log.is_file():
		print(f"no build log at {log}")
		return 1

	lines = log.read_text(errors="replace").splitlines()
	tail = "\n".join(lines[-TAIL_LINES:])

	# The end of the log holds the failure that stopped the build.
	print("=== last log lines ===")
	print(tail)
	annotate("Tail of build log:\n" + tail)

	solver_hits = [i for i, line in enumerate(lines) if SOLVER_PATTERN.search(line)]
	if solver_hits:
		chunks = []
		for index in solver_hits[-4:]:
			start = max(0, index - SOLVER_CONTEXT)
			end = min(len(lines), index + SOLVER_CONTEXT + 1)
			chunks.append("\n".join(lines[start:end]))
		solver_text = "\n...\n".join(chunks)
		print("=== package solver diagnostics ===")
		print(solver_text)
		annotate("Package solver diagnostics:\n" + solver_text)

	hits = [i for i, line in enumerate(lines) if ERROR_PATTERN.search(line)]
	selected = []
	for index in hits[-12:]:
		start = max(0, index - CONTEXT)
		end = min(len(lines), index + CONTEXT + 1)
		selected.extend(lines[start:end])
		selected.append("...")

	diagnostics = "\n".join(selected)
	if diagnostics:
		print("=== matched diagnostics ===")
		print(diagnostics)
		annotate("Matched diagnostics:\n" + diagnostics)

	return 0


if __name__ == "__main__":
	sys.exit(main())
