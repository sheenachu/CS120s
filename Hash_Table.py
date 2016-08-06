# CS122 W'16: Markov models and hash tables
# SHEENA CHU

TOO_FULL = 0.5
GROWTH_RATIO = 2

class Hash_Table:

    def __init__(self, cells,defval):
        '''
        Construct a bnew hash table with a fixed number of cells equal to the
        parameter "cells", and which yields the value defval upon a lookup to a
        key that has not previously been inserted
        '''
        self.cells = cells
        self.defval = defval
        self.count = 0
        h_table = []
        for i in range(self.cells):
            h_table.append(None)
        self.h_table = h_table

    def hash_function(self, string):
        '''
        Takes a string and returns am integer hash value.
        '''
        h = 0
        for char in string:
            h = (37 * (h + ord(char))) % self.cells
        return h

    def rehash(self):
        '''
        Expands the size of hash table by GROWTH_RATIO,
        and migrate all the data into their proper locations
        in the newly-expanded hash table
        '''
        new_table = Hash_Table(self.cells * GROWTH_RATIO, self.defval)
        for t in self.h_table:
            if t != None:
                new_table.update(t[0],t[1])
        self.cells = new_table.cells
        self.h_table = new_table.h_table

    def lookup(self,key):
        '''
        Retrieve the value associated with the specified key in the hash table,
        or return the default value if it has not previously been inserted.
        '''
        h_0= self.hash_function(key)
        h = h_0
        while self.h_table[h] != None: #for non-empty elements in hashtable
            if self.h_table[h][0] == key: #if key matches
                return self.h_table[h][1] #return value associated with specified key
            h += 1
            h = h%self.cells
            if h == h_0:
                break
        return self.defval

    def update(self,key,val):
        '''
        Change the value associated with key "key" to value "val".
        If "key" is not currently present in the hash table,  insert it with
        value "val".
        '''
        if self.count/self.cells > TOO_FULL:
            self.rehash()

        h = self.hash_function(key)
        while self.h_table[h] != None:
            if self.h_table[h][0] == key:
                break
            h += 1
            h = h%self.cells
        if self.h_table[h] == None:
            self.count += 1
        self.h_table[h] = (key,val)