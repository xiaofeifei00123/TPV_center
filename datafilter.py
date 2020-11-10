import numpy as np
from read_file import read
# from math import *
from math import pi,cos,sin
import xarray as xr


def bfilter(data,x,y,d):
    '''
    data  需要滤波的数据
    x     数据中心点的经度
    y     数据中心点的纬度
    d     数据的分辨率，单位°
    '''
    # 整个范围内的数组(60~120E,10~50N)
    # y对应纬度，x对应经度,i表示多少行，j表示多少列
    # 即y和i对应的是纬度，而x和j对应的是经度
    y1 = data.coords['latitude'].values   # 一维的纬度的数组,
    x1 = data.coords['longitude'].values  # 一维的经度的数组

    # 需要滤波的范围(75~105E,20~40N)
    y2 = np.arange(y+16*d,y-17*d,-d)
    x2 = np.arange(x-16*d,x+17*d,d)

    fn = data.values  # 大范围内所有数据的值


    def cr_ndarray(x,y):  # x是经度，y是纬度
        '''
        将经纬度标签变成2维数组
        '''
        lat = np.empty([len(y),len(x)])
        lon = np.empty([len(y),len(x)])
        for i in range(0,len(y)):  # i表示纬度
            for j in range(0,len(x)):  # j表示经度
                lat[i,j] = y[i]
                lon[i,j] = x[j]
        return lat,lon



    '''
    滤波系数计算公式
    lat1,lon1代表的是大范围，lat2,lon2代表的是需要滤波的范围
    A(lat1,lon1), B(lat2,lon2),R地球半径
    D = R*arccos(C)
    C = cos(lat1)cos(lat2)cos(lon1-lon2)+sin(lat1)sin(lat2)
    '''
    lat1, lon1 = cr_ndarray(x1, y1)
    lat2, lon2 = cr_ndarray(x2, y2)
    aa = pi/180
    lat1 = lat1*aa; lon1 = lon1*aa;
    lat2 = lat2*aa; lon2 = lon2*aa   # 将角度转换为弧度

    f1 = np.cos(lat1)  # 二维数组
    f4 = np.sin(lat1)  # 二维数组
    
    R = 6371.004*10**3  # 地球半径
    re = 75*10**3
    fbn = np.empty([len(y2),len(x2)])  # 这是我想要的那个滤波过后的全部的物理量的数组
    for i in range(0,len(y2)):   # 第多少行
        for j in range(0,len(x2)):  # 第多少列
            f2 = cos(lat2[i,j])  # 数
            x12 = lon1 - lon2[i,j] 
            f3 = np.cos(x12)  # 数组
            f5 = sin(lat2[i,j])  # 数
            # print(f5)
            temp = f1*f2*f3+f4*f5   # 数组

            temp[temp>1]=1   # 这里需要后面再考虑一下，将所有>1的值替换成1 ,现在是部分值计算略大于1，为1.0000004
            # temp = np.fabs(temp)
            dn = R*np.arccos(temp)

            tt = dn**2/(re**2)*(-1)  # 这个和上面一样
            wn = np.exp(tt)
            wf = np.sum(wn*fn)

            w1 = np.sum(wn)
            bn = wf/w1
            fbn[i,j] = bn
        

            
    fbn = xr.DataArray(fbn, coords=[y2, x2], dims=['latitude','longitude'])
    return fbn




if __name__ == "__main__":
    data = read()
    pass

    




