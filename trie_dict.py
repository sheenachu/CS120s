# CS121: Auto-completing keyboard using Tries
#
# usage: python trie_dict.py <dictionary filename>
#
# ESTELLE OSTRO & SHEENA CHU

import os
import sys
from sys import exit
import tty
import termios
import fcntl
import string

import trie_shell

def create_trie_node():
    '''
    Function returns node: dictionary
    '''
    node = {'count': 0, 'final' : False}
    return node

def add_word(word, trie):
    '''
    Function takes word and recursively adds to trie dictionary.
    If word is already in dictionary, update counts.
    If not, create new node.

    Input:
        word: string
        trie: dictionary
    '''
    trie['count'] += 1
    if word[0] in trie:
        if len(word) == 1:
            trie[word]['final'] = True
            trie[word]['count'] +=1
        else:
            add_word(word[1:], trie[word[0]])
    else:
        trie.update({ word[0] : create_trie_node()})
        if len(word) == 1:
            trie[word]['final'] = True
            trie[word]['count'] = 1
        else:
            add_word(word[1:], trie[word[0]])

def is_word(word, trie):
    '''
    Function recursively determines if word is in trie.
    
    Input:
        word: string
        trie: dictionary

    Returns:
        Boolean
    '''
    if word == '':
        return False
    if word[0] not in trie:
        return False
    if len(word) == 1:
        return trie[word]['final'] 
    return is_word(word[1:], trie[word[0]])

def locate_node(word, trie):
    '''
    Helper function that given a prefix, recursively determines the 
    node of the last letter.

    Input:
        word: string
        trie: dictionary 

    Returns:
        node: trie
    '''
    if word == '':
        return trie    
    if word[0] not in trie:
        return False
    if len(word) == 1:
        return trie[word]
    return locate_node(word[1:], trie[word[0]])

def num_completions(word, trie):
    '''
    Given a prefix, function recursively returns the number of possible
    completions.

    Input:
        word: string
        trie: dictionary

    Returns:
        integer    
    '''
    if word == '':
        return trie['count']
    if not locate_node(word, trie):
        return 0
    else:
        return locate_node(word, trie)['count']

def find_suffixes(node):
    '''
    Given a node, function recursively returns a list of suffixes.

    Input:
        node: trie

    Returns:
        list of strings
    '''
    if node['count'] == 1 and node['final']:
        return []
    else:
        rv = []
        for l in node: 
            if l != 'count' and l != 'final':
                suffix = l
                if node[l]['final']:
                    rv.append(suffix)
                next_letter = find_suffixes(node[l])
                for j in next_letter:
                    rv.append(l + j)
        return rv

def get_completions(word, trie):
    '''
    Given a word, function returns a list of possible suffixes.

    Input:
        word: string
        trie: dictionary

    Returns:
        list of strings
    '''
    node = locate_node(word, trie)
    if not node:
        return []
    completions = find_suffixes(node)
    if node['final']:
        completions.append('')
    return completions


if __name__ == "__main__":
    trie_shell.go("trie_dict")

