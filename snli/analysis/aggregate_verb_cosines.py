import sys
import re

VERB_POS_RES = ["VBZ[^\)]+",
    "VBN[^\)]+",
    "VBG[^\)]+",
    ]

def get_verb_phrase(string_parse):
  components = string_parse.split()
  vbz_start = None
  for i, component in enumerate(components):
    if "VP" in component:
      vbz_start = i
      break
  paren_count = 0
  vp_components = []
  for component in components[vbz_start:]:
   vp_components.append(component)
   for char in component:
     if char == '(':
       paren_count += 1
     elif char == ')':
       paren_count -= 1
   if paren_count == 0:
     break

  vp_string = " ".join(vp_components)
  print(vp_string)
  for verb_pos_re in VERB_POS_RES:
    print(re.findall(verb_pos_re, vp_string))
  print

def main():
  snli_file_name = sys.argv[1]

  with open(snli_file_name, 'r') as f:
    for line in f:
      fields = line.split("\t")
      p_parse, h_parse = fields[3:5]
      get_verb_phrase(p_parse)
      get_verb_phrase(h_parse)
  pass

if __name__ == "__main__":
  main()
