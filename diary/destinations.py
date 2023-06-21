from datetime import datetime

import requests
from bardapi import Bard
from bs4 import BeautifulSoup as bs
from haversine import haversine


def total_distance(path):
    return sum(haversine(path[i], path[i + 1], unit="km") for i in range(len(path) - 1))


def search(data):
    start = datetime.now()
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

    recommend = bard_ai(openai_data)
    crawling = crawling_data(answer_li)

    data["answer"] = recommend
    data["crawling"] = crawling
    end = datetime.now()
    print("all", end - start)
    return data


def bard_ai(location_li):
    token = "XQjGvFI-VaFDrPIx8PlyXRfsRnN319BMejkOWPAJvP3u7Tucgpky9hNEmLyPu9au_3yw2A."
    bard = Bard(token=token)

    start = datetime.now()

    q_str = "다음 제시 되는 질문마다 답변을 한글로 반드시 하나씩 번호를 매기면서 달아주세요!"

    for idx, location in enumerate(location_li):
        q_str += f"{location[1]}에 위치한 {location[0]}의 같은 지역 내에 있는 비슷한 한 곳과 그에 대한 설명을 반드시 답변 해주세요!"
    answer_li = [bard.get_answer(f"{q_str}")["content"]]

    li = []

    for string in answer_li[0].split("\n"):
        if ": " in string:
            li.append(string.split(": ", 1)[1])
        else:
            li.append(string[3:])

    end = datetime.now()

    print("bard", end - start)
    return li


def crawling_data(answer_li):
    start = datetime.now()
    data_li = []

    for i in answer_li:
        # 검색 결과의 URL을 저장
        url = "https://search.naver.com/search.naver?where=view&sm=tab_jum&query=" + i

        # requests 패키지를 이용해 URL의 HTML 문서를 가져옴
        response = requests.get(url)
        html_text = response.text

        # HTML을 파싱하고, 'soup' 변수에 저장
        soup = bs(html_text, "html.parser")

        # 첫 번째 링크
        link = soup.select_one(".api_txt_lines.total_tit")

        # href 속성을 가져와 data_li에 추가
        if link:
            href = link.get("href")
            data_li.append(href)
        else:
            print("No related link found")

    end = datetime.now()
    print("crawling", end - start)
    return data_li
