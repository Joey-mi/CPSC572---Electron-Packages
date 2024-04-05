from sklearn.feature_extraction.text import TfidfVectorizer
import ast
import random

def conduct_tf_idf(documents, top_n):
    # Initialize TF-IDF vectorizer with sublinear tf to diminish the skewing of
    # results to terms that appear often across all documents
    tfidf_vectorizer = TfidfVectorizer(smooth_idf=False, sublinear_tf=True)

    # Fit the vectorizer to the documents and transform the documents to TF-IDF matrix
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # Get the feature names (terms)
    feature_names = tfidf_vectorizer.get_feature_names_out()

    results = tfidf_matrix.toarray()
    # Print the TF-IDF matrix
    # print("TF-IDF Matrix:")
    # print(results)

    top_elements = []
    for i in range(0, len(results)):
        top_elements.append([])
    
    for i in range(0, len(results)):
        sorted_entry = sorted(enumerate(results[i]), key=lambda x : x[1], reverse=True)
        for index, score in sorted_entry[:top_n]:
            top_elements[i].append((feature_names[index], score))
            
    

    print("Top Elements:")
    for i in range(0, len(top_elements)):
        to_print = list(map(lambda entry: f"{entry[0]}: {round(entry[1], 5)}", top_elements[i]))

        print(f"{i+1}- {to_print}\n")

    # Print the feature names
    # print("\nFeature Names:")
    # print(feature_names)

def main():
    topics_lists = []
    descriptions_lists = []
    packages_lists = []
    for i in range(0,10):
        topics_lists.append([])
        descriptions_lists.append("")
        packages_lists.append([])

    communities_dict = {}
    with open("../data/top_communities_new.txt", "r") as communities:
        comm_line = communities.readline()
        while comm_line:
            repo, rank, _ = comm_line.strip().split('\t\t')
            communities_dict[repo] = rank
            comm_line = communities.readline()

    with open("../data/repoTopics_final.txt", "r") as topics:
        topics_line = topics.readline()
        while topics_line:
            repo, string_list = topics_line.strip().split('\t\t')
            if repo in communities_dict:
                topics_list = ast.literal_eval(string_list)
                index = int(communities_dict[repo])
                topics_lists[index-1] += topics_list
            topics_line = topics.readline()
    
    with open("../data/repoDescriptions_final.txt", "r") as descriptions:
        desc_line = descriptions.readline()
        while desc_line:
            repo_description = desc_line.strip().split('\t\t')
            if len(repo_description) < 2:
                desc_line = descriptions.readline()
                continue
            repo, description = repo_description
            if repo in communities_dict:
                index = int(communities_dict[repo])
                descriptions_lists[index-1] += f" {description.strip()}"
            desc_line = descriptions.readline()

    # with open("../data/repoPackages.txt", "r") as packages:
    with open("../data/nodeList_nonDev_final.txt", "r") as packages:
        pack_line = packages.readline()
        while pack_line:
            # repo, dependencies = pack_line.strip().split('\t\t')
            _, repo, dependencies = pack_line.strip().split('\t\t')
            if dependencies == '0' or repo not in communities_dict:
                pack_line = packages.readline()
                continue

            index = int(communities_dict[repo])
            # dependencies_list = ast.literal_eval(dependencies).keys()
            dependencies_list = ast.literal_eval(dependencies)

            packages_lists[index-1] += dependencies_list
            pack_line = packages.readline()

    topics_documents = [" ".join(topic) for topic in topics_lists]
    descriptions_documents = descriptions_lists
    packages_documents = [" ".join(packages) for packages in packages_lists]
    
    print("Topics:")
    conduct_tf_idf(topics_documents, 20)
    print("\nDescriptions:")
    conduct_tf_idf(descriptions_documents, 20)
    print("\nPackages:")
    conduct_tf_idf(packages_documents, 20)

   

if __name__ == "__main__":
    main()