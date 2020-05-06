if __name__ == '__main__':

    input = [2, -6]

    ws1 = [[0.17, 1.2], [-0.97, 1.1], [-0.77, -0.16], [-0.94, -0.19]]

    output1 = [input[0] * w[0] + input[1] * w[1] for w in ws1]
    # input2 = [i if i > 0 else 0 for i in output1]
    input2 = output1

    ws2 = [[1.1, -0.3, 0.79, .66], [-.76, 1.5, -.25, -.73]]

    output2 = [input2[0] * w[0] + input2[1] * w[1] + input2[2] * w[2] + input2[3] * w[3] for w in ws2]
    input3 = [i if i > 0 else 0 for i in output2]

    ws3 = [1.4, -2.0]
    output3 = ws3[0] * input3[0] + ws3[1] * input3[1]
    print(output2)

    # print((sum(a * b for a, b in zip([1.2, 1.1, -0.16, -0.19], [x2 for _ in range(4)]))))
