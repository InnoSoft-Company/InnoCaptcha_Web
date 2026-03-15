from datetime import datetime
import os, pytz, shlex

os.chdir(os.path.dirname(os.path.abspath(__file__)))

project = "InnoCaptcha_Web"
branch = "main"

try:
  if input("Did you have a git repo installed? (y/n): ").lower()[0] == "n": os.system(f"git init && git remote add origin https://github.com/InnoSoft-Company/{project}.git")
except: pass

q = input("Adding a commit message? (Skip available): ")

date = datetime.now(pytz.timezone("Africa/Cairo")).strftime("%d-%m-%Y | %H:%M:%S")
msg = f"| {date} | {q} |" if q else f"| {date} |"

os.system(
  f"git add . && "
  f"git commit -m {shlex.quote(msg)} && "
  f"git branch -M {branch} && "
  f"git push https://github.com/InnoSoft-Company/{project}.git {branch} --force"
)
