from __future__ import division
from collections import Counter
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
            lang = country_to_lang[country]
            if i%5 == 0:
                # use approx 20% of data for test set, other 80% for training
                test_set.append((example, lang))
            else:
                training_set.append((example, lang))
            i += 1

misclassifications = Counter()
correct = 0
incorrect = 0
m = MultinomialBayes(training_set)
for example, lang in test_set:
    try:
        most_likely_class, prob = m.classify(example)[0]
        if lang != most_likely_class:
            incorrect += 1
            misclassifications[(lang, most_likely_class)] += 1
        else:
            correct += 1
    except MultinomialBayesException, e:
        pass

print "Training set size: {}, Test set size: {}\n {} correct/{} incorrect of {} examples (accuracy: {:.2f}%)".format(
        len(training_set), len(test_set),
        correct, incorrect, correct+incorrect, 100.0*(correct/(correct+incorrect))
        )
for (true_lang, class_lang), number_wrong in misclassifications.most_common():
    print "Misclassified {} as {}: {} times".format(true_lang, class_lang, number_wrong)
