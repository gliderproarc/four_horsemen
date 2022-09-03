"""Genetic algo practice in Python."""

import functools
import math
from random import randrange, choice
from dataclasses import dataclass


@dataclass
class Place:
    """A place people can work at."""

    name: str
    x_loc: float = 0
    y_loc: float = 0
    avail_d: str = "unset"
    person: str = "none"


@dataclass
class Person:
    """A person to work at places."""

    name: str
    x_loc: float = 0
    y_loc: float = 0
    avail_d: str = "nil"
    place: str = "none"


def assign_shifts(peeps, places):
    """Create parings of people and places based on their availabiliy."""
    for peep in enumerate(peeps):
        try:
            pair_me = next(
                filter(
                    lambda x: x[1].avail_d == peep[1].avail_d and x[1].person
                    == "none", enumerate(places)))
            peeps[peep[0]] = Person(name=peep[1].name,
                                    x_loc=peep[1].x_loc,
                                    y_loc=peep[1].y_loc,
                                    avail_d=peep[1].avail_d,
                                    place=pair_me[1].name)
            places[pair_me[0]] = Place(name=pair_me[1].name,
                                       x_loc=pair_me[1].x_loc,
                                       y_loc=pair_me[1].y_loc,
                                       avail_d=pair_me[1].avail_d,
                                       person=peep[1].name)
        except StopIteration:
            pass
    return [peeps, places]


def calculate_fitness(pairs, fitness):
    """Run pairs into the fitness function
    and return the fitness value of the pair."""
    peeps = pairs[0]
    places = pairs[1]
    new_pairs = [[x, y] for x in peeps for y in places if x.place == y.name]
    return functools.reduce(fitness, new_pairs, 0.0)


def make_kids(paragon):
    """take the most fit set of pairs from
    last generation and make more kids."""
    the_nine = [
        paragon.copy(),
        paragon.copy(),
        paragon.copy(),
        paragon.copy(),
        paragon.copy(),
        paragon.copy(),
        paragon.copy(),
        paragon.copy(),
        paragon.copy()
    ]
    res = map(random_helper, the_nine)
    return [paragon] + list(res)


def generation(pairs, paragon_fitness):
    """Perform one gereration of the genetic algo."""
    the_kids = make_kids(pairs)
    paired = list(map(lambda x: assign_shifts(x[0], x[1]), the_kids))
    fit_nums = list(map(paragon_fitness, paired))
    zipped = list(zip(fit_nums, paired))
    zipped.sort()
    return zipped[0][1]


def all_together(peeps, places, paragon_fitness):
    """Put it al together."""
    pairs = [peeps, places]
    for gen in range(0, 1000):
        pairs = blank_pairs(generation(pairs, paragon_fitness))
    return assign_shifts(pairs[0], pairs[1])


def random_helper(paragon):
    """Take a paragon and mutate."""
    rand1 = randrange(0, len(paragon[0]) + 1)
    rand2 = randrange(0, len(paragon[1]) + 1)
    choice1 = choice(list(enumerate(paragon[0])))
    choice2 = choice(list(enumerate(paragon[1])))
    popped1 = paragon[0].pop(choice1[0])
    popped2 = paragon[1].pop(choice2[0])
    paragon[0].insert(rand1, popped1)
    paragon[1].insert(rand2, popped2)
    return [paragon[0], paragon[1]]


# pass these in to the main call


def fitness_1(pairs):
    """Distance calc for fitness."""
    peeps, places = pairs[0], pairs[1]
    pairs = [[x, y] for x in peeps for y in places if x.place == y.name]
    return functools.reduce(dist_calc, pairs, 0.0)


def dist_calc(acc, pair):
    """Calculate the distrance between two points."""
    x_dif = 2 * (pair[0].x_loc - pair[1].x_loc)
    y_dif = 2 * (pair[0].y_loc - pair[1].y_loc)
    tot = abs(x_dif + y_dif)
    sq = math.sqrt(tot)
    return acc + sq


def blank_pairs(pairs):
    """Set all the places and peeps to none."""
    old_peeps = pairs[0]
    old_places = pairs[1]
    new_peeps = [
        Person(x.name, x.x_loc, x.y_loc, x.avail_d, "none") for x in old_peeps
    ]
    new_places = [
        Place(x.name, x.x_loc, x.y_loc, x.avail_d, "none") for x in old_places
    ]
    return [new_peeps, new_places]


def display(pairs):
    """Pretty print pairs"""
    peeps = pairs[0]
    for peep in peeps:
        print(f'{peep.name}:{peep.place}')


bob = Person("Bob", 5.0, 6.0, "Monday")

phil = Person("Phil", 5.0, 7.0, "Tuesday")

loner = Person("Loner", 5.0, 8.0, "Sunday")

far_man = Person("FarMan", 75.0, 75.0, "Monday")

home = Place("Home", 5.0, 9.0, "Monday")

work = Place("Work", 5.0, 10.0, "Tuesday")

prison = Place("Prison", 5.0, 11.0, "Saturday")

cali = Place("Cali", 100.0, 100.0, "Monday")

my_peeps = [far_man, bob, phil, loner]

my_places = [home, work, prison, cali]

winner = all_together(my_peeps, my_places, fitness_1)
display(winner)
print(f'Fitness:{fitness_1(winner)}')
