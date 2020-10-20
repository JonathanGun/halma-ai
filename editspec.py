import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Spec file")
args = parser.parse_args()
if args.file:
    with open(args.file, "r+") as f:
        data = f.readlines()
        print("replaced", data[1], end="")
        data[1] = "from kivy_deps import sdl2, glew\n"
        print("with", data[1])

        print("replaced", data[24], end="")
        data[24] = data[24].replace("[]", "*[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + ['resource'])]")
        print("with", data[24])
        f.seek(0)
        f.write("".join(data))
        f.truncate()
