from itertools import permutations
from pprint import pprint

from haversine import haversine

import openai
import os


def total_distance(path):
    return sum(haversine(path[i], path[i + 1], unit="km") for i in range(len(path) - 1))


def search(data):
    pprint(data)

    title_li = []
    x_y_li = []
    location_li = []
    for item in data:
        title_li.append(item["title"])
        x_y_li.append((float(item["y"]), float(item["x"])))
        location_li.append((item['title'], item['location']))

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

    pprint(answer_li)
    print(total_km)
    data = {
        "title_list": answer_li,
        "total_km": total_km,
        "x_y_list": ordered_destinations,
    }
    recommend = open_ai(location_li)
    data['answer'] = recommend
    return data


openai.api_key = os.environ.get("OPENAI_API_KEY")


def open_ai(location_li):

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "추천해주세요!"}
    ]

    answer_li =[]

    if location_li:
        for location in location_li:
            messages.append({"role": "user", "content": f"{location[0]}({location[1]}) 주변에 추천 할 만한 장소 1곳 알려 주세요! 설명과 같이요!"})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            answer_li.append(response.choices[0].message.content)

    return answer_li


