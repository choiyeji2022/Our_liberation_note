from collections import defaultdict
from haversine import haversine
from itertools import permutations
from pprint import pprint
from rest_framework import permissions, status
from rest_framework.response import Response


def total_distance(path):
    return sum(haversine(path[i], path[i + 1], unit='km') for i in range(len(path) - 1))


def search(data):
    pprint(data)

    title_li = []
    x_y_li = []
    # 카테고리별로 데이터를 그룹화
    category_groups = defaultdict(list)
    for item in data:
        category_groups[item['category']].append(item)
        title_li.append(item['title'])
        x_y_li.append((float(item['y']), float(item['x'])))

    # 가장 많은 아이템이 있는 카테고리를 기준으로 정렬
    sorted_categories = sorted(category_groups.keys(), key=lambda x: len(category_groups[x]), reverse=True)

    # 각 카테고리의 시작점부터 가장 가까운 목적지를 찾아 순서를 결정
    ordered_destinations = []
    previous_destination = None
    while sorted_categories:
        current_category = sorted_categories.pop(0)

        current_group_xy_li = [(float(i['y']), float(i['x'])) for i in category_groups[current_category]]
        current_group_permutations = permutations(current_group_xy_li)
        current_group_distances = [(path, total_distance(path)) for path in current_group_permutations]
        shortest_path, _ = min(current_group_distances, key=lambda x: x[1])

        if previous_destination:
            # 이전 목적지와 현재 목적지가 중복되지 않도록 처리
            shortest_path = list(filter(lambda x: x != previous_destination, shortest_path))

        ordered_destinations.extend(shortest_path)
        previous_destination = ordered_destinations[-1]

        # 빈 카테고리 제거
        sorted_categories = [category for category in sorted_categories if category_groups[category]]

    # 목적지 리스트
    answer_li = [title_li[x_y_li.index(item)] for item in ordered_destinations]

    # 최종 경로의 총 거리 계산
    total_km = total_distance(ordered_destinations)

    pprint(answer_li)
    print(total_km)
    data = {
        'title_list': answer_li,
        'total_km': total_km,
        'x_y_list': ordered_destinations
    }
    return data


# 변경 사항 : 카페 다음에 음식점 되도록 안오게!

