'''Ultimate Tic Tac Toe'''

class Player90(object):
    '''Classname will be provided later'''
    def __init__(self):
        super(T3, self).__init__()

    def move(self, current_board_game, board_stat, move_by_opponent, flag):
        '''Return tuple of next move (row, column).Check if next move is valid or not'''
        pass

    def utility(self, game_state):
        '''Function checks utility value of a state'''
        pass

    def actions(self, temp_board, temp_block, old_move, flag):
        '''Returns all possible actions from a particular state'''
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

        # We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
        cells = self.get_empty_out_of(temp_board, blocks_allowed)
        return cells

    def get_empty_out_of(game_state, blocks_allowed):
        cells = []  # it will be list of tuples
        #Iterate over possible blocks and get empty cells
        for idb in blocks_allowed:
            id1 = idb/3
            id2 = idb%3
            for i in range(id1*3,id1*3+3):
                for j in range(id2*3,id2*3+3):
                    if game_state[i][j] == '-':
                        cells.append((i,j))

        # If all the possible blocks are full, you can move anywhere
        if cells == []:
            for i in range(9):
                for j in range(9):
                    if game_state[i][j] == '-':
                        cells.append((i,j)) 
            
        return cells

    def result(self, game_state, move):
        '''Returns result of a move in a game_state'''
        pass

    def update_lists(game_board, block_stat, move_ret, fl):
        #move_ret has the move to be made, so we modify the game_board, and then check if we need to modify block_stat
        game_board[move_ret[0]][move_ret[1]] = fl


        #print "@@@@@@@@@@@@@@@@@"
        #print block_stat

        block_no = (move_ret[0]/3)*3 + move_ret[1]/3    
        id1 = block_no/3
        id2 = block_no%3
        mg = 0
        mflg = 0
        if block_stat[block_no] == '-':

            ### now for diagonals
            ## D1
            # ^
            #   ^
            #     ^
            if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
                mflg=1
                mg=1
                #print "SEG: D1 found"

            ## D2
            #     ^
            #   ^
            # ^
            ############ MODIFICATION HERE, in second condition -> gb[id1*3][id2*3+2]
            # if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3] and game_board[id1*3+1][id2*3+1] != '-':
            if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
                mflg=1
                mg=1
                #print "SEG: D2 found"

            ### col-wise
            if mflg != 1:
                for i in range(id2*3,id2*3+3):
                    #### MODIFICATION HERE, [i] was missing previously
                    # if game_board[id1*3]==game_board[id1*3+1] and game_board[id1*3+1] == game_board[id1*3+2] and game_board[id1*3] != '-':
                    if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                        mflg = 1
                        #print "SEG: Col found"
                        break

                    ### row-wise
            if mflg != 1:
                for i in range(id1*3,id1*3+3):
                    ### MODIFICATION HERE, [i] was missing previously
                    #if game_board[id2*3]==game_board[id2*3+1] and game_board[id2*3+1] == game_board[id2*3+2] and game_board[id2*3] != '-':
                    if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                        mflg = 1
        #print "SEG: Row found"
                        break

        
        if mflg == 1:
            block_stat[block_no] = fl

        #print 
        #print block_stat
        #print "@@@@@@@@@@@@@@@@@@@@@@@"    
        return mg

    def terminal_test(self, game_state):
        '''Checks whether end is reached'''
        pass

    #Check win
    def terminal_state_reached(game_board, block_stat, point1, point2):
        ### we are now concerned only with block_stat
        bs = block_stat
        ## Row win
        if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-') or (bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
            print block_stat
            return True, 'W'
        ## Col win
        elif (bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
            print block_stat
            return True, 'W'
        ## Diag win
        elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-'):
            print block_stat
            return True, 'W'
        else:
            smfl = 0
            for i in range(9):
                for j in range(9):
                    if game_board[i][j] == '-':
                        smfl = 1
                        break
            if smfl == 1:
                return False, 'Continue'
            
            else:
                ##### check of number of DIAGONALs
                if point1 > point2:
                    return True, 'P1'
                elif point2>point1:
                    return True, 'P2'
                else:
                    return True, 'D'   

    def validate_move(self):
        '''Function to check if move is valid or not'''
        pass

def main():
    pass

if __name__ == '__main__':
    main()