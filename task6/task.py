import os
import sys
import json


sys.path.append(os.getcwd())


accessory_function = regulator = transition_rules = None


def get_function(path, set_name: str = "температура"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f).get(set_name)


def get_rules(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {element: action for element, action in data}


def calc_probability(beginner, ender, value):
    start_t, start_ind = beginner
    end_t, end_ind = ender

    ind = start_ind + end_ind
    if ind == 0:
        return 0
    elif ind == 1:
        norm = (value - start_t) if start_ind == 0 else (end_t - value)
        return norm / (end_t - start_t)
    else:
        return 1


def use_function(function, value):
    result = []
    for el_description in function:
        points = el_description.get("points")
        result.append((el_description.get("id"), 0))
        beginner = points[0]
        for point_info in points[1:]:
            ender = point_info
            if beginner[0] <= value <= ender[0]:
                probability = calc_probability(beginner, ender, value)
                result[-1] = (el_description.get("id"), probability)
                break
            beginner = ender
        
    return result


def use_rules(rules, condition_info):
    return [
        (rules[condition], probability) 
        for condition, probability in condition_info
    ]


def dephasificate(fuzzy_inputs):
    result = fuzzy_inputs[0]
    for input_info in fuzzy_inputs[1:]:
        if input_info[1] > result[1]:
            result = input_info

    return result


def regulate(regulator, optimal_regulation):
    regulation_id, probability = optimal_regulation
    for el_description in regulator:
        if el_description.get("id") == regulation_id:
            points = el_description.get("points")
            for point_prev, point_cur in zip(points[:-1], points[1:]):
                if point_prev[1] == point_cur[1] == 1:
                    return point_cur[0] + (point_prev[0] - point_cur[0]) * probability


def main(accessory_function, transition_rules, regulator, value):
    print("Входное значение:", value)
    
    condition_info = use_function(accessory_function, value)
    print("Фаззифицированные данные:", condition_info)
    
    fuzzy_inputs = use_rules(transition_rules, condition_info)
    print("После активации нечетких правил:", fuzzy_inputs)

    optimal_regulation = dephasificate(fuzzy_inputs)
    print("Дефаззификация. Оптимальное решение:", optimal_regulation)

    result = regulate(regulator, optimal_regulation)
    print("Оптимальное значение регулирования:", result)

    return result


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    data_path = os.path.join(parent_dir, "all_data")

    accessory_function = get_function(os.path.join(data_path, "accessory_function.json"))
    regulator = get_function(os.path.join(data_path, "regulator.json"))
    transition_rules = get_rules(os.path.join(data_path, "transition_rules.json"))

    main(accessory_function, transition_rules, regulator, 18.23)