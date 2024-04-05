packages = {}
with open("../data/communities.txt", 'r') as comms:
    line = comms.readline()
    while line:
        repo, comm_id = line.strip().split("\t\t")
        if comm_id in packages:
            packages[comm_id].append(repo)
        else:
            packages[comm_id] = [repo]
        line = comms.readline()

pairs = []
for key in packages:
    length = len(packages[key])
    pairs.append((key, length))

sorted_top_ten = sorted(pairs, key=lambda x : x[1], reverse=True)[:10]

print(sorted_top_ten)
with open("top_communities_new.txt", "w") as cmFile:
    for index, pair in enumerate(sorted_top_ten):
        community, _ = pair
        for repo in packages[community]:
            cmFile.write(f"{repo}\t\t{index+1}\t\t{community}\n")