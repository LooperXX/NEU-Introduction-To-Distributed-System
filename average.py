import numpy as np
import time
import json
import matplotlib.pyplot as plt

# 基于传染行为

########## Hyper_parameter ##########
num_nodes = 1000000
value = np.arange(num_nodes, dtype=float)
mean_init = np.mean(value)
state = np.zeros(num_nodes, dtype=float)  # -1 0 1 已隔离 易感染 已感染
k = 4
time_local = 0
name_list = ['push_pull', 'gossip_push', 'gossip_push_pull']
his_list = ['std', 'susceptible_nodes', 'update_times', 'removed_nodes']
color_list = ['green', 'red', 'blue']
history = {}
for name_ in name_list:
    history[name_] = {}
    for his in his_list:
        history[name_][his] = []
history['time'] = []


#####################################
def init(name):
    global value, state
    value = np.arange(num_nodes, dtype=float)
    state = np.zeros(num_nodes, dtype=float)
    np.random.shuffle(value)
    print('-------------Init_' + name + '-------------')
    show_res(0, 0, name)
    random_first = np.random.randint(0, num_nodes, 1)
    state[random_first] = 1
    print('random Infected node =', random_first[0])
    print('mean_init =', mean_init)
    print('------------------------------')


def show_res(epoch, count, name, flag=False):
    std = np.std(value)
    susceptible_nodes = state[np.where(state == 0)].size
    history[name][his_list[0]].append(std)
    history[name][his_list[1]].append(susceptible_nodes)
    history[name][his_list[2]].append(count)
    print('epoch', epoch, 'Std =', std)
    print('epoch', epoch, 'Susceptible nodes =', susceptible_nodes)
    print('epoch', epoch, 'Update times =', count)
    if flag:
        removed_nodes = state[np.where(state == -1)].size
        infected_nodes = state[np.where(state > 0)].size
        print('epoch', epoch, 'Infected nodes =', infected_nodes)
        print('epoch', epoch, 'Removed nodes =', removed_nodes)
        history[name][his_list[3]].append(removed_nodes)


def push_pull():
    name = 'push_pull'
    init(name)
    epoch = 1
    while True:
        count = 0
        for index in range(num_nodes):
            chosen_index = np.random.randint(num_nodes)
            if (state[index] == 1) | (state[chosen_index] == 1):
                mean = np.mean([value[index], value[chosen_index]])
                value[[index, chosen_index]] = mean
                state[[index, chosen_index]] = 1
                count += 1
        show_res(epoch, count, name)
        if np.std(value) < 0.001:
            break
        epoch += 1


def gossip_push():  # 一轮通讯中没有人更新
    name = 'gossip_push'
    init(name)
    epoch = 1
    while True:
        count = 0
        for index in np.argwhere(state > 0):
            index = index[0]
            chosen_index = np.random.randint(num_nodes)
            if update(value[index], value[chosen_index]):
                count += 1
                mean = np.mean([value[index], value[chosen_index]])
                value[[index,chosen_index]] = mean
                if state[chosen_index] == 0:
                    state[chosen_index] = 1
            else:
                state[index] /= k
                interest = np.random.choice(2, 1, p=[1 - state[index], state[index]])
                if not interest:
                    state[index] = -1
        show_res(epoch, count, name, True)
        if np.argwhere(state > 0).size == 0:
            break
        epoch += 1


def gossip_push_pull():  # 一轮通讯中没有人更新
    name = 'gossip_push_pull'
    init(name)
    epoch = 1
    while True:
        count = 0
        for index in np.argwhere(state > 0):
            index = index[0]
            chosen_index = np.random.randint(num_nodes)
            if update(value[index], value[chosen_index]):
                count += 1
                mean = np.mean([value[index], value[chosen_index]])
                value[[index,chosen_index]] = mean
                if state[chosen_index] == 0:
                    state[chosen_index] = 1
            else:
                state[index] /= k
                interest = np.random.choice(2, 1, p=[1 - state[index], state[index]])
                if not interest:
                    state[index] = -1
        for index in np.argwhere(state == 0):
            index = index[0]
            chosen_index = np.random.randint(num_nodes)
            if state[chosen_index] > 0:
                mean = np.mean([value[index], value[chosen_index]])
                value[[index, chosen_index]] = mean
                state[index] = 1
                count += 1
        show_res(epoch, count, name, True)
        if np.argwhere(state > 0).size == 0:
            break
        epoch += 1


def update(a, b):
    if abs(a - b) < 0.001:
        return False
    return True


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
    with open('history_average.json', 'w') as f:
        json.dump(data, f)


def plot_res():
    with open('history_average.json', 'r') as f:
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
            plt.savefig('average_' + his + '.jpg')
            plt.show()
        index = 0
        for name in name_list:
            print(name, 'time diff = ', data['time'][index + 1] - data['time'][index])
            index += 1


def main():
    show_time(True)
    push_pull()
    show_time()
    gossip_push()
    show_time()
    gossip_push_pull()
    show_time()
    save_file()
    plot_res()


if __name__ == "__main__":
    main()
