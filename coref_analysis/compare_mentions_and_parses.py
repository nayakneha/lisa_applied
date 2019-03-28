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


def get_all_spans(dep_parse, root, span_list):

  if root in dep_parse:

    child_spans = [get_all_spans(dep_parse, child, span_list)
        for child in dep_parse[root]]
    span_lefts, span_rights = zip(*child_spans)

    leftmost_child = min(span_lefts)
    rightmost_child = max(span_rights)

  else:
    leftmost_child = rightmost_child = int(root)

  print leftmost_child, rightmost_child
  span_list.append((leftmost_child, rightmost_child))
  return leftmost_child, rightmost_child


def check_phrases(bio_labels, dep_parse):
  ind_labels = independentize_labels(bio_labels)


def read_conll_file(conll_file):
  sentences = []
  current_sentence = []
  with open(conll_file, 'r') as f:
    for line in f:
      if line.startswith("#"):
        continue
      else:
        fields = line.split()
        if not len(fields):
          sentences.append(current_sentence)
          current_sentence = []
          continue
        else:
          token = fields[3]
          coref_label = fields[-1]
          current_sentence.append((token, coref_label))

  return sentences

def get_entities_from_tag(tag):
  indiv_tags = tag.split("|")
  entities = set()
  for i in indiv_tags:
    pos, entity = i.split("-")
    entities.add(entity)
  return entities

def get_starting_entities_from_tag(tag):
  indiv_tags = tag.split("|")
  entities = set()
  for i in indiv_tags:
    pos, entity = i.split("-")
    if pos == "B":
      entities.add(entity)
  return entities


def get_coref_spans(tags):
  open_tags = {}
  spans = collections.defaultdict(list)
  for i, tag in enumerate(tags):
    if tag != "_":
      starting_entities = get_starting_entities_from_tag(tag)
      for entity in starting_entities:
        open_tags[entity] = i
      entities = get_entities_from_tag(tag)
      newly_closed_tags = set(open_tags.keys()) - entities
      for entity in newly_closed_tags:
        spans[entity].append((open_tags[entity], i))
        del open_tags[entity]
  return spans

def main():

  conll_file = sys.argv[1]
  sentences = read_conll_file(conll_file)

  corenlp_dir = "/home/nnayak/stanford-corenlp-full-2018-02-27/"
  corenlp_jar = corenlp_dir + "stanford-corenlp-3.9.1.jar"
  models_jar = corenlp_dir + "stanford-corenlp-3.9.1-models.jar"

  dependency_parser = StanfordDependencyParser(path_to_jar=corenlp_jar,
    path_to_models_jar=models_jar)


  for i in sentences:
    print(i)
    x, y = zip(*i)
    sentence = " ".join(word for word, tag in i)
    #tokens, dep_parse = get_dep_parse_tree(dependency_parser, sentence)
    #span_list = []
    #get_all_spans(dep_parse, "0", [])
    #fixed_span_list = [ (i-1, j) for i, j in span_list]
    coref_spans = get_coref_spans([tag for word, tag in i])
    print(coref_spans)

if __name__ == "__main__":
  main()

