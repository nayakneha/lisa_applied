import snli_features
import sys

def main():
  snli_file, srl_file, depparse_file = sys.argv[1:4]
  print(snli_file)
  print(srl_file)
  print(depparse_file)

  dataset = snli_features.Dataset(snli_file, srl_file, depparse_file)

  pass

if __name__ == "__main__":
  main()
