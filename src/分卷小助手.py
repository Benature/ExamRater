# encoding=utf-8
import zipfile
import os
import re

root_path = os.path.dirname(os.path.abspath(__file__))
dir_path = root_path

if dir_path[0] == '/':
    dir_path = input('请把解压后的文件夹拖到此处(然后回车)\n')
    dir_path = dir_path.replace('\\', '').strip()
    dir_path = os.path.abspath(dir_path)

print("准备开始整理该文件夹下图片")
print(dir_path)

# dir_path = '60524125_附件 (1)'

file_list = os.listdir(dir_path)
L = len(file_list)

zip_list = []
csvs = {}
for i, file in enumerate(file_list):
    if '.' not in file:
        continue
    filetype = file.split('.')[-1]
    if filetype.lower() not in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
        continue
    print(int(i / L * 100), end='%  ')
    index, name, field = file.split('_')[:3]
    index = index.strip('序号 ').zfill(3)
    field = (re.findall(r"(\d+) *题", field) or [field])[0]
    print(file, " -> ", index, name, field, sep="\t")
    new_dir = os.path.join(dir_path, field)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
        zip_list.append(new_dir)
    filename = f"{index}_{name}.{filetype}"
    os.rename(os.path.join(dir_path, file), os.path.join(new_dir, filename))
    # fpath = os.path.join(dir_path, field, filename)
    fpath = os.path.join('..', field, filename)
    csv_line = f"{index}, {name}, {fpath},-1"
    if field not in csvs.keys():
        csvs[field] = [csv_line]
    else:
        csvs[field].append(csv_line)


def zip_dir(dir_path):
    file_news = dir_path.rstrip('/\\') + '.zip'  # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(dir_path):
        fpath = dirpath.replace(dir_path, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
            print('压缩成功', file_news)
    z.close()


if not os.path.exists(os.path.join(root_path, 'output')):
    os.mkdir(os.path.join(root_path, 'output'))

for key, value in csvs.items():
    with open(f'output/{key}.csv', 'w') as f:
        f.write("\n".join(value))

for zip_ in zip_list:
    zip_dir(zip_)
