import logging
import sys
import numpy
import dijkstra

logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')
#python CodeCraft-2019.py car.txt road.txt cross.txt answer.txt
##bash build_and_run.sh
##CodeCraft_tar.sh

def make_graph(roads_list, cars_list, cross_list):
    # 构建邻接矩阵graph_list
    graph_list = numpy.zeros([len(cross_list), len(cross_list)]) + 10000  # 10000作为无穷大
    for i in range(len(cross_list)):
        graph_list[i][i] = 0  # 将对角线清零
    for i in range(len(roads_list)):
        from_cross = roads_list[i][4] - 1
        to_cross = roads_list[i][5] - 1
        graph_list[from_cross][to_cross] = roads_list[i][1]  # 无向图,对称
        graph_list[to_cross][from_cross] = roads_list[i][1]

    # for i in range(len(cross_list)):
    #    print(graph_list[i])
    return graph_list


def node_to_road(roads_list, cars_list, cross_list):
    # 由于构建的是节点的路线图，故先需要转换一下,也就是说convert_list的索引是cross节点id，值是道路id，值为0则说明两个cross不相连
    convert_list = numpy.zeros([len(cross_list), len(cross_list)])
    for h in range(len(roads_list)):  # 这里不能是len(convert_list),自己可以仔细想一下

        from_cross = roads_list[h][4] - 1
        to_cross = roads_list[h][5] - 1

        convert_list[from_cross][to_cross] = roads_list[h][0]  # 无向图,对称
        convert_list[to_cross][from_cross] = roads_list[h][0]

    # for i in range(len(convert_list)):
    #     print(convert_list[i])
    return convert_list


def find_a_way(graph_list, convert_list, from_node=1, to_node=36):
    tmp_from = from_node - 1
    tmp_to = to_node - 1
    # 查找1节点，到35节点 的输出结果，要注意cross的id值全是减了一的
    distance, path = dijkstra.dijkstra(graph_list, tmp_from)
    # print("结果为", distance, path)

    #print("path[0][35]", (path))  # (path[2][35])代表从节点2到35的最短路线，实际上是cross 3到 cross 36

    tmp_path = path[tmp_from][tmp_to]
    convert_path = []
    convert_path.append(convert_list[tmp_from][tmp_path[0]])
    k = 0
    while (k < len(tmp_path) - 1):
        tmp = convert_list[tmp_path[k]][tmp_path[k + 1]]  # 两个节点对应于一条路
        convert_path.append(tmp)
        k = k + 1
    # print("最终输出的路线结果为：", convert_path)
    return convert_path


# to read input file
def read_input_data(car_filename, road_filename, cross_filename):
    roads_data = []
    with open(road_filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
            lines = lines.translate(str.maketrans('(),', '   '))  # maketrans() 方法用于创建字符映射的转换表
            line = lines.strip()
            if not len(line) or line.startswith('#'):
                continue
            road_tmp = line.split()
            road_tmp = map(int, road_tmp)
            roads_data.append(road_tmp)

    cars_data = []
    with open(car_filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
            lines = lines.translate(str.maketrans('(),', '   '))
            line = lines.strip()
            if not len(line) or line.startswith('#'):
                continue
            car_tmp = line.split()
            car_tmp = map(int, car_tmp)
            cars_data.append(car_tmp)

    cross_data = []
    with open(cross_filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
            lines = lines.translate(str.maketrans('(),', '   '))
            line = lines.strip()
            if not len(line) or line.startswith('#'):
                continue
            cross_tmp = line.split()
            cross_tmp = map(int, cross_tmp)
            cross_data.append(cross_tmp)
    roads_list = []
    for i in range(len(roads_data)):
        # print(list(roads_data[i]))
        roads_list.append(list(roads_data[i]))
    cars_list = []
    for i in range(len(cars_data)):
        cars_list.append(list(cars_data[i]))
    cross_list = []
    for i in range(len(cross_data)):
        cross_list.append(list(cross_data[i]))
    return roads_list, cars_list, cross_list


def save_answer(fileName,data_list):

       fp = open(fileName,'w+')
       fp.write("#(carId,StartTime,RoadId...)"+'\n')

       for idx in range(len(data_list)):
           fp.write("(")
           for j in range(len(data_list[idx])):
               fp.write(str(data_list[idx][j]))
               if(j!= (len(data_list[idx])-1)):  # 最后一个数据之间不需要逗号
                 fp.write(" , ")
           fp.write(")"+'\n')

       fp.write("# the end!!!")
       fp.close()
       return True



def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    roads_list, cars_list, cross_list = read_input_data(car_path, road_path, cross_path);
    #graph_list =make_graph(roads_list, cars_list, cross_list)
    #convert_list =node_to_road(roads_list, cars_list, cross_list)


    answer=[]
    for n in range(len(cars_list)):

        roads_list, cars_list, cross_list = read_input_data(car_path, road_path, cross_path); #其实我也不知道为什么每次都要重新读数据才行,因为不这样结果不对
        graph_list = make_graph(roads_list, cars_list, cross_list)
        convert_list = node_to_road(roads_list, cars_list, cross_list)

        tmp_car = cars_list[n];
        from_node =tmp_car[1]
        to_node =tmp_car[2]
        tmp_path=[]
        tmp_path.append(tmp_car[0])
        tmp_path.append(int(4*n))  #每次跑1辆

        #print(from_node,to_node)
        path = find_a_way(graph_list, convert_list, from_node,to_node)
        if(from_node>to_node):
            path.reverse() #TODO：这里注意，需要判断起始点和终止点的大小，如果终止点小于起始点，则需要reverse结果

        path =[i.astype(int) for i in path] #将所有数据，从numpy.float32类型转成int64类型

        tmp_path.extend(path)
        print("the tmp_path is:", tmp_path)
        answer.append(tmp_path)

    save_answer(answer_path,answer)





if __name__ == "__main__":
    main()
