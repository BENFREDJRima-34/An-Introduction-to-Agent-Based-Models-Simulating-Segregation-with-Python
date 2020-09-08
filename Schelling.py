'''
Author : Qichang Zhao
Email : 137241304@qq.com
Date : 3-Sep-2020
Description: Simulations of Schelling's seggregation model
http://www.binpress.com/tutorial/introduction-to-agentbased-models-an-implementation-of-schelling-model-in-python/144
'''

import matplotlib.pyplot as plt
import itertools
import random
import copy

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

class Schelling:
    def __init__(self, width, height, empty_ratio, similarity_threshold, n_iterations, races=2):
        '''城市的宽和高'''
        self.width = width
        self.height = height
        '''种族数'''
        self.races = races
        '''空房子的比例'''
        self.empty_ratio = empty_ratio
        '''相似性阈值'''
        self.similarity_threshold = similarity_threshold
        '''迭代数'''
        self.n_iterations = n_iterations
        '''存储空房子坐标'''
        self.empty_houses = []
        '''存储代理人'''
        self.agents = {}

    '''居民随机分配在网格上'''
    def populate(self):

        '''初始化房子的坐标'''
        self.all_houses = list(itertools.product(range(self.width), range(self.height)))
        '''将房子的顺序打乱'''
        random.shuffle(self.all_houses)
        '''空房个数'''
        self.n_empty = int(self.empty_ratio * len(self.all_houses))
        '''空房坐标'''
        self.empty_houses = self.all_houses[:self.n_empty]
        '''已经住人的房子坐标'''
        self.remaining_houses = self.all_houses[self.n_empty:]
        '''将房子均匀的分配给不同种族'''
        houses_by_race = [self.remaining_houses[i::self.races] for i in range(self.races)]
        '''为每一个种族，每一户人家初始化一个Agent'''
        for i in range(self.races):
            self.agents = Merge(dict(zip(houses_by_race[i], [i + 1] * len(houses_by_race[i]))),self.agents)

    '''判断代理人（x，y）是否满意'''
    def is_unsatisfied(self, x, y):
        '''
        代理人（x，y）查看周围同种群邻居的比例，小于阈值返回False，否则返回True
        :param x: int,代理人的X坐标
        :param y: int，代理人的Y坐标
        :return: bool
        '''
        '''记录代理人（x，y）的种族'''
        race = self.agents[(x, y)]
        '''记录代理人（x，y）周围同种族邻居的个数'''
        count_similar = 0
        '''记录代理人（x，y）周围不同种族邻居的个数'''
        count_different = 0
        '''统计周围邻居中各个种族人数'''
        if x > 0 and y > 0 and (x - 1, y - 1) not in self.empty_houses:
            if self.agents[(x - 1, y - 1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if y > 0 and (x, y - 1) not in self.empty_houses:
            if self.agents[(x, y - 1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width - 1) and y > 0 and (x + 1, y - 1) not in self.empty_houses:
            if self.agents[(x + 1, y - 1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and (x - 1, y) not in self.empty_houses:
            if self.agents[(x - 1, y)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width - 1) and (x + 1, y) not in self.empty_houses:
            if self.agents[(x + 1, y)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and y < (self.height - 1) and (x - 1, y + 1) not in self.empty_houses:
            if self.agents[(x - 1, y + 1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and y < (self.height - 1) and (x, y + 1) not in self.empty_houses:
            if self.agents[(x, y + 1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width - 1) and y < (self.height - 1) and (x + 1, y + 1) not in self.empty_houses:
            if self.agents[(x + 1, y + 1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if (count_similar + count_different) == 0:
            return False
        else:
            return float(count_similar) / (count_similar + count_different) < self.similarity_threshold

    '''查看网格上的居民是否满意,如果尚未满意，将随机把此人分配到空房子中'''
    def update(self):
        '''循环n_iterations次'''
        for i in range(self.n_iterations):
            self.old_agents = copy.deepcopy(self.agents)
            '''统计搬家人数'''
            n_changes = 0

            for agent in self.old_agents:
                '''判断agent是否满意，不满意则将他随机分配到空房子中'''
                if self.is_unsatisfied(agent[0], agent[1]):
                    agent_race = self.agents[agent]
                    '''随机选择待搬入的空房子'''
                    empty_house = random.choice(self.empty_houses)
                    '''搬家后生成新的agent'''
                    self.agents[empty_house] = agent_race
                    '''删除原来的坐标，因为他搬家了'''
                    del self.agents[agent]
                    '''更新空房子列表'''
                    self.empty_houses.remove(empty_house)
                    self.empty_houses.append(agent)

                    n_changes += 1

            '''如果大家都满意，则迭代结束'''
            if n_changes == 0:
                break

    # def move_to_empty(self, x, y):
    #
    #     race = self.agents[(x, y)]
    #
    #     empty_house = random.choice(self.empty_houses)
    #
    #     self.updated_agents[empty_house] = race
    #
    #     del self.updated_agents[(x, y)]
    #
    #     self.empty_houses.remove(empty_house)
    #
    #     self.empty_houses.append((x, y))

    def plot(self, title, file_name):

        fig, ax = plt.subplots()

        # If you want to run the simulation with more than 7 colors, you should set agent_colors accordingly

        agent_colors = {1: 'b', 2: 'r', 3: 'g', 4: 'c', 5: 'm', 6: 'y', 7: 'k'}

        for agent in self.agents:
            ax.scatter(agent[0] + 0.5, agent[1] + 0.5, color=agent_colors[self.agents[agent]])

        ax.set_title(title, fontsize=10, fontweight='bold')

        ax.set_xlim([0, self.width])

        ax.set_ylim([0, self.height])

        ax.set_xticks([])

        ax.set_yticks([])

        plt.savefig(file_name, dpi=600)
    '''统计所有agent的平均满意度'''
    def calculate_similarity(self):
        similarity = []
        for agent in self.agents:
            count_similar = 0
            count_different = 0
            x = agent[0]
            y = agent[1]
            race = self.agents[(x, y)]
            if x > 0 and y > 0 and (x - 1, y - 1) not in self.empty_houses:
                if self.agents[(x - 1, y - 1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            if y > 0 and (x, y - 1) not in self.empty_houses:
                if self.agents[(x, y - 1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width - 1) and y > 0 and (x + 1, y - 1) not in self.empty_houses:
                if self.agents[(x + 1, y - 1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and (x - 1, y) not in self.empty_houses:
                if self.agents[(x - 1, y)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width - 1) and (x + 1, y) not in self.empty_houses:
                if self.agents[(x + 1, y)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and y < (self.height - 1) and (x - 1, y + 1) not in self.empty_houses:
                if self.agents[(x - 1, y + 1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and y < (self.height - 1) and (x, y + 1) not in self.empty_houses:
                if self.agents[(x, y + 1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width - 1) and y < (self.height - 1) and (x + 1, y + 1) not in self.empty_houses:
                if self.agents[(x + 1, y + 1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            try:
                similarity.append(float(count_similar) / (count_similar + count_different))
            except:
                similarity.append(1)
        return sum(similarity) / len(similarity)


def main():
    ##First Simulation
    '''城市的大小'''
    width, height = 50,50
    '''种族数量'''
    race = 2
    '''最大迭代次数'''
    max_iterations = 500
    '''空房子的比列'''
    empty_ratio = 0.3

    schelling_1 = Schelling(width, height, empty_ratio, 0.3, max_iterations, race)

    schelling_1.populate()

    schelling_2 = Schelling(width, height, empty_ratio, 0.5, max_iterations, race)

    schelling_2.populate()

    schelling_3 = Schelling(width, height, empty_ratio, 0.8, max_iterations, race)

    schelling_3.populate()

    schelling_1.plot('Schelling Model with 2 colors: Initial State', 'schelling_2_initial.png')

    schelling_1.update()

    schelling_2.update()

    schelling_3.update()

    schelling_1.plot('Schelling Model with 2 colors: Final State with Happiness Threshold 30%',
                     'schelling_2_30_final.png')

    schelling_2.plot('Schelling Model with 2 colors: Final State with Happiness Threshold 50%',
                     'schelling_2_50_final.png')

    schelling_3.plot('Schelling Model with 2 colors: Final State with Happiness Threshold 80%',
                     'schelling_2_80_final.png')

    ##Second Simulation Measuring Seggregation

    similarity_threshold_ratio = {}

    for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
        schelling = Schelling(width, height, empty_ratio, i, max_iterations, race)

        schelling.populate()

        schelling.update()

        similarity_threshold_ratio[i] = schelling.calculate_similarity()

    fig, ax = plt.subplots()

    plt.plot(list(similarity_threshold_ratio.keys()), list(similarity_threshold_ratio.values()), 'ro')

    ax.set_title('Similarity Threshold vs. Mean Similarity Ratio', fontsize=15, fontweight='bold')

    ax.set_xlim([0, 1])

    ax.set_ylim([0, 1.1])

    ax.set_xlabel("Similarity Threshold")

    ax.set_ylabel("Mean Similarity Ratio")

    plt.savefig('schelling_segregation.png')


if __name__ == "__main__":
    main()