# /dev/null

> 记下生活，也留下学过的。

一个安静的角落。<https://notguigao-afk.github.io/>

---

Hugo 生成，PaperMod 打底，剩下的都是自己的。暖白纸面，暗红边批，宋体标题配黑体正文，明暗皆宜。

没什么宏大叙事，只是一些不想被忘掉的东西。

## 本地跑起来

```bash
git clone --recurse-submodules <repo-url>
hugo server -D
```

## 部署

推到 `main`，GitHub Actions 自己会把它送到该去的地方。

## AI 边批

每篇文章末尾有独立署名的 AI 边批，保存在 `data/annotations.toml`。新文章需要补写对应边批和真实的模型／effort 署名，详见 `docs/brand-notes.md`。

构建后运行 `python3 scripts/ux_invariants.py`（Python 3.11+），检查页面与边批是否完整。
