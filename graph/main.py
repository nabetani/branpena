from matplotlib import pyplot
import re

DATA = [
    "../cppso/mac_clang.txt",
    "../cppso/mac_gcc.txt",
    "../cppso/win_x64.txt",
    "../cppso/win_x86.txt",
    "../goso/mac_amd64.txt",
    "../goso/mac_m1.txt",
    "../goso/win_386.txt",
    "../goso/win_amd64.txt",
]


def prop(e):
    return {
        "device": ("mbp" if "/mac" in e else "thinkpad"),
        "compiler": (
            "clang"
            if "_clang" in e
            else ("gcc" if "_gcc" in e else ("cl.exe" if "cppso/win" in e else "go"))
        ),
        "lang": ("go" if "/goso/" in e else "c++"),
        "bin": (
            "m1"
            if ("_m1" in e or "/cppso/mac" in e)
            else ("ia32" if "_x86" in e or "_386" in e else "amd64")
        ),
    }


def load_data(fn):
    r = {}
    mode = None
    with open(fn) as f:
        for line in f:
            line = line.strip()
            if line == "sorted" or line == "shuffled":
                mode = line
                continue
            result = re.match(r"(\S+)\s*\:\s*duration\s*\=\s*(\S+)s", line)
            if result:
                key = f"{mode}/{result.group(1)}"
                r[key] = float(result.group(2))
    return r


def graph(data_fns, title, fn):
    pyplot.style.use("ggplot")
    x = []
    y0 = []
    y1 = []
    for data_fn in data_fns:
        p = prop(data_fn)
        cat = f"{p['compiler']} {p['bin']}"
        print(repr(p))
        data = load_data(data_fn)
        print(repr(data))
        for k in data:
            c = k.split("/")
            sub = cat + " " + c[1]
            if not (sub in x):
                x.append(sub)
            if c[0] == "shuffled":
                y0.append(data[k])
            else:
                y1.append(data[k])
    fig, ax = pyplot.subplots(
        nrows=1, ncols=1, figsize=(6, (len(x) + 1) * 0.35), dpi=200
    )
    ax.set_title(title)
    print(repr([x, y0, y1]))
    ax.barh(x, y0, color="red", align="edge", height=0.4)
    ax.barh(x, y1, color="blue", align="edge", height=-0.4)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=10)
    print(data_fns, title, fn)
    pyplot.tight_layout()
    pyplot.savefig(fn)
    pyplot.clf()
    pyplot.close()
    pyplot.gca().clear()


def main():
    print("hoge")
    for device in ["mbp", "thinkpad"]:
        for lang in ["c++", "go"]:
            t = [
                e
                for e in DATA
                if prop(e)["device"] == device and prop(e)["lang"] == lang
            ]
            graph(t, f"device={device}, lang={lang}", f"im/{device}{lang}.png")


main()
