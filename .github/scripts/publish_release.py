#!/usr/bin/env python3
"""Publish the built images as release assets.

Workflow artifacts need a GitHub login and arrive as a zip, which is awkward on
a phone. A release asset is a direct download, so the disk image can be handed
straight to an emulator.
"""

import json
import os
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"
TAG = "latest"


def request(url, method="GET", payload=None, token=None, data=None,
            content_type="application/json"):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ponedelnikos-build",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    body = data
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
    if body is not None:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=900) as response:
        raw = response.read()
    return json.loads(raw) if raw else None


def main():
    repo = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GITHUB_TOKEN"]
    sha = os.environ["GITHUB_SHA"]
    assets = sys.argv[1:]
    if not assets:
        print("no assets to publish")
        return 0

    base = f"{API}/repos/{repo}"

    # Replace the previous rolling release so the tag always names the newest
    # validated build.
    try:
        existing = request(f"{base}/releases/tags/{TAG}", token=token)
    except urllib.error.HTTPError as error:
        if error.code != 404:
            raise
        existing = None

    if existing:
        request(f"{base}/releases/{existing['id']}", method="DELETE",
                token=token)
    try:
        request(f"{base}/git/refs/tags/{TAG}", method="DELETE", token=token)
    except urllib.error.HTTPError as error:
        if error.code not in (404, 422):
            raise

    release = request(f"{base}/releases", method="POST", token=token, payload={
        "tag_name": TAG,
        "target_commitish": sha,
        "name": "PonedelnikOS " + sha[:8],
        "body": (
            "Bootable PonedelnikOS images built from " + sha + ".\n\n"
            "* `PonedelnikOS.iso` - anyboot image, boot it as a CD or a disk.\n"
            "* `PonedelnikOS.img` - the same bytes, named for emulators that "
            "only accept a raw disk in the hard disk slot.\n\n"
            "Both are validated to reach the kernel in QEMU, including a "
            "device set without ACPI, USB and networking."
        ),
        "prerelease": True,
        "make_latest": "false",
    })

    upload = release["upload_url"].split("{")[0]
    for path in assets:
        name = os.path.basename(path)
        with open(path, "rb") as handle:
            data = handle.read()
        request(f"{upload}?name={name}", method="POST", token=token, data=data,
                content_type="application/octet-stream")
        print("uploaded", name, len(data), "bytes")

    print("release:", release["html_url"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
