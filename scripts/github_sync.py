"""Secure NAVARIS GitHub Contents API helper.

Credentials are read only from NAVARIS_GITHUB_TOKEN (or passed explicitly by a caller).
Never hard-code personal access tokens in source files.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path, PurePosixPath
from typing import Any

DEFAULT_REPOSITORY = "mohamed007hafez-bit/navaris-business-intelligence-os"
API_ROOT = "https://api.github.com/repos/"


class SyncError(RuntimeError):
    """A safe-to-display synchronization error without credential contents."""


def validate_repo_path(value: str) -> str:
    """Return a normalized repository-relative path or reject traversal."""
    if not value or value.startswith("/") or "\\" in value or "\x00" in value:
        raise ValueError("Repository path must be relative and use forward slashes.")
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise ValueError("Repository path must not contain empty, dot, or parent segments.")
    return PurePosixPath(*parts).as_posix()


def _validate_repository(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value):
        raise ValueError("Repository must use owner/name format.")
    return value


def _request(url: str, token: str, *, method: str = "GET", payload: dict[str, Any] | None = None) -> dict[str, Any] | None:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=body, method=method)
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    request.add_header("User-Agent", "NAVARIS-Core-Sync")
    if body is not None:
        request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404 and method == "GET":
            return None
        # Do not echo request headers or token values into logs.
        raise SyncError(f"GitHub API request failed with HTTP {exc.code}. Check token scope, repository, and branch.") from None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        raise SyncError("GitHub API request failed due to a network, timeout, or JSON response error.") from None


def push_file_to_github(
    file_path: str,
    file_content: str,
    commit_message: str,
    *,
    repository: str | None = None,
    branch: str = "main",
    token: str | None = None,
) -> dict[str, Any]:
    """Create or update one text file using a token supplied outside the repository."""
    repo_path = validate_repo_path(file_path)
    repo = _validate_repository(repository or os.environ.get("NAVARIS_GITHUB_REPO", DEFAULT_REPOSITORY))
    credential = token or os.environ.get("NAVARIS_GITHUB_TOKEN")
    if not credential:
        raise SyncError("Set NAVARIS_GITHUB_TOKEN in the local environment; no credential is stored in this repository.")
    if not branch.strip() or "\n" in branch:
        raise ValueError("Branch must be a non-empty single-line name.")
    if not commit_message.strip():
        raise ValueError("Commit message must be non-empty.")

    endpoint = f"{API_ROOT}{repo}/contents/{urllib.parse.quote(repo_path, safe='/')}"
    metadata = _request(f"{endpoint}?{urllib.parse.urlencode({'ref': branch})}", credential)
    payload: dict[str, Any] = {
        "message": commit_message,
        "content": base64.b64encode(file_content.encode("utf-8")).decode("ascii"),
        "branch": branch,
    }
    if metadata and metadata.get("sha"):
        payload["sha"] = metadata["sha"]
    result = _request(endpoint, credential, method="PUT", payload=payload)
    if not result or not result.get("commit", {}).get("sha"):
        raise SyncError("GitHub API did not confirm a commit SHA.")
    return {"path": repo_path, "branch": branch, "commit_sha": result["commit"]["sha"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sync one local text file to the NAVARIS GitHub repository.")
    parser.add_argument("local_file", type=Path)
    parser.add_argument("--repo-path", help="Destination path relative to repository root; defaults to local filename.")
    parser.add_argument("--repository", default=os.environ.get("NAVARIS_GITHUB_REPO", DEFAULT_REPOSITORY))
    parser.add_argument("--branch", default="main")
    parser.add_argument("--message", default="chore: sync NAVARIS file")
    args = parser.parse_args(argv)
    try:
        text = args.local_file.read_text(encoding="utf-8")
        result = push_file_to_github(
            args.repo_path or args.local_file.name,
            text,
            args.message,
            repository=args.repository,
            branch=args.branch,
        )
    except (OSError, UnicodeError, ValueError, SyncError) as exc:
        print(f"NAVARIS sync failed: {exc}", file=sys.stderr)
        return 1
    print(f"Committed {result['path']} to {result['branch']}: {result['commit_sha']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
