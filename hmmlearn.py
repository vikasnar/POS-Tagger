import sys
import codecs
import time

model = codecs.open("hmmmodel.txt", "w",'utf-8')
emission = dict()
transitions = dict()
count = dict()
vocab = set()


def read_data(train_file):
    data_file = codecs.open(train_file, "r", "utf-8")
    train_data = data_file.readlines()
    for line in train_data:
        word_tag_list = line.strip().split(" ")
        previous = "<s>"
        if previous in count:
            count[previous] += 1
        else:
            count[previous] = 1
        for word_tag in word_tag_list:
            word = word_tag[:-3]
            vocab.add(word)
            tag = word_tag[-2:]
            if previous + " " + tag in transitions:
                transitions[previous + " " + tag] += 1
            else:
                transitions[previous + " " + tag] = 1
            if tag in count:
                count[tag] += 1
            else:
                count[tag] = 1
            if tag+' '+word in emission:
                emission[tag+" "+word] += 1
            else:
                emission[tag+" "+word] = 1
            previous = tag
        if previous + " </s>" not in transitions:
            transitions[previous + " </s>"] = 1
        else:
            transitions[previous + " </s>"] += 1
            # word_tag_file.write(u'{} - {}\n'.format(word, tag).encode('utf-8'))


def generate_model():
    v_len = len(vocab)
    t_len = len(count)
    for key, value in transitions.iteritems():
        previous = key.split(" ")[0]
        probability = (float(value)+1)/(count[previous]+ t_len)
        model.write(u'T {} {}\n'.format(key, probability))
    for key, value in emission.iteritems():
        tag = key.split(" ")[0]
        probability = float(value + 1)/(count[tag] + v_len)
        model.write(u'E {} {}\n'.format(key, probability))


def normalize():
    l = len(count)
    for word in count.keys():
        if word+" </s>" not in transitions:
            transitions[word+" </s>"] = 1 / l
    for u in count.keys():
        for v in count.keys():
            if u+" "+v not in transitions:
                transitions[u+" "+v] = 1 / l


def main():
    s = time.time()
    train_file = sys.argv[1]
    read_data(train_file)
    normalize()
    generate_model()
    model.close()
    end = time.time()
    print end-s
main()
