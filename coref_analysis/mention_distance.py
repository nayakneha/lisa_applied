import collections
import sys

def read_file(input_file):
  sentences = {}
  mentions = collections.defaultdict(lambda:collections.defaultdict(list))
  with open(input_file, 'r') as f:
    for line in f:
      if line.startswith("# "):
        fields = line.strip().split()
        sentence_id = fields[1]
        sentence = " ".join(fields[2:])
        sentences[sentence_id] = sentence
      else:
        (sentence_id, start_idx, end_idx, entity,
            phrase_label, text) = line.strip().split("\t")
        doc_id, sentence_number = sentence_id.rsplit("_", 1)
        mentions[doc_id][entity].append(int(sentence_number))
  return sentences, mentions

def get_distances(sentence_numbers):
  distances = []
  sorted_numbers = sorted(sentence_numbers)
  for i, num in enumerate(sorted_numbers):
    for num_2 in sorted_numbers[i:]:
      distances.append(num_2 - num)
  return distances

def average_distance(sentence_numbers):
  distances = get_distances(sentence_numbers)
  return sum(distances)/len(distances)

def main():
  input_file = sys.argv[1]

  sentences, mention_positions = read_file(input_file)
  distances = []
  average_distances = []
  for document, mention_map in mention_positions.iteritems():
    doc_distances = []
    for sentence_numbers in mention_map.values():
      doc_distances += get_distances(sentence_numbers)
    distances += doc_distances
    average_distances.append(average_distance(doc_distances))
  avg_dist_counter = collections.Counter(average_distances)
  for k, v in avg_dist_counter.items():
    print(str(k) + "\t" + str(v))
  dist_counter = collections.Counter(distances)
  print
  print
  for k, v in dist_counter.items():
    print(str(k) + "\t" + str(v))



if __name__ == "__main__":
  main()
