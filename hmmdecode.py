import codecs
import sys
import math

model = codecs.open('hmmmodel.txt', 'r', 'utf-8')
out_file = codecs.open('hmmoutput.txt', 'w', 'utf-8')
transition = {}
emission = {}
tag_set = set()


def read_model():
    line = model.readline()
    while line:
        data = line.strip().split(' ')
        if data[0] == 'T':
            transition[data[1]+" "+data[2]] = float(data[3])
            tag_set.add(data[1])
        elif data[0] == 'E':
            emission[data[1]+" "+data[2]] = float(data[3])
        line = model.readline()


def process_input(path):
    input_file = codecs.open(path, 'r', 'utf-8')
    line = input_file.readline()
    state_prob = {}
    best_prob = {}
    state_prob["0 <s>"] = 0
    best_prob["0 <s>"] = None
    while line:
        words = line.strip().split(" ")
        length = len(words)
        for i in range(0, length):
            for prev in tag_set:
                for nxt in tag_set:
                    cur_state = "{} {}".format(i, prev)
                    nxt_state = "{} {}".format(i+1, nxt)
                    tran_key = "{} {}".format(prev, nxt)
                    em_key = "{} {}".format(nxt, words[i])
                    if cur_state in state_prob and tran_key in transition:
                        if em_key in emission:
                            prob = state_prob[cur_state] + (-1 * math.log(transition[tran_key])) + (-1 * math.log(emission[em_key]))
                        else:
                            prob = state_prob[cur_state] + (-1 * math.log(transition[tran_key]))
                        if nxt_state not in state_prob or state_prob[nxt_state] > prob:
                            state_prob[nxt_state] = prob
                            best_prob[nxt_state] = cur_state

        nxt = " </s>"
        for prev in tag_set:
            prev_state = "{} {}".format(i, prev)
            end_state = "{}{}".format(i+1, nxt)
            end_key = "{}{}".format(prev, nxt)
            if prev_state in state_prob and end_key in transition:
                prob = state_prob[prev_state] + (-1 * math.log(transition[end_key]))
                if end_state not in state_prob or state_prob[end_state] > prob:
                    state_prob[end_state] = prob
                    best_prob[end_state] = prev_state

        tags = []
        back_path = best_prob["{}{}".format(i+1, " </s>")]
        while back_path != "0 <s>":
            tag = back_path.split(" ")[1]
            tags.append(tag)
            back_path = best_prob[back_path]
        tags.reverse()
        for i in range(0, length-1):
            out_file.write(u"{}/{} ".format(words[i], tags[i]))
        out_file.write(u"{}/{}\n".format(words[length-1], tags[length-1]))
        line = None


def main():
    read_model()
    path = sys.argv[1]
    process_input(path)
    out_file.close()
    model.close()
main()

