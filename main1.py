'''
给定中心点，64*64的数据
找到这组数据的极值，返回极值大小和格点位置
'''
import numpy as np
from read_file import read
from datafilter import bfilter
from interpolation import interplot
from get_data import getdata


def max_value(data,y,x,d):
    '''
    取得范围的最大值及其坐标
    '''
    dvalue = data.values
    max_value = np.max(dvalue)
    maxp = np.where(dvalue==max_value)  # 最大值位置
    lat_y = maxp[0][0]
    lon_x = maxp[1][0]
    maxlat = y+16*d-lat_y*d
    maxlon = x-16*d+lon_x*d
    return max_value,maxlat,maxlon

def min_value(data,y,x,d):
    '''
    取得范围内的最小值及其坐标
    '''
    dvalue = data.values
    min_value = np.min(dvalue)
    minp = np.where(dvalue==min_value)  # 最小值位置
    lat_y = minp[0][0]
    lon_x = minp[1][0]
    minlat = y+16*d-lat_y*d
    minlon = x-16*d+lon_x*d
    return min_value,minlat,minlon



def pos_height(data0,m,n,d):
    '''
    寻找height最低值得位置
    '''
    # m = 32;n=86   # 滤波前，由500hPa风场确定的大致中心位置,m是纬度，n是经度
    p0 = (m,n)
    position = []  # 位置
    extreme = []   # 极值
    position.append(p0)   # 假定中心点位置

    y = position[0][0]
    x = position[0][1]
    aa = bfilter(data0,x,y,d)   # 第一次滤波,输入数据、中心点的经纬度、分辨率，进行滤波,返回小范围内的滤波值
    h_extreme1,y1,x1 = min_value(aa,y,x,d)  # 滤波范围内极值的位置,和极值大小
    position.append((y1,x1))
    extreme.append(h_extreme1)

    datalist = list(range(1,6)) # 设置一个空的列表
    datalist[0] = data0

    num = 4  # 调整迭代次数
    for i in range(1,num):
        x1 = position[i][1]  # 上一步所确定的中心点
        y1 = position[i][0]  
        # 插值函数用到的分辨率还是d
        datalist[i] = interplot(datalist[i-1],x1,y1,d)  # 这里应该是要把新的中心点，和上次的原始数据放进去，进行插值,得到新的数据
        d = d/2
        # 滤波用到的分辨率就是要减半了
        aa = bfilter(datalist[i],x1,y1,d)   # 第二次滤波,输入数据、中心点的经纬度、分辨率，进行滤波,返回小范围内的滤波值
        h_extreme2,y2,x2 = min_value(aa,y1,x1,d)  # 滤波范围内极值的位置,和极值大小
        position.append((y2,x2))
        extreme.append(h_extreme2)

    return position,extreme


def pos_vorticity(data0,m,n,d):
    '''
    寻找height最低值得位置
    '''
    # m = 32;n=86   # 滤波前，由500hPa风场确定的大致中心位置,m是纬度，n是经度
    p0 = (m,n)
    position = []  # 位置
    extreme = []   # 极值
    position.append(p0)   # 假定中心点位置

    y = position[0][0]
    x = position[0][1]
    aa = bfilter(data0,x,y,d)   # 第一次滤波,输入数据、中心点的经纬度、分辨率，进行滤波,返回小范围内的滤波值
    h_extreme1,y1,x1 = min_value(aa,y,x,d)  # 滤波范围内极值的位置,和极值大小
    position.append((y1,x1))
    extreme.append(h_extreme1)

    datalist = list(range(1,6)) # 设置一个空的列表
    datalist[0] = data0

    num = 4  # 调整迭代次数
    for i in range(1,num):
        x1 = position[i][1]  # 上一步所确定的中心点
        y1 = position[i][0]  
        # 插值函数用到的分辨率还是d
        datalist[i] = interplot(datalist[i-1],x1,y1,d)  # 这里应该是要把新的中心点，和上次的原始数据放进去，进行插值,得到新的数据
        d = d/2
        # 滤波用到的分辨率就是要减半了
        aa = bfilter(datalist[i],x1,y1,d)   # 第二次滤波,输入数据、中心点的经纬度、分辨率，进行滤波,返回小范围内的滤波值
        h_extreme2,y2,x2 = min_value(aa,y1,x1,d)  # 滤波范围内极值的位置,和极值大小
        position.append((y2,x2))
        extreme.append(h_extreme2)

    return position,extreme

if __name__ == "__main__":

    data = read()  # 读取全部数据

# 第0步，根据风场假定中心点
    # 根据风场设置假定中心点
    m = 32;n=86   # 滤波前，由500hPa风场确定的大致中心位置,m是纬度，n是经度
    p0 = (m,n)
    d = 0.25
    # 初始范围内的位势高度场和涡度场
    height, vorticity= getdata(data,m,n,d)  # 取得想要的初始范围内的数据,y纬度,x经度
    h40,h45,h50,h55 = height
    vo40,vo45,vo50,vo55 = vorticity
    # ps0 = pos(data0)

    # 迭代过程中的一系列位置
    ps_h40,exh40 = pos_height(vo55,m,n,d)
    ps_h45,exh45 = pos_height(h45,m,n,d)
    ps_h50,exh50 = pos_height(h50,m,n,d)
    ps_h55,exh55 = pos_height(h55,m,n,d)

    ps_vo40,exvo40 = pos_vorticity(vo40,m,n,d)
    ps_vo45,exvo45 = pos_vorticity(vo45,m,n,d)
    ps_vo50,exvo50 = pos_vorticity(vo50,m,n,d)
    ps_vo55,exvo55 = pos_vorticity(vo55,m,n,d)

    print(ps_h40)
    print(ps_h45)
    print(ps_h50)
    print(ps_h55)

    print(ps_vo40)
    print(ps_vo45)
    print(ps_vo50)
    print(ps_vo55)