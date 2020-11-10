import numpy as np
import xarray as xr
import os

def read():
    '''
    根据给定的文件，读出想要的物理量
    返回的是某一层的某个物理量的多时次的数据
    '''
    # 设置文件路径
    path = "/mnt/Disk4T_5/fengxiang_file/Data/"
    path0 = "ERA5/Plateau_vortex"
    # 高空数据
    file_name0 = "2006-08-13T00-23.nc"
    file0 = os.path.join(path,path0,file_name0)
    # 地面数据
    # file_name1 = "mslp_2006_0813_0816.nc"
    # file1 = os.path.join(path,path0,file_name1)


    ## 读取文件
    ds0 = xr.open_dataset(file0)
    # ds1 = xr.open_dataset(file1)
    # print(ds1.data_vars)

    vo = ds0['vo']
    z  = ds0['z']
    u  = ds0['u']
    v  = ds0['v']
    # mslp = ds1['msl']
    # print(mslp.coords)



    ##  处理数据
    #  取14日00时-16日00时
    #  选择了7点到15点(共9个时次)
    #  主要参数 时间,纬度，经度
    vo_400 = vo[7:16,1,:,:]  # 400hPa的相对涡度
    z_400 = z[7:16,1,:,:]    # 400hPa的位势高度

    vo_450 = vo[7:16,2,:,:]  # 450hPa的相对涡度
    z_450 = z[7:16,2,:,:]    # 450hPa的位势高度

    vo_500 = vo[7:16,3,:,:]  # 500hPa的相对涡度
    z_500 = z[7:16,3,:,:]    # 500hPa的位势高度

    vo_550 = vo[7:16,4,:,:]  # 500hPa的相对涡度
    z_550 = z[7:16,4,:,:]    # 500hPa的位势高度
    # mslp = mslp[4:13,:,:]    # 平均海平面气压
    #  次要参数
    # u_400 = u[7:16,1,:,:] 
    # v_400 = v[7:16,1,:,:] 
    u_500 = u[7:16,3,:,:] 
    v_500 = v[7:16,3,:,:] 



    # 返回处理数据
    # 这里的数据有很多变量,每个变量都是三维的数组,总体上是四维数组
    data = {
            'vo_400':vo_400,
            'z_400':z_400,
            'vo_450':vo_450,
            'z_450':z_450,
            'vo_500':vo_500,
            'z_500':z_500,
            'vo_550':vo_550,
            'z_550':z_550,
            # 'u_400':u_400,
            # 'v_400':v_400,
            'u_500':u_500,
            'v_500':v_500
    }
    return data

if __name__ == "__main__":
    a = read()
    print(a['vo_500'])
    