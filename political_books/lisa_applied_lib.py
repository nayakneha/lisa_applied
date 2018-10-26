import collections

class DependencyParse(object):
  def __init__(self, tokens, parent_idxs, parent_rels):
    self.dependency_nodes = []
    root_node = DependencyNode("ROOT")
    for token in tokens:
      self.dependency_nodes.append(DependencyNode(token))
    for i, (token, parent_idx, parent_rel) in enumerate(zip(tokens, parent_idxs,
      parent_rels)):
      node = self.dependency_nodes[i]
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


