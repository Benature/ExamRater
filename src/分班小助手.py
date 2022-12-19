import pandas as pd
import os

excel_path = input('问卷星 excel 文件名/路径（带后缀）：\n')
df = pd.read_excel(excel_path)

names = df['用户名'].tolist()
classes = df['班别'].tolist()

name2class = dict(zip(names, classes))

dir_path = input('附件路径：\n')
file_list = os.listdir(dir_path)

errors = []

for i, file in enumerate(file_list):
    filetype = file.split('.')[-1]
    if filetype.lower() not in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
        continue
    index, name, field = file.split('_')[:3]
    try:
        c = name2class[name]
        print(name, c)
        new_dir = os.path.join(dir_path, str(c))
        new_dir = os.path.join(new_dir, field)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        os.rename(os.path.join(dir_path, file), os.path.join(new_dir, file))
    except KeyError:
        errors.append(name)

if errors:
    print("没有这些人：")
    print(errors)
    input('回车结束程序')
