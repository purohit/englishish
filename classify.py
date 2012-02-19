from multibayes.multibayes import MultinomialBayes
test_set = []
training_set = []

with open("data/parsed_corpus.data", "r") as f:
    i = 0
    for line in f:
        example, country = line.rstrip().split("\t")
        example = example.strip()
        if example:
            if i%5 == 0:
                test_set.append((example, country))
            else:
                training_set.append((example, country))
            i += 1

correct = 0
incorrect = 0
m = MultinomialBayes(training_set)
for example, country in test_set:
    most_likely_class, prob = m.classify(example)[0]
    if country != most_likely_class:
        incorrect += 1
    else:
        correct += 1

print "Accuracy: {} correct/ {} incorrect of {} examples (accuracy: {})".format(correct, incorrect, correct+incorrect, correct/(correct+incorrect))
