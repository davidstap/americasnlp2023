import argparse
import os

def query_cgpt(target, split, model, temp):
    
    filename = f"data/{target.lower()}-spanish/{split}.es"

    def batch_sentences(filename):
        # Initialize an empty list to hold the batches of sentences
        sentence_batches = []
        
        # Open the file in read mode
        with open(filename, 'r') as file:
            # Read all the lines in the file
            lines = file.readlines()
            
            # Loop over the lines in increments of 10
            for i in range(0, len(lines), 10):
                # Get the current batch of 10 sentences
                batch = lines[i:i+10]
                
                # Add the batch to the sentence_batches list
                sentence_batches.append(batch)
        
        return sentence_batches

    data = batch_sentences(filename)

    for idx, batch in enumerate(data):
        print(f"Processing {idx}/{len(data)}.....")        

        if idx not in [14,17,20]: continue

        text     = "".join([f"{idx+1}. {s}" for idx, s in enumerate(batch)])

        cmd = f'python main.py --prompt "You are a translation machine. Follow orders without adding comments. Sentences are independent of each other." --model {model} --temp {temp} --mode "feed" --save_fn "{split}.batch-{idx}.{target}" --user_input "Translate the following sentences to {target}: {text}"'

        os.system(cmd)


if __name__ == "__main__":
  ap = argparse.ArgumentParser()
  ap.add_argument("--target")
  ap.add_argument("--split", type=str, default="test")
  ap.add_argument("--temp", type=float)
  ap.add_argument("--model", default="gpt-4")
  args = ap.parse_args()

  query_cgpt(args.target, args.split, args.model, args.temp)

  