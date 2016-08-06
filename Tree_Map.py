# CS122 W'16: treemaps
# SHEENA CHU

import Deposit_Tree
import Color_Key
import Chi_Canvas
import sys


MIN_RECT_SIDE=0.01
MIN_RECT_SIDE_FOR_TEXT=0.03
X_SCALE_FACTOR=12
Y_SCALE_FACTOR=10

def compute_weight(t):
    '''
    Input:
        t: tree

    Recursive function computes the weight for each node of a given tree
    '''

    if t.is_leaf_node():
        t.set_weight(t.branch.deposits)
        return t.weight
    else:
        weight = 0
        for node in t.children:
            weight += compute_weight(node)
        t.set_weight(weight)
        return weight

def institution_set(t, cls_set):
    '''
    Inputs:
        t: tree
        cls_set: set

    Recursive function creates set of institution classes
    '''

    for node in t.children:
        if node.is_leaf_node():
            if node.branch.cls not in cls_set:
                cls_set.add(node.branch.cls)
        else:
            institution_set(node, cls_set)

def color_key(cls_set, c):
    '''
    Inputs:
        cls_set: set
        c: canvas

    Function assigns a color for each institution and draws a color key on the canvas
    '''
    ck = Color_Key.Color_Key(cls_set)
    ck.draw_color_key(c,.8,0,1.0,.30)
    return ck

def create_tree_map(c, ck, t, x0, y0, x1, y1, axis):
    '''
    Inputs:
        c: canvas 
        ck: color key
        t: tree
        (x0, y0): coordinates of top left corner
        (x1, y1): coordinates of bottom right corner
        axis: Boolean -- True (rectangle is partitioned from left to right) or False (rectangle
            is partitioned from up to down)

    Recursive function creates a treemap
    '''

#base case
    if t.is_leaf_node():
        c.draw_rectangle(x0, y0, x1, y1, fill = ck.get_color(t.branch.cls),outline = "black")
        if abs(x1-x0) and abs(y1-y0) > MIN_RECT_SIDE_FOR_TEXT:
            txt = t.branch.label
            if abs(y1-y0) <= abs(x1-x0):
                c.draw_text(x0 + abs(x1-x0)/2, y0 + abs(y1-y0)/2, (x1 - x0), txt, fg = "black")
            else:
                c.draw_text_vertical(x0 + abs(x1-x0)/2, y0 + abs(y1-y0)/2, (y1-y0), txt, fg="black")
    
#recursive case
    else:
        x_distance = abs(x1-x0)
        y_distance = abs(y1-y0)
        if x_distance < MIN_RECT_SIDE or y_distance < MIN_RECT_SIDE:
            c.draw_rectangle(x0, y0, x1, y1, fill=ck.get_color("Default"), outline="black")
        else:
            for node in t.children:
                relative_weight = node.weight / t.weight
                if axis:
                  width = x_distance * relative_weight
                  create_tree_map(c, ck, node, x0, y0, x0 + width, y1, False)
                  x0 += width
                else:
                  height = y_distance * relative_weight
                  create_tree_map(c, ck, node, x0, y0, x1, y0 + height, True)
                  y0 += height
                  
def draw_tree_map(c, t):
    '''
    Inputs:
        c: canvas
        t: deposit tree

    Function draws a treemap
    '''
    cls_set = set()
    compute_weight(t)
    institution_set(t, cls_set)
    ck = color_key(cls_set, c)
    create_tree_map(c, ck, t, 0.0, 0.0, 0.8, 1.0, True)


def test_subtree(input_filename, path, output_filename):
    ''' 
    Generate a treemap for a specific subtree of the tree
    specified in the input file.  The subtree is specified by
    a list of labels for nodes along the path.  

    If output_filename is None, the resulting treemap is displayed (shown),
    otherwise it is saved in the specified output file.
        
    sample use:
        test_subtree("CPA.csv", ['PA', 'Washington', 'Charleroi', 'SB'], None)

    generates a treemap for the savings banks example from the
    description and displays it.
    '''

    c = Chi_Canvas.Chi_Canvas(X_SCALE_FACTOR, Y_SCALE_FACTOR)
    t = Deposit_Tree.Deposit_Tree(filename=input_filename)
    if len(path) > 0:
        t = t.get_subtree(path)
        if t is None:
            print("Could not build subtree")
            return
    draw_tree_map(c, t)
    if output_filename == None:
        c.show()
    else:
        c.savefig(output_filename)


def test_savings_banks(output_filename):
    '''
    generates a treemap for the savings banks example in the description
    '''
    test_subtree("CPA.csv", ['PA', 'Washington', 'Charleroi', 'SB'],
                 output_filename)


def test_charleroi(output_filename):
    '''
    generates a treemap for all institutions in Charleroi
    (one of the examples in the description)
    '''
    test_subtree("CPA.csv", ['PA', "Washington", 'Charleroi'], output_filename)


def test_greater_charleroi(output_filename):
    '''
    generates a treemap for banks in and around Charleroi
    '''
    test_subtree("CPA.csv", [], output_filename)


def go(input_filename, output_filename):
    '''
    draw a treemap for the deposit data in the input file
    and save the result in the output file (or display it,
    if output_filename is None).
    '''
    test_subtree(input_filename, [], output_filename)


if __name__=="__main__":
    num_args = len(sys.argv)

    if num_args < 2 or num_args > 4:
        print("usage: python3 " + sys.argv[0] + " [savings-banks | charleroi | greater-charleroi | <a file name>] [output filename]")
        sys.exit(0)

    if num_args == 3:
        output_filename = sys.argv[2]
    else:
        output_filename = None

    if sys.argv[1] == "savings-banks":
        test_savings_banks(output_filename)
    elif sys.argv[1] == "charleroi":
        test_charleroi(output_filename)
    elif sys.argv[1] == "greater-charleroi":
        test_greater_charleroi(output_filename)
    else:
        go(sys.argv[1], output_filename)



            
    
    
        
