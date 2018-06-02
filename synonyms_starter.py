'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 18, 2015.
'''
def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    return sum_of_squares ** 0.5


def cosine_similarity(vec1, vec2):
    '''Return the cosine similarity between two vectors defined
    as a dictinoary'''
    # get the union of all keys in both the dictionaries
    union_keys = list(set(vec1.keys()) | set(vec2.keys())) 
    sumNumerator = 0 # get the value on the numerator of the equation
    for key in union_keys:
        val1 = 0
        val2 = 0
        if key in vec1:
            val1 = vec1[key]
        if key in vec2:
            val2 = vec2[key]
        # for each key add to numerator vec1[key]*vec2[key]
        sumNumerator = sumNumerator + (val1*val2) 
    denominator = norm(vec1) * norm(vec2)
    if (denominator == 0):
        # Means the norm is 0 for atleast one vector,
        # Either vec1 or vec2 is zero
        return -1
    else:
        # Return the cosine similarity
        return sumNumerator/denominator

def build_semantic_descriptors(sentences):
    semantic_dict = {}
    # create empty semantic dicts
    for sentence in sentences:
        for word in sentence:
            if word == '':
                continue
            word_dict = {}
            if word in semantic_dict:
                word_dict = semantic_dict[word]
            for otherword in sentence:
                if not (otherword == word and otherword != ''):
                    if otherword in word_dict:
                        word_dict[otherword] = word_dict[otherword] + 1
                    else:
                        word_dict[otherword] = 1
            semantic_dict[word] = word_dict
    return semantic_dict

def build_semantic_descriptors_from_files(filenames):
    sentences = []
    punctuation = [',','-','--',':',';','"',"'"]
    for filename in filenames:
        try:
            fileVar = open(filename, "r", encoding="utf-8")
        except IOError:
            print ("[ERROR] File not found")
            exit()
        fileContents = fileVar.read()
        fileContents = fileContents.replace('.','\n')
        fileContents = fileContents.replace('!', '\n')
        fileContents = fileContents.replace('?', '\n')
        fileContentslist = fileContents.split('\n')

        for sentence in fileContentslist:
            sentence = ''.join(c for c in sentence if c not in punctuation)
            sentence = sentence.strip()
            sentence = sentence.replace('\n','')
            sentencelist = sentence.split(" ")
            sentencelist = [word.lower() for word in sentencelist]
            sentences.append(sentencelist)
        fileVar.close()
    semantic_dict = build_semantic_descriptors(sentences)
    return semantic_dict

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max_similarity = -1
    answer = ""
    for choice in choices:
        if word in semantic_descriptors:
            if choice in semantic_descriptors:
                similarity = similarity_fn(semantic_descriptors[choice], semantic_descriptors[word])
                if similarity > max_similarity:
                    answer = choice
                    max_similarity = similarity
    return answer


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    numwords = 0
    numcorrect = 0
    try:
        fileVar = open(filename, "r", encoding ="utf-8")
    except IOError:
        print ("[ERROR] Test file not found")
        exit()
    for line in fileVar:
        line = line.strip('\n')
        question = line.split(' ')
        answer = question[1]
        word = question[0]
        choices = question[2:]
        if word in semantic_descriptors:
            answerComp = most_similar_word(word, choices, semantic_descriptors, similarity_fn)
            if answer == answerComp:
                numcorrect = numcorrect + 1
            numwords = numwords + 1
    fileVar.close()
    return (numcorrect/numwords * 100)