# CS121 A'15: Benford's Law
#
# Functions for evaluating data using Benford's Law.
#
# Sheena Chu

import math

def extract_leading_digits_single(amount, num_digits):
    '''
    Given a positive floating point number and a number of digits,
    extract the specified number of leading digits

    Inputs:
        amount: float
        num_digits: the number of leading digits to extract from the
            amount.

    Returns:
        integer
    '''
    assert(num_digits > 0)
    assert(amount > 0)
    x = math.trunc(10**(-math.floor(math.log10(amount))+num_digits - 1) * amount)
    return int(x)


def extract_leading_digits_from_list(dollar_amounts, num_digits):
    '''
    Given a list of strings that represent positive amounts
    in dollars and a number of digits extract the specified
    number of leading digits.

    Inputs:
        dollar_amounts = list of strings
        num_digits = the number of leading digits
            to extract from the amount


    Returns: l1 = list of integers

    '''
    assert(num_digits > 0)
    l1=[]
    for i in dollar_amounts:
        amount = float("".join(i).strip('$'))
        x= extract_leading_digits_single(amount, num_digits)
        l1.append(int(x))

    return l1


def compute_expected_benford_dist(num_digits):
    '''
    Given the number of digits as an argument
    return a list of floats with the expected distribution.

    Inputs:
        num_digits = the number of leading digits

    Returns: l1 = list of floats

    '''

    expected=[]
    for N in range(10**(num_digits-1),10**num_digits):
        x = math.log10(1+1/N)
        expected.append(x)

    return expected


def compute_benford_dist(dollar_amounts, num_digits):
    '''
    Given a non-empty list of strings that represent
    positive amounts in dollars and a number of digits
    as arguments compute the Benford distribution
    of the given data for the specified number of digits. 
    
    Inputs:
        dollar_amounts = list of strings
        num_digits = the number of leading digits
            to extract from the amount

    Returns: l1 = list of floats

    '''

    assert(num_digits > 0)
    l2=[]
    for i in dollar_amounts:
        amount = float("".join(i).strip('$'))
        x= extract_leading_digits_single(amount, num_digits)
        l2.append(int(x))
    N = 10**num_digits-(10**(num_digits-1))
    N1 = 10**(num_digits-1)
    count_list=[0]*N
    for i in l2:
        for j  in range(10**(num_digits-1),10**num_digits):
            if i == j:
                k = count_list[i-N1]
                k = k + 1
                count_list[i-N1]= k
    n = len(dollar_amounts)
    actual = [x/n for x in count_list]   

    return actual


def compute_benford_MAD(dollar_amounts, num_digits):
    '''
    Given a non-empty list of strings that represent
    positive amounts in dollars and a number of digits as arguments.
    Complete the function compute_benford_MAD to find
    mean absolute difference (MAD) of the expected distribution
    and the actual distribution for a given set of data
    and specified number of digits as our quantitative measure.

    Inputs:
    dollar_amounts = list of strings
    num_digits = the number of leading digits
    to extract from the amount

    Returns:
    MAD float

    '''

    MAD = []
    actual = compute_benford_dist(dollar_amounts, num_digits)
    expected = compute_expected_benford_dist(num_digits)
    N = len(expected)
    for i in range(0, N):
        for j in range(0,N):
            if i == j:
                x = 1/N*abs(expected[i]-actual[j])
                MAD.append(x)
    MAD = sum(MAD)

    return MAD