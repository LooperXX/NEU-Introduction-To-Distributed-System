import numpy as np
import time
import json
import matplotlib.pyplot as plt

# 基于传染行为

########## Hyper_parameter ##########
num_nodes = 1000000
value = np.zeros(num_nodes, dtype=int)
time_local = 0
name_list = ['push', 'pull', 'push_pull']
his_list = ['infected_nodes', 'update_times']
color_list = ['green', 'red', 'blue']
history = {}
for name_ in name_list:
    history[name_] = {}
    for his in his_list:
        history[name_][his] = []
history['time'] = []


#####################################
def init(name):
    global value
    value = np.zeros(num_nodes, dtype=int)
    np.random.shuffle(value)
    print('-------------Init_' + name + '-------------')
    show_res(0, 0, name)
    random_first = np.random.randint(0, num_nodes, 1)
    value[random_first] = 1
    print('random Infected node =', random_first[0])
    print('------------------------------')


def show_res(epoch, count, name):
    infected_nodes = value[np.where(value == 1)].size
    history[name][his_list[0]].append(infected_nodes)
    history[name][his_list[1]].append(count)
    print('epoch', epoch, 'Infected nodes =', infected_nodes)
    print('epoch', epoch, 'Update times =', count)


def push():
    name = 'push'
    init(name)
    epoch = 1
    while True:
        count = 0
        for index in np.argwhere(value == 1):
            chosen_index = np.random.randint(num_nodes)
            if value[chosen_index] == 0:
                value[chosen_index] = 1
                count += 1
        show_res(epoch, count, name)
        if value[np.argwhere(value == 0)].size == 0:
            break
        epoch += 1


def pull():
    name = 'pull'
    init(name)
    epoch = 1
    while True:
        count = 0
        for index in np.argwhere(value == 0):
            chosen_index = np.random.randint(num_nodes)
            if value[chosen_index] == 1:
                value[index[0]] = 1
                count += 1
        show_res(epoch, count, name)
        if value[np.argwhere(value == 0)].size == 0:
            break
        epoch += 1


def push_pull():
    name = 'push_pull'
    init(name)
    epoch = 1
    while True:
        count = 0
        for index in range(num_nodes):
            chosen_index = np.random.randint(num_nodes)
            if value[index] ^ value[chosen_index]:
                value[[index, chosen_index]] = 1
                count += 1
        show_res(epoch, count, name)
        if value[np.argwhere(value == 0)].size == 0:
            break
        epoch += 1


def show_time(flag=False):
    global time_local
    if flag:
        time_local = time.time()
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    else:
        time_temp = time_local
        time_local = time.time()
        print('time difference =', time_local - time_temp)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    history['time'].append(time_local)


def save_file():
    data = json.dumps(history)
    with open('history.json', 'w') as f:
        json.dump(data, f)


def plot_res():
    with open('history.json', 'r') as f:
        data = json.loads(json.load(f))
        for his in his_list:
            data_list = []
            for name in name_list:
                data_list.append(data[name][his])
            plt.title(his)
            index = 0
            for plot_data in data_list:
                plt.plot(np.arange(len(plot_data)), plot_data, color=color_list[index], label=name_list[index])
                index += 1
            plt.legend()
            plt.xlabel('epoch')
            plt.ylabel('value')
            plt.savefig('anti_entropy_' + his + '.jpg')
            plt.show()
        index = 0
        for name in name_list:
            print(name, 'time diff = ', data['time'][index + 1] - data['time'][index])
            index += 1


def main():
    show_time(True)
    push()
    show_time()
    pull()
    show_time()
    push_pull()
    show_time()
    save_file()
    plot_res()


if __name__ == "__main__":
    main()
