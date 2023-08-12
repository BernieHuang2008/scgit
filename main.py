import sys
from zipfile import ZipFile
import libs.jsondiff as jsondiff

cwd = "examples/example1/src/"
old_file = "Scratch作品.sb3"
new_file = "Scratch作品 (1).sb3"


def _get_json(fname):
    """
    get json script file from sb3.
    """
    zf = ZipFile(fname).open("project.json")
    return zf.read().decode('utf-8')


def _show_diff(d):
    """
    show difference.
    """
    path, value = d
    print("\033[94m"+"\033[96m >>> \033[94m".join(map(str, path)))
    print("\033[1;37;42m + \033[0m\033[92m", value)
    print("\033[0m")


old_json = _get_json(cwd + old_file)
new_json = _get_json(cwd + new_file)


def diff():
    """
    get differences between two Scratch Script Files.
    """
    return jsondiff.diff(old_json, new_json, load=True)


def merge():
    """
    merge two Scratch Script Files.
    """
    diffs = diff()
    differences = []

    def helper(key, value, path):
        if not isinstance(value, dict) or (len(path) and path[-1] == "blocks"):
            # found difference.
            path.append(key)
            differences.append((tuple(path), value))
            _show_diff(differences[-1])
            path.pop()
            return

        path.append(key)
        for key in value:
            helper(key, value[key], path)
        path.pop()

    for key in diffs:
        helper(key, diffs[key], [])

    return differences


merge()
