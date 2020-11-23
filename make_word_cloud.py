from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
import re
import pandas as pd
import datetime
import os


def preprocess_for_message(data):
    chat_list = []
    cur_date = datetime.datetime.today()
    for one_line in data:
        # date
        if one_line.startswith("---------------"):
            p = list(map(int, re.findall("\d+", one_line)))
            cur_date = datetime.date(p[0], p[1], p[2])
        else:
            msg_pattern = re.compile("\[([\S\s]+)\] \[(오전|오후) ([0-9:\s]+)\] ([^\n]+)")
            msg_pattern_result = msg_pattern.findall(one_line)
            # 채팅 시작
            if len(msg_pattern_result) > 0:
                info = msg_pattern_result[0]
                name = info[0]
                if info[1] == '오전':
                    time_str = info[2] + ' AM'
                else:
                    time_str = info[2] + ' PM'
                time_str = cur_date.strftime('%Y %m %d ') + time_str
                time = datetime.datetime.strptime(time_str, '%Y %m %d %I:%M %p')
                content = info[3]
                if content != "사진":
                    chat_list.append([time, name, content])
            # 채팅 내용 추가
            else:
                # 시스템 메시지 제외
                in_msg_flag = one_line.endswith("님을 초대하였습니다.")
                out_msg_flag = one_line.endswith("님이 나갔습니다.")
                if in_msg_flag is True or out_msg_flag is True:
                    continue
                # 엔터 구분 메시지 붙여주기
                cur_chat = chat_list[-1][-1]
                new_chat = cur_chat + "\n" + one_line
                chat_list[-1][-1] = new_chat

    df = pd.DataFrame(chat_list, columns=['time', 'name', 'content'])
    return df


def make_cloud(word_count, chat_name, chat_data):
    okt = Okt()

    # 형태소 분석
    sentences_tag = []
    for sentence in chat_data:
        morph = okt.pos(sentence)
        sentences_tag.append(morph)

    # 명사, 형용사만
    noun_adj_list = []
    for one_sentence in sentences_tag:
        for word, tag in one_sentence:
            if tag in ['Noun', 'Adjective'] and ("내" not in word) and \
                    ("너" not in word) and ("나" not in word) and \
                    ("수" not in word):
                noun_adj_list.append(word)

    # 형태소별 count
    counts = Counter(noun_adj_list)
    # default 50
    tags = counts.most_common(word_count)

    # word cloud 생성
    wc = WordCloud(font_path='./font/NanumGothic.ttf', background_color='black', colormap='Accent_r', width=800,
                   height=600)
    cloud = wc.generate_from_frequencies(dict(tags))
    fig = plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()
    save_path = os.path.join(os.path.abspath(__file__), '../word_cloud_img')
    file_name = chat_name + '.png'
    fig.savefig(os.path.join(save_path, file_name))
