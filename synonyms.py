from synonyms_starter import *

filenames = ["text1.txt", "text2.txt"]
semantic_dict =  build_semantic_descriptors_from_files(filenames)

Result = run_similarity_test("test.txt", semantic_dict, cosine_similarity)

print ("Pass percentage is ", Result, "%")