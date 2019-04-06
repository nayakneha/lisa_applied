import collections
import sys

def main():

  bio_input_file = sys.argv[1]
  mention_map = collections.defaultdict(list)
  with open(bio_input_file, 'r') as f:
    for line in f:
      fields = line.strip().split()
      if not fields:
        continue
      document, coref_labels = fields[0], fields[-1].split("|")
      begin_labels = [label for label in coref_labels if label.startswith("B")]
      mention_map[document] += begin_labels

  for document, mentions in mention_map.items():
    print("\t".join([document, str(len(mentions)), str(len(set(mentions)))]))


if __name__ == "__main__":
  main()
