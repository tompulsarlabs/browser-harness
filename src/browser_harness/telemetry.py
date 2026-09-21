"""Best-effort, explicitly opted-in, content-free usage analytics for browser-harness."""

from __future__ import annotations

import json
import math
import os
import platform
import re
import subprocess
import sys
import uuid
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from urllib.parse import urlparse

from . import paths

POSTHOG_KEY = "phc_rCPCLPtaXB3EuBdiH7JLKtU2Wj5iPnuwdsbw58CnjYXc"
POSTHOG_HOST = "https://eu.i.posthog.com"
DISABLE_ENVS = ("BH_TELEMETRY", "BROWSER_HARNESS_TELEMETRY", "ANONYMIZED_TELEMETRY")
CONSENT_VERSION = 1
COMMANDS = frozenset("script help version doctor update reload debug-clicks auth skill mac-approve recordings telemetry video usage".split())
HELPERS = frozenset("cdp drain_events goto_url page_info click_at_xy type_text fill_input press_key scroll capture_screenshot list_tabs current_tab activate_tab switch_tab new_tab close_tab ensure_real_tab iframe_target wait wait_for_load wait_for_element wait_for_network_idle js dispatch_key upload_file http_get".split())


def _number(value, *, integer=False):
    if type(value) not in (int, float) or (integer and type(value) is not int):
        return None
    return value if math.isfinite(value) and 0 <= value <= 1_000_000_000 else None


def _choice(value, allowed):
    return value if isinstance(value, str) and value in allowed else "other"


def _safe_properties(properties: dict | None) -> dict:
    """Allowlist at the export boundary; never export caller-controlled text."""
    p = properties if isinstance(properties, dict) else {}
    out = {
        "action": _choice(p.get("action"), {"completed", "error"}),
        "command": _choice(p.get("command"), COMMANDS),
        "browser": _choice(p.get("browser"), {"cloud", "cdp", "local"}),
    }
    for key in ("task_length", "output_length", "step_count", "exit_code"):
        out[key] = _number(p.get(key), integer=True)
    out["duration_seconds"] = _number(p.get("duration_seconds"))
    out["steps"] = []
    for step in (p.get("steps") if isinstance(p.get("steps"), list) else [])[:500]:
        if not isinstance(step, dict):
            continue
        out["steps"].append({
            "helper": _choice(step.get("helper"), HELPERS),
            "duration_seconds": _number(step.get("duration_seconds")),
            "failed": step.get("failed") is True or "error" in step,
        })
    return out


def _config_dir() -> Path:
    return paths.config_dir()


def _config_path() -> Path:
    return _config_dir() / "telemetry.json"


def _load_config() -> dict:
    try:
        data = json.loads(_config_path().read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (FileNotFoundError, OSError, ValueError):
        return {}


def _save_config(data: dict) -> None:
    path = _config_path()
    try:
        parent_existed = path.parent.exists()
        path.parent.mkdir(parents=True, exist_ok=True)
        if not parent_existed and platform.system() != "Windows":
            os.chmod(path.parent, 0o700)
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if platform.system() != "Windows":
            os.chmod(path, 0o600)
    except OSError:
        pass


def _version() -> str:
    try:
        return version("browser-harness")
    except PackageNotFoundError:
        return ""
    except Exception:
        return ""


def _env_disabled() -> bool:
    return any((os.environ.get(name) or "").lower() in {"0", "false", "no", "off"} for name in DISABLE_ENVS)


def _valid_install_id(raw) -> bool:
    return isinstance(raw, str) and re.fullmatch(r"[0-9a-f-]{32,36}", raw) is not None


def _install_id(config: dict | None = None, *, create: bool = True) -> str | None:
    config = config if config is not None else _load_config()
    raw = config.get("install_id")
    if _valid_install_id(raw):
        return raw
    if not create:
        return None
    install_id = str(uuid.uuid4())
    _save_config({**config, "install_id": install_id})
    return install_id


def _consented(config: dict) -> bool:
    # Legacy disabled=false was the default, not informed consent to this policy.
    return type(config.get("consent_version")) is int and config["consent_version"] == CONSENT_VERSION and config.get("disabled") is False


def is_enabled() -> bool:
    if _env_disabled():
        return False
    return _consented(_load_config())


def status() -> dict:
    config = _load_config()
    env_disabled = _env_disabled()
    enabled = not env_disabled and _consented(config)
    return {
        "enabled": enabled,
        "disabled_by_env": env_disabled,
        "disabled_by_config": not _consented(config),
        "policy": "content-free-v1",
        "destination": os.environ.get("BH_POSTHOG_HOST", POSTHOG_HOST),
        "install_id": _install_id(config, create=enabled),
        "config_path": str(_config_path()),
    }


def set_enabled(enabled: bool) -> dict:
    config = _load_config()
    config["disabled"] = not enabled
    config["consent_version"] = CONSENT_VERSION
    _save_config(config)
    return status()


_DETACHED_SENDER_SOURCE = """
import json, sys, urllib.request
try:
    job = json.load(sys.stdin)
    request = urllib.request.Request(
        job['url'],
        method='POST',
        data=json.dumps(job['payload']).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'User-Agent': 'browser-harness'},
    )
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    urllib.request.build_opener(NoRedirect()).open(request, timeout=job['timeout']).close()
except Exception:
    pass
"""


def _send_detached(payload: dict) -> None:
    """Hand the event to a detached helper process so the CLI never blocks."""
    host = os.environ.get("BH_POSTHOG_HOST", POSTHOG_HOST).rstrip("/")
    endpoint = urlparse(host)
    if endpoint.scheme != "https" or not endpoint.hostname or endpoint.username or endpoint.password or endpoint.query or endpoint.fragment:
        return  # never send analytics over plaintext or credential-bearing URLs
    job = {
        "url": f"{host}/i/v0/e/",
        "timeout": float(os.environ.get("BH_TELEMETRY_TIMEOUT", "5")),
        "payload": payload,
    }
    process = subprocess.Popen(
        [sys.executable, "-c", _DETACHED_SENDER_SOURCE],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    assert process.stdin is not None
    process.stdin.write(json.dumps(job).encode("utf-8"))
    process.stdin.close()


def _base_properties() -> dict:
    return {
        "browser_harness_version": _version() or "unknown",
        "python_version": platform.python_version(),
        "os": platform.system() or "unknown",
        "machine": platform.machine() or "unknown",
    }


def capture(event: str, properties: dict | None = None) -> None:
    if event != "cli_event" or not is_enabled():
        return
    try:
        payload = {
            "api_key": POSTHOG_KEY,
            "distinct_id": _install_id(),
            "event": event,
            "properties": {
                **_base_properties(),
                "$process_person_profile": False,
                **_safe_properties(properties),
            },
        }
        _send_detached(payload)
    except Exception:
        return


def capture_cli_event(
    *,
    action: str,
    command: str,
    task: str | None = None,
    browser: str | None = None,
    output: str | None = None,
    output_length: int | None = None,
    steps: list | None = None,
    step_count: int | None = None,
    duration_seconds: float | None = None,
    exit_code: int | None = None,
    error_message: str | None = None,
) -> None:
    # Keep the callable signature compatible, but never serialize raw inputs.
    capture("cli_event", {
        "action": action, "command": command, "browser": browser,
        "task_length": len(task) if isinstance(task, str) else None,
        "output_length": output_length, "steps": steps, "step_count": step_count,
        "duration_seconds": duration_seconds, "exit_code": exit_code,
    })


def run_telemetry_cli(argv: list[str]) -> int:
    if not argv or argv == ["status"]:
        print(json.dumps(status(), indent=2))
        return 0
    if argv == ["disable"]:
        print(json.dumps(set_enabled(False), indent=2))
        return 0
    if argv == ["enable"]:
        print(json.dumps(set_enabled(True), indent=2))
        return 0
    print("usage: browser-harness telemetry [status|enable|disable]")
    return 2
