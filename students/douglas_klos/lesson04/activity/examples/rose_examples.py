#!/usr/bin/env python3

import sys
import random
import functools
import operator


def ex_squares():
    squares = map(lambda x: x * x, [0, 1, 2, 3, 4])
    print(list(squares))


def rose_1():
    names = ["Mary", "Isla", "Sam"]
    code_names = ["Mr. Pink", "Mr. Orange", "Mr. Blonde"]

    # for i in range(len(names)):
    #     names[i] = random.choice(code_names)
    # print(names)

    names = map(lambda x: random.choice(code_names), names)
    print(list(names))


def rose_2():
    names = ["Mary", "Isla", "Sam"]

    # for i in range(len(names)):
    #     names[i] = hash(names[i])
    # print(names)

    names = map(hash, names)
    print(list(names))


def rose_3():
    sum = functools.reduce(lambda a, x: a + x, [0, 1, 2, 3, 4])
    print(sum)


def rose_4():
    sentences = ["Mary read a story to Sam and Isla.", "Isla cuddled Sam.", "Sam chortled."]

    # sam_count = 0
    # for sentence in sentences:
    #     sam_count += sentence.count('Sam')
    # print(f'Sam_count : {sam_count}')

    sam_count = functools.reduce(lambda a, x: a + x.count("Sam"), sentences, 0)
    print(f"Sam_count : {sam_count}")


def rose_5():
    people = [
        {"name": "Mary", "height": 160},
        {"name": "Isla", "height": 80},
        {"name": "Sam", "height": 120},
    ]

    # height_total = 0
    # height_count = 0
    # for person people:
    #     if 'height' in person:
    #         height_total += person['height']
    #         height_count += 1
    # if height_count > 0:
    #     average_height = height_total / height_count
    # print(average_height)

    heights = map(lambda x: x["height"], filter(lambda x: "height" in x, people))
    if len(list(heights)) > 0:
        # average_height = functools.reduce(operator.add, heights) / len(list(heights))
        average_height = functools.reduce(
            operator.add, map(lambda x: x["height"], filter(lambda x: "height" in x, people))
        ) / len(list(map(lambda x: x["height"], filter(lambda x: "height" in x, people))))
        print(f"average_height: {average_height}")


def race_1():
    time = 5
    car_positions = [1, 1, 1]

    while time:
        time -= 1
        print('')
        for i in range(len(car_positions)):
            if random.random() > 0.3:
                car_positions[i] += 1

            print('-' * car_positions[i])

time = 5
def race_2():
    
    car_positions = [1, 1, 1]

    def move_cars():
        for i, _ in enumerate(car_positions):
            if random.random() > 0.3:
                car_positions[i] += 1
    
    def draw_car(car_position):
        print('-' * car_position)

    def run_step_of_race():
        global time
        time -= 1
        move_cars()

    def draw():
        print('')
        for car_position in car_positions:
            draw_car(car_position)
    
    while time:
        run_step_of_race()
        draw()


def race_fp():
    def move_cars(car_positions):
        return list(map(lambda x: x + 1 if random.random() > 0.3 else x, car_positions))
    
    def output_car(car_position):
        return '-' * car_position

    def run_step_of_race(state):
        return {'time': state['time'] - 1, 
                'car_positions': move_cars(state['car_positions'])}

    def draw(state):
        print('')
        print('\n'.join(map(output_car, state['car_positions'])))
        
    def race(state):
        draw(state)
        if state['time']:
            race(run_step_of_race(state))

    race({'time': 5,
          'car_positions': [1, 1, 1]})
        



if __name__ == "__main__":
    # ex_squares()
    # rose_1()
    # rose_2()
    # rose_3()
    # rose_4()
    # rose_5()
    # race_1()
    # race_2()
    race_fp()