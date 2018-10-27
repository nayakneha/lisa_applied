import collections

class SRLParse(object):
  def __init__(self, sentence_lines):
    self.sentence = sentence_lines.pop(0)
    print(self.sentence)
    print(sentence_lines)
    self.graph = {}
    for line in sentence_lines:
      label, child = line.split(": ")
      self.graph[label] = child
    print(self.graph)


class DependencyParse(object):
  def __init__(self, sentence_lines):
    token_sequences = zip(*[line.split("\t") for line in sentence_lines])
    print(token_sequences)
    (_, tokens, _, _, _, parent_idxs, parent_rels) = token_sequences
    self.sentence = " ".join(tokens)
    print("**" + self.sentence)

    root_node = DependencyNode("ROOT")
    self.dependency_nodes = [root_node]
    for token in tokens:
      self.dependency_nodes.append(DependencyNode(token))
    for i, (token, parent_idx, parent_rel) in enumerate(zip(tokens, parent_idxs,
      parent_rels)):
      node = self.dependency_nodes[i]
      print(parent_idx)
      node.parent = self.dependency_nodes[int(parent_idx)]
      node.parent_rel = parent_rel
      node.parent.children[parent_rel].append(node)


class DependencyNode(object):
  def __init__(self, text, parent=None, parent_rel=None):
    self.text = text
    if parent is not None:
      self.parent = parent
      self.parent_rel = parent_rel
    self.children = collections.defaultdict(list)
    pass


class Sentence(object):
  def __init__(self, token_lists):
    (_, tokens, normalized_tokens, unk, pos, unk, par, par_dep, unk_2, unk_3,
        is_event) = zip(*token_lists)
    self.tokens = tokens
    self.normalized_tokens = normalized_tokens
    self.dependency_parse = DependencyParse(tokens, par, par_dep)
    self.is_event = is_event

  def str_sentence(self):
    return " ".join(self.tokens)


class Dataset(object):
  def __init__(self, snli_file, srl_file, depparse_file):
    self.dep_parses = self.get_dep_parses(depparse_file)
    self.srl_parses = self.get_srl_parses(srl_file)
    self.snli_lines = self.get_snli_lines(snli_file)

  def get_snli_lines(self, snli_file):
    print("\n".join(sorted(self.dep_parses.keys())))
    print("\n".join(sorted(self.srl_parses.keys())))
    failed  = []
    with open(snli_file, 'r') as f:
      _ = f.readline()
      for line in f:
        fields = line.split("\t")
        label, _, _, p_parse, h_parse, p_str, h_str = fields[:7]
        print("p_str", p_str)
        print("h_str", h_str)
        if not (p_str in self.srl_parses and h_str in self.srl_parses):
          failed.append(line.strip())
          continue
        p_str = p_str.replace(".", " .").replace(",", " ,")
        h_str = h_str.replace(".", " .").replace(",", " ,")
        if not (p_str in self.dep_parses and h_str in self.dep_parses):
          print("Dep fail")
          print(p_str)
          print(h_str)
          #failed.append(line.strip())
          continue
    print(len(failed))    
    print("\n".join(failed))

  def get_dep_parses(self, depparse_file):
    dep_parses = {}
    with open(depparse_file, 'r') as f:
      current_sentence_lines = []
      for line in f:
        if not line.strip():
          dep_parse = DependencyParse(current_sentence_lines)
          dep_parses[dep_parse.sentence] = dep_parse
          current_sentence_lines = []
        else:
          current_sentence_lines.append(line.strip())
      if current_sentence_lines:
        dep_parse = DependencyParse(current_sentence_lines)
        dep_parses[dep_parse.sentence] = dep_parse
    return dep_parses    

  def get_srl_parses(self, srl_file):
    srl_parses = {}
    with open(srl_file, 'r') as f:
      current_sentence_lines = []
      for line in f:
        if not line.strip():
          srl_parse = SRLParse(current_sentence_lines)
          srl_parses[srl_parse.sentence] = srl_parse
          current_sentence_lines = []
        else:
          current_sentence_lines.append(line.strip())
      if current_sentence_lines:
        srl_parse = SRLParse(current_sentence_lines)
        srl_parses[srl_parse.sentence] = srl_parse
    return srl_parses


