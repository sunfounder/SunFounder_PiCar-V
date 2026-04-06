"""A simple file-based key-value database."""


class fileDB:
    def __init__(self, db=None):
        self.db = db if db is not None else "config"

    def get(self, name, default_value=None):
        try:
            with open(self.db, "r") as conf:
                lines = conf.readlines()
            for line in lines:
                if line.strip() and line[0] != "#":
                    key = line.split("=")[0].strip()
                    if key == name:
                        return line.split("=")[1].strip()
            return default_value
        except Exception:
            return default_value

    def set(self, name, value):
        with open(self.db, "r") as conf:
            lines = conf.readlines()

        flag = False
        for i in range(len(lines)):
            if lines[i].strip() and lines[i][0] != "#":
                key = lines[i].split("=")[0].strip()
                if key == name:
                    lines[i] = "%s = %s\n" % (name, value)
                    flag = True

        if not flag:
            lines.append("%s = %s\n\n" % (name, value))

        with open(self.db, "w") as conf:
            conf.writelines(lines)
