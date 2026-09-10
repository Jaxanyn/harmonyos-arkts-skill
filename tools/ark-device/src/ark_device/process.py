"""Own only the HDC client process created by this invocation."""
import subprocess
import threading
import time


class CommandCancelled(KeyboardInterrupt):
    """Cancellation with the partial output collected before cleanup."""
    def __init__(self, evidence):
        super().__init__('Command cancelled')
        self.evidence = evidence


class Capture:
    def __init__(self, argv, limit=10 * 1024 * 1024, *, cwd=None, env=None):
        self.argv = argv
        self.limit = limit
        self.data = bytearray()
        self.truncated = False
        self.started = time.monotonic()
        self.process = subprocess.Popen(
            argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL, shell=False, cwd=cwd, env=env,
        )
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()

    def _read(self):
        try:
            while True:
                chunk = self.process.stdout.read1(65536)
                if not chunk:
                    break
                remaining = self.limit - len(self.data)
                self.data.extend(chunk[:remaining])
                if len(chunk) > remaining:
                    self.truncated = True
                    self.stop_process()
                    break
        finally:
            self.process.stdout.close()

    def stop_process(self):
        if self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=3)
            except ProcessLookupError:
                pass

    def finish(self):
        self.stop_process()
        self.reader.join(timeout=4)
        if self.reader.is_alive():
            raise RuntimeError("HDC output reader did not stop")
        return self.data.decode("utf-8", "replace")


def execute(argv, timeout=20, limit=1024 * 1024, *, cwd=None, env=None):
    capture = Capture(argv, limit, cwd=cwd, env=env)
    timed_out = False
    cancelled = False
    try:
        capture.process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
    except KeyboardInterrupt:
        cancelled = True
    finally:
        output = capture.finish()
    evidence = {
        "argv": argv, "exit_code": capture.process.returncode,
        "output": output, "timed_out": timed_out,
        "truncated": capture.truncated,
        "duration_seconds": round(time.monotonic() - capture.started, 3),
    }

    if cancelled:
        raise CommandCancelled(evidence)
    return evidence
