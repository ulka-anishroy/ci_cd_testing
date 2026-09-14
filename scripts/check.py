#!/usr/bin/env python3
"""Run local code quality and security checks for this project."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET_FILE = PROJECT_ROOT / "main.py"
LOG_DIR = PROJECT_ROOT / "logs"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOG_DIR / f"quality_check_{TIMESTAMP}.log"


def write_log(message: str) -> None:
    """Write a message to both the terminal and the log file."""
    print(message)
    with LOG_FILE.open("a", encoding="utf-8") as log:
        log.write(message + "\n")


def run_check(name: str, command: list[str]) -> bool:
    """Run a check and record its output and exit code."""
    separator = "=" * 70
    write_log(f"\n{separator}")
    write_log(f"CHECK: {name}")
    write_log(separator)
    write_log("$ " + " ".join(command))

    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        write_log(f"\nERROR: Failed to execute command: {exc}")
        write_log(f"FAIL: {name}")
        return False

    if result.stdout:
        write_log("\n--- STDOUT ---")
        write_log(result.stdout.rstrip())
    if result.stderr:
        write_log("\n--- STDERR ---")
        write_log(result.stderr.rstrip())

    write_log(f"\nExit code: {result.returncode}")
    passed = result.returncode == 0
    write_log(f"{'PASS' if passed else 'FAIL'}: {name}")
    return passed


def main() -> int:
    """Run all quality and security checks."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    write_log("=" * 70)
    write_log("PYTHON CODE QUALITY & SECURITY CHECK")
    write_log("=" * 70)
    write_log(f"Started: {datetime.now():%Y-%m-%d %H:%M:%S}")
    write_log(f"Target:  {TARGET_FILE}")
    write_log(f"Log:     {LOG_FILE}")

    if not TARGET_FILE.exists():
        write_log(f"\nERROR: Target file not found: {TARGET_FILE}")
        return 2

    checks = [
        ("Code Formatting", [sys.executable, "-m", "ruff", "format", "--check", str(TARGET_FILE)]),
        ("Linting", [sys.executable, "-m", "ruff", "check", str(TARGET_FILE)]),
        ("Static Type Checking", [sys.executable, "-m", "pyright", str(TARGET_FILE)]),
        ("Security Scan", [sys.executable, "-m", "bandit", "-q", "-r", str(TARGET_FILE)]),
        (
            "Dependency Vulnerability Scan",
            [sys.executable, "-m", "pip_audit", "-r", str(PROJECT_ROOT / "requirements-dev.txt")],
        ),
    ]

    required_modules = {"ruff": "ruff", "pyright": "pyright", "bandit": "bandit", "pip_audit": "pip_audit"}
    missing = [name for name, module in required_modules.items() if importlib.util.find_spec(module) is None]
    if missing:
        write_log("\nERROR: Missing required tools: " + ", ".join(missing))
        write_log("Install them with: python -m pip install -r requirements-dev.txt")
        return 2

    results = {name: run_check(name, command) for name, command in checks}

    write_log(f"\n{'=' * 70}")
    write_log("QUALITY & SECURITY CHECK SUMMARY")
    write_log(f"{'=' * 70}")
    for name, passed in results.items():
        write_log(f"{'PASS' if passed else 'FAIL'}  {name}")
    write_log(f"\nCompleted: {datetime.now():%Y-%m-%d %H:%M:%S}")

    overall_passed = all(results.values())
    write_log(f"Overall result: {'PASS' if overall_passed else 'FAIL'}")
    return 0 if overall_passed else 1


if __name__ == "__main__":
    sys.exit(main())