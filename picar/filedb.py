"""A simple file-based key-value database."""

import os
import tempfile


class fileDB:
    def __init__(self, db=None):
        self.db = db if db is not None else "config"

    def _read(self):
        try:
            with open(self.db, "r") as conf:
                return conf.readlines()
        except FileNotFoundError:
            return []

    def get(self, name, default_value=None):
        try:
            for line in self._read():
                if line.strip() and line[0] != "#":
                    key = line.split("=")[0].strip()
                    if key == name:
                        return line.split("=")[1].strip()
            return default_value
        except Exception:
            return default_value

    def set(self, name, value):
        """Write a key, then replace the file atomically.

        The previous implementation wrote in place, so a power loss partway
        through (a stalling servo can brown the Pi out) left a truncated,
        half-written config. Writing to a temporary file in the same
        directory and calling os.replace makes the update all-or-nothing.
        Duplicate keys, which earlier in-place writes could leave behind,
        are collapsed to the first occurrence on every write.
        """
        lines = self._read()

        out = []
        seen = set()
        flag = False
        for line in lines:
            if line.strip() and line[0] != "#":
                key = line.split("=")[0].strip()
                if key in seen:
                    # Drop a duplicate left by an earlier interrupted write.
                    continue
                seen.add(key)
                if key == name:
                    out.append("%s = %s\n" % (name, value))
                    flag = True
                    continue
            out.append(line)

        if not flag:
            out.append("%s = %s\n" % (name, value))

        directory = os.path.dirname(os.path.abspath(self.db)) or "."
        fd, tmp = tempfile.mkstemp(dir=directory, prefix=".config.", suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as conf:
                conf.writelines(out)
                conf.flush()
                os.fsync(conf.fileno())
            os.replace(tmp, self.db)
        except BaseException:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise
