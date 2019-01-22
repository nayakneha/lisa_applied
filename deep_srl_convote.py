import csv
import glob
import os
import sys

def read_frames_from_file(f):
  frames = []
  current_frame = {}
  fieldnames = set()
  for line in f:
    if not line.strip():
      frames.append(current_frame)
      current_frame = {}
      continue
    elif line.startswith("\t\t"): # This is an argument
      key, value = line.strip().split(":", maxsplit=1)
      fieldnames.add(key)
    elif line.startswith("\t"): # This is a predicate
      key, value = line.strip().split(":", maxsplit=1)
    else:
      key, value = "Sentence", line.strip()
    current_frame[key] = value

  return frames, fieldnames

METADATA_FIELDS = ["bill", "speaker", "page_pos", "party", "mention", "vote"]

def get_file_info(filename):
  bill_index, speaker, page_pos, party_mention_vote = filename[:-8].split("_")
  party, mention, vote = list(party_mention_vote)
  metadata_dict = dict(zip(METADATA_FIELDS, [bill_index, speaker, page_pos,
    party, mention, vote]))
  return metadata_dict


def main():
  input_directory = sys.argv[1]

  all_fieldnames = set()
  all_frames = []

  for file_name in glob.glob(input_directory + "/*.srl"):
    file_info = get_file_info(os.path.basename(file_name))
    with open(file_name, 'r') as f:
      frames, fieldnames = read_frames_from_file(f)
      all_fieldnames.update(fieldnames)
      for frame in frames:
        frame.update(file_info)
      all_frames += frames

  fieldnames = ["Predicate"] + METADATA_FIELDS + sorted(all_fieldnames) + ["Sentence"]
  spamwriter = csv.DictWriter(sys.stdout, fieldnames, delimiter="\t")
  spamwriter.writeheader()
  for frame in all_frames:
    spamwriter.writerow(frame)


if __name__ == "__main__":
  main()
