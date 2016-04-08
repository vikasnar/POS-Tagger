import sys
import codecs
import math

model = open("hmmmodel.txt", "w")
emission = {}
transitions = {}
count = {}


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
            word = word_tag[:2]
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
            # word_tag_file.write(u'{} - {}\n'.format(word, tag).encode('utf-8'))
        if previous+" </s>" in transitions:
            transitions[previous+" "+"</s>"] += 1
        else:
            transitions[previous + " " + "</s>"] = 1


def generate_model():
    for key, value in transitions.iteritems():
        previous = key.split(" ")[0]
        probability = math.log(float(value)/count[previous])
        model.write(u'T {}={}\n'.format(key, probability))


def main():
    train_file = sys.argv[1]
    read_data(train_file)
    generate_model()
    model.close()
main()
