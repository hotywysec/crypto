 # 5*5的矩阵, I与J同, 注意是大写的，也可以自己定义矩阵(不要重复)
SECRET_LIST = [["M","O","N","A","R"],
               ["C","H","Y","B","D"],
               ["E","F","G","J","K"],
               ["L","P","Q","S","T"],
               ["U","V","W","X","Z"]]

#加密
def encryption(clear_text):
    #去除空格与逗号
    clear_text = clear_text.replace(" ", "").replace(",", "")
    list_clear_text = list(clear_text)   #字符串转化为列表
    print(list_clear_text)
    #两个字母为一组，在重复的明文字母中插入填充字母Z
    flag = False
    while not flag:
        list_clear_text = deal_repeat(list_clear_text)[0]
        flag = deal_repeat(list_clear_text)[1]
    print(list_clear_text)
    #若分组到最后一组时只有一个字母，则补充字母Z
    if len(list_clear_text) % 2 == 1:
        list_clear_text.append("Z")
    print(list_clear_text)
    #加密的核心代码
    encryption_list = core_encryption(list_clear_text)  #返回密文列表
    return ("").join(encryption_list)


#处理一组字线是重复明文字母
def deal_repeat(list_clear_text):
    count = 0    #计算列表中有多少组是不同的
    flag = False
    for i in range(len(list_clear_text)):
        if(i % 2 == 1):   #列表中的第d奇数个
            if(list_clear_text[i] == list_clear_text[i-1]):   #第奇数个与前一个(偶数)是否相同
                list_clear_text.insert(i, "Z")   #有重复明文字母则插入一个填充字母Z 并且退出循环
                break
            if (list_clear_text[i] != list_clear_text[i - 1]):
                count += 1
                if count == int(len(list_clear_text) / 2):
                    flag = True

    return list_clear_text,flag   #返回的是元组 (list_clear_text, flag)

#获得字母在矩阵中的行与列
def get_rows_columns(alphabet):
    if alphabet == "I":  #矩阵中只有25个字母，I同J
        alphabet = "J"
    for i in range(len(SECRET_LIST)):
        for j in range(len(SECRET_LIST[i])):
            if (SECRET_LIST[i][j] == alphabet):
                return i,j


# 加密的核心代码,先找出每一组字母在5*5矩阵 的行与列
def core_encryption(list_clear_text):
    encryption_list = []
    for i in range(len(list_clear_text)):
        if(i % 2 == 0):
            x = list_clear_text[i].upper()   #将一组字母转为大写，因为矩阵的字母全是大写的
            y = list_clear_text[i+1].upper()
            x_tuple = get_rows_columns(x)   #返回元组形式
            y_tuple = get_rows_columns(y)
            # print(x_tuple)
            # print(y_tuple)
            if x_tuple[0] == y_tuple[0]:   #若明文字母在矩阵中同行
                x_secret = SECRET_LIST[x_tuple[0]][(x_tuple[1] + 1) % 5]
                y_secret = SECRET_LIST[y_tuple[0]][(y_tuple[1] + 1) % 5]
            elif x_tuple[1] == y_tuple[1]:  #若明文字母在矩阵中同列
                x_secret = SECRET_LIST[(x_tuple[0] + 1) % 5][x_tuple[1]]
                y_secret = SECRET_LIST[(y_tuple[0] + 1) % 5][y_tuple[1]]
            else:      #若明文字母在矩阵中不同行不同列
                x_secret = SECRET_LIST[x_tuple[0]][y_tuple[1]]
                y_secret = SECRET_LIST[y_tuple[0]][x_tuple[1]]
            encryption_list.append(x_secret)
            encryption_list.append(y_secret)
    return encryption_list      #返回字母加密后的列表


#解密核心代码，返回解密后的明文列表,密文肯定是偶数的，每一组密文字母也肯定是不同的
def core_decryption(list_cipher_text):
    decryption_list = []
    for i in range(len(list_cipher_text)):
        if(i % 2 == 0):
            x = list_cipher_text[i]
            y = list_cipher_text[i+1]
            x_tuple = get_rows_columns(x)   #返回元组形式
            y_tuple = get_rows_columns(y)
            if x_tuple[0] == y_tuple[0]:   #若密文字母在矩阵中同行
                x_clear = SECRET_LIST[x_tuple[0]][(x_tuple[1] - 1) % 5]
                y_clear = SECRET_LIST[y_tuple[0]][(y_tuple[1] - 1) % 5]
            elif x_tuple[1] == y_tuple[1]:  #若密文字母在矩阵中同列
                x_clear = SECRET_LIST[(x_tuple[0] - 1) % 5][x_tuple[1]]
                y_clear = SECRET_LIST[(y_tuple[0] - 1) % 5][y_tuple[1]]
            else:      #若密文字母在矩阵中不同行不同列
                x_clear = SECRET_LIST[x_tuple[0]][y_tuple[1]]
                y_clear = SECRET_LIST[y_tuple[0]][x_tuple[1]]
            decryption_list.append(x_clear)
            decryption_list.append(y_clear)
    return decryption_list       #返回解密后的明文列表(需进一步处理,eg:去掉Z)

#解密
def decryption(cipher_text):
    cipher_text = cipher_text.replace(" ", "").replace(",", "")
    list_cipher_text = list(cipher_text.strip())   #将密文转化为列表
    decryption_list = core_decryption(list_cipher_text)   #调用函数
    if decryption_list[-1] == "Z":      #若列表最后一个元素是Z，则删除
        decryption_list.pop(-1)
    #找出列表应该删除的下标
    delete_list = []
    for i in range(len(decryption_list)):
        if i % 2 == 0:          #第偶数个
            #不越界
            if i+2 < len(decryption_list) and \
                            decryption_list[i] == decryption_list[i+2] and decryption_list[i+1] == "Z":
                delete_list.append(i+1)
                #decryption_list.pop(i+1)
    delete_list.reverse()     #反序，从后往前删除，每次删完下标就不会再变化，我真是太聪明了！
    for i in delete_list:
        print(i)
        decryption_list.pop(i)
    return "".join(decryption_list)



if __name__ == "__main__":
    while True:
        choice = input("Please input E for encryption or D for decryption：")
        if choice.strip() != "E" and choice.strip() != "D":
            print("Input Error")
        #加密
        if choice.strip() == "E":
            clear_text = input("请输入明文:")
            print("加密成功！密文:%s" % encryption(clear_text))
        #解密
        if choice.strip() == "D":
            cipher_text = input("请输入密文(大写字母/偶数):")
            print("解密成功！明文:%s" % decryption(cipher_text))
