import snli_data
import sys
import pickle

def main():
  snli_file, srl_file, depparse_file, output_file = sys.argv[1:5]
  
  dataset = snli_data.Dataset(snli_file, srl_file, depparse_file)

  with open(output_file, 'w') as f:
    pickle.dump(dataset, f)

if __name__ == "__main__":
  main()
