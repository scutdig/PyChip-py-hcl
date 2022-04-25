if __name__ == '__main__':

    path = './tmp/test'
    cnt = 0
    # with open(path, "a") as file:
    #     while file:
    #         line = file.readline().strip(' ')
    #         if line == '':
    #             break
    #         print(line)
    #         cnt = cnt + 1

    # f = open(path, "a")
    # inputs = [[2000, 230032]] * 4
    # print(inputs)
    # print(cnt)
    a = {'a': 'b', 'b': 'c'}
    if 'c' in a:
        print("XX")
        pass
    input_data = ['0111', '0011']
    input_data = [int(k, base=2) for k in input_data]
    print(input_data)


