# arxiv-scratcher

- A tool to scatch the paper from Arxiv
- Applying ChatGLM to summarize these papers

使用ChatGLM API对爬取到的论文进行分类和预览

## Requirement

install rye in you computer
[rye doc](https://rye.astral.sh/guide/installation/)

## Usage

creat `src/APIKEY.py` and Write you key, you can get it form [zhipuapi](https://open.bigmodel.cn/)

```python
ZHIPU_key
```

then

```shell
rye run arxiv-scratcher
```

you can get res in dictionary `data`
