import collections
import sys
import re
import lisa_prep_lib


label_splitter = re.compile("([0-9]+|\(|\))")

def format_label(next_coref_field, curr_entities):

  # Entities whose spans end at this token
  to_end = set()

  # Split out parens and entity numbers
  contents = re.findall(label_splitter, next_coref_field)

  while contents:
    elem = contents.pop(0)

    if elem == "(":
      # Should start a new entity span
      num = contents.pop(0)
      assert num.isdigit()
      curr_entities.add(TokenLabel(BIOLabels.B, num))

      if contents:
        # Check for single-token mentions
        maybe_close_brace = contents.pop(0)
        if maybe_close_brace == ")":
          to_end.add(num)
        else:
          contents.insert(0, maybe_close_brace)

    elif elem != ")":
      # Check for span ending
      close_brace = contents.pop(0)
      assert close_brace == ")"
      to_end.add(elem)

  final_labels = "|".join(sorted(x.bio + '-' + x.entity
      for x in curr_entities))
  if not final_labels:
    final_labels = "_"

  curr_entities = set([change_label(BIOLabels.I, label)
      for label in curr_entities
      if label.entity not in to_end])

  return curr_entities, final_labels


def main():

  conll_file = sys.argv[1]
  """Convert coref labels to BIO and write to stdout."""
  sentences = []
  curr_entities = set()

  with open(conll_file, 'r') as f:
    for line in f:
      if line.startswith("#"):
        sys.stdout.write(line)
      else:
        fields = line.split()
        if not len(fields):
          sys.stdout.write(line)
          # Start a new sentence
          curr_entities = set()
        else:
          curr_entities, new_label = format_label(fields[-1], curr_entities)
          output = "\t".join(fields[:-1] + [new_label])
          sys.stdout.write(output + "\n")



if __name__ == "__main__":
  main()

