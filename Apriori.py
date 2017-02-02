import sys
import itertools
candidate_itemsets = None
frequent_itemsets = None
input_file = None
output_file = None
num_item = 0
num_trans = 0
min_sup = 0
trans_list = []


def config(args = ["gene_data_binary.txt",0.5,"output.txt"]):
    global input_file,output_file
    global min_sup
    global num_trans, num_item
    global trans_list
    num_trans = 0
    # Get the input args
    input_file = args[0]
    min_sup = float(args[1])
    if 1 < min_sup < 0:
        raise Exception
    output_file = args[2]

    # initialize num_trans and num_item
    with open (input_file,'r') as f:
        for line in f:
            split_line = line.split()
            split_line = [int(i) for i in split_line]
            trans_list.append(split_line)
            num_trans += 1
            num_item = len(split_line)
    f.close()
    print("Input File " + input_file + "Output File" + output_file)
    print("Input configuration: " + str(num_item) + "items, " + str(num_trans) + "transactions, ")
    print("minsup = " + str(min_sup))


def assign(a_list,var):
    if len(a_list) == 0:
        a_list = var
    else:
        a_list.append(var)

def execute():
    try:
        curr_length = 1
        global candidate_itemsets, frequent_itemsets
        global num_item
        candidate_itemsets = [[]]
        frequent_itemsets = [[]]
        candidate_itemsets.append([])
        for i in range(num_item):
            cand = [i]
            candidate_itemsets[-1].append(cand)
        while len(candidate_itemsets[-1])> 0:
            frequent_itemsets.append([])
            gen_frequent_itemsets(curr_length)
            curr_length += 1
            candidate_itemsets.append([])
            if(curr_length>3):
                break
            if len(frequent_itemsets[curr_length-1]) != 0:
                gen_candidate_itemsets(curr_length)
    except:
        raise Exception


def count_support(itemset):
    count = 0
    for order in trans_list:
        flag = False
        for product in itemset:
            if order[product] == 0:
                flag = True
                break
        if flag is False:
            count += 1

    return count


# Choose frequent itemsets based on candidate itemsets
def gen_frequent_itemsets(curr_length):
    # Fill in here

    for i in candidate_itemsets[-1]:
        if count_support(i)/num_trans >= min_sup:
            frequent_itemsets[-1].append(i)



# Generate candidate itemsets based on previous frequent itemsets
def gen_candidate_itemsets(curr_length):
    # Fill in here



    if(curr_length ==2):
        temp = itertools.combinations(frequent_itemsets[-1], curr_length)
        for i in temp:
            candidate_itemsets[-1].append(i[0]+i[1])
    else:
        temp = itertools.combinations(frequent_itemsets[-2], curr_length)
        previous_set = [set(item) for item in frequent_itemsets[-1]]

        currentset = [set(i[0] + i[1] + i[2]) for i in temp]

        for i in currentset:
            subsets = [set(item) for item in itertools.combinations(i,2)]
            if all(item in previous_set for item in subsets):
                candidate_itemsets[-1].append(list(i))




def output_result():
    global output_file
    global frequent_itemsets
    global candidate_itemsets
    with open (output_file, 'w') as f:
        for i in range(1, len(frequent_itemsets)):
            f.write("Length " + str(i) + ":\n")
            candidate_itemsets[i].sort()
            f.write("Candidate: \n")
            for j in range(len(candidate_itemsets[i])):
                f.write(str(candidate_itemsets[i][j]) + " ")
            f.write("\n")
            f.write("Number of candidates: " + str(len(candidate_itemsets[i])) + "\n")
            frequent_itemsets[i].sort()
            f.write("Frequent Itemsets: \n")
            for j in frequent_itemsets[i]:
                f.write(str(j) + " ")
            f.write("\n")
            f.write("Number of frequent itemsets: " + str(len(frequent_itemsets[i])) + "\n")
    f.close()

def main():
    arg = sys.argv[1:]
    if len(arg) > 2:
        arg[1] = float(arg[1])
        config(arg)
    else:
        config()
    execute()
    output_result()
main()

