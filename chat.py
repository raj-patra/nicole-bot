import aiml
import os

kernel = aiml.Kernel()

bot_name = "Nicole"
user_name = "Raj"

kernel.verbose(1)
kernel.setBotPredicate("name", bot_name)
kernel.setPredicate('name', user_name)

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles="startup.xml", commands="LOAD AIML B")
    kernel.saveBrain("bot_brain.brn")

while(1):
    print(kernel.respond(input(">>> ")))