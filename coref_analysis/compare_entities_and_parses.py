import collections
import sys
import re

from nltk.parse.stanford import StanfordDependencyParser

def get_dep_parse_tree(dependency_parser, sentence):

  result = dependency_parser.raw_parse(sentence)
  conll_parse = result.next().to_conll(10)

  dep_parse = collections.defaultdict(list)
  tokens = []
  for line in conll_parse.split("\n"):
    if not line:
      continue
    fields = line.split()
    index, word, _, _, _, _, parent_index, _ , _, _ = line.split()
    dep_parse[parent_index].append(index)
    tokens.append(word)

  return tokens, dep_parse

def get_entity_or_none(entity_field):
  if entity_field == "-":
    return None
  else:
    return entity_field.replace("(", "").replace(")", "")

def read_conll_file(conll_file):
  sentences = []
  current_sentence = []
  current_entities = []
  with open(conll_file, 'r') as f:
    for line in f:
      if line.startswith("#"):
        continue
      fields = line.split()
      if not len(fields):
        sentences.append((current_sentence, current_entities))
        current_sentence = []
        current_entities = []

      else:
        current_sentence.append(fields[3])
        entity_field = fields[-1]
        current_entities.append(fields[-1])
        entity = get_entity_or_none(entity_field)

  return sentences

class BIOLabels(object):
  B = "B"
  I = "I"
  O = "O"

def make_label(bio, entity):
  return bio + "_" + entity

def change_label(bio, old_label):
  _, entity = old_label.split("_")
  return make_label(bio, entity)

def get_entity_from_label(label):
  return label.split("_")[1]


label_splitter = re.compile("([0-9]+|\(|\))")

def independentize_labels(orig_labels):
  stack = []
  final_labels = []
  curr_entities = set()
  to_end = set()
  for label in orig_labels:
    contents = re.findall(label_splitter, label)
    while contents:
      elem = contents.pop(0)
      if elem == "(":
        num = contents.pop(0)
        curr_entities.add(make_label(BIOLabels.B, num))
        if contents:
          maybe_close_brace = contents.pop(0)
          if maybe_close_brace == ")":
            to_end.add(num)
          else:
            contents.insert(0, maybe_close_brace)
      elif elem != ")":
        close_brace = contents.pop(0)
        assert close_brace == ")"
        to_end.add(elem)
    final_labels.append(list(curr_entities))
    curr_entities = set([change_label(BIOLabels.I, label) 
        for label in curr_entities
        if get_entity_from_label(label) not in to_end])

  print(orig_labels)
  print(final_labels)
  print("*" * 80)

def check_phrases(bio_labels, dep_parse):
  ind_labels = independentize_labels(bio_labels)

def main():

  conll_file = sys.argv[1]
  sentences = read_conll_file(conll_file)

  corenlp_dir = "/home/nnayak/stanford-corenlp-full-2018-02-27/"
  corenlp_jar = corenlp_dir + "stanford-corenlp-3.9.1.jar"
  models_jar = corenlp_dir + "stanford-corenlp-3.9.1-models.jar"

  dependency_parser = StanfordDependencyParser(path_to_jar=corenlp_jar,
    path_to_models_jar=models_jar)

  empty_label_set = set([BIOLabels.O])

  for i, j in sentences:
    check_phrases(j, i)

if __name__ == "__main__":
  main()

