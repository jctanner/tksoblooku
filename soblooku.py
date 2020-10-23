#!/usr/bin/env python3

import copy
import math
import random
import time
from itertools import zip_longest
from pprint import pprint

import tkinter as tk
from tkinter import *

from soblooku_lib import TESTGAME
import soblooku_lib as sl


class Application(Frame):

    solving = False
    tested = []
    txtids = []
    rectangles = []
    active_tile = None
    examined_tiles = []
    _game = TESTGAME
    board = copy.deepcopy(TESTGAME)
    solved = True

    def __init__(self, master=None, rows=9, columns=9, size=32, color1="white", color2="blue"):

        self.master = master
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        canvas_width = columns * size
        canvas_height = rows * size
        tk.Frame.__init__(self, master)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
            width=canvas_width, height=canvas_height + 100, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        self.canvas.bind("<Configure>", self.refresh)

        tk.Button(self, text="RESET", command=self.reset).pack()
        tk.Button(self, text="RANDOMIZE", command=self.randomize).pack()
        tk.Button(self, text="SOLVE", command=self.solve_backtrack).pack()
        #tk.Button(self, text="SOLVE TREE", command=self.solve_tree).pack()
        #tk.Button(self, text="SOLVE RANDOM", command=self.solve_randomly).pack()
        tk.Button(self, text="QUIT", command=self.quit).pack()

        #self.active_tile = None


    def get_tile_color(self, x,y):
        '''color coding by grid'''

        #if self.active_tile:
        #    import epdb; epdb.st()

        if self.active_tile and self.active_tile == (x, y):
            #import epdb; epdb.st()
            return 'red'
        
        if self.examined_tiles and (x,y) in self.examined_tiles:
            return 'deep pink'

        if x < 3 and y < 3:
            return 'pink'
        if x >= 3 and x < 6 and y >= 3 and y < 6:
            return 'orange'
        if x >= 6 and y >= 6:
            return 'green'

        if x >= 3 and x < 6 and y < 3:
            return 'yellow'
        if x >= 6 and y >= 3 and y <= 6:
            return 'white'
        if x >= 6 and y <= 3:
            return 'orchid1'
        if x < 3 and y >= 6:
            return 'aquamarine'

        return 'lightblue'

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        self.redraw()
    
    def redraw(self):
        self.canvas.delete("all")
        color = self.color2
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black",
                        fill=self.get_tile_color(row, col), tags="square")
                self.rectangles.append(rect)
        self.fill_board()

    def fill_board(self):
        '''populates all tiles with values'''

        '''
        # wipe out old values
        for x in self.txtids:
            self.canvas.delete(x)
        '''

        for x in range(0, self.columns):
            for y in range(0, self.rows):
                #print(x,y, self.board[x][y])
                self.set_grid_value(self.board[x][y], x, y)
        
        #self.canvas.delete("all")
        self.master.update_idletasks()
        self.master.update()
        #print('board filled ... %s' % self.board)

    def set_grid_value(self, name, row, column):
        '''populate a single tile value'''
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        #print(x0,y0,name)
        txtid = self.canvas.create_text(x0, y0, text=name)
        self.txtids.append(txtid)

    def reset(self):
        '''set back to testgame'''
        print('RESETTING ...')
        self.solved = False
        self.active_tile = None
        self.examined_tiles = []
        self.board = copy.deepcopy(self._game)
        self.fill_board()
        self.redraw()

    def answerset_to_cells(self, answerset):
        row = 0
        col = 0
        for idx,x in enumerate(answerset):
            self.board[row][col] = x
            if col == 8:
                col = 0
                row = row + 1
            else:
                col += 1
        self.fill_board()

    def randomize(self):

        print('RANDOMIZE ...')
        '''
        self.reset()
        problemset = sl.board_to_problemset(self.board)
        #print(problemset)
        answerset = self.randomize_solution(problemset)
        #print(answerset)
        self.answerset_to_cells(answerset)
        '''

        '''
        problemset = sl.board_to_problemset(self.board)
        try:
            self.backtrack_solution(problemset)
        except Exception:
            pass
        '''

        self.solved = False
        self._game = sl.generate_game_board()
        self.board = self._game
        self.redraw()

    def solve_backtrack(self):
        print('solving ...')
        if self.solved:
            return

        problemset = sl.board_to_problemset(self.board)
        solution = None
        while solution is None:
            try:
                solution = self.backtrack_solution(problemset)
            except Exception:
                pass
        if solution:
            self.solved = True
        
        #import epdb; epdb.st()

    def solve_tree(self):
        print('solving ...')
        count = 0
        solved = False
        while not solved:
            print(f'iteration {count}')
            self.reset()
            problemset = sl.board_to_problemset(self.board)
            answerset = self.treesearch_solution(problemset)
            self.answerset_to_cells(answerset)
            count += 1

    def solve_randomly(self):
        print('solving ...')
        '''
        count = 0
        solved = False
        while not solved:

            print(f'iteration {count}')
            self.reset()
            problemset = sl.board_to_problemset(self.board)
            answerset = self.randomize_solution(problemset)
            self.answerset_to_cells(answerset)
            count += 1
        '''
        
        problemset = sl.board_to_problemset(self.board)
        try:
            self.backtrack_solution(problemset)
        except Exception:
            pass

    def backtrack_solution(self, problemset):

        print('backtrack start ...')

        answerset = [x for x in problemset]
        answer_chunks = sl.chunk_set(problemset)
        
        #answer_chunks = [list(x) for x in answer_chunks]
        #answer_chunks_original = [x for x in answer_chunks]

        tilecount = len(answer_chunks)
        tilesq = int(math.sqrt(len(answer_chunks)))

        solved = False
        iteration = 0
        while not solved:

            iteration += 1
            print('iteration: %s' % iteration)

            ctuples = sl.get_choice_map(answer_chunks)
            print('unfilled: %s' % len(ctuples))
            #print(ctuples)
            ct = ctuples[0]
            idc = ct[0][0]
            idx = ct[0][1]
            self.active_tile = \
                sl.get_chunk_bit_location(idc, idx, val=None, chunks=None)
            self.redraw()
            
            '''
            invalid, examined = sl.get_invalid_values_for_cell(
                answer_chunks,
                tilecount,
                tilesq,
                idc,
                idx
            )
            self.examined_tiles = examined[:]
            '''

            '''
            #choices = [y for y in range(1, (tilecount + 1)) if y not in ac and y not in invalid]
            choices = [y for y in range(1, 10) if y not in invalid]
            print(f'\tinvalid: {invalid}')
            print(f'\tchoices: {choices}')
            if not choices and 1 not in invalid:
                import epdb; epdb.st()
            '''

            #self.redraw()

            #if not choices:
            #    raise Exception('STUCK!')

            #choice = random.choice(choices)
            choice = random.choice(ct[2])
            answer_chunks[idc][idx] = choice
            self.answerset_to_cells(sl.dechunk_set(answer_chunks))
            self.redraw()
            #time.sleep(.5)

            #if len(ctuples) > 1:
            #    continue

            score = sl.score_bits(answer_chunks)
            print('SCORE: %s' % score)
            if score == 81:
                solved = True

        #import epdb; epdb.st()
        solution = sl.dechunk_set(answer_chunks)
        print('back track finished')
        return solution

    def treesearch_solution(self, problemset):

        print('treesearch start ...')

        answerset = [x for x in problemset]
        answer_chunks = sl.chunk_set(problemset)
        answer_chunks = [list(x) for x in answer_chunks]
        answer_chunks_original = [x for x in answer_chunks]

        tilecount = len(answer_chunks)
        tilesq = int(math.sqrt(len(answer_chunks)))

        choicemax = 1
        finished = False
        choice_trees = []

        # cleanup the inputs
        for idc, ac in enumerate(answer_chunks):
            for idx,x in enumerate(ac):
                if not isinstance(x, int) and x.isdigit():
                    ac[idx] = int(x)

        choicemax = 1
        finished = False
        choice_trees = []

        count1 = 0
        while not finished:

            for idc, ac in enumerate(answer_chunks):
                for idx,x in enumerate(ac):
                    if not isinstance(x, int):

                        invalid = self.get_invalid_values_for_cell(answer_chunks, tilecount, tilesq, idc, idx)
                        choices = [y for y in range(1, (tilecount + 1)) if y not in ac and y not in invalid]
                        print(f'\tinvalid: {invalid}')
                        #print(f'\tchoices: {choices}')

                        if not choices:
                            choice = 'X'
                            answer_chunks[idc][idx] = choice
                            #import epdb; epdb.st()
                            return sl.dechunk_set(answer_chunks)
                        elif len(choices) == choicemax:
                            choice = random.choice(choices)
                            answer_chunks[idc][idx] = choice
                            self.answerset_to_cells(sl.dechunk_set(answer_chunks))
                            #time.sleep(.05)

            choicemax += 1
            if choicemax == tilecount:
                finished = True

            # update display
            answerset = sl.dechunk_set(answer_chunks)
            self.answerset_to_cells(answerset)

            print(f'\tcount1: {count1}')
            count1 += 1

        #answer_chunks = self.create_solution(answer_chunks)
        solution = sl.dechunk_set(answer_chunks)

        print('treesearch finished')
        return solution

    def randomize_solution(self, problemset):
        answerset = [x for x in problemset]
        answer_chunks = sl.chunk_set(problemset)
        answer_chunks = [list(x) for x in answer_chunks]
        tilecount = len(answer_chunks)
        tilesq = int(math.sqrt(len(answer_chunks)))


        choicemax = 1
        finished = False
        while not finished:

            print('choicemax:', choicemax)

            for idc, ac in enumerate(answer_chunks):

                for idx,x in enumerate(ac):
                    if not isinstance(x, int) and x.isdigit():
                        ac[idx] = int(x)

                for idx,x in enumerate(ac):
                    if not isinstance(x, int):

                        invalid = sl.get_invalid_values_for_cell(
                                answer_chunks, tilecount, tilesq, idc, idx)
                        choices = [
                                y for y in range(1, 10)
                                if y not in ac and y not in invalid
                                ]

                        if not choices:
                            answer_chunks[idc] = ac
                            answer_chunks[idc][idx] = '*'
                            return sl.dechunk_set(answer_chunks)

                        elif len(choices) == choicemax:
                            #choice = choices[0]
                            choice = random.choice(choices)
                            ac[idx] = choice
                        '''
                        else:
                            print(len(choices))
                            #choice = random.choice(choices)
                            pass
                        '''

                answer_chunks[idc] = ac

            choicemax += 1
            if choicemax == tilecount:
                finished = True

            # update display
            answerset = sl.dechunk_set(answer_chunks)
            #self.update_board_with_answerset(answerset)
            self.answerset_to_cells(answerset)


        #answer_chunks = self.create_solution(answer_chunks)
        solution = sl.dechunk_set(answer_chunks)
        return solution

    def create_solution(self, answer_chunks):
        tilecount = len(answer_chunks)
        tilesq = int(math.sqrt(len(answer_chunks)))
        choicemax = 1
        finished = False

        while not finished:

            print('choicemax:', choicemax)

            for idc, ac in enumerate(answer_chunks):

                for idx,x in enumerate(ac):
                    if not isinstance(x, int) and x.isdigit():
                        ac[idx] = int(x)

                for idx,x in enumerate(ac):
                    if not isinstance(x, int):

                        # shift from beginning of tile
                        col_offset = idx % tilesq
                        # shift from beginning of board
                        board_offset = (idc % tilesq) * tilesq
                        # column number is the tile offset plus the board offset
                        column_number = board_offset + col_offset
                        column_values = self.column_from_tiles(answer_chunks, column_number)
                        column_values = [z for z in column_values if z]

                        # what is the row num?
                        #tile_row_starts = [i for i in range(0,tilecount,tilesq)]
                        row_indexes = [y for y in zip_longest(*[iter(range(0,tilecount))]*tilesq)]
                        row_offset_board = next(ix for ix, val in enumerate(row_indexes) if idc in val)
                        row_offset_tile = next(ix for ix, val in enumerate(row_indexes) if idx in val)
                        row_id = (row_offset_board * tilesq) + row_offset_tile
                        row_values = self.row_from_tiles(answer_chunks, row_id)
                        #import pdb; pdb.set_trace()

                        invalid = column_values + row_values
                        invalid = [y for y in invalid if y]
                        invalid = sorted(set(invalid))
                        choices = [y for y in range(1, 10) if y not in ac and y not in invalid]

                        if not choices:
                            answer_chunks[idc] = ac
                            answer_chunks[idc][idx] = '*'
                            return sl.dechunk_set(answer_chunks)
                            
                        elif len(choices) == choicemax:
                            #choice = choices[0]
                            choice = random.choice(choices)
                            ac[idx] = choice

                answer_chunks[idc] = ac

            # update display
            answerset = sl.dechunk_set(answer_chunks)
            #self.update_board_with_answerset(answerset)
            self.answerset_to_cells(answerset)

            choicemax += 1
            if choicemax == tilecount:
                finished = True

        return answer_chunks

    def _randomize_solution(self, problemset):
        answerset = [x for x in problemset]
        answer_chunks = sl.chunk_set(problemset)

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

        solution = sl.dechunk_set(answer_chunks)
        return solution

    def is_solved(self, answerset):
        score = 0

        # cleanup
        for idx,x in enumerate(answerset):
            if not isinstance(x, int):
                answerset[idx] = 0

        tiles = sl.chunk_set(answerset)
        tilecount = len(tiles)
        tilesq = int(math.sqrt(tilecount))
        expected = sum([x for x in range(1,tilecount + 1)])

        for tile in tiles:
            if sum(tile) != expected:
                print('tilesum != %s ... %s ... %s' % (expected, sum(tile), score))
                return False
            else:
                score += 1

        # make rows and check them
        rows = [x for x in zip_longest(*[iter(answerset)]*tilecount)]
        for row in rows:
            if sum(row) != expected:
                print('rowsum != %s ... %s .. %s' % (expected, sum(row), score))
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
                print('colsum != %s ... %s .. %s' % (expected, sum(column), score))
                return False
            else:
                score += 1

        print('score: %s' % score)
        return True

    def column_from_tile(self, tile, colnum):
        '''Get a column within a single tile'''
        tilesq = int(math.sqrt(len(tile)))
        column = []
        for idx in [x for x in range(0, len(tile), tilesq)]:
            idx = idx + colnum
            column.append(tile[idx])
        return column


    def column_from_tiles(self, tiles, column_number):
        '''Get a column from the entire board'''
        columns = self.columns_from_tiles(tiles)
        return columns[column_number]

    def columns_from_tiles(self, tiles):
        tilecount = len(tiles)
        tilesq = int(math.sqrt(tilecount))

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

        # cleanup
        for idx,x in enumerate(columns):
            for idy,y in enumerate(x):
                if not isinstance(y, int):
                    if y.isdigit():
                        columns[idx][idy] = int(y)

        return columns

    def row_from_tiles(self, tiles, row_number):
        rows = self.rows_from_tiles(tiles)
        return rows[row_number]

    def rows_from_tiles(self, tiles):
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


if __name__ == "__main__":
    root = tk.Tk()
    #app = Application(master=root)
    app = Application(master=root)
    app.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    app.mainloop()
