"""Genetic algo practice in Python."""

# import functools
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
    """run pairs into the fitness function
    and return the fitness value of the pair."""

    # reduce(pairs, fitness)
    pass


def make_kids(paragon):
    """take the most fit set of pairs from
    last generation and make more kids."""

    # shuffle the order of the places a bit for copies of the paragon
    pass


def generation(pairs, paragon_fitness):
    """Perform one gereration of the genetic algo."""

    # make_kids()
    # pass the kids to threads
    # run assign shifts on all the kids
    # calculate fitness on the resulting pairs
    # elect a new paragon or keep the old one
    # return the paragon
    pass


def all_together(peeps, places):
    """Put it al together."""

    # shuffle the order of the places
    # assign_shifts()
    # calculte_fitness()
    # pass the first set of pairs and their fitness score to generation()
    # run generation for as many times as needed
    # return final paragagon
    pass


bob = Person("Bob", 5.0, 5.0, "Monday")

phil = Person("Phil", 5.0, 5.0, "Tuesday")

loner = Person("Loner", 5.0, 5.0, "Sunday")

home = Place("Home", 5.0, 5.0, "Monday")

work = Place("Work", 5.0, 5.0, "Tuesday")

prison = Place("Prison", 5.0, 5.0, "Saturday")

my_peeps = [bob, phil, loner]

my_places = [home, work, prison]

print(assign_shifts(my_peeps, my_places))
