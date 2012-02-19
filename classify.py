from multibayes.multibayes import MultinomialBayes, MultinomialBayesException
test_set = []
training_set = []

country_to_lang = {"Singapore": "Singlish",
        "China": "Singlish",
        "India": "Indian English",
        "Bangladesh": "Indian English",
        "United States": "English",
        "United Kingdom": "English"
        }

with open("data/parsed_corpus.data", "r") as f:
    i = 0
    for line in f:
        example, country = line.rstrip().split("\t")
        example = example.strip()
        if example:
            country = country_to_lang[country]
            if i%5 == 0:
                test_set.append((example, country))
            else:
                training_set.append((example, country))
            i += 1

correct = 0
incorrect = 0
m = MultinomialBayes(training_set)
for example, country in test_set:
    try:
        most_likely_class, prob = m.classify(example)[0]
        if country != most_likely_class:
            incorrect += 1
        else:
            correct += 1
    except MultinomialBayesException, e:
        pass

print "Training set size: {}, Test set size: {}\n {} correct/{} incorrect of {} examples (accuracy: {:.2f}%)".format(
        len(training_set), len(test_set),
        correct, incorrect, correct+incorrect, 100.0* (correct/(correct+incorrect))
        )
