import argparse
import glob
import os
import time
from utils import get_embed
from notion_helper import NotionHelper

def rename_file_to_timestamp(type):
    # 指定目录路径
    directory_path = './OUT_FOLDER'
    
    # 查找并删除目录下所有以type开头的.svg文件
    for file in glob.glob(os.path.join(directory_path, f"{type}_*.svg")):
        os.remove(file)
        print(f"Deleted {file}")

    # 获取当前时间戳，转换为整数
    timestamp = int(time.time())
    
    # 构造新的文件名，使用type参数和当前时间戳
    new_file_name = f"{type}_{timestamp}.svg"
    # 构造新的文件路径
    new_file_path = os.path.join(directory_path, new_file_name)
    
    # 指定原始文件路径
    original_file_path = os.path.join(directory_path, 'notion.svg')
    
    # 重命名文件
    os.rename(original_file_path, new_file_path)
    return new_file_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type")
    options = parser.parse_args()
    type = options.type
    is_movie = True if type=="movie" else False
    notion_url = os.getenv("NOTION_MOVIE_URL") if is_movie else os.getenv("NOTION_BOOK_URL")
    notion_helper = NotionHelper(notion_url)
    image_file = rename_file_to_timestamp(type)
    if image_file:
        image_url = f"https://raw.githubusercontent.com/{os.getenv('REPOSITORY')}/{os.getenv('REF').split('/')[-1]}/OUT_FOLDER/{image_file}"
        heatmap_url = f"https://heatmap.malinkang.com/?image={image_url}"
        if notion_helper.heatmap_block_id:
            response = notion_helper.update_heatmap(
                block_id=notion_helper.heatmap_block_id, url=heatmap_url
            )
        else:
            response = notion_helper.append_blocks(
                block_id=notion_helper.page_id, children=[get_embed(heatmap_url)]
            )