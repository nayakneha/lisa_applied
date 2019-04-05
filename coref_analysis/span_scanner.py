import collections
import re
import sys

from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse.stanford import StanfordParser
from nltk.parse.corenlp import CoreNLPParser

def get_examples_from_file(filename):
  examples = {}
  current_example = []
  sentence_id_counter = 0
  curr_doc_id = None

  with open(filename, 'r') as f:
    for line in f:
      # Ignore meta lines
      if line.startswith("#"):
        continue

      fields = line.strip().split()

      if len(fields) == 0:
        sentence_id = doc_id + "_" + str(sentence_id_counter).zfill(4)
        sentence_id_counter += 1
        examples[sentence_id] = current_example
        current_example = []
      else:
        # Get doc and sentence ID
        doc_id = fields[0]
        if doc_id != curr_doc_id:
          sentence_id_counter = 0
          curr_doc_id = doc_id
        current_example.append((fields[3], fields[4], fields[-1]))

  return examples


# ====================== Coref processing ===================================

label_splitter = re.compile("([0-9]+|\(|\))")

def get_entities_from_label(label):
  curr_entities = []
  to_end = []
  contents = re.findall(label_splitter, label)
  while contents:
    elem = contents.pop(0)
    if elem == "(":
      # Should start a new entity span
      num = contents.pop(0)
      assert num.isdigit()
      curr_entities.append(num)

      if contents:
        # Check for single-token mentions
        maybe_close_brace = contents.pop(0)
        if maybe_close_brace == ")":
          to_end.append(num)
        else:
          contents.insert(0, maybe_close_brace)

    elif elem != ")":
      # Check for span ending
      close_brace = contents.pop(0)
      assert close_brace == ")"
      to_end.append(elem)
  return curr_entities, to_end


def get_coref_span_map(example):
  span_map = {}
  open_spans = collections.defaultdict(list)
  for i, (token, _, label) in enumerate(example):
    span_starts, span_ends = get_entities_from_label(label)
    for label in span_starts:
      open_spans[label].append(i)
    for label in span_ends:
      open_idx = open_spans[label].pop(-1)
      label_span = (open_idx, i)
      assert label_span not in span_map
      span_map[label_span] = label
  return span_map


# ====================== Parse processing ===================================


def get_parse(parser, sentence):
  result = parser.raw_parse(sentence)
  parse = next(result)
  return parse

def indexify(index, word):
  return str(index) + "_" + word

def unindexify(indexed_word):
  str_index, word = indexed_word.split("_")
  return int(str_index), word

def enumerate_parse(node, token_list, index=0):
  if len(node) == 1 and type(node[0]) == str:
    (maybe_word, ) = node
    i_word = indexify(index, maybe_word)
    _ = node.pop(0)
    node.insert(0, i_word)
    token_list.append(i_word)
    return index + 1
  else:
    for child in node:
      index = enumerate_parse(child, token_list, index)
    return index


def get_span(node):
  label = node.label()
  nodes = [node]
  tokens = []
  while nodes:
    curr_node = list(nodes.pop(0))
    if len(curr_node) == 1 and type(curr_node[0]) == str:
      (maybe_word, ) = curr_node
      tokens.append(maybe_word)
    else:
      child_list = [i for i in curr_node]
      nodes = child_list + nodes

  just_tokens = [x.split("_")[1] for x in tokens]
  start_token = int(tokens[0].split("_")[0])
  end_token = int(tokens[-1].split("_")[0])
  return  (start_token, end_token), label, just_tokens

def get_all_spans(parse, span_list):
  idxs, label, tokens = get_span(parse)
  span_list[idxs] = (label, tokens)
  for child in parse:
    if type(child)  != str:
      get_all_spans(child, span_list)


# ============================================================================


def process_example(example_id, example, parser):
  coref_tokens, pos_tags, coref_labels = zip(*example)
  sentence = " ".join(coref_tokens)
  parse = get_parse(parser, sentence)
  token_list = []
  enumerate_parse(parse, token_list)
  parse_spans = {}
  get_all_spans(parse, parse_spans)
  coref_spans = get_coref_span_map(example)
  print(" ".join(["#", example_id] + list(coref_tokens)))
  for k, (label, tokens) in parse_spans.items():
    if k in coref_spans:
      start, end = k
      print("\t".join([example_id, str(start), str(end),
        coref_spans[k], label, " ".join(tokens)]))

def main():
  filename = sys.argv[1]
  examples = get_examples_from_file(filename)

  corenlp_dir = "/home/nnayak/stanford-corenlp-full-2018-02-27/"
  corenlp_jar = corenlp_dir + "stanford-corenlp-3.9.1.jar"
  models_jar = corenlp_dir + "stanford-corenlp-3.9.1-models.jar"

  parser = StanfordParser(path_to_jar=corenlp_jar,
    path_to_models_jar=models_jar)

  for example_id in sorted(examples.keys()):
    example = examples[example_id]
    process_example(example_id, example, parser)

if __name__ == "__main__":
  main()
