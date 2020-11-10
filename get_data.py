import numpy as np
from read_file import read

def getdata(data,m,n,d):
    '''
    data：原始数据
    m,m 纬度和经度
    在原始数据中获得要研究的大区域的数据
    获得以m,n为中心点，64格*64格（16*16度）的数据
    '''
    # 确定中心点格点坐标
    # y = (50-m)*4  # 纵向的格点数
    # x = (n-60)*4  # 横向的格点数

#     # 读取不同时次的数据，并将它们放在一个列表里面
    y1 = np.arange(m+32*d,m-33*d,-d)
    x1 = np.arange(n-32*d,n+33*d,d)
    t = 4  # 设置时间的次序

    h40 = 'z_400'
    h45 = 'z_450'
    h50 = 'z_500'
    h55 = 'z_550'

    vo40 = 'z_400'
    vo45 = 'z_450'
    vo50 = 'z_500'
    vo55 = 'z_550'

    def ts_data(name,data,t):
        '''
        把三维的数据变成二维的了
        xarray 中读数据
        '''
        h = data[name]  #  读这个名字的数据
        d = h.isel(time=t)  # 在选择它这个时间
        f = d.loc[y1[0]:y1[-1],x1[0]:x1[-1]]  # 再选择它的坐标取中心点附近，半径为32网格的数据
        return f 
    
    h400 = ts_data(h40,data,t)
    h450 = ts_data(h45,data,t)
    h500 = ts_data(h50,data,t)
    h550 = ts_data(h55,data,t)

    vo400 = ts_data(vo40,data,t)
    vo450 = ts_data(vo45,data,t)
    vo500 = ts_data(vo50,data,t)
    vo550 = ts_data(vo55,data,t)
    height = [h400, h450, h500, h550]  # 返回多个高度场数据
    vorticity = [vo400, vo450, vo500, vo550]  # 返回多个涡度场数据
    # print(vo400)
    return height, vorticity


if __name__ == "__main__":
    data = read()  # 读取全部数据
    m = 32;n=86   # 滤波前，由500hPa风场确定的大致中心位置,m是纬度，n是经度
    d = 0.25
    p0 = (m,n)
    data1, data2 = getdata(data,m,n,d)  # 取得想要的初始范围内的数据,y纬度,x经度