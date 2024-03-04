
from string import ascii_lowercase

def createTable(phrase):
    '''
    Given an input string, create a lowercase playfair table.  The
    table should include no spaces, no punctuation, no numbers, and 
    no Qs -- just the letters [a-p]+[r-z] in some order.  Note that 
    the input phrase may contain uppercase characters which should 
    be converted to lowercase.
    
    Input:   string:         a passphrase
    Output:  list of lists:  a ciphertable
    '''
    # Converts to lowercase and removes non-alpha chars and q
    phrase = phrase.lower()
    filtered_phrase = ''.join(filter(str.isalpha, phrase)).replace('q', '')
    seen = set()
    table = []

    # Adds unique characters from the phrase to the table, excluding q
    for char in filtered_phrase:
        if char not in seen:
            seen.add(char)
            table.append(char)
   
    # Adds the rest of the alphabet, excluding q
    for char in ascii_lowercase:
        if char not in seen and char != 'q':  
            seen.add(char)
            table.append(char)
   
    # Converts the flat list to a 5x5 list
    return [table[i:i+5] for i in range(0, 25, 5)]
    pass

def splitString(plaintext):
    '''
    Splits a string into a list of two-character pairs.  If the string
    has an odd length, append an 'x' as the last character.  As with
    the previous function, the bigrams should contain no spaces, no
    punctuation, no numbers, and no Qs.  Return the list of bigrams,
    each of which should be lowercase.
    
    Input:   string:  plaintext to be encrypted
    Output:  list:    collection of plaintext bigrams
    '''
   # Converts to lowercase
    lowercase_text = plaintext.lower()
    
    # Removes non-alphabetic characters and q
    filtered_text = ''.join(filter(lambda x: x.isalpha() and x != 'q', lowercase_text))
    
    # Appends x if the length of the string is odd
    if len(filtered_text) % 2 != 0:
        filtered_text += 'x'
    
    # Splits the string into bigrams
    bigrams = [filtered_text[i:i+2] for i in range(0, len(filtered_text), 2)]
    
    return bigrams
    pass

def playfairRuleOne(pair):
    '''
    If both letters in the pair are the same, replace the second
    letter with 'x' and return; unless the first letter is also
    'x', in which case replace the second letter with 'z'.
    
    You can assume that any input received by this function will 
    be two characters long and already converted to lowercase.
    
    After this function finishes running, no pair should contain two
    of the same character   
    
    Input:   string:  plaintext bigram
    Output:  string:  potentially modified bigram
    '''
    # Checks if both characters in the bigram are the same
    if pair[0] == pair[1]:
        # If the first letter is x, replace the second with z
        if pair[0] == 'x':
            return pair[0] + 'z'
        # Otherwise, replace the second letter with x
        else:
            return pair[0] + 'x'
    # If the characters are not the same, return the pair unchanged
    else:
        return pair
    pass

def playfairRuleTwo(pair, table):
    '''
    If the letters in the pair appear in the same row of the table, 
    replace them with the letters to their immediate right respectively
    (wrapping around to the left of a row if a letter in the original
    pair was on the right side of the row).  Return the new pair.
    
    You can assume that the pair input received by this function will 
    be two characters long and already converted to lowercase, and
    that the Playfair Table is valid.
    
    Input:   string:         potentially modified bigram
    Input:   list of lists:  ciphertable
    Output:  string:         potentially modified bigram
    '''
    # Finds the row and column of each character in the pair
    first_char_pos = next((row, col) for row, line in enumerate(table) for col, ch in enumerate(line) if ch == pair[0])
    second_char_pos = next((row, col) for row, line in enumerate(table) for col, ch in enumerate(line) if ch == pair[1])

    # Checks if both chars are in the same row
    if first_char_pos[0] == second_char_pos[0]:
        # Wraps around if the character is at the end of the row
        first_char_new_pos = (first_char_pos[0], (first_char_pos[1] + 1) % 5)
        second_char_new_pos = (second_char_pos[0], (second_char_pos[1] + 1) % 5)

        # Replaces chars with the ones to their immediate right
        new_pair = table[first_char_new_pos[0]][first_char_new_pos[1]] + table[second_char_new_pos[0]][second_char_new_pos[1]]
    else:
        # If chars are not on the same row, return the pair unchanged
        new_pair = pair

    return new_pair
    pass

def playfairRuleThree(pair, table):
    '''
    If the letters in the pair appear in the same column of the table, 
    replace them with the letters immediately below respectively
    (wrapping around to the top of a column if a letter in the original
    pair was at the bottom of the column).  Return the new pair.
    
    You can assume that the pair input received by this function will 
    be two characters long and already converted to lowercase, and
    that the Playfair Table is valid.
    
    Input:   string:         potentially modified bigram
    Input:   list of lists:  ciphertable
    Output:  string:         potentially modified bigram
    '''    
    #Transpose the table
    transposed_table = list(zip(*table))

    for col_index, col in enumerate(transposed_table):
       if pair[0] in col and pair[1] in col:
           idx1 = col.index(pair[0])
           idx2 = col.index(pair[1])
           # Determines the new chars by wrapping around to the top if necessary
           new_char1 = transposed_table[col_index][(idx1 + 1) % 5]
           new_char2 = transposed_table[col_index][(idx2 + 1) % 5]
           # Forms the new pair with the charss below the original chars
           new_pair = new_char1 + new_char2
           return new_pair

    return pair
    pass

def playfairRuleFour(pair, table):
    '''
    If the letters are not on the same row and not in the same column, 
    replace them with the letters on the same row respectively but in 
    the other pair of corners of the rectangle defined by the original 
    pair.  The order is important -- the first letter of the ciphertext
    pair is the one that lies on the same row as the first letter of 
    the plaintext pair.
    
    You can assume that the pair input received by this function will 
    be two characters long and already converted to lowercase, and
    that the Playfair Table is valid.  
    
    Input:   string:         potentially modified bigram
    Input:   list of lists:  ciphertable
    Output:  string:         potentially modified bigram
    '''
    # Finds the row and column of each letter in the pair
    pos = {char: (row_idx, row.index(char))
           for row_idx, row in enumerate(table)
           for char in row if char in pair}

    # Checks if both chars are in different rows and columns
    if pos[pair[0]][0] != pos[pair[1]][0] and pos[pair[0]][1] != pos[pair[1]][1]:
        # Swaps columns but keep rows the same
        new_pair = (table[pos[pair[0]][0]][pos[pair[1]][1]] +
                    table[pos[pair[1]][0]][pos[pair[0]][1]])
        return new_pair
    else:
        # If they are in the same row or column, return the pair unchanged
        return pair
    pass

def encrypt(pair, table):
    '''
    Given a character pair, run it through all four rules to yield
    the encrypted version!
    
    Input:   string:         plaintext bigram
    Input:   list of lists:  ciphertable
    Output:  string:         ciphertext bigram
    '''
    # Applies all the rules
    pair = playfairRuleOne(pair)
    pair = playfairRuleTwo(pair, table)
    pair = playfairRuleThree(pair, table)
    pair = playfairRuleFour(pair, table)
    
    return pair
    pass

def joinPairs(pairsList):
    '''
    Given a list of many encrypted pairs, join them all into the 
    final ciphertext string (and return that string)
    
    Input:   list:    collection of ciphertext bigrams
    Output:  string:  ciphertext
    '''
    # Joins the list of bigrams into a single string
    ciphertext = ''.join(pairsList)
    return ciphertext
    pass

def main():
    '''
    Example main() function; can be commented out when running your
    tests
    '''
 
    table = createTable("i am entering a pass phrase")
    splitMessage = splitString("this is a test message")
    pairsList = []

    print(table) # printed for debugging purposes
    
    for pair in splitMessage:
        # Note: encrypt() should call the four rules
        pairsList.append(encrypt(pair, table))
    cipherText = joinPairs(pairsList)    
    
    print(cipherText) #printed as the encrypted output
    #output will be hjntntirnpginprnpm

    # Calls all my test functions
    test_createTable_simple()
    test_createTable_allChars()
    test_createTable_spacesPunctuation()
    test_createTable_empty()
    
    test_splitString_evenLength()
    test_splitString_oddLength()
    test_splitString_SpacesPunctuation()
    test_splitString_Q()
    
    test_playfairRuleOne_sameCharacters()
    test_playfairRuleOne_firstCharacterX()
    test_playfairRuleOne_differentCharacters()
    test_playfairRuleOne_lastCharacterX()
    
    test_playfairRuleTwo_sameRowWrap()
    test_playfairRuleTwo_sameRowNoWrap()
    test_playfairRuleTwo_notSameRow()
    test_playfairRuleTwo_startEnd()
    
    test_playfairRuleThree_sameColumnWrap()
    test_playfairRuleThree_sameColumnNoWrap()
    test_playfairRuleThree_notSameColumn()
    test_playfairRuleThree_startEnd()
    
    test_playfairRuleFour_differentRowAndColumn()
    test_playfairRuleFour_otherCorners()
    test_playfairRuleFour_sameRow()
    test_playfairRuleFour_sameColumn()
    
    test_encrypt_gg()
    test_encrypt_ss()
    test_encrypt_en()
    test_encrypt_aa()
    
    test_joinPairs()
    test_joinPairs_empty_list()
    test_joinPairs_single_character()
    test_joinPairs_mixed_length()
###############################################################

# Here is where you will write your test case functions
    
# Below are the tests for createTable()
def test_createTable_simple():
    # Tests if a table is created correctly using simple
    passphrase = "simple"
    expected_table = [
        ['s', 'i', 'm', 'p', 'l'],
        ['e', 'a', 'b', 'c', 'd'],
        ['f', 'g', 'h', 'j', 'k'],
        ['n', 'o', 'r', 't', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    assert createTable(passphrase) == expected_table, "Test with simple passphrase failed."
    pass

def test_createTable_allChars():
    # Tests if a table is created correctly using the alphabet
    passphrase = "abcdefghijklmnopqrstuvwxyz"
    expected_table = [
        ['a', 'b', 'c', 'd', 'e'],
        ['f', 'g', 'h', 'i', 'j'],
        ['k', 'l', 'm', 'n', 'o'],
        ['p', 'r', 's', 't', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    assert createTable(passphrase) == expected_table, "Test with all letters passphrase failed."
    pass

def test_createTable_spacesPunctuation():
    # Tests if a table is created correctly using a sentence
    passphrase = "Hello, World! This is a Test."
    expected_table = [
        ['h', 'e', 'l', 'o', 'w'],
        ['r', 'd', 't', 'i', 's'],
        ['a', 'b', 'c', 'f', 'g'],
        ['j', 'k', 'm', 'n', 'p'],
        ['u', 'v', 'x', 'y', 'z']
    ]
    assert createTable(passphrase) == expected_table, "Test with uppercase, spaces, and punctuation failed."
    pass

def test_createTable_empty():
    # Tests if the passphrase is empty
    passphrase = ""
    expected_table = [
        ['a', 'b', 'c', 'd', 'e'],
        ['f', 'g', 'h', 'i', 'j'],
        ['k', 'l', 'm', 'n', 'o'],
        ['p', 'r', 's', 't', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    assert createTable(passphrase) == expected_table, "Test with empty passphrase failed."
    pass

# Below are the tests for splitString()
def test_splitString_evenLength():
    # Tests plaintext of even length without needing to append x
    assert splitString("plaintext") == ["pl", "ai", "nt", "ex", "tx"], "Failed on even length plaintext"
    pass

def test_splitString_oddLength():
    # Tests plaintext of odd length, rshould append x
    assert splitString("oddlength") == ["od", "dl", "en", "gt", "hx"], "Failed on odd length plaintext"
    pass

def test_splitString_SpacesPunctuation():
    # Tests plaintext with spaces and punctuation
    assert splitString("with spaces, and punctuation!") == ["wi", "th", "sp", "ac", "es", "an", "dp", "un", "ct", "ua", "ti", "on"], "Failed on plaintext with spaces and punctuation"
    pass

def test_splitString_Q():
    # Tests plaintext including q
    assert splitString("example with q") == ["ex", "am", "pl", "ew", "it", "hx"], "Failed on plaintext including 'q'"
    pass

# Below are the tests for playfairRuleOne()
def test_playfairRuleOne_sameCharacters():
    #Tests a pair with the same characters, should be x
    assert playfairRuleOne("aa") == "ax", "Failed on same characters"
    pass

def test_playfairRuleOne_firstCharacterX():
    # Tests a pair where both characters are x, should be z
    assert playfairRuleOne("xx") == "xz", "Failed on first character x"
    pass

def test_playfairRuleOne_differentCharacters():
    # Tests a pair with different characters, no change
    assert playfairRuleOne("ab") == "ab", "Failed on different characters"
    pass

def test_playfairRuleOne_lastCharacterX():
    # Tests when the last char is x, no change as well
    assert playfairRuleOne("ax") == "ax", "Failed on last character with 'a' and 'x'"
    pass

# Below are the tests for playfairRuleTwo()
def test_playfairRuleTwo_sameRowWrap():
    # Tests a pair in the same row where wrapping is necessary
    table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    pair = "en"
    expected_result = "ni"
    assert playfairRuleTwo(pair, table) == expected_result, "Test with bigram in the same row (with wrap) failed."
    pass

def test_playfairRuleTwo_sameRowNoWrap():
    # Tests a pair in the same row with no wrapping needed
    table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    pair = "am"
    expected_result = "me"
    assert playfairRuleTwo(pair, table) == expected_result, "Test with bigram in the same row (no wrap) failed."
    pass

def test_playfairRuleTwo_notSameRow():
    # Tests a pair not in the same row, original pair should be returned
    table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    pair = "af"
    expected_result = "af"
    assert playfairRuleTwo(pair, table) == expected_result, "Test with bigram not in the same row failed."
    pass

def test_playfairRuleTwo_startEnd():
    # Tests the start and end of the same row
   table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
   pair = "ps"
   expected_result = "st"
   assert playfairRuleTwo(pair, table) == expected_result, "Test with bigram in the same row (both characters at end) failed."
   pass

# Below are the tests for playfairRuleThree()
def test_playfairRuleThree_sameColumnWrap():
    # Tests a pair in the same column where wrapping is necessary
    table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    pair = "iv"
    expected_result = "ti"
    assert playfairRuleThree(pair, table) == expected_result, "Test with bigram in the same column (with wrap) failed."
    pass

def test_playfairRuleThree_sameColumnNoWrap():
    # Tests a pair in the same column with no wrapping 
    table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    pair = "th"
    expected_result = "hj"
    assert playfairRuleThree(pair, table) == expected_result, "Test with bigram in the same column (no wrap) failed."
    pass

def test_playfairRuleThree_notSameColumn():
    # Tests a pair not in the same column, orginal pair should be returned
    table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    pair = "ax"
    expected_result = "ax"
    assert playfairRuleThree(pair, table) == expected_result, "Test with bigram not in the same column failed."
    pass

def test_playfairRuleThree_startEnd():
    # Tests the top and bottom of the same column.
    table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    pair = "iv"
    expected_result = "ti"
    assert playfairRuleThree(pair, table) == expected_result, "Test with bigram in the same column (both characters at bottom) failed."
    pass

# Below are the tests for playfairRuleFour()
def test_playfairRuleFour_differentRowAndColumn():
    # Tests if fm returns cn
    table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    assert playfairRuleFour("fm", table) == "cn", "Failed on pair with different row and column"
    pass

def test_playfairRuleFour_otherCorners():
    # tests if as returns nr and jw returns kv
    table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    assert playfairRuleFour("as", table) == "nr", "Failed on pair with different row and column"
    assert playfairRuleFour("jw", table) == "kv", "Failed on pair with different row and column"
    pass

def test_playfairRuleFour_sameRow():
    # tests the some row tr, should be no change
    table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    assert playfairRuleFour("tr", table) == "tr", "Failed on pair in the same row"
    pass

def test_playfairRuleFour_sameColumn():
    # Tests the same column do, should be unchanged
   table = [
       ['i', 'a', 'm', 'e', 'n'],
       ['t', 'r', 'g', 'p', 's'],
       ['h', 'b', 'c', 'd', 'f'],
       ['j', 'k', 'l', 'o', 'u'],
       ['v', 'w', 'x', 'y', 'z']
   ]
   assert playfairRuleFour("do", table) == "do", "Failed on pair in the same column"
   pass

# Below are the tests for encyrpt()
def test_encrypt_gg():
    # Tests if gg retuns cm
    table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    bigram = "gg"
    expected_result = "cm"
    assert encrypt(bigram, table) == expected_result, "Encryption test failed for bigram 'gg'."
    pass

def test_encrypt_ss():
    # Tests if ss returns gz
    table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    bigram = "ss"
    expected_result = "gz"
    assert encrypt(bigram, table) == expected_result, "Encryption test failed for bigram 'ss'."
    pass

def test_encrypt_en():
    # Tests if en returns ni
    table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    bigram = "en"
    expected_result = "ni"
    assert encrypt(bigram, table) == expected_result, "Encryption test failed for bigram 'en'."
    pass

def test_encrypt_aa():
    # Tests if aa returns mw
    table = [
        ['i', 'a', 'm', 'e', 'n'],
        ['t', 'r', 'g', 'p', 's'],
        ['h', 'b', 'c', 'd', 'f'],
        ['j', 'k', 'l', 'o', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]
    bigram = "aa"
    expected_result = "mw"
    assert encrypt(bigram, table) == expected_result, "Encryption test failed for bigram 'aa'."
    pass

# Below are the tests for joinPairs()
def test_joinPairs():
   # Tests if a bigram returns correctly
    encrypted_bigrams = ['cm', 'ni', 'it', 'ar']
    expected_ciphertext = 'cmniitar'
    assert joinPairs(encrypted_bigrams) == expected_ciphertext, "Failed to correctly join encrypted bigrams into ciphertext."
    pass

def test_joinPairs_empty_list():
    # Tests if an empty list returns correctly
    encrypted_bigrams = []
    expected_ciphertext = ""
    actual_ciphertext = joinPairs(encrypted_bigrams)
    assert actual_ciphertext == expected_ciphertext, "Failed with empty list."
    pass

def test_joinPairs_single_character():
    # Tests if single characters will return correctly
    encrypted_bigrams = ['aa', 'bb', 'cc']
    expected_ciphertext = "aabbcc"
    actual_ciphertext = joinPairs(encrypted_bigrams)
    assert actual_ciphertext == expected_ciphertext, "Failed with single character."
    pass

def test_joinPairs_mixed_length():
    # Tests if a bigram with mixed char lengths returns correctly
    encrypted_bigrams = ['xyz', 'ab', 'cde', 'f']
    expected_ciphertext = "xyzabcdef"
    actual_ciphertext = joinPairs(encrypted_bigrams)
    assert actual_ciphertext == expected_ciphertext, f"Failed with mixed length bigrams. Expected '{expected_ciphertext}', got '{actual_ciphertext}'."
    pass

###############################################################    
    
if __name__ == "__main__":
    main()        