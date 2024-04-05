# with open('errors.txt', 'r') as file, open("undone.txt", 'w') as undone:
#     line = file.readline()
#     while line:
#         parts = line.strip().split(' ')
#         undone.write(f"{parts[1]}\n")
#         line = file.readline()


packages = []
with open("undone.txt", 'r') as undone:
    line = undone.readline()
    while line:
        repo = line.strip()
        packages.append(repo)
        line = undone.readline()

with open("repoDescriptions_partial.txt", 'r') as partial, open("repoDescriptions_final.txt", 'w') as final:
    lineA = partial.readline()
    while lineA:
        repo = lineA.strip().split('\t\t')[0]
        if repo not in packages:
            final.write(lineA)
        lineA = partial.readline()
        