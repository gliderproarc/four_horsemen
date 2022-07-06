from dataclasses import dataclass
from pyrsistent import *
import functools
import operator
import itertools


class Simulation_state(PRecord):
    "Hold the parts of a Simulation"
    names = field()
    m_pred = field()
    g_pred = field()
    visited = field()

lunch_vars = ["ann", "bob", "phil"]

lunch_domains = [
    ("breakfast", "Mon"),
    ("breakfast", "Tue"),
    ("lunch", "Mon"),
    ("lunch", "Tue"),
    ("dinner", "Mon"),
    ("dinner", "Tue")]

def make_spots(dimensions):
    "Take a size and return a grid of coordinates"
    nums = list(range(0, dimensions))
    return list(itertools.product(nums, repeat=2))

def cords_from_word_length(length, cord, s_list):
    "take a length, coordinate, and the set of all cords a grid and return only the valid rotation of a words of that length at that coordinate"
    x = cord[0]
    y = cord[1]

    # Make lists of what the Xs and Ys could be
    x_list = list(range(x, x+length))
    x_list_rep = [x] * length
    x_list_neg = list(reversed(range((x - length) + 1, x + 1)))

    y_list = list(range(y, y+length))
    y_list_rep = [y] * length
    y_list_neg = list(reversed(range((y - length) + 1, y + 1)))

    # Zip them up into the rotations
    rot0 = list(zip(x_list, y_list_rep))
    rot45 = list(zip(x_list, y_list_neg))
    rot90 = list(zip(x_list_rep, y_list_neg))
    rot135 = list(zip(x_list_neg, y_list_neg))
    rot180 = list(zip(x_list_neg, y_list_rep))
    rot225 = list(zip(x_list_neg, y_list))
    rot270 = list(zip(x_list_rep, y_list))
    rot315 = list(zip(x_list, y_list))

    # use the temp pred to filter the list into only those that fall within the bounds of the grid
    temp_pred = functools.partial(in_bounds_pred, s_list)
    rot_list = [rot0, rot45, rot90, rot135, rot180, rot225, rot270, rot315]
    ret = filter(temp_pred, rot_list)
    return list(ret)

def in_bounds_pred(spots_list, rot):
    "A pred that checks if a rotated spot is within the bounds of a grid"
    ret = [r in spots_list for r in rot]
    return all(ret)

def word_lengths_list(words):
    "return a list of all the different length of words in a list"
    ret = [len(word) for word in words]
    return list(set(ret))

def word_search_prep(words, grid_size):
    "take the words for a search and the size of grid they will go on and return the doms that can be used for this simulation"
    my_spots = make_spots(grid_size)
    doms = []
    for num in word_lengths_list(words):
        for spot in my_spots:
            doms = doms + cords_from_word_length(num, spot, my_spots)
    return doms

# Preds for Word search
def length_pred(sim_state):
    "check length of pred and it's domain to be same length"
    list_of_names = list(sim_state.names)
    check = []
    for name in list_of_names:
        if sim_state.names[name] == []:
            check = check + [True]
        elif len(sim_state.names[name]) == len(name):
            check = check + [True]
        else:
            check = check + [False]
    return all(check)

def member_pred(sim_state):
    "check none of the letters collide"
    all_names = list(sim_state.names)
    list_of_names = [name for name in all_names if sim_state.names[name] != []]
    assigned_doms = [sim_state.names[x] for x in list_of_names if sim_state.names[x] != []]
    letters_at_where = []
    for i in range(0,len(list_of_names)):
        letters_at_where = letters_at_where + list(zip(list_of_names[i],assigned_doms[i]))
    check = []
    flat = set(functools.reduce(operator.iconcat, assigned_doms, []))
    for spot in flat:
        same_doms = list(filter(lambda x : x[1] == spot, letters_at_where))
        if len(same_doms) > 1:
            heads = [l[0] for l in same_doms]
            if len(set(heads)) == 1:
                check = check + [True]
            else:
                check = check + [False]
    return all(check)

def master_pred(sim_state):
    "predicate for checking all the other predicates"
    if False in[member_pred(sim_state),
                length_pred(sim_state)]:
        return False
    else:
        return True

def goal_pred(sim_state):
    "predicate for checking non empty and master predicates"
    all_names = list(sim_state.names)
    assigned_doms = [sim_state.names[x] for x in all_names]
    checks = []
    if [] in assigned_doms:
        return False
    if len(assigned_doms) != len(set(tuple(i) for i in assigned_doms)):
        checks = checks + [False]
    checks = checks + [master_pred(sim_state)]
    return all(checks)

def names_all_assigned_pred(sim_state):
    "predicate for knowing if a state has had all it's names assigned"
    list_of_names = list(sim_state.names)
    res = next((x for x in list_of_names if sim_state.names[x] == []), None)
    if res == None:
        return True
    else:
        return False

def get_next_empty_name(sim_state):
    "take a sim_state, and give back the first name that hasn't been assigned yet"
    list_of_names = list(sim_state.names)
    return next((x for x in list_of_names if sim_state.names[x] == []), None)

def assign_empty(cue, doms):
    "assumes there is an empty name to set and sets the first sim's first empty name to all the options"
    sim_state = cue[0]
    cue_pred = functools.partial(is_dup_pred,  cue)
    empty_name = get_next_empty_name(sim_state)
    new_cue = map(lambda x : sim_state.set('names', sim_state.names.set(empty_name, x)), doms)
    first_cue = filter(sim_state.m_pred, new_cue)
    final_cue = filter(cue_pred, first_cue)
    final_list = [*final_cue]
    intermediate_rep = final_list + cue[1:]
    return intermediate_rep + [mark_sim_visited(cue[0])]

def process_next_in_cue(cue, doms):
    "take a cue, find the first un-visited sim and visit it"
    head = cue[0]
    if get_next_empty_name(head) == None:
        return cue[1:] + [head]
    else:
        return_me = assign_empty(cue, doms)
        return return_me

def mark_sim_visited(sim_state):
    "take a sim and mark it's visited flag to true"
    res = sim_state.set(visited=True)
    return res

def is_dup_pred(cue, sim):
    "predicate to see if a sim is in a cue"
    map_res = map(lambda x: x.names == sim.names, cue)
    if True in map_res:
        return False
    else:
        return True



def main_loop():
    "run the simulation"
    alpha = Simulation_state(names = m(anker = [],
                                       Scott=[],
                                       Bobby = [],
                                       zone = [],
                                       gopro = [],
                                       polar = []),
                             m_pred = master_pred,
                             g_pred = goal_pred,
                             visited = False)
    the_cue = [alpha]
    stopper = True
    final = ""
    solition = []
    domains = word_search_prep(["anker","Scott","Bobby","zone","gopro","polar"],6)
    while stopper:
        c_head = the_cue[0]
        if goal_pred(c_head):
            stopper = False
            final = "solved"
            solution = c_head
        elif c_head.visited:
            stopper = False
            final = "exhausted"
        else:
            the_cue = process_next_in_cue(the_cue, domains)
    print(final)
    print(solution.names)

if __name__ == '__main__':
    main_loop()
