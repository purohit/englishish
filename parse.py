import xml.parsers.expat
from collections import Counter
from multibayes.multibayes import MultinomialBayes

# Handlers to parse the data
class XReader:
    examples = []
    text, country, read = None, None, None
    countries = Counter()
    should_classify = False

    def __init__(self, classifier):
        self.classifier = classifier

    def valid_country(self, country):
        return country in ("Singapore","United States",
                "China", "India", "Bangladesh", "United Kingdom")

    def parse_country(self, data):
        if data in ("Singapore", "SG"):
            return "Singapore"
        return data

    def start_element(self, name, attrs):
        if name in ('text', 'country'):
            self.read = name
        else:
            self.read = None

    def end_element(self, name):
        if name == 'message' and self.should_classify:
            self.classifier.train(self.text, self.country)

    def char_data(self, data):
        if self.read == 'text':
            self.text = data
        elif self.read == 'country':
            self.country = self.parse_country(data)
            self.should_classify = self.valid_country(self.country)
            self.countries[self.country] += 1

p = xml.parsers.expat.ParserCreate()
x = XReader(MultinomialBayes())
p.StartElementHandler = x.start_element
p.EndElementHandler = x.end_element
p.CharacterDataHandler = x.char_data
p.ParseFile(open("data/smsCorpus_en_2011.12.30_all.xml"))
# If there are less than these many labeled examples, don't use the example
print x.classifier.classify("can u come to my house leh")
print x.classifier.classify("Will you call me at 10am?")
