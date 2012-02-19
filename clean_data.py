import xml.parsers.expat
import codecs
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
        return country in ("Singapore","United States", "China", "India")

    def parse_country(self, data):
        return "Singapore" if data in ("Singapore", "SG") else data

    def start_element(self, name, attrs):
        self.read = name if name in ('text', 'country') else None

    def end_element(self, name):
        if name == 'message' and self.should_classify:
            f.write(u"{}\t{}\n".format(self.text, self.country))
            self.classifier.train(self.text, self.country)

    def char_data(self, data):
        if self.read == 'text':
            self.text = data
        elif self.read == 'country':
            self.country = self.parse_country(data)
            self.should_classify = self.valid_country(self.country)
            self.countries[self.country] += 1

if __name__ == '__main__':
    p = xml.parsers.expat.ParserCreate()
    p.StartElementHandler = x.start_element
    p.EndElementHandler = x.end_element
    p.CharacterDataHandler = x.char_data
    f = codecs.open("data/parsed_corpus.data", encoding="utf-8", mode="w")
    p.ParseFile(open("data/smsCorpus_en_2011.12.30_all.xml"))
    f.close()
