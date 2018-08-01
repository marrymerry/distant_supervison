import json
import numpy as np
import matplotlib.pyplot as plt
import re
import jieba.posseg as pseg


def split_file(file, limit):
    result_list = []
    file_count = 0
    with open(file) as f:
        for line in f:
            result_list.append(line)
            if len(result_list) < limit:
                continue
            file_name = "data/split/"+str(file_count)+".txt"
            with open(file_name, 'w') as file:
                for result in result_list[:-1]:
                    file.write(result)
                file.write(result_list[-1].strip())
                result_list = []
                file_count += 1
    if result_list:
        file_name = "data/split/"+str(file_count)+".txt"
        with open(file_name, 'w') as file:
            for result in result_list:
                file.write(result)


def json_content_each_txt(json_path, save_path):
    # 从json文件读取里面的文本内容‘content’,每个文本内容单独存放在一个文件中
    pos = 0
    with open(json_path) as load_json:
        while 1:
            line = load_json.readline()
            if not line:
                break
            load_dict = json.loads(line)
            # print(type(load_dict.get('content')))
            if load_dict.get('content') is not None and load_dict.get('title').find("产业链") >= 0:
                with open(save_path + str(pos) + ".txt", "w") as save_file:
                    save_file.write(load_dict.get('title'))
                    save_file.write('\n')
                    for string in load_dict.get('content'):
                        save_file.write(string)
                        save_file.write('\n')
            pos += 1


def json_content_all_txt(json_path, save_path):
    # 从json文件读取里面的文本内容‘content’,所有文本内容存放在一个文件中
    save_file = open(save_path, "w", encoding='UTF-8')
    with open(json_path, encoding='UTF-8') as load_json:
        while 1:
            line = load_json.readline()
            if not line:
                break
            load_dict = json.loads(line)
            # print(type(load_dict.get('content')))
            # if load_dict.get('content') is not None and load_dict.get('title').find("产业链") >= 0:
                # save_file.write(load_dict.get('title'))
                # save_file.write('\n')
            if load_dict.get('content') is not None:
                for string in load_dict.get('content'):
                    save_file.write(string)
                    save_file.write('\n')


def split_paragraph_short(file_path, save_path):
    # 从file_path中读取按段落划分的文本改为按句号划分的文本，并且保存在save_path中
    paragraph_file = open(file_path, encoding='UTF-8')
    save_file = open(save_path, "w", encoding='UTF-8')
    for line in paragraph_file.readlines():
        if line.find("。") > 1 and line.find("。") != len(line)-2:
            result = line.split("。")
            for string in result:
                if len(string) > 5:
                    save_file.write(string)
                    if string.find('\n') < 0:
                        save_file.write('\n')
        else:
            save_file.write(line)


def file_text_length(file_path):
    # 从file_path中读取文件，打印该文件所有行的长度平均值、中位数、最小值、最大值
    list_length = []
    short_file = open(file_path, "r")
    for line in short_file.readlines():
        list_length.append(len(line))
    print("平均值：")
    print(np.mean(list_length))
    print("中位数：")
    print(np.median(list_length))
    print("最小值：")
    print(np.min(list_length))
    print("最大值：")
    print(np.max(list_length))
    plt.hist(list_length, bins=10)
    plt.show()


def text_process_min(file_path, save_path, min_length):
    # 从file_path中读取每一行，如果长度大于200则按分号分割，去除长度低于min_length的行，保存剩下的文本到save_path中
    read_file = open(file_path, "r")
    save_toFile = open(save_path, "w")
    for line in read_file.readlines():
        if len(line) > 200 and (line.find("；") or line.find(";")):
            result = re.split('[;；]', line)
            for string in result:
                if len(string) > min_length:
                    save_toFile.write(string)
                    if string.find('\n') < 0:
                        save_toFile.write('\n')
        else:
            if len(line) > min_length:
                save_toFile.write(line)


def text_process_min_max(file_path, save_path, min_length, max_length):
    # 从file_path中读取每一行，如果长度大于max_length则进行分号分割；
    # 去除长度低于min_length的行和长度超过max_length的句子，保存剩下的文本到save_path中
    print("\n min_length: " + str(min_length) + '\n')
    print("\n max_length: " + str(max_length) + '\n')
    read_file = open(file_path, encoding='UTF-8')
    save_toFile = open(save_path, "w",encoding='UTF-8')
    for line in read_file.readlines():
        if len(line) > max_length and (line.find("；") or line.find(";")):
            result = re.split('[;；]', line)
            for string in result:
                if max_length > len(string.strip()) > min_length:
                    save_toFile.write(string.strip())
                    save_toFile.write('\n')
        else:
            if min_length < len(line.strip()) < max_length:
                save_toFile.write(line.strip())
                save_toFile.write('\n')


def find_long_text(file_path, limit_length):
    # 从file_path中读取每一行，打印长度超过limit_length的文本，并统计超过的个数
    num = 0
    read_file = open(file_path, "r")
    print("\n line exceeding the limit_length at " + str(limit_length) + ":\n")
    for line in read_file.readlines():
        if len(line) > limit_length:
            print(len(line))
            print(line)
            num += 1
    print("the num is " + str(num))


def jieba_exaction(file_path, save_path):
    # 读取文件的每一行，保存每一行及分词结果到save_path中，每一行以制表符分割
    read_file = open(file_path)
    save_file = open(save_path, "w")
    for line_sentence in read_file.readlines():
        res_list = []
        words = pseg.cut(line_sentence)
        for word, flag in words:
            if flag == 'n' and not word in res_list:
                res_list.append(word)
        for word in res_list:
            save_file.write(word + '\t')
        save_file.write('\n')


def text_process_final(file_all_path, file_short_save_path, min_length, max_length):
    paragraph_file = open(file_all_path, encoding='UTF-8')
    save_file = open(file_short_save_path, "w", encoding='UTF-8')
    for line in paragraph_file.readlines():
        if len(line)> min_length and 1 < line.find("。") < len(line)-2:
            sentences = line.split("。")
            for sentence in sentences:
                if len(sentence) > max_length and (sentence.find("；") or line.find(";")):
                    result = re.split('[;；]', line)
                    for string in result:
                        if max_length > len(string.strip()) > min_length:
                            save_file.write(string.strip())
                            save_file.write('\n')
                else:
                    if min_length < len(sentence.strip()) < max_length:
                        save_file.write(sentence.strip())
                        save_file.write('\n')
        else:
            if min_length < len(line.strip()) < max_length:
                save_file.write(line.strip())
                save_file.write('\n')


if __name__ == "__main__":
    json_path = "data/new_car/new_car_Tsh_0725.json"
    # 将json文件中的文本内容取出，保存路径
    file_all = "data/new_car/new_car_tsh_result.txt"
    # 将所有文本内容（此时是段落），按句号分割成句子后的保存路径"图表3:国家从2016 年起开始严查骗补行为 (7)
    # "
    file_short_paragraph = "data/new_car/new_car_chyxx_short.txt"
    # 将所有的句子，排除过长和过短后，保存路径
    file_short_sentence = "data/new_car/new_car_chyxx_short3.txt"
    # json_content_all_txt(json_path, file_all)
    # split_paragraph_short(file_all, file_short_paragraph)
    text_process_final(file_all, file_short_sentence, 80, 100)
    # jieba_exaction(file_name3, sentence_word)

