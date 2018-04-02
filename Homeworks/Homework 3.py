'''
SI 206 W18 Homework03: Classes and Inheritance

Your discussion section:
People you worked with:

######### DO NOT CHANGE PROVIDED CODE ############
'''

#######################################################################
#---------- Part 1: Class
#######################################################################

'''
Task A
'''
from random import randrange
import random
class Explore_pet:
    boredom_decrement = -4
    hunger_decrement = -4
    boredom_threshold = 6
    hunger_threshold = 10

    def __init__(self, name="Coco"):
        self.name = name
        self.hunger = randrange(self.hunger_threshold)
        self.boredom = randrange(self.boredom_threshold)
        

    def mood(self):
        if self.hunger <= self.hunger_threshold and self.boredom <= self.boredom_threshold:
            return "happy"
        elif self.hunger > self.hunger_threshold:
            return "hungry"
        else:
            return "bored"

    def __str__(self):
        state = "I'm " + self.name + '. '
        state += 'I feel ' + self.mood() + '. '
        if self.mood() == 'hungry':
            state += 'Feed me.'
        if self.mood() == 'bored':
            state += 'You can teach me new words.'
        return state

coco = Explore_pet()
brain= Explore_pet("Brian")
brain.hunger=11



#your code begins here . . .

'''
Task B
'''
#For task B, add your code inside the Pet class
class Pet:
    boredom_decrement = -4
    hunger_decrement = -4
    boredom_threshold = 6
    hunger_threshold = 10
    

    def __init__(self, name="Coco"):
        self.name = name
        self.hunger = randrange(self.hunger_threshold)
        self.boredom = randrange(self.boredom_threshold)
        self.words=["hello"]

    def clock_tick(self):
         self.hunger+=2
         self.boredom+=2

    def say(self):
        print("I know how to say:")
        for word in self.words:
            print(word)

    def teach(self,word):
        self.words.append(word)
        self.boredom+= -4
        if self.boredom>0:
            self.boredom=0

    def feed(self):
        self.hunger+=hunger_decrement
        if self.hunger>0:
            self.hunger=0

    def mood(self):
        if self.hunger <= self.hunger_threshold and self.boredom <= self.boredom_threshold:
            return "happy"
        elif self.hunger > self.hunger_threshold:
            return "hungry"
        else:
            return "bored"
        
    def hi(self):
        print(random.choice(self.words))
        

    def __str__(self):
        state = "I'm " + self.name + '. '
        state += 'I feel ' + self.mood() + '. '
        if self.mood() == 'hungry':
            state += 'Feed me.'
        if self.mood() == 'bored':
            state += 'You can teach me new words.'
        return state






'''
Task C
'''

def teaching_session(my_pet,new_words):
    for nw in new_words:
        my_pet.teach(nw)
        my_pet.hi()
        print(my_pet)
        if my_pet.mood()=="hungry":
            my_pet.feed()
        my_pet.clock_tick()
don=Pet("Don")
new_words=['I am sleepy', 'You are the best','I love you, too']
teaching_session(don,new_words)
    
    





#######################################################################
#---------- Part 2: Inheritance - subclasses
#######################################################################
'''
Task A: Dog and Cat
'''
class Dog(Pet):
    def __init__(self,name="Coco"):
        super().__init__(name="Coco")

    def __str__(self):
        state = "I'm " + self.name + ',arrf!'
        state += 'I feel ' + self.mood() + ',arrf! '
        if self.mood() == 'hungry':
            state += 'Feed me.'
        if self.mood() == 'bored':
            state += 'You can teach me new words.'
        return state

class Cat(Pet):
    def __init__(self,name="Coco",meow_count=3):
        super().__init__(name="Coco")
        self.meow_count=meow_count

    def hi(self):
        rand_word=random.choice(self.words)
        estring=""
        for time in range(self.meow_count):
            estring+=rand_word
        print(estring)



'''
Task B: Poodle
'''
class Poodle(Dog):
    def __init__(self,name="Coco"):
        super().__init__(name="Coco")

    def dance(self):
        return "Dancing in circles like poodles do!"
    def say(self):
        print(self.dance())
        print("I know how to say:")
        for word in self.words:
            print(word)

pood1=Poodle("Charlie")
pood1.say()
print("-----------")

cat1=Cat("Tom",5)
cat1.hi()

