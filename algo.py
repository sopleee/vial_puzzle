from classes import Vial
import re
import os

UNKNOWN_C = "unknown"
MAX_HEIGHT = 4

vial_dict = {
    0: [UNKNOWN_C, "mint", "pink", "yellow"],
    1: ["brown", "l_blue", "purple", "purple"], 
    2: ["yellow", "jungle", "orange", "gray"],
    3: ["yellow", "red", "gray", "orange"],
    4: ["l_blue", "red", "brown", "jungle"],
    5: ["mint", "d_green", "red", "d_blue"],
    6: ["brown", "purple", "l_blue", "d_green"],
    7: ["mint", "red", "orange", "gray"],
    8: ["pink", "l_blue", "d_blue", "d_green"],
    9: ["yellow", "jungle", "orange", "purple"],
    10: [UNKNOWN_C, "pink", "d_blue", "mint"],
    11: ["brown", "d_green", "d_blue", "jungle"],
    12: [],
    13: [],
}

def calculate_all_moves():
    all_moves = []
    for a in range(14):
        for b in range(14):
            if a != b: 
                all_moves.append((a,b))
    return all_moves  


def init_vials():
    vials = [Vial(i, vial_dict[i]) for i in list(range(14))]
    return vials
    

def find_next_possible(state, index, moves, debug=False):
    if index >= len(all_moves):
        return (-1, None, None)
    for i in range(index, len(all_moves)):
        give_vial = state[all_moves[i][0]]
        recieve_vial = state[all_moves[i][1]]
        if give_vial.completed or recieve_vial.completed or moves.count(i) > 4: 
            continue
        give_height = len(give_vial.color_list)
        receive_height = len(recieve_vial.color_list)
        same_color = False if receive_height == 0 or give_height == 0 else (give_vial.color_list[-1] == recieve_vial.color_list[-1])   # this doesn't matter if height for recieve = 0
        less_than_max = len(recieve_vial.color_list) < MAX_HEIGHT
        if debug: 
            print(all_moves[i])
            print(give_vial.number, recieve_vial.number)
            print(same_color)
            if give_height != 0:
                print(give_vial.color_list[-1])
            if receive_height != 0:
                print(recieve_vial.color_list[-1])
            print(less_than_max, "\n")
        if less_than_max and (same_color or receive_height == 0):
            return (i, give_vial, recieve_vial)
    return (-1, None, None)


def main():
    global all_moves
    all_moves = calculate_all_moves()
    state = init_vials()        # list of vials in current state

    # init loop variables
    cur_index = 0
    moves = []
    while True: 
        os.system('cls||clear')
        # hi = False
        # 1: check for next legal move (from current index) and add it to the move list 
        print(f"First valid move: {cur_index} / {len(all_moves)}")
        if cur_index < len(all_moves):
            print(f"\t{all_moves[cur_index]}")
        next_move = find_next_possible(state=state, index=cur_index, moves=moves)
        cur_index = 0
        if next_move[0] == -1: 
            # remove the last move in the list + revert form, make the current index = index of new last move
            last_move = moves.pop()
            print(f"Next move not found, reverting-- Give: {state[all_moves[last_move][0]].color_list} \t Recieve: {state[all_moves[last_move][1]].color_list}")
            state[all_moves[last_move][0]].pour(state[all_moves[last_move][1]])
            print(f"Reverted-- Give: {state[all_moves[last_move][0]].color_list} \t Recieve: {state[all_moves[last_move][1]].color_list}")
            print(f"{moves}\t The following move is a bust: {last_move}\n")
            cur_index = last_move + 1
            continue
        moves.append(next_move[0])
        give_vial = next_move[1]
        receive_vial = next_move[2]
        # print(next_move, all_moves[next_move])
        
        # 2: update vials and check conditions
        print(f"Pouring.. (move {moves[-1]})- Give: {give_vial.color_list}\t Recieve: {receive_vial.color_list}")
        print(f"Moves {moves}")
        receive_vial.pour(give_vial)
        print(f"Give:{give_vial.color_list} {give_vial.completed}, Recive:{receive_vial.color_list} {receive_vial.completed}")
        # cond 1: flip-flop (what if there's a flip flop of more than a few vials?)
        #       if the last few moves are the same two moves
        flip_flop = len(set(moves[-4:])) == 2 and len(moves) > 4
        # cond 2: if the solution is found-- aka all vials are completed
        all_completed = all(vial.completed for vial in state)
        # cond 3: unknown found (exists a vial with only unknowns)
        unknown_found = any(vial.color_list[-1] == UNKNOWN_C for vial in state if len(vial.color_list) > 0)
        print(f"Flipflop: {flip_flop}, All completed: {all_completed}, Unknown found: {unknown_found}")
        
        # 3: act appropriately on conditions
        if flip_flop:
            rev_moves = moves.copy()
            rev_moves.reverse()
            # removes all flipflops except for first move that started it
            for i in range(len(moves)):
                if not rev_moves[i+1] in set(rev_moves[:4]):
                    break
                last_move = moves.pop()
                print(f"Flip-floppin, reverting-- Given: {state[all_moves[last_move][0]].color_list} \t Recieve: {state[all_moves[last_move][1]].color_list}")
                state[all_moves[last_move][0]].pour(state[all_moves[last_move][1]])
                print(f"Reverted-- Given: {state[all_moves[last_move][0]].color_list} \t Recieve: {state[all_moves[last_move][1]].color_list}")
                cur_index = last_move + 1
            print("\n")
            continue
        if all_completed or unknown_found: 
            print("Unknown found!")
            print(str([all_moves[move] for move in moves]))
            break
        print("\n")
    return
    with open("output.txt", "w") as f:
        while True: 
            # hi = False
            # 1: check for next legal move (from current index) and add it to the move list 
            f.write(f"First valid move: {cur_index} / {len(all_moves)}")
            f.write(f"\t{all_moves[cur_index]}\n")
            next_move = find_next_possible(state=state, index=cur_index, moves=moves)
            cur_index = 0
            if next_move[0] == -1: 
                # remove the last move in the list + revert form, make the current index = index of new last move
                last_move = moves.pop()
                f.write(f"Next move not found, reverting-- Give: {state[all_moves[last_move][0]].color_list} \t Recieve: {state[all_moves[last_move][1]].color_list}\n")
                state[all_moves[last_move][0]].pour(state[all_moves[last_move][1]])
                f.write(f"Reverted-- Give: {state[all_moves[last_move][0]].color_list} \t Recieve: {state[all_moves[last_move][1]].color_list}\n")
                f.write(f"{moves}\t The following move is a bust: {last_move}\n\n")
                cur_index = last_move + 1
                continue
            moves.append(next_move[0])
            give_vial = next_move[1]
            receive_vial = next_move[2]
            # print(next_move, all_moves[next_move])
            
            # 2: update vials and check conditions
            f.write(f"Pouring.. (move {moves[-1]})- Give: {give_vial.color_list}\t Recieve: {receive_vial.color_list}\n")
            f.write(f"Moves {moves}\n")
            receive_vial.pour(give_vial)
            f.write(f"Give:{give_vial.color_list} {give_vial.completed}, Recive:{receive_vial.color_list} {receive_vial.completed}\n")
            # cond 1: flip-flop (what if there's a flip flop of more than a few vials?)
            #       if the last few moves are the same two moves
            flip_flop = len(set(moves[-4:])) == 2 and len(moves) > 4
            # cond 2: if the solution is found-- aka all vials are completed
            all_completed = all(vial.completed for vial in state)
            # cond 3: unknown found (exists a vial with only unknowns)
            unknown_found = any(vial.color_list[-1] == UNKNOWN_C for vial in state if len(vial.color_list) > 0)
            f.write(f"Flipflop: {flip_flop}, All completed: {all_completed}, Unknown found: {unknown_found}\n")
            
            # 3: act appropriately on conditions
            if flip_flop:
                rev_moves = moves.copy()
                rev_moves.reverse()
                # removes all flipflops except for first move that started it
                for i in range(len(moves)):
                    if not rev_moves[i+1] in set(rev_moves[:4]):
                        break
                    last_move = moves.pop()
                    f.write(f"Flip-floppin, reverting-- Given: {state[all_moves[last_move][0]].color_list} \t Recieve: {state[all_moves[last_move][1]].color_list}\n")
                    state[all_moves[last_move][0]].pour(state[all_moves[last_move][1]])
                    f.write(f"Reverted-- Given: {state[all_moves[last_move][0]].color_list} \t Recieve: {state[all_moves[last_move][1]].color_list}\n")
                    cur_index = last_move + 1
                f.write("\n")
                continue
            if all_completed or unknown_found: 
                f.write("Unknown found!\n")
                f.write(str([all_moves[move] for move in moves]))
                f.write("\n")
                break
            f.write("\n")
    # wonder how to print + delete to terminal

def print_move_tree(moves):
    
    pass
    

# instead of loop through each: from current index- find next possible move

def do_move(state, move):
    # check legality
    # same color or not
    # less than max
    vial_give = int(re.search("\d", move))
    vial_recieve = int(re.search("\d", move))
    
    # if legal do else return None
    

if __name__ == "__main__":
    main()
    
    # all_moves = calculate_all_moves()
    # moves = [11, 25, 129, 47, 28, 119, 170, 25, 34, 170, 25, 119, 170, 25, 34, 170]
    # print([all_moves[move] for move in moves])
    # # print(chr(27) + "[2J")
    # for i in range(10):
    #     os.system('cls||clear')
    #     print(i)
    
    # print(moves.count(25))
