import snli_lib

class FeatureSets(object):
  MATCHING_PATHS = "matching_paths"
  pass

def tag_features(features, tag):
  return [tag + "$" + feature for feature in features]

def matching_paths(example):
  return example.premise.srl_parse.graph.keys()[0]

def featurize(example, dataset, feature_set):
  features = []

  if FeatureSets.MATCHING_PATHS in feature_set:
    features += tag_features(matching_paths(example),
        FeatureSets.MATCHING_PATHS)

  return " ".join(features)  


