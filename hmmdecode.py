import codecs
import sys
import time

model = codecs.open('hmmmodel.txt', 'r', 'utf-8')
out_file = codecs.open('hmmoutput.txt', 'w', 'utf-8')
transition = {}
emission = {}
tag_count = {}


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
        line = model.readline()


def process_input(path):
    input_file = codecs.open(path, 'r', 'utf-8')
    line = input_file.readline()
    tag_set = tag_count.keys()
    t_len = len(tag_count) - 1
    while line:
        words = line.split()
        # dictionary to store the probability of each possible tag to each word in sentence
        best_scores = []
        # back pointers to get the maximum tag sequence
        back_pointers = []
        start_score = {}
        start_pointer = {}
        cur_word = words[0]
        # get all possible seen tags for the current word if not found use all tags
        if cur_word in emission:
            possible_tags = emission[cur_word].keys()
        else:
            possible_tags = tag_set
        # use delimiter and find probability for each possible transitions from start
        for tag in possible_tags:
            if tag == "<s>":
                continue
            start_score[tag] = transition_probability("<s>", tag, t_len) * emission_probability(cur_word, tag)
            start_pointer[tag] = "<s>"
        best_scores.append(start_score)
        back_pointers.append(start_pointer)
        for i in range(1, len(words)):
            cur_word = words[i]
            # dictionary with tag and probability for current word
            cur_score = {}
            cur_pointer = {}
            # dictionary with tag and probability for previous word
            previous_tags = best_scores[-1]
            if cur_word in emission:
                possible_tags = emission[cur_word].keys()
            else:
                possible_tags = tag_set
            for tag in possible_tags:
                if tag == "<s>":
                    continue
                previous_best = previous_tags.keys()[0]
                max = 0.0
                for prev_tag in previous_tags.keys():
                    prob = previous_tags[prev_tag] * transition_probability(prev_tag, tag,t_len) * emission_probability(words[i],tag)
                    if prob >= max:
                        max = prob
                        previous_best = prev_tag
                cur_score[tag] = max
                cur_pointer[tag] = previous_best

            max = 0.0
            last_tag = cur_score.keys()[0]
            for tag in cur_score.keys():
                if cur_score[tag] >= max:
                    max = cur_score[tag]
                    last_tag = tag
            best_scores.append(cur_score)
            back_pointers.append(cur_pointer)
        previous_tags = best_scores[-1]
        previous_best = previous_tags.keys()[0]
        max = 0.0
        for prev_tag in previous_tags.keys():
            prob = previous_tags[prev_tag] * transition_probability(prev_tag, last_tag, t_len)
            if prob >= max:
                max = prob
                previous_best = prev_tag

        tag_sequence = [previous_best]
        back_pointers.reverse()
        cur_score = previous_best
        for bp in back_pointers:
            tag_sequence.append(bp[cur_score])
            cur_score = bp[cur_score]
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
        return float(emission[word][tag])/tag_count[tag]
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
