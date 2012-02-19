from multibayes.multibayes import MultinomialBayes
with open("data/parsed_corpus.data", "r") as f:
    for line in f:
        example, country = line.split("\t")
        print example, country
