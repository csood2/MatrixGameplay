import itertools
from itertools import permutations
import copy

def main():
    # first = [0,1,2,3,4,5,6,7,8,9,10,11]
    # second = [0,1,2,3,4,5,6,7,8,9,10,11]
    # sums = []
    #
    # for i in first:
    #     for j in second:
    #         for k in second:
    #             sums.append(i+j+k)
    # print(sums)
    #
    # odd_count = 0
    # even_count = 0
    # other = 0
    # for x in sums:
    #     if (x%2) == 0:
    #         even_count+=1
    #         continue
    #
    #     if (x%2) == 1:
    #         odd_count+=1
    #         continue
    #
    #     other+=1
    #
    # print("even:")
    # print(even_count)
    # print("odd")
    # print(odd_count)
    # print("other:")
    # print(other)

    first = [0,1,2,3,4,5,6,7]

    a=list(itertools.combinations(first,4))
    #print(len(a))
    output = []

    for x in a:
        chosen2_combinations = list(itertools.combinations(x,3))
        #print(x)
        #print(list(chosen2_combinations))


        for y in chosen2_combinations:
            this_result = [0,0,0,0,0,0,0,0]
            chosen_2_copy = copy.deepcopy(list(x))
            for comb_elements in y:
                chosen_2_copy.remove(comb_elements)

                this_result[comb_elements]= 1

            for copy_elem in chosen_2_copy:

                this_result[copy_elem]= 2


            output.append(this_result)



    for a in output:
        #print(len(output))
        print(a)

    print(len(output))
    # L = [1, 2, 3, 4]
    # x= [",".join(map(str, comb)) for comb in itertools.combinations(L, 3)]
    # print(x)


if __name__ == "__main__":
    main()
