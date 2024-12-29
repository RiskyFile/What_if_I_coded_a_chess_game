print("My first line")
print("Second line")

me = "Confused"

print("Some line")
print(f"I am {me}")

class Programmer:
    def delusional_state(self):
        return print("Funny")

    state = "thinking"
    interests = "none"
    def retrieve_state(self, state):
        print(f"This programmer is {state}")

    def retrieve_actual_state(self):
        print(f'This programmer is {self.state}')

I = Programmer()
I.delusional_state()
I.retrieve_state("obnoxious")
I.retrieve_actual_state()
I.state = "stinky"
I.retrieve_actual_state()
other_guy = Programmer()
other_guy.retrieve_actual_state()

print("_" * 20, "\n")
print("n")
print("\n new line")

class SophisticatedProgrammer:
    def __init__(self, state, smell, brain_size):
        self.state = state
        self.smell = smell
        self.brain_size = brain_size

    def retrieve_state(self):
        print(f"{self} is {self.state}")

man_with_big_forehead = SophisticatedProgrammer("bored", "Sauvage premium", "mediocre")
print(man_with_big_forehead.state)
man_with_big_forehead.retrieve_state()
print(man_with_big_forehead.smell)

with open("random_text.txt", "r") as random_text:
    for random_line in random_text:
        print(random_line)
