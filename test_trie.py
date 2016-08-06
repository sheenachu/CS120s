from trie_dict import create_trie_node, add_word, is_word, num_completions, get_completions

t = create_trie_node()
add_word("a", t)
add_word("an", t) 
add_word("and", t)
add_word("are", t) 
add_word("bee", t)

# Write your tests here

# Test create_trie_node() and add_word():
assert t == {'a': {'count': 4, 'final': True, 'n': {'count': 2, 'd': 
            {'count': 1, 'final': True}, 'final': True}, 'r': {'count': 
            1, 'e': {'count': 1, 'final': True}, 'final': False}},
            'b': {'count': 1, 'e': {'count': 1, 'e': {'count': 1, 'final': 
            True}, 'final': False}, 'final': False}, 'count': 5, 'final': False}

# Test is_word():
assert is_word("bee", t)

# Test num_completions:
assert num_completions('', t) == 5
assert num_completions('a', t) == 4
assert num_completions('b', t) == 1
assert num_completions('an', t) == 2

# Test get_completions():
assert sorted(get_completions('', t)) == ['a', 'an', 'and', 'are', 'bee']
assert sorted(get_completions('an', t)) == ['', 'd']
assert sorted(get_completions('b', t)) == ['ee']

print('YAY!  YOU PASSED EVERYTHING!')
