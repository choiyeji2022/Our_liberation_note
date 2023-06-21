import os
from itertools import permutations
from pprint import pprint

import openai
from haversine import haversine
import time
from datetime import datetime
from bardapi import Bard


def total_distance(path):
    return sum(haversine(path[i], path[i + 1], unit="km") for i in range(len(path) - 1))


def search(data):
    title_li = []
    x_y_li = []
    location_li = []
    for item in data:
        title_li.append(item["title"])
        x_y_li.append((float(item["y"]), float(item["x"])))
        location_li.append((item["location"]))

    ordered_destinations = []
    remaining_points = list(range(len(x_y_li)))

    # 기차역이나 터미널 이름이 포함된 경우 해당 위치를 가장 처음에 배치
    for idx, item in enumerate(data):
        if "역" == item["title"][-1] or "터미널" in item["title"]:
            ordered_destinations.append(x_y_li[idx])
            remaining_points.remove(idx)

    # 첫 번째 좌표를 시작으로 가장 가까운 좌표 순서로 돌아다닙니다.
    current_point = remaining_points.pop(0)
    ordered_destinations.append(x_y_li[current_point])

    while remaining_points:
        closest_point = None
        closest_distance = float("inf")
        for point in remaining_points:
            distance = haversine(x_y_li[current_point], x_y_li[point])
            if distance < closest_distance:
                closest_distance = distance
                closest_point = point

        ordered_destinations.append(x_y_li[closest_point])
        current_point = closest_point
        remaining_points.remove(closest_point)

    # 목적지 리스트
    answer_li = [title_li[x_y_li.index(item)] for item in ordered_destinations]

    # 최종 경로의 총 거리 계산
    total_km = total_distance(ordered_destinations)

    openai_data = []

    for i in answer_li:
        idx = title_li.index(i)
        openai_data.append((i, location_li[idx]))

    data = {
        "title_list": answer_li,
        "total_km": total_km,
        "x_y_list": ordered_destinations,
    }
    # recommend = open_ai(openai_data)
    recommend = bard_ai(openai_data)
    data["answer"] = recommend
    return data


def bard_ai(location_li):
    token = "XQjGvFI-VaFDrPIx8PlyXRfsRnN319BMejkOWPAJvP3u7Tucgpky9hNEmLyPu9au_3yw2A."
    bard = Bard(token=token)

    start = datetime.now()

    q_str = ''

    for idx, location in enumerate(location_li):
        q_str += f'{location[1]}에 위치한 {location[0]} !!이 장소를 제외하고!! 이 주변에 추천 할 만한 장소 1곳 알려 주세요! 설명과 같이요!' \
                 f'이것에 대한 답변은 반드시 "{idx}번:" 형식을 지켜서 답변 해주세요!'

    answer_li = [bard.get_answer(f"{q_str} 반드시 가게 이름이랑 설명만 말해주세요!")['content']]

    li = []

    for string in answer_li[0].split('\n'):
        if ": " in string:
            li.append(string.split(": ", 1)[1])

    end = datetime.now()

    pprint(start)
    pprint(end)
    print(end-start)

    return li


def open_ai(location_li):
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    # 회원 정보 기준으로 role 추가?
    start = datetime.now()

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "추천해주세요!"},
    ]

    answer_li = []

    q_str = ''

    for idx, location in enumerate(location_li):
        q_str += f'{location[1]}에 위치한 {location[0]} 주변에 추천 할 만한 장소 1곳 알려 주세요! 설명과 같이요!' \
                 f'이것에 대한 답변은 반드시 "{idx}번:" 형식을 지켜서 답변 해주세요!'

    if location_li:
            messages.append(
                {
                    "role": "user",
                    "content": f"내가 이전에 했던 말은 잊고, 대답도 하지 말아줘!! 정보만 주면 됩니다. {q_str}"
                }
            )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
    answer_li.append(response.choices[0].message.content)

    end = datetime.now()

    li = []

    for string in answer_li[0].split('\n'):
        if ": " in string:
            li.append(string.split(": ", 1)[1])

    pprint(start)
    pprint(end)
    print(end-start)

    return li

