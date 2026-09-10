"""Adapter for the HDC install, aa and HiLog command family."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile

from .process import CommandCancelled, execute


class DeviceError(Exception):
    def __init__(self, code, message, evidence=None):
        super().__init__(message)
        self.code = code
        self.evidence = evidence


def identifier(value, label):
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", value):
        raise DeviceError("INVALID_INPUT", f"Invalid {label}")
    return value


def inspect_hap(path):
    path = Path(path).resolve(strict=True)
    if path.suffix.lower() != ".hap" or not path.is_file():
        raise DeviceError("INVALID_HAP", "Expected a single HAP file")
    try:
        with zipfile.ZipFile(path) as archive:
            info = archive.getinfo("module.json")
            if info.file_size > 2 * 1024 * 1024:
                raise DeviceError("INVALID_HAP", "Oversized module metadata")
            metadata = json.loads(archive.read(info))
        app, module = metadata["app"], metadata["module"]
        bundle = identifier(app["bundleName"], "bundle")
        abilities = [identifier(a["name"], "ability") for a in module.get("abilities", [])]
        module_name = identifier(module["name"], "module")
    except (KeyError, TypeError, ValueError, zipfile.BadZipFile) as error:
        raise DeviceError("INVALID_HAP", "Cannot read HAP module metadata") from error
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return {
        "path": str(path), "sha256": digest.hexdigest(), "bytes": path.stat().st_size,
        "bundle": bundle, "module": module_name, "abilities": abilities,
        "version": app.get("versionName"),
        "signature": "not locally verified; device installer is authoritative",
    }


class Hdc:
    def __init__(self, executable=None, runner=execute):
        resolved = shutil.which(executable or "hdc")
        if not resolved:
            raise DeviceError("HDC_MISSING", "HDC not found; supply --hdc or configure PATH")
        if Path(resolved).suffix.lower() in (".bat", ".cmd"):
            raise DeviceError("INVALID_HDC", "Use the HDC executable, not a shell wrapper")
        self.executable = resolved
        self.runner = runner
        self.device = None
        self.evidence = []

    def argv(self, args):
        return [self.executable] + (["-t", self.device] if self.device else []) + args

    def call(self, args, timeout=20):
        try:
            result = self.runner(self.argv(args), timeout=timeout)
        except CommandCancelled as error:
            self.evidence.append(error.evidence)
            raise
        self.evidence.append(result)
        if result["timed_out"]:
            raise DeviceError("COMMAND_TIMEOUT", "HDC command timed out", result)
        if result["truncated"]:
            raise DeviceError("OUTPUT_LIMIT", "HDC output exceeded the limit", result)
        if result["exit_code"] != 0:
            raise DeviceError("COMMAND_FAILED", "HDC command failed", result)
        return result["output"]

    def devices(self):
        text = self.call(["list", "targets"])
        if "[Empty]" in text or not text.strip():
            return []
        values = text.split()
        if not all(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]*", v) for v in values):
            raise DeviceError("DEVICE_LIST_UNKNOWN", "Unrecognized device enumeration output")
        return list(dict.fromkeys(values))

    def select(self, requested=None):
        devices = self.devices()
        if requested:
            if requested not in devices:
                raise DeviceError("DEVICE_UNAVAILABLE", "Selected device is not connected")
            self.device = requested
        elif len(devices) == 1:
            self.device = devices[0]
        else:
            raise DeviceError("NO_DEVICE" if not devices else "DEVICE_REQUIRED",
                              "Connect one authorized device or specify --device")
        return self.device

    def check_capabilities(self):
        # Fail closed if this tool family cannot confirm the required switches.
        checks = [(["shell", "aa", "start", "-h"], ["-b", "-a", "-m"]),
                  (["shell", "hilog", "-h"], ["epoch", "-t", "-P"])]
        for args, expected in checks:
            help_text = self.call(args)
            if not all(token in help_text for token in expected):
                raise DeviceError("UNSUPPORTED_TOOLS", "Required aa/HiLog capabilities are missing")

    def install(self, hap, timeout=180):
        help_text = self.call(["-h"])
        if "replace existing application" not in help_text:
            raise DeviceError("UNSUPPORTED_TOOLS", "HDC replacement install support is unknown")
        text = self.call(["install", "-r", hap["path"]], timeout)
        if "install sign info inconsistent" in text.lower():
            raise DeviceError("INSTALL_SIGNATURE_MISMATCH",
                              "Installed and incoming signing identities differ; restore matching signing or obtain explicit approval before uninstalling and losing app data",
                              self.evidence[-1])
        if not re.search(r"\binstall bundle successfully\b", text, re.I) or re.search(r"\b(failed|failure)\b", text, re.I):
            raise DeviceError("INSTALL_UNCONFIRMED", "Installer did not confirm success", self.evidence[-1])
        return {"status": "passed", "criterion": "installer accepted the specified HAP"}

    def launch(self, bundle, ability, module):
        for value, name in [(bundle, "bundle"), (ability, "ability"), (module, "module")]:
            identifier(value, name)
        text = self.call(["shell", "aa", "start", "-b", bundle, "-a", ability, "-m", module])
        if not re.search(r"\bstart ability successfully\b", text, re.I) or re.search(r"\b(failed|failure)\b", text, re.I):
            raise DeviceError("LAUNCH_UNCONFIRMED", "Device did not confirm the launch request", self.evidence[-1])
        return {"status": "passed", "criterion": "launch request accepted; UI not verified"}

    def pids(self, bundle):
        identifier(bundle, "bundle")
        result = self.runner(self.argv(["shell", "pidof", bundle]), timeout=10)
        self.evidence.append(result)
        text = result["output"].strip()
        if result["timed_out"] or result["truncated"] or result["exit_code"] not in (0, 1):
            raise DeviceError("PROCESS_QUERY_FAILED", "Cannot observe the target process", result)
        if not text:
            return []
        if not re.fullmatch(r"\d+(?:\s+\d+)*", text):
            raise DeviceError("PROCESS_QUERY_UNKNOWN", "Unrecognized process query output", result)
        return text.split()
