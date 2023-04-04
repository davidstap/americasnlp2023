import argparse
from colorama import Fore, Back, Style, init; init()
import openai


class Chat:
  def __init__(self, model, prompt, temp, save_fn):
    openai.organization = "org-3dnDSrRL4rl9uvuxDNLbIBno"
    openai.api_key = open('key.txt', 'r').read()
    self.model = model
    self.prompt = prompt
    self.temp = temp
    self.save_fn = save_fn
    self.completion_tokens = 0
    self.prompt_tokens = 0
    self.total_tokens = 0

  def chat(self):
    conversation = [{"role": "system", "content": self.prompt}]

    while True:
      user_input = input(Fore.RED + Back.GREEN + "User:" + Style.RESET_ALL + "      ")
      if user_input == "exit":
          break

      conversation.append({"role": "user", "content": user_input})
      
      output = openai.ChatCompletion.create(model=self.model, messages=conversation, temperature=self.temp)
      content                = output["choices"][0]["message"]["content"]
      role                   = output["choices"][0]["message"]["role"]
      self.completion_tokens = output["usage"]["completion_tokens"]
      self.prompt_tokens     = output["usage"]["prompt_tokens"]
      self.total_tokens      = output["usage"]["total_tokens"]

      print(Fore.RED + Back.GREEN + "ChatGPT:" + Style.RESET_ALL + "   " + content)

      conversation.append({"role": role, "content": content})


      print(self.completion_tokens, self.prompt_tokens, self.total_tokens)


  def feed(self, user_input, verbose=True):
    conversation = [
      {"role": "system", "content": self.prompt},
      {"role": "user", "content": user_input}
    ]

    if verbose: print(conversation)

    output = openai.ChatCompletion.create(model=self.model, messages=conversation)
    content = output["choices"][0]["message"]["content"]

    if verbose: print(content)

    with open(self.save_fn, "w") as f:
      f.write(content)





if __name__ == "__main__":
  ap = argparse.ArgumentParser("ChatGPT CLI")
  ap.add_argument("--prompt", default="You are a helpful assistant.")
  ap.add_argument("--model", default="gpt-4")
  ap.add_argument("--temp", default=0.5, type=float)
  ap.add_argument("--save_fn", type=str, default=None, help="Filename")
  ap.add_argument("--mode", type=str, default="chat")
  ap.add_argument("--user_input", type=str, default=None)
  args = ap.parse_args()

  assert args.mode in ["chat", "feed"]

  chat = Chat(model=args.model, prompt=args.prompt, temp=args.temp, save_fn=args.save_fn)

  if args.mode == "chat":
    assert args.user_input is None
    chat.chat()
  else:
    chat.feed(args.user_input)











