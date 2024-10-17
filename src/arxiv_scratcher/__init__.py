
from arxiv_scratcher.constant import arxiv_prefix, arxiv_cs_cl_url, instructions, prefix_foler
from arxiv_scratcher.entity import Paper, ChatModel
from arxiv_scratcher.APIKEY import ZHIPU_KEY
import requests
import json
import os
from bs4 import BeautifulSoup


def scratcher(folder_name="default"):

    response = requests.get(arxiv_cs_cl_url)
    soup = BeautifulSoup(response.text, "html.parser")

    link = soup.find_all("a", title="Abstract")
    title = soup.find_all("div", class_="list-title mathjax")
    abstract = soup.find_all("p", class_="mathjax")

    paper_lst = []
    for link, title, abstract in zip(link, title, abstract):
        paper = Paper(title.text.split('\n')[1].strip(
        ), abstract.text.strip(), arxiv_prefix+link['href'])
        paper_lst.append(paper.get())

    if os.path.exists(f'{folder_name}/papers.json'):
        return
    with open(f'{folder_name}/papers.json', 'w+') as f:
        json.dump(paper_lst, f, indent=4)


def init():
    import os
    from datetime import datetime

    current_time = datetime.now()
    folder_name = prefix_foler + current_time.strftime("%Y-%m-%d")

    try:
        os.makedirs(folder_name, exist_ok=True)
        print(f"文件夹 '{folder_name}' 创建成功！")
    except Exception as e:
        print(f"创建文件夹时出错: {e}")
    return folder_name


def instruct_reader(folder_name):
    input_text = ''
    with open(f'{folder_name}/papers.json', 'r', encoding='utf-8') as file:
        paper_list = json.load(file)  # 将 JSON 数据加载到字典中
    for paper in paper_list[:min(50, len(paper_list))]:
        input_text = input_text + paper['title'] + '\n'
    return paper_list, input_text+instructions


def main():
    folder_name = init()
    scratcher(folder_name)

    paper_list, input_text = instruct_reader(folder_name)

    if not os.path.exists(f'{folder_name}/overview.md'):

        chatmodel = ChatModel(ZHIPU_KEY)
        response = chatmodel.chat(input_text)
        # print(response)

        with open(f'{folder_name}/overview.md', 'w+') as f:
            f.write(response)

    with open(f'{folder_name}/overview.md', 'r') as f:
        overview = f.readlines()

    new_overview = []
    for line in overview:
        new_overview.append(line)
        for paper in paper_list:
            if paper['title'] in line:
                new_overview.append(
                    f"摘要\n{paper['abstract']} \n[{paper['title']}]({paper['url']})\n")

    # print(new_overview)
    with open(f'{folder_name}/new_overview.md', 'w+') as f:
        f.writelines(new_overview)
