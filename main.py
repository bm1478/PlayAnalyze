import os
from make_word_cloud import preprocess_for_message, make_cloud


def load_chats():
    chat_data = []
    path = "./chat_data"
    for file in os.listdir(path):
        f = open(os.path.join(path, file), 'r', encoding='UTF8')
        lines = f.readlines()
        f.close()
        title = ''
        data = []
        for idx, line in enumerate(lines):
            if idx == len(lines) - 1:
                clean_line = line
            else:
                clean_line = line[:-1]
            if idx == 0:
                title = clean_line[:-11]
            elif idx >= 3:
                data.append(clean_line)
        chat_data.append({"title": title, "data": data})
    return chat_data


if __name__ == '__main__':
    chat_data = load_chats()
    for one_data in chat_data:
        print(one_data['title'])
        extract_info = preprocess_for_message(one_data['data'])
        # 50개 word count
        word_cloud = make_cloud(50, one_data['title'], extract_info['content'])
