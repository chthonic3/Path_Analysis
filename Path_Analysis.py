#pyinstaller -F Path_Analysis.py 封裝執行檔
#V1.0.1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection


file_path='QJM_model.csv'
#file_path=input('請輸入csv檔路徑名稱\n')

def Plot3DPoints(X,Y,Z,depvarb):
    fig = plt.figure()
    ax = plt.axes(projection= '3d')
    lc=ax.scatter(X, Y, Z, marker ='.',c=depvarb)
    #軸向標籤
    ax.set_xlabel('X axis', color = 'b')
    ax.set_ylabel('Y axis', color='b')
    ax.set_zlabel('Z axis', color='b')
    #顯示圖示區域的軸範圍
    ax.set_xlim(X.min(), X.max())
    ax.set_ylim(Y.min(), Y.max())
    ax.set_zlim(Z.min(), Z.max())
    plt.colorbar(lc)
    plt.title(selected)
    #plt.clf
    plt.show()
    

def Plot3Dline(X,Y,Z,depvarb):
    points = np.array([X, Y, Z]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    fig = plt.figure()
    ax = plt.axes(projection= '3d')
    lc = Line3DCollection(segments, cmap='viridis')
    lc.set_array(depvarb)#設定顏色範圍
    lc.set_linewidth(1)
    ax.add_collection(lc)
    #軸向標籤
    ax.set_xlabel('X axis', color = 'b')
    ax.set_ylabel('Y axis', color='b')
    ax.set_zlabel('Z axis', color='b')
    #顯示圖示區域的軸範圍
    ax.set_xlim(X.min(), X.max())
    ax.set_ylim(Y.min(), Y.max())
    ax.set_zlim(Z.min(), Z.max())
    plt.colorbar(lc)
    plt.title(selected)
    #plt.clf
    plt.show()

#用PANDAS讀CSV檔    
  
df=pd.read_csv(file_path, delimiter=";",usecols=[
                                                "          s act/X1", 
                                                "          s act/Y1", 
                                                "          s act/Z1",
                                                "         s diff/X1",
                                                "         s diff/Y1",
                                                "         s diff/Z1",
                                                "    v act vctrl/X1",
                                                "    v act vctrl/Y1",
                                                "    v act vctrl/Z1",
                                                ])

#重新命名Colums名稱
df = df.rename(columns={"          s act/X1": "act/X1", 
                        "          s act/Y1": "act/Y1",
                        "          s act/Z1": "act/Z1",
                        "         s diff/X1": "diff/X1",
                        "         s diff/Y1": "diff/Y1",
                        "         s diff/Z1": "diff/Z1",
                        "    v act vctrl/X1": "v act vctrl/X1",
                        "    v act vctrl/Y1": "v act vctrl/Y1",
                        "    v act vctrl/Z1": "v act vctrl/Z1",
                        })
#重新排列column
column_names = ["act/X1","act/Y1","act/Z1", "diff/X1", "diff/Y1", "diff/Z1","v act vctrl/X1", "v act vctrl/Y1", "v act vctrl/Z1"]
df = df.reindex(columns=column_names)

#顏色的參考是用那個資料去做
j=0
for i in df.columns[3:]:
    print('參考資料 {} 請選擇 {} '.format(i,j))
    j+=1
selected_data = input('選擇參考項目?\n')
selected = df.columns[int(selected_data)+3]

#參考資料是否取絕對值，一般是
inputvalue = input('是否取絕對值 Yes(Y)/no(n)\n')
if inputvalue == 'Y' or inputvalue =='Yes' or inputvalue == 'yes' or inputvalue == 'y':
    ignore_minus = True
else:
    ignore_minus = False

#是否軸向過濾程式
filter_value = input('是否需軸向過濾程式 Yes(Y)/no(n)\n')
if filter_value == 'Y' or filter_value =='Yes' or filter_value == 'yes' or filter_value == 'y':
    while True:
        k=0
        #軸向的選擇X、Y、Z
        for i in df.columns[0:3]:
            print(f'選擇軸向 {i} 請選擇 {k}')
            k+=1
        filter_data = input('選擇參考項目?\n')

        filter = df.columns[int(filter_data)]
        #顯示資料的百分比占比20%、50%、80%
        print(df[filter].describe(percentiles=[.2,.5,.8]))
        filter_select = input('請選擇分割位置\n')
        #要保留的資料區域，所以顯示會是切割的正或負
        direction_select = input('請選擇顯示正負方向 "+" 或 "-"\n')
        if direction_select == '-':
            filt = (df[filter] <= int(filter_select))
            df = df[filt]
        elif direction_select == '+':
            filt = (df[filter] >= int(filter_select))
            df = df[filt]
        #重複詢問是否繼續切割程式
        continue_filt=input('是否仍需軸向過濾Yes(Y)/no(n)\n')
        if continue_filt == 'Y' or continue_filt =='Yes' or continue_filt == 'yes' or continue_filt == 'y':
            continue
        elif continue_filt == 'N' or continue_filt =='No' or continue_filt == 'no' or continue_filt == 'n':
            break
        #print(df)

#是否順序拆程式
split_value = input('分割程式 Yes(Y)/no(n)\n')
if split_value == 'Y' or split_value =='Yes' or split_value == 'yes' or split_value == 'y':
    #計算df總共多少數量
    print('此程式共 {} 單節:'.format(df.shape[0]))
    prog_range_start=input('開始單節: ')
    prog_range_end=input('結束單節: ')
    #如切割就將新資料丟入df1
    df1=df.iloc[int(prog_range_start):int(prog_range_end),0:9]
    xarray = df1["act/X1"]
    yarray = df1["act/Y1"]
    zarray = df1["act/Z1"]
    if ignore_minus == True:
        plotdata =abs(df1[selected])
    else:
        plotdata =df1[selected]
#不切就用原本的df
else:
    xarray = df["act/X1"]
    yarray = df["act/Y1"]
    zarray = df["act/Z1"]
    if ignore_minus == True:
        plotdata =abs(df[selected])
    else:
        plotdata =df[selected]

#輸出線圖或點圖
while True:
    try:
        Line_Point = int(input('請輸入點圖型 : 0 或 線圖型 : 1\n'))
        if Line_Point>1:
            assert False, '請輸入數值"0"或"1"'
        if Line_Point==0:
            Plot3DPoints(xarray, yarray, zarray, plotdata)
        elif Line_Point==1:
            Plot3Dline(xarray, yarray, zarray, plotdata)
        break
    except AssertionError as msg:
        print(msg)
    except :
            print('輸入錯誤')