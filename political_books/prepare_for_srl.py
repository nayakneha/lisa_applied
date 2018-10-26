import collections
import re
import sys
import lisa_applied_lib

def join(things):
  return "\n".join([str(x) + "\t" + y for x, y in sorted(things)])

def get_sentences_from_conll(conll_file):

  temp_sentences = []
  current_sentence = []

  with open(conll_file, 'r') as f:
    for line in f:
      if not line.strip():
        temp_sentences.append(current_sentence)
        current_sentence = []
      else:
        fields = line.strip().split('\t')
        current_sentence.append(fields)

  sentences = {}
  for token_lists in temp_sentences:
    this_sentence = lisa_applied_lib.Sentence(token_lists)
    sentences[this_sentence.str_sentence()] = this_sentence

  return sentences

def read_line_collection(line_collection):
  srl_parse = {}
  sentence = line_collection.pop(0)
  for line in line_collection:
    match = re.search(r"([^\:]*):\s(.*)", line.strip())
    if match:
      srl_parse[match.group(1)] = match.group(2)
    else:
      dsds
    srl_parse["__whole_parse"] = "\n".join(line_collection)  

  return sentence, srl_parse


def get_parses_from_srl_file(srl_file):
  line_collections = []
  with open(srl_file, 'r') as f:
    line_collection = []
    for line in f:
      if not line.strip():
        line_collections.append(line_collection)
        line_collection = []
      else:
        line_collection.append(line)
  parses = collections.defaultdict(list)
  for line_collection in line_collections:
    sentence, parse = read_line_collection(line_collection)
    parses[sentence.strip()].append(parse)

  return parses

def main():
  conll_input_filename = sys.argv[1]
  srl_input_filename = sys.argv[2]

  sentences = get_sentences_from_conll(conll_input_filename)
  parses = get_parses_from_srl_file(srl_input_filename)
  for sentence_str, sentence in sentences.iteritems():
    original_event_roots = [(i, token)
        for i, (token, is_event) in enumerate(zip(sentence.tokens,
          sentence.is_event)) if is_event == "event"]
    detected_event_roots = []
    print sentence_str
    for parse in parses[sentence_str]:
      print parse["__whole_parse"]
      if 'V' in parse:
        verb = parse['V'].split(' ')[0]
        verb_index = list(sentence.tokens).index(verb)
        detected_event_roots.append((verb_index, verb))

    print "Original event roots:\n", join(original_event_roots)
    print "Detected event roots:\n", join(detected_event_roots)
    print "Novel possible event roots:\n", join((set(detected_event_roots) -
    set(original_event_roots)))
    print "Undetected event roots:\n", join((set(original_event_roots) -
    set(detected_event_roots)))
    print
    print("-" * 100)

if __name__ == "__main__":
  main()
