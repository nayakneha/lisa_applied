import collections
import re
import sys

def get_examples_from_file(filename):
  examples = []
  current_example = []
  with open(filename, 'r') as f:
    for line in f:
      if line.startswith("#"):
        continue
      fields = line.strip().split()
      if len(fields) == 0:
        examples.append(current_example)
        current_example = []
      else:
        current_example.append((fields[3], fields[4], fields[-1]))
  return examples


class BIOLabels(object):
  B = "B"
  I = "I"
  O = "O"



class TokenLabel(object):
  def __init__(self, bio, entity):
    self.bio = bio
    self.entity = entity


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


def get_span_map(example):
  span_map = collections.defaultdict(list)
  open_spans = collections.defaultdict(list)
  for i, (token, _, label) in enumerate(example):
    span_starts, span_ends = get_entities_from_label(label)
    for label in span_starts:
      open_spans[label].append(i)
    for label in span_ends:
      open_idx = open_spans[label].pop(-1)
      span_map[label].append((open_idx, i+1))
  return span_map




def main():
  filename = sys.argv[1]
  examples = get_examples_from_file(filename)
  for i in examples:
    print(i)
    print(get_span_map(i))
  pass


if __name__ == "__main__":
  main()
