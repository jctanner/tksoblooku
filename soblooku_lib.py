#!/usr/bin/env python

import copy
import json
import math
import os
import random
import time
from itertools import zip_longest
from pprint import pprint


'''
TESTGAME =  [4,8,5,1,7,9,2,6,3]
TESTGAME += [1,9,2,6,3,4,5,8,7]
TESTGAME += [3,7,6,2,8,5,9,1,4]

TESTGAME += [6,4,7,3,5,2,1,9,8]
TESTGAME += [5,1,8,9,4,7,6,3,2]
TESTGAME += [2,3,9,8,1,6,7,4,5]
#TESTGAME += ['','','', '','','', '','','']

TESTGAME += [7,5,1,4,9,3,8,2,6]
TESTGAME += [9,2,4,5,6,8,3,7,1]
#TESTGAME += [8,6,3,7,2,1,4,5,9]
#TESTGAME += [8,6,3,7,2,1,'','','']
TESTGAME += ['','','', '','','', '','','']
'''


TESTGAME  = [['','','', '','','', '','','']]
TESTGAME += [[4,'','', 1,'',2, '','',3]]
#TESTGAME += [['','','', 1,'',2, '','',3]]
TESTGAME += [['','',3, '','','', 4,'','']]

TESTGAME += [[2,'','', 4,'',7, '','',9]]
TESTGAME += [[3,'','', '','','', '','',8]]
TESTGAME += [['','',6, '',8,'', 5,'','']]

TESTGAME += [['',8,'', '',7,'', '',1,'']]
TESTGAME += [[7,'','', '','','', '','',2]]
TESTGAME += [['','',9, '',6,'', 7,'','']]

'''
TESTGAME = []
for x in range(0,9):
    TESTGAME += [[''] * 9]
TESTGAME[0][0] = 1
#import epdb; epdb.st()
'''

if os.path.exists('board.json'):
    TESTGAME = []
    for x in range(0, 9):
        row = []
        for y in range(0, 9):
            row.append('')
        TESTGAME.append(row)

    with open('board.json', 'r') as f:
        board = json.loads(f.read())

    rownum = 0
    rowix = 0
    for x in range(0, 81):
        #print(x)
        xid = x + 1
        #rowix = x % 8

        #if x > 0 and (xid % 9 == 0):
        #    rownum += 1

        val = board[x] or ''
        if val:
            val = int(val)

        print(f'{x} rown:{rownum} ix:{rowix} --> {val}')

        #if x != 0 and (rownum == 0 and rowix == 0):
        #    import epdb; epdb.st()

        TESTGAME[rownum]
        TESTGAME[rownum][rowix] = val

        #if x > 0 and (xid % 9 == 0):
        #    rownum += 1
        if rowix == 8:
            rownum += 1
            rowix = 0
        else:
            rowix += 1

    #import epdb; epdb.st()

TESTGRID = []
TESTGRID += [['A0', 'B0', 'C0', 'D0', 'E0', 'F0', 'G0', 'H0', 'I0']]
TESTGRID += [['J0', 'K0', 'L0', 'M0', 'N0', 'O0', 'P0', 'Q0', 'R0']]
TESTGRID += [['S0', 'T0', 'U0', 'V0', 'W0', 'X0', 'Y0', 'Z0', '_0']]

TESTGRID += [['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']]
TESTGRID += [['J1', 'K1', 'L1', 'M1', 'N1', 'O1', 'P1', 'Q1', 'R1']]
TESTGRID += [['S1', 'T1', 'U1', 'V1', 'W1', 'X1', 'Y1', 'Z1', '_1']]

TESTGRID += [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2']]
TESTGRID += [['J2', 'K2', 'L2', 'M2', 'N2', 'O2', 'P2', 'Q2', 'R2']]
TESTGRID += [['S2', 'T2', 'U2', 'V2', 'W2', 'X2', 'Y2', 'Z2', '_2']]


def generate_game_board(difficulty=50):
    base  = 3
    side  = base*base

    # pattern for a baseline valid solution
    def pattern(r,c): return (base*(r%base)+r//base+c)%side

    # randomize rows, columns and numbers (of valid base pattern)
    #from random import sample
    def shuffle(s): return random.sample(s,len(s)) 
    rBase = range(base) 
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,base*base+1))

    # produce board using randomized baseline pattern
    board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

    for x in range(0, difficulty):
        while True:
            rowid = random.choice(range(0, side))
            colid = random.choice(range(0, side))
            if isinstance(board[rowid][colid], int):
                board[rowid][colid] = ''
                break
            #import epdb; epdb.st()

    #import epdb; epdb.st()
    return board


def board_to_problemset(board):
    problemset = []
    for row in board:
        for col in row:
            problemset.append(col)
    return problemset


def answerset_to_cells(answerset):
    cells = [
        [], [], [],
        [], [], [],
        [], [], []
    ]
    row = 0
    col = 0
    for idx, x in enumerate(answerset):
        # self.board[row][col] = x
        #print(row)
        cells[row].append(x)
        if col == 8:
            col = 0
            row = row + 1
            # cells.append([])
        else:
            col += 1
        # cells[row].append(x)
    # import epdb; epdb.st()
    return cells


def get_invalid_values_for_cell(self, answer_chunks, tilecount, tilesq, tilenumber, tileindex):

    #print('get_invalid_values ...')

    # shift from beginning of tile
    col_offset = tileindex % tilesq
    # shift from beginning of board
    board_offset = (tilenumber % tilesq) * tilesq
    # column number is the tile offset plus the board offset
    column_number = board_offset + col_offset
    column_values = self.column_from_tiles(answer_chunks, column_number)
    column_values = [z for z in column_values if z]

    # what is the row num?
    #tile_row_starts = [i for i in range(0,tilecount,tilesq)]
    row_indexes = [y for y in zip_longest(*[iter(range(0,tilecount))]*tilesq)]
    row_offset_board = next(ix for ix, val in enumerate(row_indexes) if tilenumber in val)
    row_offset_tile = next(ix for ix, val in enumerate(row_indexes) if tileindex in val)
    row_id = (row_offset_board * tilesq) + row_offset_tile
    row_values = self.row_from_tiles(answer_chunks, row_id)
    #import pdb; pdb.set_trace()

    invalid = column_values + row_values
    invalid = [y for y in invalid if y and isinstance(y, int)]

    try:
        invalid = sorted(set(invalid))
    except TypeError as e:
        print(e)
        import epdb; epdb.st()

    return invalid


def randomize_solution(problemset):
    answerset = [x for x in problemset]
    answer_chunks = chunk_set(problemset)

    for idc, ac in enumerate(answer_chunks):
        ac = list(ac)
        for idx,x in enumerate(ac):
            if x is not None and x.strip() is not '':
                #import pdb; pdb.set_trace()
                ac[idx] = int(x)
        for idx,x in enumerate(ac):
            if not isinstance(x, int):
                choices = [y for y in range(1, 10) if y not in ac]
                choice = random.choice(choices)
                ac[idx] = choice
        answer_chunks[idc] = ac

    solution = dechunk_set(answer_chunks)
    return solution


def is_solved(answerset):
    score = 0

    # cleanup
    for idx,x in enumerate(answerset):
        if not isinstance(x, int):
            answerset[idx] = 0

    tiles = self.chunk_set(answerset)
    tilecount = len(tiles)
    tilesq = int(math.sqrt(tilecount))
    expected = sum([x for x in range(1,tilecount + 1)])

    for tile in tiles:
        if sum(tile) != expected:
            #print('tilesum != %s ... %s ... %s' % (expected, sum(tile), score))
            return False
        else:
            score += 1

    # make rows and check them
    rows = [x for x in zip_longest(*[iter(answerset)]*tilecount)]
    for row in rows:
        if sum(row) != expected:
            #print('rowsum != %s ... %s .. %s' % (expected, sum(row), score))
            return False
        else:
            score += 1

    # make columns and check them
    columns = []
    for x in range(0, tilecount):
        columns.append([])

    column_index = 0
    for tile_start in [x for x in range(0,tilesq)]:
        for column_number in [x for x in range(0,tilesq)]:
            for tile_offset in [x for x in range(0,tilecount,tilesq)]:
                
                col = self.column_from_tile(tiles[tile_start+tile_offset], column_number)
                columns[column_index].extend(col)

            column_index += 1

    for column in columns:
        if sum(column) != expected:
            #print('colsum != %s ... %s .. %s' % (expected, sum(column), score))
            return False
        else:
            score += 1

    #print('score: %s' % score)
    return True

def column_from_tile(tile, colnum):
    '''Get a column within a single tile'''
    tilesq = int(math.sqrt(len(tile)))
    column = []
    for idx in [x for x in range(0, len(tile), tilesq)]:
        idx = idx + colnum
        column.append(tile[idx])
    return column


def column_from_tiles(tiles, column_number):
    '''Get a column from the entire board'''
    columns = columns_from_tiles(tiles)
    return columns[column_number]


def columns_from_tiles(tiles):
    tilecount = len(tiles)
    tilesq = int(math.sqrt(tilecount))

    columns = []
    for x in range(0, tilecount):
        columns.append([])

    column_index = 0
    for tile_start in [x for x in range(0,tilesq)]:
        for column_number in [x for x in range(0,tilesq)]:
            for tile_offset in [x for x in range(0,tilecount,tilesq)]:
                col = column_from_tile(tiles[tile_start+tile_offset], column_number)
                columns[column_index].extend(col)
            column_index += 1

    # cleanup
    for idx,x in enumerate(columns):
        for idy,y in enumerate(x):
            if not isinstance(y, int):
                if y.isdigit():
                    columns[idx][idy] = int(y)

    return columns


def row_from_tiles(tiles, row_number):
    rows = rows_from_tiles(tiles)
    return rows[row_number]


def rows_from_tiles(tiles):
    tilecount = len(tiles)
    tilesq = int(math.sqrt(tilecount))
    row_tuples = [y for y in zip_longest(*[iter(range(0,tilecount))]*tilesq)]

    rows = []
    for x in range(0,tilecount):
        rows.append([])

    for idrt,row_tuple in enumerate(row_tuples):
        #print('########################################')
        #print('row_tuple',row_tuple)
        for rownum in range(0,tilesq):
            rownum = rownum + (tilesq * idrt)
            #print('rownum', rownum)

            for tilenum in row_tuple:
                #print('\ttilenum: %s' % tilenum)

                current_indexes = row_tuples[rownum % tilesq]
                #print('\t\tcindexes: %s' % str(current_indexes))

                for ci in current_indexes:
                    rows[rownum].append(tiles[tilenum][ci])

    # cleanup
    for idx,x in enumerate(rows):
        for idy,y in enumerate(x):
            if not isinstance(y, int):
                if y.isdigit():
                    rows[idx][idy] = int(y)

    #pprint(rows)
    #import pdb; pdb.set_trace()
    return rows


def get_chunk_bit_location(chunkid, chunkloc, val=None, chunks=None):
    '''What x,y is this chunk bit in the grid?'''

    #print(f'\tinput: ({chunkid}, {chunkloc})')

    if chunkid == 0 and chunkloc == 0:
        return (0, 0)
    
    if chunkid == 0 and chunkloc <= 2:
        return (0, chunkloc)

    if chunkid == 0 and chunkloc >= 3 and chunkloc < 6:
        return(chunkid + 1, chunkloc % 3)

    if chunkid == 0 and chunkloc >= 6:
        return(chunkid + 2, chunkloc % 3)
    
    if chunkid == 1 and chunkloc == 0:
        return(0, 3 + chunkloc)
    
    if chunkid == 1 and chunkloc <= 2:
        return (0, 3 + chunkloc % 3)

    if chunkid == 1 and chunkloc >= 3 and chunkloc < 6:
        return(1, chunkloc)
    
    if chunkid == 1 and chunkloc >= 6:
        return(3 - (chunkid % 3), 3 + (chunkloc % 3))

    if chunkid == 2 and chunkloc == 0:
        return (0, 6)
    
    if chunkid == 2 and chunkloc <= 2:
        return (0, 6 + (chunkloc % 3))
    
    if chunkid == 2 and chunkloc >= 3 and chunkloc < 6:
        return (3 - chunkid, 6 + (chunkloc % 3))

    if chunkid == 2 and chunkloc >= 6:
        return ((chunkid % 3), 6 + (chunkloc % 3))

    if chunkid == 3 and chunkloc == 0:
        return (3, 0)

    if chunkid == 3 and chunkloc <= 2:
        return (3, (chunkloc % 3))
    
    if chunkid == 3 and chunkloc >= 3 and chunkloc < 6:
        return (4, chunkloc % 3)
    
    if chunkid == 3 and chunkloc >= 6:
        return(6 + (chunkid%3 - 1), chunkloc % 3)
    
    if chunkid == 4 and chunkloc <= 2:
        return (chunkid-1, 3 + chunkloc%3)
    
    if chunkid == 4 and chunkloc >= 3 and chunkloc < 6:
        return (chunkid, chunkloc)
    
    if chunkid == 4 and chunkloc >= 6:
        return (5, 3 + chunkloc%3)

    if chunkid == 5 and chunkloc <= 2:
        return (3, 6 + chunkloc)
    
    if chunkid == 5 and chunkloc >= 3 and chunkloc < 6:
        return (4, 6 + chunkloc%3)

    if chunkid == 5 and chunkloc >= 6:
        return (chunkid, 6 + chunkloc%3)
    
    if chunkid == 6 and chunkloc <= 2:
        return (chunkid, 0 + chunkloc%3)
    
    if chunkid == 6 and chunkloc >= 3 and chunkloc < 6:
        return (chunkid+1, chunkloc%3)
    
    if chunkid == 6 and chunkloc >= 6:
        return (chunkid+2, chunkloc%3)
    
    if chunkid == 7 and chunkloc <= 2:
        return (chunkid-1, 3 + chunkloc%3)

    if chunkid == 7 and chunkloc >= 2 and chunkloc < 6:
        return (chunkid, 3 + chunkloc%3)
    
    if chunkid == 7 and chunkloc >= 6:
        return (chunkid+1, 3 + chunkloc%3)
    
    if chunkid == 8 and chunkloc <= 2:
        return (chunkid-2, 6 + chunkloc%3)
    
    if chunkid == 8 and chunkloc >= 3 and chunkloc < 6:
        return (chunkid-1, 6 + chunkloc%3)
    
    if chunkid == 8 and chunkloc >= 6:
        return (chunkid, 6 + chunkloc%3)

    print('\nNEED NEW STATEMENT >>')
    import epdb; epdb.st()


def get_chunk_bit_coordinates(chunks, chunkid):
    '''What grid coordinates does this chunk contain?'''

    # get_chunk_bit_location(chunkid, chunkloc, val=val, chunks=chunks)
    coords = [get_chunk_bit_location(chunkid, x) for x in range(0,9)]
    
    #import epdb; epdb.st()
    return coords


def get_chunk_bit_row_coordinates(chunkid, chunkloc):
    coords = []
    chunk_coord = get_chunk_bit_location(chunkid, chunkloc)
    for x in range(0, 9):
        coords.append((x, chunk_coord[1]))
    #import epdb; epdb.st()
    return coords


def get_chunk_bit_col_coordinates(chunkid, chunkloc):
    coords = []
    chunk_coord = get_chunk_bit_location(chunkid, chunkloc)
    for y in range(0, 9):
        coords.append((chunk_coord[0], y))
    #import epdb; epdb.st()
    return coords


def chunk_set(numberset):
    ''' Make list of lists for numberset '''

    # A "chunk" is a 3x3 tile from the board ...

    """
    1,2,3, 1,2,3, 1,2,3
    4,5,6, 4,5,6, 4,5,6
    7,8,9, 7,8,9, 7,8,9

    1,2,3, 1,2,3, 1,2,3
    4,5,6, 4,5,6, 4,5,6
    7,8,9, 7,8,9, 7,8,9

    1,2,3, 1,2,3, 1,2,3
    4,5,6, 4,5,6, 4,5,6
    7,8,9, 7,8,9, 7,8,9
    """

    board_sq = int(math.sqrt(len(numberset)))
    tile_sq = int(math.sqrt(board_sq))

    board = []
    for x in range(0, board_sq):
        tile = []
        board.append(tile)

    rows = [x for x in zip_longest(*[iter(numberset[:])]*board_sq)]

    tileno_row = 0
    tileno_offset = 0

    for idrow,row in enumerate(rows):

        subrows = [x for x in zip_longest(*[iter(row)]*tile_sq)]

        for idsr,sr in enumerate(subrows):
            board[tileno_offset + idsr] += sr

        if ((idrow + 1) % 3) == 0:
            tileno_offset += tile_sq

    return board


def dechunk_set(chunkset):
    ''' Make single list from a chunkset '''

    result = []

    tilecount = len(chunkset)
    tilesq = int(math.sqrt(tilecount))

    tilegroups = [x for x in zip_longest(*[iter(chunkset)]*tilesq)]

    for tg in tilegroups:
        subgroups = []
        for t in tg:
            t_subgroups = [x for x in zip_longest(*[iter(t)]*tilesq)]
            subgroups.append(t_subgroups)
        for x in range(0, tilesq):
            for sg in subgroups:
                #print(sg[x])
                for y in sg[x]:
                    result.append(y)

    #import pdb; pdb.set_trace()
    return result


def get_choice_map(chunks):
    choice_map = {}
    for idc, ac in enumerate(chunks):
        for idx,x in enumerate(ac):
            if not isinstance(x, int):
                invalid, examined = \
                    get_invalid_values_for_cell(
                        chunks,
                        len(chunks),
                        int(math.sqrt(len(chunks))),
                        idc,
                        idx
                    )
                choices = [y for y in range(1, (len(chunks) + 1)) 
                    if y not in ac and y not in invalid]
                choice_map[(idc, idx)] = copy.deepcopy(choices)
                #import epdb; epdb.st()

    ctuples = [x for x in choice_map.items()]
    ctuples = [[x[0],len(x[1]), x[1][:]] for x in ctuples]
    random.shuffle(ctuples)
    ctuples = sorted(ctuples, key=lambda x: x[1])
    #import epdb; epdb.st()
    return ctuples


def get_invalid_values_for_cell(answer_chunks, tilecount, tilesq, tilenumber, tileindex):

    #print('get_invalid_values ...')
    # need all board indexes for this tile so they can be highlighted ...
    '''
    self.examined_tiles = \
        sl.get_chunk_bit_coordinates(answer_chunks, tilenumber)
    self.examined_tiles += \
        sl.get_chunk_bit_row_coordinates(tilenumber, tileindex)
    self.examined_tiles += \
        sl.get_chunk_bit_col_coordinates(tilenumber, tileindex)
    #import epdb; epdb.st()
    '''
    examined = get_chunk_bit_coordinates(answer_chunks, tilenumber)
    examined += get_chunk_bit_row_coordinates(tilenumber, tileindex)
    examined += get_chunk_bit_col_coordinates(tilenumber, tileindex)

    # shift from beginning of tile
    col_offset = tileindex % tilesq
    # shift from beginning of board
    board_offset = (tilenumber % tilesq) * tilesq
    # column number is the tile offset plus the board offset
    column_number = board_offset + col_offset
    column_values = column_from_tiles(answer_chunks, column_number)
    column_values = [z for z in column_values if z]

    # what is the row num?
    #tile_row_starts = [i for i in range(0,tilecount,tilesq)]
    row_indexes = [y for y in zip_longest(*[iter(range(0,tilecount))]*tilesq)]
    row_offset_board = next(ix for ix, val in enumerate(row_indexes) if tilenumber in val)
    row_offset_tile = next(ix for ix, val in enumerate(row_indexes) if tileindex in val)
    row_id = (row_offset_board * tilesq) + row_offset_tile
    row_values = row_from_tiles(answer_chunks, row_id)
    #import pdb; pdb.set_trace()

    invalid = column_values + row_values
    invalid = [y for y in invalid if y and isinstance(y, int)]

    try:
        invalid = sorted(set(invalid))
    except TypeError as e:
        print(e)
        import epdb; epdb.st()

    return invalid, examined


def score_bits(bits):
    score = 0
    for row in bits:
        for col in row:
            if isinstance(col, int):
                score += 1
    #import epdb; epdb.st()
    return score


def test_fill(ingame):
    board  = copy.deepcopy(ingame)
    problemset = board_to_problemset(board)
    chunks = chunk_set(problemset)

    iteration = 0
    solved = False
    while not solved:
        iteration += 1
        ctuples = get_choice_map(chunks)
        if not ctuples:
            break

        ct = ctuples[0]
        idc = ct[0][0]
        idx = ct[0][1]

        if not ct[2]:
            # no valid choices ...
            board  = copy.deepcopy(ingame)
            problemset = board_to_problemset(board)
            chunks = chunk_set(problemset)
            continue

        chunks[idc][idx] = random.choice(ct[2])
        #import epdb; epdb.st()
        
        print('#'*35 + ' ' + str(iteration))
        for x in chunks:
            print(x)
        score = score_bits(chunks)
        print('.............. score: %s' % score)

    #import epdb; epdb.st()


def main():
    '''
    board  = copy.deepcopy(TESTGRID)
    problemset = board_to_problemset(board)
    chunks = chunk_set(problemset)

    #print(board)
    print('#board')
    for x in board:
        print(x)
    print('#ps')
    print(problemset)
    #for x in problemset:
    #    print(x)
    print('#chunks')
    #print(chunks)
    for x in chunks:
        print(x)
    
    print('')
    print('#############################')

    for x in range(0,9):
        for y in range(0, 9):
            print(x,y)
            #print(f'\tboard: {board[x][y]}')
            print(f'\tchunk val: {chunks[x][y]}')

            expected = None
            for x2 in range(0, 9):
                for y2 in range(0, 9):
                    if board[x2][y2] == chunks[x][y]:
                        expected = (x2,y2)
                        break
            print(f'\texpected board coords: {expected}')

            # get_chunk_bit_location(chunkid, chunkloc, val=None, chunks=None):
            chunkid = x
            chunkloc = y
            val = chunks[x][y]

            res = get_chunk_bit_location(chunkid, chunkloc, val=val, chunks=chunks)
            print(f'\tresult: {res}')

            assert res == expected, f"{res} != {expected}"
            #import epdb; epdb.st()
    
    for x in range(0, 9):
        coords = get_chunk_bit_coordinates(chunks, x)
        print(coords)
    '''

    #test_fill(TESTGAME)
    test_fill(generate_game_board())




if __name__ == "__main__":
    main()
