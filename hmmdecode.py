import codecs
import sys
import time

model = codecs.open('hmmmodel.txt', 'r', 'utf-8')
out_file = codecs.open('hmmoutput.txt', 'w', 'utf-8')
transition = {}
emission = {}
tag_count = {}
last_tag = {}


def read_model():
    line = model.readline()
    while line:
        data = line.strip().split()
        if data[0] == 'T':
            transition[data[1]] = eval(model.readline())
        elif data[0] == 'E':
            emission[data[1]] = eval(model.readline())
        elif data[0] == "Count":
            global tag_count
            tag_count = eval(model.readline())
        elif data[0] == "Last Tags":
            global last_tag
            last_tag = eval(model.readline())
        line = model.readline()


def process_input(path):
    input_file = codecs.open(path, 'r', 'utf-8')
    line = input_file.readline()
    tag_set = tag_count.keys()
    t_len = len(tag_count) - 1
    while line:
        words = line.split()
        viterbi = []
        backpointer = []
        first_tag = {}
        first_backpointer = {}
        cur_word = words[0]
        if cur_word in emission:
            possible_tags = emission[cur_word].keys()
        else:
            possible_tags = tag_set
        for tag in possible_tags:
            if tag == "<s>":
                continue
            first_tag[tag] = transition_probability("<s>", tag, t_len) * emission_probability(cur_word, tag)
            first_backpointer[tag] = "<s>"

        viterbi.append(first_tag)
        backpointer.append(first_backpointer)

        for i in range(1, len(words)):
            cur_word = words[i]
            this_tag = {}
            this_backpointer = {}
            prev_tags = viterbi[-1]
            if cur_word in emission:
                possible_tags = emission[cur_word].keys()
            else:
                possible_tags = tag_set
            for tag in possible_tags:
                if tag == "<s>":
                    continue
                best_previous = prev_tags.keys()[0]
                max = 0.0
                for prevtag in prev_tags.keys():
                    prob = prev_tags[prevtag] * transition_probability(prevtag, tag,t_len) * emission_probability(words[i],tag)
                    if prob >= max:
                        max = prob
                        best_previous = prevtag
                this_tag[tag] = prev_tags[best_previous] * transition_probability(best_previous,tag,t_len) * emission_probability(words[i],tag)
                this_backpointer[tag] = best_previous
            max = 0.0
            currbest = this_tag.keys()[0]
            for tag in this_tag.keys():
                if this_tag[tag] >= max:
                    max = this_tag[tag]
                    currbest = tag

            viterbi.append(this_tag)
            backpointer.append(this_backpointer)
        prev_tags = viterbi[-1]
        best_previous = prev_tags.keys()[0]
        max = 0.0
        for prevtag in prev_tags.keys():
            prob = prev_tags[prevtag] * transition_probability(prevtag,currbest,t_len)
            if prob >= max:
                max = prob
                best_previous = prevtag

        tag_sequence = [best_previous]
        backpointer.reverse()
        cur_tag = best_previous
        for bp in backpointer:
            tag_sequence.append(bp[cur_tag])
            cur_tag = bp[cur_tag]
        tag_sequence.pop()
        tag_sequence.reverse()
        write_to_file(tag_sequence, line)
        line = input_file.readline()


def write_to_file(tag_sequence, line):
    tagged_words = []
    words = line.split()
    for i in range(0, len(words)):
        tagged_words.append(u"{}/{}".format(words[i], tag_sequence[i]))
    out_file.write(' '.join(tagged_words))
    out_file.write("\n")


def transition_probability(prev, nxt, t_len):
    if prev in transition and nxt in transition[prev]:
        prob = float(transition[prev][nxt] + 1) / (float(tag_count[prev]) + t_len)
    else:
        prob = float(1)/(float(tag_count[prev] + t_len))
    return prob


def emission_probability(word, tag):
    if word in emission and tag in emission[word]:
        return float(emission[word][tag])/ tag_count[tag]
    else:
        return 1


def main():
    s = time.time()
    read_model()
    path = sys.argv[1]
    process_input(path)
    out_file.close()
    model.close()
    e = time.time()
    print(e-s)
main()

