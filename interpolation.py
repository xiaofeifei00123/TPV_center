import numpy as np
from read_file import read
from math import *
import xarray as xr


def interplot(data,x,y,d):
    '''
    根据中心点和上次插值的数据
    确定这次中心点周围32格的数据
    为下一次插值做准备
    '''

    # print(x,y,d)

    y1 = np.arange(y+16*d,y-17*d,-d)
    x1 = np.arange(x-16*d,x+17*d,d)

    f = data.loc[y1[0]:y1[-1],x1[0]:x1[-1]]  # 取中心点附近，半径为32网格的数据
    data1 = interplot1(f,d)  # 调用插值函数，得到想要的插值过后的数据
    # print(data1.shape)
    # for row in data1:
    #     for item in row:
    #         print(item.values)
    return data1


def interplot1(data,d):
    '''
    对确定网格内的数据进行插值，
    分辨率提升一倍
    '''

    y = data.coords['latitude'].values   # 一维的纬度的数组,
    x = data.coords['longitude'].values  # 一维的经度的数组

    he = data.values
    m = len(y)  # 多少行
    n = len(x)  # 多少列
    
    he1 = np.empty((2*m-1,2*n-1))  # 滤波过后的数据总共应该是这么多

    for i in range(m-1):
        he1[2*i+1,2*n-2] = (he[i,n-1]+he[i+1,n-1])/2
        he1[2*i,2*n-2] = he[i,n-1]
        for j in range(n-1):
            he1[2*i,2*j] = he[i,j]
            he1[2*i,2*j+1] = (he[i,j]+he[i,j+1])/2
            he1[2*i+1,2*j] = (he[i,j]+he[i+1,j])/2
            he1[2*i+1,2*j+1] = (he[i,j]+he[i+1,j]+he[i,j+1]+he[i+1,j+1])/4

            he1[2*m-2,2*j+1] = (he[m-1,j]+he[m-1,j+1])/2
            he1[2*m-2,2*j] = he[m-1,j]
            # print(he[i,j])
            
    
            
            # print(i,j)
    he1[2*m-2,2*n-2] = he[m-1,n-1]
            

    # 将得到的插值数据转换为DataArray数组
    y2 = np.arange(y[0],y[-1]-d/2,-d/2)
    x2 = np.arange(x[0],x[-1]+d/2,d/2)
    data1 = xr.DataArray(he1, coords=[y2, x2], dims=['latitude','longitude'])
    return data1



if __name__ == "__main__":
    pass

    




