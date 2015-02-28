import sys
import random
import copy
import time

infinity = 100000

class Player90(object):

    def __init__(self):
        pass

    def move(self, current_board_game, board_stat, move_by_opponent, flag):
        '''Return tuple of next move (row, column).Check if next move is valid or not'''

        #Assign variables
        # temp_board = current_board_game[:]
        temp_board = copy.deepcopy(current_board_game)
        # temp_block = board_stat[:]
        temp_block = copy.deepcopy(board_stat)
        old_move = move_by_opponent
        own_flag = flag

        no_moves_possible = len(self.actions(temp_board, temp_block, old_move, flag))
        print "no_moves_possible: %s" % (str(no_moves_possible))
        d = 2
        if no_moves_possible > 40:
            d = 2
        elif no_moves_possible > 20:
            d = 3
        elif no_moves_possible > 10:
            d = 3
        else:
            d = 3

        start = time.time()
        move = self.alphabeta_search(temp_board, temp_block, old_move, flag, own_flag, d)
        end = time.time()
        print "DEBUG 90"
        print "Time taken", end - start
        print move
        # print_lists(current_board_game, board_stat)
        # print_lists(temp_board, temp_block)
        return move
        # cells = self.actions(temp_board, temp_block, old_move, flag)
        # #jaadu returns best possible move
        # return self.jaadu(cells, temp_board, flag)

    def alphabeta_search(self, state, block, old_move, flag, own_flag, d=2, cutoff_test=None, eval_fn=None):
        """Search game to determine best action; use alpha-beta pruning.
        This version cuts off search and uses an evaluation function."""

        # player = game.to_move(state)
        player = self.to_move(state)
        start = time.time()

        def max_value(cell, state, block, flag, own_flag, alpha, beta, depth):
            if cutoff_test(state, depth):
                return eval_fn(cell, state, flag, own_flag)
            v = -infinity
            old_move = cell
            # new_state = state[:][:]
            new_state = copy.deepcopy(state)
            # new_block = block[:]
            new_block = copy.deepcopy(block)
            self.update_lists(new_state, new_block, cell, flag)

            for a in self.actions(new_state, new_block, old_move, flag):
                v = max(v, min_value(a, new_state, new_block, self.next_move(flag), own_flag,
                                     alpha, beta, depth+1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(cell, state, block, flag, own_flag, alpha, beta, depth):
            if cutoff_test(state, depth):
                return eval_fn(cell, state, flag, own_flag)
            v = infinity
            old_move = cell
            # new_state = state[:][:]
            new_state = copy.deepcopy(state)
            # new_block = block[:]
            new_block = copy.deepcopy(block)
            self.update_lists(new_state, new_block, cell, flag)
            #update block and state
            for a in self.actions(new_state, new_block, old_move, flag):
                v = min(v, max_value(a, new_state, new_block, self.next_move(flag), own_flag,
                                     alpha, beta, depth+1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        # Body of alphabeta_search starts here:
        # The default test cuts off at depth d or at a terminal state
        cutoff_test = (cutoff_test or
                       (lambda state,depth: depth>d or self.terminal_test(state, block) or (time.time() - start) > 5.9))
        # cutoff_test = (cutoff_test or
        #                (lambda state,depth: depth>d or self.terminal_test(state, block)))
        eval_fn = eval_fn or (lambda cell,state,flag,own_flag: self.utility(cell, state, flag, own_flag))
        ''' There are three versions of argmin/argmax, depending on what you want to
            do with ties: return the first one, return them all, or pick at random.
            argmax, argmax_list, argmax_random_tie.
        '''
        return self.argmax_random_tie(self.actions(state, block, old_move, flag),
                      lambda a: min_value(a, state, block, self.next_move(flag), own_flag,
                                          -infinity, infinity, 0))


    def actions(self, temp_board, temp_block, old_move, flag):
        '''Returns all possible actions from a particular state'''
        #Check if terminal state is reached
        if self.terminal_test(temp_board, temp_block):
            return []

        for_corner = [0,2,3,5,6,8]

        #List of permitted blocks, based on old move.
        blocks_allowed  = []

        if old_move[0] in for_corner and old_move[1] in for_corner:
            ## we will have 3 representative blocks, to choose from

            if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
                ## top left 3 blocks are allowed
                blocks_allowed = [0, 1, 3]
            elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
                ## top right 3 blocks are allowed
                blocks_allowed = [1,2,5]
            elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
                ## bottom left 3 blocks are allowed
                blocks_allowed  = [3,6,7]
            elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
                ### bottom right 3 blocks are allowed
                blocks_allowed = [5,7,8]
            else:
                print "SOMETHING REALLY WEIRD HAPPENED!"
                sys.exit(1)
        else:
        #### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
            if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
                ## upper-center block
                blocks_allowed = [1]
    
            elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
                ## middle-left block
                blocks_allowed = [3]
        
            elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
                ## lower-center block
                blocks_allowed = [7]

            elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
                ## middle-right block
                blocks_allowed = [5]
            elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
                blocks_allowed = [4]

        for i in reversed(blocks_allowed):
            if temp_block[i] != '-':
                blocks_allowed.remove(i)
    # We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
        cells = self.get_empty_out_of(temp_board, blocks_allowed, temp_block)
        return cells

    def result(self, state, move):
        "Return the state that results from making a move from a state."
        x, y  = move
        new_state = copy.deepcopy(state)
        new_state[x][y] = to_move(state)
        return new_state

    def get_empty_out_of(self, gameb, blal, block_stat):
        '''Gets empty cells from the list of possible blocks. Hence gets valid moves.'''
        cells = []  # it will be list of tuples
        #Iterate over possible blocks and get empty cells
        for idb in blal:
            id1 = idb/3
            id2 = idb%3
            for i in range(id1*3,id1*3+3):
                for j in range(id2*3,id2*3+3):
                    if gameb[i][j] == '-':
                        cells.append((i,j))

        # If all the possible blocks are full, you can move anywhere
        if cells == []:
            for i in range(9):
                for j in range(9):
                    no = (i/3)*3
                    no += (j/3)
                    if gameb[i][j] == '-' and block_stat[no] == '-':
                        cells.append((i,j)) 
        return cells

    def terminal_test(self, state, block):
        "Return True if this is a final state for the game."
        return self.terminal_state_reached(state, block)

    def terminal_state_reached(self, game_board, block_stat):
        '''Checks whether end is reached'''
        #Check if game is won!
        bs = block_stat
        ## Row win
        if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
            # print block_stat
            return True
        ## Col win
        elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
            # print block_stat
            return True
        ## Diag win
        elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
            # print block_stat
            return True
        else:
            smfl = 0
            for i in range(9):
                for j in range(9):
                    if game_board[i][j] == '-' and block_stat[(i/3)*3+(j/3)] == '-':
                        smfl = 1
                        break
            if smfl == 1:
                #Game is still on!
                return False
            
            else:
                #Changed scoring mechanism
                # 1. If there is a tie, player with more boxes won, wins.
                # 2. If no of boxes won is the same, player with more corner move, wins. 
                point1 = 0
                point2 = 0
                for i in block_stat:
                    if i == 'x':
                        point1+=1
                    elif i=='o':
                        point2+=1
                if point1>point2:
                    return True
                elif point2>point1:
                    return True
                else:
                    point1 = 0
                    point2 = 0
                    for i in range(len(game_board)):
                        for j in range(len(game_board[i])):
                            if i%3!=1 and j%3!=1:
                                if game_board[i][j] == 'x':
                                    point1+=1
                                elif game_board[i][j]=='o':
                                    point2+=1
                    if point1>point2:
                        return True
                    elif point2>point1:
                        return True
                    else:
                        return True

    def update_lists(self, game_board, block_stat, move_ret, fl):
        #move_ret has the move to be made, so we modify the game_board, and then check if we need to modify block_stat
        game_board[move_ret[0]][move_ret[1]] = fl

        block_no = (move_ret[0]/3)*3 + move_ret[1]/3
        id1 = block_no/3
        id2 = block_no%3
        mg = 0
        mflg = 0
        if block_stat[block_no] == '-':
            if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
                mflg=1
            if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
                mflg=1
            
            if mflg != 1:
                for i in range(id2*3,id2*3+3):
                    if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                        mflg = 1
                        break

                    ### row-wise
            if mflg != 1:
                for i in range(id1*3,id1*3+3):
                    if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                        mflg = 1
                        break

        
        if mflg == 1:
            block_stat[block_no] = fl
        
        #check for draw on the block.

        id1 = block_no/3
        id2 = block_no%3
        cells = []
        for i in range(id1*3,id1*3+3):
            for j in range(id2*3,id2*3+3):
                if game_board[i][j] == '-':
                    cells.append((i,j))

        if cells == [] and mflg!=1:
            block_stat[block_no] = 'd' #Draw
        
        return

    def to_move(self, state):
        "Return the player whose move it is in this state."
        total_turns = 0
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] in ['x', 'o']:
                    total_turns += 1
        if total_turns % 2:
            return 'o'
        else:
            return 'x'

    def next_move(self, flag):
        if flag == 'x':
            return 'o'
        else:
            return 'x'

    def jaadu(self, available_cells, board, flag):
        values = {}
        max_cell = ()
        max_value = 0
        for cell in available_cells:
            values[cell] = self.utility(cell, board, flag)
            if values[cell] > max_value:
                max_value = values[cell]
                max_cell = cell
            # print cell, values[cell]
        print max_cell, max_value
        # x = raw_input()
        return max_cell
        # exit(0)

    def debug_chota_board(self, board):
        for i in [0,1,2]:
            print board[i]

    def get_2d_list_slice(self, matrix, start_row, end_row, start_col, end_col):
        return [row[start_col:end_col] for row in matrix[start_row:end_row]]

    def line_possible(self, x, y):
        # x,y = cell
        if x == 1 and y == 1:
            return 4
        elif x in [0,2] and y in [0, 2]:
            return 3
        else:
            return 2

    def line_bani(self, board):
        #chota board
        for i in [0,1,2]:
            if board[i][0] != '-' and board[i][0]==board[i][1]==board[i][2]:
                return 1
            if board[0][i] != '-' and board[0][i]==board[1][i]==board[2][i]:
                return 1
        if board[0][0] != '-' and board[0][0]==board[1][1]==board[2][2]:
            return 1
        if board[2][0] != '-' and board[2][0]==board[1][1]==board[0][2]:
            return 1
        return 0

    def line_bani_flag(self, board):
        '''Returns flag if a line is formed'''
        #chota board
        for i in [0,1,2]:
            if board[i][0] != '-' and board[i][0]==board[i][1]==board[i][2]:
                if board[i][0] == 'x':
                    return 'x'
                else:
                    return 'o'
            if board[0][i] != '-' and board[0][i]==board[1][i]==board[2][i]:
                if board[0][i] == 'x':
                    return 'x'
                else:
                    return 'o'
        if board[0][0] != '-' and board[0][0]==board[1][1]==board[2][2]:
            if board[0][0] == 'x':
                return 'x'
            else:
                return 'o'
        if board[2][0] != '-' and board[2][0]==board[1][1]==board[0][2]:
            if board[2][0] == 'x':
                return 'x'
            else:
                return 'o'
        return '-'

    def line_bani_alternate(self, board):
        #chota board
        for i in [0,1,2]:
            if board[i*3] != '-' and board[i*3] == board[i*3 + 1] == board[i*3 + 2]:
                return 1
            if board[i*3] != '-' and board[i] == board[i + 3]==board[i + 6]:
                return 1
        if board[0] != '-' and board[0] == board[4] == board[8]:
            return 1
        if board[2] != '-' and board[4] == board[2] == board[6]:
            return 1
        return 0

    #______________________________________________________________________________
    # Functions on sequences of numbers
    # NOTE: these take the sequence argument first, like min and max,
    # and like standard math notation: \sigma (i = 1..n) fn(i)
    # A lot of programing is finding the best value that satisfies some condition;
    # so there are three versions of argmin/argmax, depending on what you want to
    # do with ties: return the first one, return them all, or pick at random.

    def argmin(self, seq, fn):
        """Return an element with lowest fn(seq[i]) score; tie goes to first one.
        >>> argmin(['one', 'to', 'three'], len)
        'to'
        """
        best = seq[0]; best_score = fn(best)
        for x in seq:
            x_score = fn(x)
            if x_score < best_score:
                best, best_score = x, x_score
            #Randomized
            # if x_score <= best_score and random.randint(0,1)>0:
            #     best, best_score = x, x_score
        return best

    def argmin_list(self, seq, fn):
        """Return a list of elements of seq[i] with the lowest fn(seq[i]) scores.
        >>> argmin_list(['one', 'to', 'three', 'or'], len)
        ['to', 'or']
        """
        best_score, best = fn(seq[0]), []
        for x in seq:
            x_score = fn(x)
            if x_score < best_score:
                best, best_score = [x], x_score
            elif x_score == best_score:
                best.append(x)
        return best

    def argmin_random_tie(self, seq, fn):
        """Return an element with lowest fn(seq[i]) score; break ties at random.
        Thus, for all s,f: argmin_random_tie(s, f) in argmin_list(s, f)"""
        best_score = fn(seq[0]); n = 0
        for x in seq:
            x_score = fn(x)
            if x_score < best_score:
                best, best_score = x, x_score; n = 1
            elif x_score == best_score:
                n += 1
                if random.randrange(n) == 0:
                    best = x
        return best

    def argmax(self, seq, fn):
        """Return an element with highest fn(seq[i]) score; tie goes to first one.
        >>> argmax(['one', 'to', 'three'], len)
        'three'
        """
        return self.argmin(seq, lambda x: -fn(x))

    def argmax_list(self, seq, fn):
        """Return a list of elements of seq[i] with the highest fn(seq[i]) scores.
        >>> argmax_list(['one', 'three', 'seven'], len)
        ['three', 'seven']
        """
        return self.argmin_list(seq, lambda x: -fn(x))

    def argmax_random_tie(self, seq, fn):
        "Return an element with highest fn(seq[i]) score; break ties at random."
        return self.argmin_random_tie(seq, lambda x: -fn(x))

    #______________________________________________________________________________

    def utility(self, cell, board, flag=None, own_flag=None):
        super_block_factor = 10
        block_factor = 5
        line_factor = 300
        super_line_factor = 10000

        if not flag:
            flag = self.to_move(board)

        value = 0
        x, y = cell
        #block
        value = (self.line_possible(x%3, y%3)*block_factor)
        #super block
        value += (self.line_possible(x/3, y/3)*super_block_factor)
        board[x][y] = flag
        
        #for chota board
        chota_board = self.get_2d_list_slice(board, (x/3) * 3, ((x/3) * 3) + 3, (y/3) * 3, ((y/3) * 3) + 3)
        value += self.line_bani(chota_board)*line_factor
        #end for chota board

        super_block_status = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                chotu = self.get_2d_list_slice(board, i * 3, (i * 3) + 3, j * 3, (j * 3) + 3)
                # if self.line_bani(chotu):
                #     super_block_status[i][j] = 1
                # else:
                #     super_block_status[i][j] = '-'
                super_block_status[i][j] = self.line_bani_flag(chotu)

        #bug since we only assign value 1 to whether line is formed by x or o this results in next result
        #becoming true for most cases
        #fixed above
        value += self.line_bani(super_block_status)*super_line_factor

        board[x][y] = '-'
        if flag != own_flag:
            return -value
        return value

class Player91(Player90):

    def __init__(self):
        super(Player91, self).__init__()

    def move(self, current_board_game, board_stat, move_by_opponent, flag):
        print "DEBUG 91"
        return super(Player91, self).move(current_board_game, board_stat, move_by_opponent, flag)

    def utility(self, cell, board, flag = None, own_flag = None):
        super_block_factor = 8
        block_factor = 12
        line_factor = 300
        super_line_factor = 10000
        if not flag:
            flag = self.to_move(board)

        value = 0
        x, y = cell
        #block
        value = (self.line_possible(x%3, y%3)*block_factor)
        #super block
        value += (self.line_possible(x/3, y/3)*super_block_factor)
        board[x][y] = flag
        
        #for chota board
        chota_board = self.get_2d_list_slice(board, (x/3) * 3, ((x/3) * 3) + 3, (y/3) * 3, ((y/3) * 3) + 3)
        value += self.line_bani(chota_board)*line_factor
        #end for chota board

        super_block_status = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                chotu = self.get_2d_list_slice(board, i * 3, (i * 3) + 3, j * 3, (j * 3) + 3)
                # if self.line_bani(chotu):
                #     super_block_status[i][j] = 1
                # else:
                #     super_block_status[i][j] = '-'
                super_block_status[i][j] = self.line_bani_flag(chotu)

        #bug since we only assign value 1 to whether line is formed by x or o this results in next result
        #becoming true for most cases
        #fixed above
        value += self.line_bani(super_block_status)*super_line_factor

        board[x][y] = '-'
        if flag != own_flag:
            return -value
        return value
