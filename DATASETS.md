<p align="center" width="60%">
<img src="LOGO.png"  width="40%" height="40%">
</p>
  
# <div align="center">LLMDataHub: Datasets </div>
----------------------------------
<p align="center">
  🔥 <a href="DATASETS.md#general_aligment">Alignment Datasets</a> • 💡 <a href="DATASETS.md#domain-specific">Domain-specific Datasets</a> • :atom: <a href="DATASETS.md#pretrain">Pretraining Datasets</a> • 🖼️ <a href="DATASETS.md#multimodal">Multimodal Datasets</a> <br> 
</p>

<p align="center">
<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Project-Hierion/LLMDataHub"> <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Project-Hierion/LLMDataHub"> <img alt="Repo Automation Status" src="https://github.com/Project-Hierion/LLMDataHub/actions/workflows/vault-check.yml/badge.svg">
</p>

# Dataset Collections By Most Recent And In Alphabetical Order

**🤑 = HuggingFace-hosted (link omitted).** Following Nvidia's acquisition of HF (Sept 2026), we no longer link to their platform. Seek mirrors or GitHub sources. See full note at the bottom of this page. Let's keep open-source, open. Together.

## Table of Contents
- [General Open Access Datasets for Alignment](#general_aligment)
  - [2026](#datasets-2026)
  - [2025](#datasets-2025)
  - [2024](#datasets-2024)
  - [2023](#datasets-2023)
- [Open Datasets for Pretraining](#pretrain)
- [Domain-specific Datasets](#domain-specific)
- [Multimodal Datasets for VLM](#multimodal)
- [Private Datasets](#private-datasets)
- [HuggingFace-Hosted Datasets](#hf-datasets)

## <div id="general_aligment">General Open Access Datasets for Alignment 🟢</div>

#### Type Tags 🏷️:
- **SFT:** Supervised Finetune
  - Dialog: Each entry contains continuous conversations 
  - Pairs: Each entry is an input-output pair 
  - Context: Each entry has a context text and related QA pairs
- **PT:** pretrain
- **CoT:** Chain-of-Thought Finetune
- **RLHF:** train reward model in Reinforcement Learning with Human Feedback 
- **DPO:** Direct Preference Optimization

### <div id="datasets-2026">2026</div>

<details>
  <summary>📁 2026 Datasets</summary>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [MetaMathQA](https://github.com/microsoft/LLaVA-MetaMath) | — | SFT | English | 395K | Math QA dataset for instruction tuning. Improves math reasoning in LLMs. |
| [RIF-Layoff-Dataset](https://github.com/davidfue/RIF-Layoff-Dataset) | — | Dataset | English | — | Schema and records for RIF (Reduction in Force) tracking. |

</details>

### <div id="datasets-2025">2025</div>

<details>
  <summary>📁 2025 Datasets</summary>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [ClickHouse/ClickBench](https://github.com/ClickHouse/ClickBench) | — | Benchmark | — | — | ClickBench: a Benchmark For Analytical Databases. |
| [Wider-Community/quranic-universal-audio](https://github.com/Wider-Community/quranic-universal-audio) | — | Audio Dataset | — | — | Unified audio and timing for Qur'an apps, developers, and researchers. |
| [MixtureVitae](https://github.com/ontocord/mixturevitae) | — | PT | English | 50B–300B tokens | Permissive-first pretraining corpus. Outperforms FineWeb-Edu on math and code. |
| [ROOTS](https://github.com/bigscience-workshop/roots-data) | BLOOM | PT | Multilingual, code | 1.6TB | Diverse open-source pretraining dataset. |

</details>

### <div id="datasets-2024">2024</div>

<details>
  <summary>📁 2024 Datasets</summary>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [the-stack](https://github.com/bigcode-project/the-stack) | — | PT | Multilingual (code) | 6TB | Large-scale source code dataset for pretraining. 358 programming languages. |

</details>

### <div id="datasets-2023">2023</div>

<details>
  <summary>📁 2023 Datasets</summary>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [helpSteer](HF-hosted (no link) 🤑) | / | RLHF | English | 37k instances | RLHF dataset annotated by human with helpfulness, correctness, coherence, complexity and verbosity measures. |
| [no_robots](HF-hosted (no link) 🤑) | / | SFT | English | 10k instance | High-quality human-created SFT data, single turn. |
| [Anthropic_HH_Golden](HF-hosted (no link) 🤑) | ULMA | SFT / RLHF | English | train 42.5k + test 2.3k | Improved on the harmless dataset of Anthropic's Helpful and Harmless (HH) datasets. |
| [AmericanStories](HF-hosted (no link) 🤑) | / | PT | English | / | Vast sized corpus scanned from US Library of Congress. |
| [dolma](HF-hosted (no link) 🤑) | OLMo | PT | / | 3T tokens | A large diverse open-source corpus for LM pretraining. |
| [function_calling_extended](HF-hosted (no link) 🤑) | / | Pairs | English/code | / | High quality human created dataset for enhancing LM's API using ability. |
| [LongBench](HF-hosted (no link) 🤑) | / | Evaluation Only | English/Chinese | 17 tasks | A benchmark for evaluating LLM's long context understanding capability. |
| [Platypus](HF-hosted (no link) 🤑) | Platypus2 | Pairs | English | 25K | A very high quality dataset for improving LM's STEM reasoning ability. |
| [Puffin](HF-hosted (no link) 🤑) | Redmond-Puffin Series | Dialog | English | ~3k entries | Conversations between real human and GPT-4 with long context. |
| [tiny series](HF-hosted (no link) 🤑) | / | Pairs | English | / | A series of short and concise codes or texts for improving LM's reasoning ability. |

</details>

---

## <div id="pretrain">Open Datasets for Pretraining 🟢 :atom:</div>

<details>
  <summary>📁 Pretraining Datasets</summary>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [C4](HF-hosted (no link) 🤑) | Google T5 Series, LLaMA | PT | English | 305GB | A colossal, cleaned version of Common Crawl's web crawl corpus. |
| [CBook-150K](https://github.com/FudanNLPLAB/CBook-150K) | / | PT, building dataset | Chinese | 150K+ books | A raw Chinese books dataset. |
| [CLUECorpus](https://github.com/CLUEbenchmark/CLUE) | / | PT, finetune, evaluation | Chinese | 100GB | A Chinese pretraining Corpus sourced from Common Crawl. |
| [Common Crawl](https://commoncrawl.org/) | LLaMA (After some process) | building datasets, PT | / | / | The most well-known raw dataset. |
| [falcon-refinedweb](HF-hosted (no link) 🤑) | tiiuae/falcon series | PT | English | / | A refined subset of CommonCrawl. |
| [Gutenberg project](https://www.gutenberg.org/policy/robot_access.html) | LLaMA | PT | Multilingual | / | A book dataset, mostly novels. |
| [nlp_Chinese_Corpus](https://github.com/brightmart/nlp_chinese_corpus) | / | PT,TF | Chinese | / | A Chinese pretrain corpus. |
| [NMBVC](https://github.com/esbatmop/MNBVC) | / | PT | Chinese | / | A large scale, continuously updating Chinese pretraining dataset. |
| [peS2o](HF-hosted (no link) 🤑) | / | PT | English | 7.5GB | A high quality academic paper dataset for pretraining. |
| [proof-pile](HF-hosted (no link) 🤑) | proof-GPT | PT | English/LaTeX | 13GB | A pretraining dataset with LaTeX corpus to enhance LM's ability in proof. |
| [Pushshift reddit](https://files.pushshift.io/reddit/) | OPT-175b | PT | / | / | Raw reddit data. |
| [ROOTS](HF-hosted (no link) 🤑) | BLOOM | PT | Multilingual, code | 1.6TB | A diverse open-source dataset for language modeling. |
| [SlimPajama](HF-hosted (no link) 🤑) | / | PT | Primarily English | / | A cleaned and deduplicated version of RedPajama. |
| [StackOverflow post](HF-hosted (no link) 🤑) | / | PT | / | 35GB | Raw StackOverflow data in markdown format. |
| [The Pile (V1)](https://pile.eleuther.ai/) | GLM, LLaMA, GPT-J, GPT-NeoX-20B, Cerebras-GPT, OPT-175b | PT | Multilingual, code | 825GB | A diverse open-source language modeling dataset. |

</details>

---

## <div id="domain-specific">Domain-specific Datasets 🟢 💡</div>

<details>
  <summary>📁 Domain-specific Datasets</summary>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [awesome chinese legal resources](https://github.com/pengxiao-song/awesome-chinese-legal-resources) | LaWGPT | / | Chinese | / | A collection of Chinese legal data for LLM training. |
| [ChatGPT-Jailbreak-Prompts](HF-hosted (no link) 🤑) | / | / | English | 163KB | Prompts for bypassing safety regulation of ChatGPT. |
| [code_instructions_120k_alpaca](HF-hosted (no link) 🤑) | / | Pairs | English/code | 121,959 entries | Code instruction dataset in instruction finetune format. |
| [finance-alpaca](HF-hosted (no link) 🤑) | / | Pairs | English | 1.3K entries | An Alpaca-style dataset focusing on financial topics. |
| [FinNLP](https://github.com/AI4Finance-Foundation/FinNLP) | FinGPT | Raw data | English, Chinese | / | Open-source raw financial text data. |
| [function-invocations-25k](HF-hosted (no link) 🤑) | some MPT variants | Pairs | English code | 25K entries | Teach AI models how to correctly invoke API functions. |
| [instructional_codesearchnet_python](HF-hosted (no link) 🤑) | / | Pairs | English & Python | 192MB | Instructional Python dataset for the Open-Assistant project. |
| [Long Form](https://github.com/akoksal/LongForm) | / | Pairs | English | 23.7K entries | Improve the long text generation ability of LLMs. |
| [MeChat data](https://github.com/qiuhuachuan/smile) ⚠️use with care | MeChat | Dialog | Chinese | 355733 utterances | A Chinese SFT dataset for training a mental healthcare chatbot. |
| [phi-1](HF-hosted (no link) 🤑) | phi-1 | Dialog | English | / | Math and CS problems generated using the method in "Textbooks Are All You Need". |
| [PRM800K](https://github.com/openai/prm800k) | A variant of GPT-4 | Context | English | 800K entries | A process supervision dataset for mathematical problems. |
| [Safety Prompt](https://github.com/thu-coai/Safety-Prompts) | / | Evaluation only | Chinese | 100k entries | Chinese safety prompts for evaluating and improving the safety of LLMs. |
| [starcoderdata](HF-hosted (no link) 🤑) | starcoder series | PT | code | 783GB | A large pretraining dataset for improving LM's coding ability. |
| [symbolic-instruction-tuning](HF-hosted (no link) 🤑) | / | Pairs | English, code | 796 | Focuses on 'symbolic' tasks like SQL coding and mathematical computation. |
| [Tapir-Cleaned](HF-hosted (no link) 🤑) | / | Pairs | English | 116k entries | Revised version of the DAISLab dataset, cleaned and scored for instruction-tuning. |
| [TheoremQA](HF-hosted (no link) 🤑) | / | Pairs | English | 800 | A high quality STEM theorem QA dataset. |

</details>

---

## <div id="multimodal">Multimodal Datasets for VLM 🖼️</div>

<details>
  <summary>📁 Multimodal Datasets</summary>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [JourneyDB](HF-hosted (no link) 🤑) | / | image-prompt-caption | English | 4M instances | QA, caption, and text prompting tasks based on Midjourney images. |
| [LLaVA Instruction](HF-hosted (no link) 🤑) | LLaVA | instruction-image | English | 158k samples | Multimodal dataset generated from COCO dataset by prompting GPT-4. |
| [M3IT](HF-hosted (no link) 🤑) | Ying-VLM | instruction-image | Multilingual | 2.4M instances | 40 tasks with 400 human written instructions. |
| [MIMIC-IT](https://github.com/Luodian/Otter/tree/main/mimic-it) | Otter | instruction-image | Multilingual | 2.2M instances | High quality multi-modal instruction-response pairs based on images and videos. |
| [OBELICS](HF-hosted (no link) 🤑) | idefics series | image-document | English | 141M documents | An open, massive, and curated collection of interleaved image-text web documents. |
| [ShareGPT4V](HF-hosted (no link) 🤑) | / | image-prompt-caption | English | 1.2M instances | GPT4-Vision-powered multi-modal captions data. |

</details>

---

## <div id="private-datasets">Private Datasets 🔴</div>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [MassiveText](https://arxiv.org/abs/2112.11446) | Gopher, Chinchilla | PT | 99% English, 1% other | | A massive curated dataset for training Gopher and Chinchilla models. |
| [WebText (Reddit links)](https://openai.com/blog/better-language-models/) | GPT-2 | PT | English | / | Data crawled from Reddit and filtered for GPT-2 pretraining. |
| [WuDao (悟道) Corpora](https://wudaoai.cn/) | GLM | PT | Chinese | 200GB | A large scale Chinese corpus, originally open-sourced but not available now. |

---

## <div id="hf-datasets">HuggingFace-Hosted Datasets</div>

*The following datasets are hosted exclusively on HuggingFace. We do not provide links to their platform following Nvidia's acquisition (Sept 2026). These entries are maintained for reference only. If you find a non-HF source for any of these, please contribute it.*

🤑 = HuggingFace-hosted (link omitted)

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| *No HF-hosted datasets currently listed.* | | | | | |

---

## Contact 📬

**Original project authors:**
- [Junhao Zhao](zhaol9555@gmail.com) 📧  
- Advised by [Prof. Wanyun Cui](https://cuiwanyun.github.io/) [![GitHub.io](https://img.shields.io/badge/GitHub.io-@cuiwanyun-green.svg)](https://cuiwanyun.github.io/)

---

**Project Hierion maintainers:**
- [project-hierion@proton.me](mailto:project-hierion@proton.me)
- **ORCID:** [![ORCID](https://img.shields.io/badge/ORCID-0009--0000--8877--2731-A6CE39?style=flat&logo=orcid&logoColor=white)](https://orcid.org/0009-0000-8877-2731)

*Our work is open, traceable, and part of the scientific record.*

---

*With gratitude and much respect to the community, for providing such useful resources, [Project-Hierion](https://github.com/Project-Hierion) will attempt to maintain and keep this forked branch of the original [LLMDataHub](https://github.com/Zjh-819/LLMDataHub) by Junhao Zhao, up to date and current. 🙏*

---

**📌 Note on HuggingFace links:**  
Following Nvidia's acquisition of HuggingFace (September 2026), this archive no longer links directly to HF-hosted datasets. We believe in open infrastructure, not corporate consolidation. Datasets hosted exclusively on HF are marked `🤑` and quarantined in the HuggingFace-Hosted Datasets section at the bottom of this page — no links, no traffic. We encourage users to seek out mirrors, GitHub repos, or paper sources. If you find a non-HF link for a dataset, please contribute it. Let's keep open-source, open. Together.
