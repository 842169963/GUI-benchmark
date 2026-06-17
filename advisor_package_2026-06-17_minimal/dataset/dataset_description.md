# Dataset Description

The current Track B pilot uses a reduced subset derived from Vision2Web.

Links:

- Hugging Face dataset: https://huggingface.co/datasets/zai-org/Vision2Web
- GitHub repository: https://github.com/zai-org/Vision2Web
- Paper: https://arxiv.org/abs/2603.26648

Current normalized local subset:

- 14 total items,
- 10 Level 2 frontend items,
- 4 Level 1 static webpage/control items,
- Level 3 full-stack items excluded because they require backend state,
  deployment, authentication, and longer workflows.

The included sample item is `sample_item_F01`:

- `requirement.md`: natural-language requirement given to the generator model,
- `workflow.json`: actions and validations,
- `source_meta.json`: source dataset metadata.

Open review question:

- Is this Vision2Web-derived subset suitable for the thesis benchmark, or should
  the benchmark use a more abstract dataset with more design freedom?
