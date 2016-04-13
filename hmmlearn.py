import sys
import codecs
import time

model = codecs.open("hmmmodel.txt", "w", 'utf-8')
emission = {}
transitions = {}
count = dict()
last_tags = dict()
vocab = set()


def read_data(train_file):
    data_file = codecs.open(train_file, "r", "utf-8")
    train_data = data_file.readlines()
    for line in train_data:
        previous = "<s>"
        for word_tag in line.split():
            word = word_tag[:-3]
            tag = word_tag[-2:]
            vocab.add(word)
            # Construct a transition matrix
            if previous in transitions:
                if tag in transitions[previous]:
                    transitions[previous][tag] += 1
                else:
                    transitions[previous][tag] = 1
                count[previous] += 1
            else:
                transitions[previous] = {}
                transitions[previous][tag] = 1
                count[previous] = 1
            # Construct Emission matrix
            if word in emission:
                if tag in emission[word]:
                    emission[word][tag] += 1
                else:
                    emission[word][tag] = 1
            else:
                emission[word] = {}
                emission[word][tag] = 1
            if tag in last_tags:
                last_tags[tag] += 1
            else:
                last_tags[tag] = 1
            previous = tag


def generate_model():
    for key, value in transitions.iteritems():
        model.write(u"T {}\n{}\n".format(key, value))
    for key, value in emission.iteritems():
        model.write(u"E {}\n{}\n".format(key, value))
    model.write(u"Count\n{}\n".format(count))
    model.write(u"Last Tags\n{}\n".format(last_tags))
    model.close()


def main():
    s = time.time()
    train_file = sys.argv[1]
    read_data(train_file)
    # print time.time()-s
    generate_model()
    end = time.time()
    print end-s
main()
