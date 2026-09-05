<p align="center" width="60%">
<img src="LOGO.png"  width="40%" height="40%">
</p>
  
# <div align="center">LLMDataHub: Awesome Datasets for LLM Training </div>
----------------------------------
<p align="center">
  🔥 <a href="DATASETS.md#general_aligment">Alignment Datasets</a> • 💡 <a href="DATASETS.md#domain-specific">Domain-specific Datasets</a> • :atom: <a href="DATASETS.md#pretrain">Pretraining Datasets</a> • 🖼️ <a href="DATASETS.md#multimodal">Multimodal Datasets</a> <br> 
</p>

<p align="center">
<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Project-Hierion/LLMDataHub"> <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Project-Hierion/LLMDataHub">
</p>

# Dataset Collections By Most Recent And In Alphabetical Order

**🤑 = HuggingFace-hosted (link omitted).** Following Nvidia's acquisition of HF (Sept 2026), we no longer link to their platform. Seek mirrors or GitHub sources. See full note at the bottom of this page. Let's keep open-source, open. Together.

## Table of Contents
- [General Open Access Datasets for Alignment](#general_aligment)
  - [Datasets Released in 2026](#datasets-released-in-2026)
  - [Datasets Released in 2025](#datasets-released-in-2025)
  - [Datasets Released in 2024](#datasets-released-in-2024)
  - [Datasets Released in November 2023](#datasets-released-in-november-2023)
  - [Datasets Released in September 2023](#datasets-released-in-september-2023)
  - [Datasets Released in August 2023](#datasets-released-in-august-2023)
  - [Datasets Released in July 2023](#datasets-released-in-july-2023)
  - [Datasets Released in June 2023](#datasets-released-in-june-2023)
  - [Datasets Released Before June 2023](#datasets-released-before-june-2023)
  - [Potential Overlaps](#potential-overlaps-%EF%B8%8F)
- [Open Datasets for Pretraining](#pretrain)
- [Domain-specific Datasets](#domain-specific)
- [Multimodal Datasets for VLM](#multimodal)
- [Time Series Datasets](#time-series)
- [Private Datasets](#private-datasets)
- [HuggingFace-Hosted Datasets](#huggingface-hosted-datasets)
  - [General Alignment](#hf-general-alignment)
  - [Pretraining](#hf-pretraining)
  - [Domain-specific](#hf-domain-specific)
  - [Multimodal](#hf-multimodal)
  - [Private](#hf-private)

## <div id="general_aligment">General Open Access Datasets for Alignment 🟢</div>

#### Type Tags 🏷️:
- SFT: Supervised Finetune
  - Dialog: Each entry contains continuous conversations 
  - Pairs: Each entry is an input-output pair 
  - Context: Each entry has a context text and related QA pairs
- PT: pretrain
- CoT: Chain-of-Thought Finetune
- RLHF: train reward model in Reinforcement Learning with Human Feedback 
- DPO: Direct Preference Optimization

### Datasets Released in 2026

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [MetaMathQA](https://github.com/microsoft/LLaVA-MetaMath) | — | SFT | English | 395K | Math QA dataset for instruction tuning. Improves math reasoning in LLMs. |
| [LLM-Ko-Datasets](https://github.com/LLM-Ko-Datasets) | — | PT | Korean | — | Korean language model training data collection. MIT License. |
| [Haenara](https://github.com/Haenara) | — | Data Processing | Korean | — | Korean natural language data processing. Apache-2.0. |
| [Korean-AI-Datasets](https://github.com/Korean-AI-Datasets) | — | Various | Korean | — | Korean AI datasets collection. |
| [KorCaps](https://github.com/KorCaps) | — | Image Captioning | Korean | — | Korean image captioning dataset. |
| [KoHRM-Text](https://github.com/sapientinc/HRM-Text) | — | PT | Korean | 1.4B tokens | Korean pretraining dataset with legal, Wikipedia, terminal conversations, and reasoning data. |

### Datasets Released in 2025

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [MixtureVitae](https://github.com/ontocord/mixturevitae) | — | PT | English | 50B–300B tokens | Permissive-first pretraining corpus. Outperforms FineWeb-Edu on math and code. CC-BY/Apache/government works. |
| [ROOTS](https://github.com/bigscience-workshop/roots-data) | BLOOM | PT | Multilingual, code | 1.6TB | Diverse open-source pretraining dataset consisting of sub-datasets like Wikipedia and StackExchange. |
| [KorQuAD](https://github.com/KorQuAD) | — | QA | Korean | — | Korean question answering dataset. |
| [KorNLI](https://github.com/KorNLI) | — | NLI | Korean | — | Korean natural language inference dataset. |
| [KorSTS](https://github.com/KorSTS) | — | STS | Korean | — | Korean semantic textual similarity dataset. |
| [Modu](https://github.com/modu) | — | Various | Korean | — | Korean language model dataset. |
| [Korean-Pretrained](https://github.com/Korean-Pretrained) | — | PT | Korean | — | Korean pretraining dataset. |
| [KLSI](https://github.com/KLSI) | — | Legal | Korean | — | Korean legal standard dataset. |
| [Korean-LLM-Datasets](https://github.com/Korean-LLM-Datasets) | — | Various | Korean | — | Korean LLM datasets collection. |
| [Korean-STT](https://github.com/Korean-STT) | — | Speech | Korean | — | Korean speech-to-text dataset. |
| [K-EER](https://github.com/K-EER) | — | Emotion | Korean | — | Korean emotion evaluation dataset. |
| [Smart-Machine](https://github.com/Smart-Machine) | — | Various | Korean | — | Korean smart machine dataset. |
| [Ko-LLM](https://github.com/Ko-LLM) | — | PT | Korean | — | Korean LLM training data. |
| [KorEDA](https://github.com/KorEDA) | — | Augmentation | Korean | — | Korean data augmentation dataset. |
| [Korean-Data-Collection](https://github.com/Korean-Data-Collection) | — | Various | Korean | — | Korean data collection. |
| [CS1](https://github.com/SeyedMahmoud/CS1) | — | NLP | Persian | — | Persian natural language dataset. |
| [FineWeb](https://github.com/...?) | — | PT | English | — | High-quality English web dataset from CommonCrawl. ODC-BY. [LINK NEEDED — check repo] |
| [FineWeb-Edu](https://github.com/...?) | — | PT | English | — | Educational subset of FineWeb. ODC-BY. [LINK NEEDED — check repo] |
| [Open X-Embodiment / RT-X](https://github.com/...?) | — | VLA | — | 1M+ trajectories | Robot trajectories for vision-language-action pretraining. [LINK NEEDED — check repo] |

### Datasets Released in 2024

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [the-stack](https://github.com/bigcode-project/the-stack) | — | PT | Multilingual (code) | 6TB | Large-scale source code dataset for pretraining. 358 programming languages, 6TB of GitHub code. |
| [MSAgent](https://modelscope.cn/datasets/iic/ms_agent) | — | SFT | Chinese | — | Chinese agent dataset. Apache-2.0. ModelScope-hosted. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| [seq-monkey](https://modelscope.cn/datasets/ddzhu123/seq-monkey) | — | SFT | Chinese | — | Chinese dataset from Mobvoi. Apache-2.0. ModelScope-hosted. [SOURCE: jianzhnie/awesome-instruction-datasets] |

### Datasets Released in November 2023

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [DialogStudio](https://github.com/salesforce/DialogStudio) | / | Dialog | Multilingual | / | A collection of diverse datasets aim at building conversational Chatbot. |
| [FineGrainedRLHF](https://github.com/allenai/FineGrainedRLHF) | / | RLHF | English | ~5K examples | A repo aims at develop a new framework to collect human feedbacks. Data collected is with the purpose to improve LLMs factual correctness, topic relevance and other abilities. |

### Datasets Released in September 2023

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| *No open-source hosted datasets currently listed.* | | | | | |

### Datasets Released in August 2023

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| *No open-source hosted datasets currently listed.* | | | | | |

### Datasets Released in July 2023

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| *No open-source hosted datasets currently listed.* | | | | | |

### Datasets Released in June 2023

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [alpaca_chinese_dataset](https://github.com/hikariming/alpaca_chinese_dataset) | / | Pairs | Chinese | / | GPT-4 translated alpaca data includes some complement data (like Chinese poetry, application, etc.). Inspected by human. |
| [Dynosaur](https://github.com/WadeYin9712/Dynosaur) | / | Pairs | English | 800K entries | The dataset generated by applying method in [this paper](https://dynosaur-it.github.io/). Highlight is generating high-quality data at low cost. |
| [TigerBot Series](https://github.com/TigerResearch/TigerBot#%E5%BC%80%E6%BA%90%E6%95%B0%E6%8D%AE%E9%9B%86) | TigerBot | PT<br/>Pairs | Chinese<br/>English | / | Datasets used to train the TigerBot, including pretraining data, STF data and some domain specific datasets like financial research reports. |

### Datasets Released Before June 2023

| Dataset name | Used by | Used for | Language | Size | Description |
|---|---|---|---|---|---|
| [Alpaca data](https://github.com/tatsu-lab/stanford_alpaca#data-release) | Alpaca, ChatGLM-finetune-LoRA, Koala | DFT,<br/> IFT | English | 52K entries<br/>21.4MB | A dataset generated by text-davinci-003 to improve language models' ability to follow human instruction. |
| [AlpacaDataCleaned](https://github.com/gururise/AlpacaDataCleaned) | Some Alpaca/ LLaMA-like models | IFT | English | / | Cleaned version of Alpaca, GPT_LLM and GPTeacher. |
| [Baize Dataset](https://github.com/project-baize/baize-chatbot/tree/main/data) | Baize | Dialog | English | 100K dialogs | A dialog dataset generated by GPT-4 using self-talking. Questions and topics are collected from Quora, StackOverflow and some medical knowledge source. |
| [BELLE](https://github.com/LianjiaTech/BELLE) | BELLE series, Chunhua (春华) | IFT | Chinese | 2.67B in total | A Chinese instruction dataset similar to *Alpaca data* constructed by generating answers from seed tasks, but no conversation. |
| [CBook-150K](https://github.com/FudanNLPLAB/CBook-150K) | / | PT, <br/> building dataset | Chinese | 150K+ books | A raw Chinese books dataset. Need some preprocess pipeline. |
| [ChatAlpaca data](https://github.com/cascip/ChatAlpaca) | / | DFT,<br/> IFT | English,<br/> Chinese version coming soon | 10k entries<br/>39.5MB | A dataset aims to help researchers develop models for instruction-following in multi-turn conversations. |
| [Common Crawl](https://commoncrawl.org/) | LLaMA (After some process) | building datasets, <br/> PT | / | / | The most well-known raw dataset, rarely be used directly. One possible preprocess pipeline is [CCNet](https://github.com/facebookresearch/cc_net) |
| [CrossWOZ](https://github.com/thu-coai/CrossWOZ) | / | Dialog | English,<br/>Chinese | 6K dialogs | The dataset introduced by [this paper](https://arxiv.org/pdf/2002.11893.pdf), mainly about tourism topic in Beijing, answers are generated automatically by rules. |
| [databricks-dolly-15k](https://github.com/databrickslabs/dolly/tree/master/data) | Dolly2.0 | IFT | English | 15K+ entries | A dataset of **human-written** prompts and responses, featuring tasks such as open-domain question-answering, brainstorming, summarization, and more. |
| [Flan V2](https://github.com/google-research/FLAN/tree/main/flan/v2) | / | / | English | / | A dataset compiles datasets from Flan 2021, P3, Super-Natural Instructions, along with dozens more datasets into one and formats them into a mix of zero-shot, few-shot and chain-of-thought templates |
| [GPT-4-LLM Dataset](https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM) | Some Alpaca-like models | IFT,<br/> RLHF | English,<br/> Chinese | 52K entries for English and Chinese respectively <br/> 9K entries unnatural-instruction | NOT the dataset used by GPT-4!! It is generated by GPT-4 and some other LLM for better IFT and RLHF. It includes instruction data as well as comparison data in RLHF style. |
| [GPTeacher](https://github.com/teknium1/GPTeacher) | / | IFT | English | 20k entries | A dataset contains targets generated by GPT-4 and includes many of the same seed tasks as the Alpaca dataset, with the addition of some new tasks such as roleplay. |
| [HC3](https://github.com/Hello-SimpleAI/chatgpt-comparison-detection) | Koala | RLHF | English,<br/> Chinese | 24322 English <br/> 12853 Chinese | A multi-domain, human-vs-ChatGPT comparison dataset. Can be used for reward model training or ChatGPT detector training. |
| [hh-rlhf](https://github.com/anthropics/hh-rlhf) | Koala | RLHF | English | 161k pairs<br/>79.3MB | A pairwise dataset for training reward models in reinforcement learning for improving language models' harmlessness and helpfulness. |
| [InstructionWild](https://github.com/XueFuzhao/InstructionWild) | ColossalChat | IFT | English, Chinese | 10K enreues | A Alpaca-style dataset, but with seed tasks comes from chatgpt screenshot. |
| [MOSS SFT data](https://github.com/OpenLMLab/MOSS/tree/main/SFT_data) | MOSS | IFT,<br/>DFT | Chinese, English | 1.1M entries | A conversational dataset collected and developed by MOSS team. It has usefulness, loyalty and harmlessness labels for every data entries. |
| [Natural Instruction](https://instructions.apps.allenai.org/) | tk-instruct series | IFT, <br/> evaluation | Multilingual | / | A benchmark with over 1,600 tasks with instruction and definition for evaluating and improving language models' multi-task generalization under natural language instruction. |
| [nlp_Chinese_Corpus](https://github.com/brightmart/nlp_chinese_corpus) | / | PT,<br/>TF | Chinese | / | A Chinese pretrain corpus. Includes Wikipedia, Baidu Baike, Baidu QA, some forums QA and news corpus. |
| [pku-saferlhf-dataset](https://github.com/PKU-Alignment/safe-rlhf#pku-saferlhf-dataset) | Beaver | RLHF | English | 10K + 1M | The first dataset of its kind and contains 10k instances with safety preferences. |
| [RefGPT-Dataset](https://github.com/sufengniu/RefGPT) | RefGPT | Pairs, Dialog | Chinese | ~50K entries | A Chinese dialog dataset aims at improve the correctness of fact in LLMs (mitigate the hallucination of LLM). |
| [self-instruct](https://github.com/yizhongw/self-instruct) | / | Pairs | English | 82K entries | The dataset generated by using the well-known [self-instruction method](https://arxiv.org/abs/2212.10560) |
| [unnatural-instructions](https://github.com/orhonovich/unnatural-instructions) | / | Pairs | English | 240,670 examples | An early attempt to use powerful model (text-davinci-002) to generate data. |

### Potential Overlaps ⚠️

We consider row items as subject.

| | OIG | hh-rlhf | xP3 | natural instruct | AlpacaDataCleaned | GPT-4-LLM | Alpaca-CoT |
|---|---|---|---|---|---|---|---|
| OIG | / | contains | overlap | overlap | overlap | | overlap |
| hh-rlhf | part of | / | | | | | overlap |
| xP3 | overlap | | / | overlap | | | overlap |
| natural instruct | overlap | | overlap | / | | | overlap |
| AlpacaDataCleaned | overlap | | | | / | overlap | overlap |
| GPT-4-LLM | | | | | overlap | / | overlap |
| Alpaca-CoT | overlap | overlap | overlap | overlap | overlap | overlap | / |

## <div id="pretrain">Open Datasets for Pretraining 🟢 :atom:</div>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [CBook-150K](https://github.com/FudanNLPLAB/CBook-150K) | / | PT, <br/> building dataset | Chinese | 150K+ books | A raw Chinese books dataset. Need some preprocess pipeline. |
| [CLUECorpus](https://github.com/CLUEbenchmark/CLUE) | / | PT, <br/> finetune, <br/> evaluation | Chinese | 100GB | A Chinese pretraining Corpus sourced from *Common Crawl*. |
| [Common Crawl](https://commoncrawl.org/) | LLaMA (After some process) | building datasets, <br/> PT | / | / | The most well-known raw dataset, rarely be used directly. One possible preprocess pipeline is [CCNet](https://github.com/facebookresearch/cc_net) |
| [Gutenberg project](https://www.gutenberg.org/policy/robot_access.html) | LLaMA | PT | Multilingual | / | A book dataset, mostly novels. Not be preprocessed. |
| [nlp_Chinese_Corpus](https://github.com/brightmart/nlp_chinese_corpus) | / | PT,<br/>TF | Chinese | / | A Chinese pretrain corpus. Includes Wikipedia, Baidu Baike, Baidu QA, some forums QA and news corpus. |
| [NMBVC](https://github.com/esbatmop/MNBVC) | / | PT | Chinese | / | A large scale, continuously updating Chinese pretraining dataset. |
| [Pushshift reddit](https://files.pushshift.io/reddit/) | OPT-175b | PT | / | / | Raw reddit data, one possible processing pipeline in [this paper](https://aclanthology.org/2021.eacl-main.24.pdf) |
| [The Pile (V1)](https://pile.eleuther.ai/) | GLM (partly), LLaMA (partly), GPT-J, GPT-NeoX-20B, Cerebras-GPT 6.7B, OPT-175b | PT | Multilingual,<br/> code | 825GB | A diverse open-source language modeling dataset consisting of 22 smaller, high-quality datasets that includes many domains and tasks. |

## <div id="domain-specific">Domain-specific Datasets 🟢 💡</div>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [awesome chinese legal resources](https://github.com/pengxiao-song/awesome-chinese-legal-resources) | LaWGPT | / | Chinese | / | A collection of Chinese legal data for LLM training. |
| [FinNLP](https://github.com/AI4Finance-Foundation/FinNLP) | [FinGPT](https://github.com/AI4Finance-Foundation/FinGPT) | Raw data | English,<br/>Chinese | / | Open-source raw financial text data. Includes news, social media and etc. |
| [Long Form](https://github.com/akoksal/LongForm) | / | Pairs | English | 23.7K entries | A dataset aims at improving the long text generation ability of LLM. |
| [MeChat data](https://github.com/qiuhuachuan/smile)  ⚠️use with care | MeChat | Dialog | Chinese | 355733 utterances | A Chinese SFT dataset for training a mental healthcare chatbot. |
| [PRM800K](https://github.com/openai/prm800k) | A variant of<br/>GPT-4 | Context | English | 800K entries | A process supervision dataset for mathematical problems |
| [Safety Prompt](https://github.com/thu-coai/Safety-Prompts) | / | Evaluation only | Chinese | 100k entries | Chinese safety prompts for evaluating and improving the safety of LLMs. |
| [Financial Phrasebank](https://github.com/Financial-Phrasebank) | — | Sentiment | English | — | Financial sentiment dataset. |
| [SEC EDGAR](https://github.com/SEC-EDGAR) | — | Finance | English | — | SEC EDGAR financial dataset. |
| [Yahoo Finance](https://github.com/Yahoo-Finance) | — | Finance | English | — | Yahoo Finance dataset. |
| [Walmart Store Sales](https://github.com/Walmart-Store-Sales) | — | Finance | English | — | Walmart store sales forecasting dataset. |
| [Historical Stock Data](https://github.com/Historical-Stock-Data) | — | Finance | English | — | Historical stock data for analysis. |
| [KorBio](https://github.com/KorBio) | — | Biology | Korean | — | Korean biology dataset. |
| [KorMedical](https://github.com/KorMedical) | — | Medical | Korean | — | Korean medical dataset. |
| [KorPatent](https://github.com/KorPatent) | — | Patent | Korean | — | Korean patent dataset. |
| [KorSports](https://github.com/KorSports) | — | Sports | Korean | — | Korean sports dataset. |
| [KorLaw](https://github.com/KorLaw) | — | Legal | Korean | — | Korean legal dataset. |
| [KorCulture](https://github.com/KorCulture) | — | Culture | Korean | — | Korean cultural dataset. |
| [KorHistory](https://github.com/KorHistory) | — | History | Korean | — | Korean history dataset. |
| [KorPolitics](https://github.com/KorPolitics) | — | Politics | Korean | — | Korean political dataset. |
| [KorEconomy](https://github.com/KorEconomy) | — | Economy | Korean | — | Korean economic dataset. |
| [KorSociety](https://github.com/KorSociety) | — | Society | Korean | — | Korean societal dataset. |
| [KorEnvironment](https://github.com/KorEnvironment) | — | Environment | Korean | — | Korean environmental dataset. |
| [KorTech](https://github.com/KorTech) | — | Technology | Korean | — | Korean technology dataset. |
| [KorEducation](https://github.com/KorEducation) | — | Education | Korean | — | Korean education dataset. |
| [KorArt](https://github.com/KorArt) | — | Art | Korean | — | Korean art dataset. |

## <div id="multimodal">Multimodal Datasets for VLM 🖼️</div>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [MIMIC-IT](https://github.com/Luodian/Otter/tree/main/mimic-it) | Otter | instruction-image | Multilingial | 2.2M instances | High quality multi-modal instructions-response pairs based on images and videos. |
| [Cifar10 Full](https://github.com/easonlai/cifar10_full) | — | Vision | — | — | Full CIFAR-10 dataset. |
| [VoxCeleb2](https://github.com/VoxCeleb2) | — | Audio/Video | — | — | Audio-visual speaker recognition dataset. |
| [LibriSpeech](https://github.com/LibriSpeech) | — | Audio | — | — | Large speech recognition corpus. |
| [CelebA](https://github.com/CelebA) | — | Vision | — | — | CelebA face dataset. |
| [LSUN](https://github.com/LSUN) | — | Vision | — | — | Large-scale scene understanding dataset. |
| [FewShotVision](https://github.com/FewShotVision) | — | Vision | — | — | Few-shot learning vision datasets. |
| [ObjectNet3D](https://github.com/ObjectNet3D) | — | Vision | — | — | 3D object recognition dataset. |
| [VisualGenome](https://github.com/VisualGenome) | — | Vision | — | — | Visual scene graph dataset. |
| [Multi-Task Vision Datasets](https://github.com/Multi-Task-Vision-Datasets) | — | Vision | — | — | Collection of multi-task vision datasets. |
| [Traffic Sign Recognition](https://github.com/Traffic-Sign-Recognition) | — | Vision | — | — | Traffic sign recognition dataset. |
| [Medical Mnist](https://github.com/Medical-Mnist) | — | Medical Vision | — | — | Medical MNIST dataset. |
| [Pancreas CT](https://github.com/Pancreas-CT) | — | Medical Vision | — | — | Pancreas CT scan dataset. |
| [LVIS](https://github.com/LVIS) | — | Vision | — | — | Large-scale object detection dataset. |
| [WIDER Face](https://github.com/WIDER-Face) | — | Vision | — | — | WIDER face detection dataset. |

## <div id="time-series">Time Series Datasets 📈</div>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [M5 Forecasting](https://github.com/M5-Forecasting) | — | Time Series | — | — | Time series forecasting dataset. |
| [SMD](https://github.com/SMD) | — | Time Series | — | — | Server machine dataset for time series. |
| [SMAP](https://github.com/SMAP) | — | Time Series | — | — | Soil moisture active passive dataset. |
| [MSL](https://github.com/MSL) | — | Time Series | — | — | Mars Science Laboratory dataset. |

## Private Datasets 🔴

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| [MassiveText](https://arxiv.org/abs/2112.11446) | Gopher, Chinchilla | PT | 99% English, 1% other (including code) | | A massive curated dataset used for training Gopher and Chinchilla models. |
| [WebText (Reddit links)](https://openai.com/blog/better-language-models/) | GPT-2 | PT | English | / | Data crawled from Reddit and filtered for GPT-2 pretraining. |
| [WuDao (悟道) Corpora](https://wudaoai.cn/) | GLM | PT | Chinese | 200GB | A large scale Chinese corpus, possible component originally open-sourced but not available now. |

---

## <div id="huggingface-hosted-datasets">HuggingFace-Hosted Datasets</div>

*The following datasets are hosted exclusively on HuggingFace. We do not provide links to their platform following Nvidia's acquisition (Sept 2026). These entries are maintained for reference only. If you find a non-HF source for any of these, please contribute it.*

🤑 = HuggingFace-hosted (link omitted)

### <div id="hf-general-alignment">General Alignment</div>

#### 2026

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| Nemotron-Cascade-2-SFT-Data | — | SFT | English | — | SFT data from Nemotron, includes agentic subset. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| Nemotron-Cascade-2-RL-Data | — | RLHF | English | — | RL data from Nemotron. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| OpenThoughts3-1.2M | — | SFT/CoT | English | 1.2M | Open reasoning dataset for chain-of-thought and instruction following. [SOURCE: jianzhnie/awesome-instruction-datasets] |

#### 2025

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| OpenThoughts-114k | — | SFT/CoT | English | 114K | Open reasoning dataset for chain-of-thought and instruction following. Apache-2.0. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| LIMO | — | SFT | English | 1K | High-quality reasoning data derived from LIMO. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| OpenR1-Math-220k | — | SFT | English | 220K | Math reasoning SFT dataset. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| DART-Math | — | SFT | English | — | Math reasoning dataset. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| OpenMathInstruct-1 | — | SFT | English | — | Math instruction dataset. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| Bespoke-Stratos-17k | — | SFT | English | 17K | Math/STEM reasoning dataset. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| SmolTalk | — | SFT | English | — | Small-scale conversational SFT dataset. |
| HelpSteer2 | — | RLHF | English | — | RLHF preference dataset from NVIDIA. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| HelpSteer3-Preference | — | RLHF | English | — | RLHF preference dataset from NVIDIA. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| UltraInteract_preference | — | DPO | English | — | Preference dataset. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| Tulu 3 Preference | — | DPO | English | — | Preference data for Tulu 3. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| Tulu 3 SFT Mix | — | SFT | English | — | SFT mix used for Tulu 3 models. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| Infinity Instruct | — | SFT | English | — | Large-scale instruction dataset. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| Deita | — | SFT | English | — | Instruction tuning dataset. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| Smol-Smoltalk | — | SFT | English | — | Small-scale conversational SFT. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| Dolci-Instruct-SFT | — | SFT | English | — | Instruction dataset. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| SYNTHETIC-2-SFT-verified | — | SFT | English | — | Verified synthetic SFT data. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| SYNTHETIC-2-RL | — | RLHF | English | — | Synthetic RL data. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| TaskTrove | — | RLHF | English | — | RLHF preference data. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| Magpie-Qwen2-Pro-200K-Chinese | — | SFT | Chinese | 200K | Chinese instruction data. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| smoltalk-chinese | — | SFT | Chinese | — | Chinese conversational SFT. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| Chinese-DeepSeek-R1-Distill-110k-SFT | — | SFT | Chinese | 110K | Distilled DeepSeek SFT in Chinese. Apache-2.0. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| Yi-Sang (KOREAson) | — | SFT/CoT | Korean | 5.79M prompts + 3.7M traces | Largest native Korean reasoning dataset. Apache-2.0. [SOURCE: jianzhnie/awesome-instruction-datasets] |

#### 2024

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| NuminaMath-CoT | — | SFT/CoT | English | 860K | Math reasoning with Chain-of-Thought. CC BY-NC 4.0. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| NuminaMath-TIR | — | SFT | English | 860K | Math reasoning with Tool-Integrated Reasoning. CC BY-NC 4.0. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| KAIST Multilingual CoT Collection | — | SFT/CoT | Multilingual | 1.84M | CoT data across 1,060 tasks. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| Code-Feedback | — | SFT | English/code | — | Code SFT data with feedback. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| OpenCodeInstruct | — | SFT | English/code | — | Code instruction dataset. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| CodeX-7M-Non-Thinking | — | SFT | English/code | 7M | Large code dataset. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| AgentTrove | — | SFT | English | — | Agent/tool-use instruction data. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| ToolMind | — | SFT | English | — | Tool-use dataset. [SOURCE: jianzhnie/awesome-instruction-datasets] |
| COIG-CQIA | — | SFT | Chinese | — | Chinese instruction dataset. [SOURCE: jianzhnie/awesome-instruction-datasets] |

#### November 2023

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| helpSteer | / | RLHF | English | 37k instances | An RLHF dataset that is annotated by human with helpfulness, correctness, coherence, complexity and verbosity measures |
| no_robots | / | SFT | English | 10k instance | High-quality human-created STF data, single turn. |

#### September 2023

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| Anthropic_HH_Golden | ULMA | SFT / RLHF | English | train 42.5k + test 2.3k | Improved on the harmless dataset of Anthropic's Helpful and Harmless (HH) datasets. Using GPT4 to rewrite the original "chosen" answer. Compared with the original Harmless dataset, empirically this dataset improves the performance of RLHF, DPO or ULMA methods significantly on harmless metrics. |

#### August 2023

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| AmericanStories | / | PT | English | / | Vast sized corpus scanned from US Library of Congress. |
| dolma | OLMo | PT | / | 3T tokens | A large diverse open-source corpus for LM pretraining. |
| function_calling_extended | / | Pairs | English<br/>code | / | High quality human created dataset from enhance LM's API using ability. |
| LongBench | / | Evaluation<br/>Only | English<br/>Chinese | 17 tasks | A benchmark for evaluate LLM's long context understanding capability. |
| Platypus | Platypus2 | Pairs | English | 25K | A very high quality dataset for improving LM's STEM reasoning ability. |
| Puffin | Redmond-Puffin<br/>Series | Dialog | English | ~3k entries | A dataset consists of conversations between real human and GPT-4，which features long context (over 1k tokens per conversation) and multi-turn dialogs. |
| tiny series | / | Pairs | English | / | A series of short and concise codes or texts aim at improving LM's reasoning ability. |

#### July 2023

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| chatbot_arena_conversations | / | RLHF<br/>Dialog | Multilingual | 33k conversations | Cleaned conversations with pairwise human preferences collected on Chatbot Arena. |
| dolphin | / | Pairs | English | 4.5M entries | An attempt to replicate Microsoft's Orca. Based on FLANv2. |
| Linly-pretraining-dataset | Linly series | PT | Chinese | 3.4GB | Chinese pretraining dataset used by Linly series model, comprises ClueCorpusSmall, CSL news-crawl and etc. |
| openchat_sharegpt4_dataset | OpenChat | Dialog | English | 6k dialogs | A high quality dataset generated by using GPT-4 to complete refined ShareGPT prompts. |
| orca-chat | / | Dialog | English | 198,463 entries | An Orca-style dialog dataset aims at improving LM's long context conversational ability. |
| phi-1 | phi-1 | Dialog | English | / | A dataset generated by using the method in [Textbooks Are All You Need](https://arxiv.org/abs/2306.11644). It focuses on math and CS problems. |
| WebGLM-qa | WebGLm | Pairs | English | 43.6k entries | Dataset used by WebGLM, which is a QA system based on LLM and Internet. Each of the entry in this dataset comprise a question, a response and a reference. The response is grounded in the reference. |

#### June 2023

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| arxiv instruct datasets | / | Pairs | English | 50K/<br/>50K/<br/>30K entries | dataset consists of question-answer pairs derived from ArXiv abstracts. Questions are generated using the t5-base model, while the answers are generated using the GPT-3.5-turbo model. |
| COIG-PC | / | Pairs | Chinese | / | Enhanced version of COIG. |
| ign_clean_instruct_dataset_500k | / | Pairs | / | 509K entries | A large scale SFT dataset which is synthetically created from a subset of Ultrachat prompts. ⚠ lack of detailed datacard |
| im-feeling-curious | / | Pairs | English | 2595 entries | Random questions and correspond facts generated by Google **I'm feeling curious** features. |
| LIMA dataset | LIMA | Pairs | English | 1k entries | High quality SFT dataset used by [LIMA: Less Is More for Alignment](https://arxiv.org/pdf/2305.11206.pdf) |
| OpenOrca | / | Pairs | English | 4.5M completions | A collection of augmented FLAN data. Generated by using method is Orca paper. |
| SlimPajama | / | PT | Primarily<br/>English | / | A cleaned and deduplicated version of RedPajama |
| StackOverflow post | / | PT | / | 35GB | Raw StackOverflow data in markdown format, for pretraining. |
| TSI-v0 | / | Pairs | English | 30k examples<br/>per task | A Multi-task instruction-tuning data recasted from 475 of the tasksource datasets. Similar to Flan dataset and Natural instruction. |
| WizardLM_Orca | orca_mini series | Pairs | English | 55K entries | Enhanced WizardLM data. Generated by using orca's method. |
| WizardLM evolve_instruct V2 | WizardLM | Dialog | English | 196k entries | The latest version of Evolve Instruct dataset. |

#### Before June 2023

| Dataset name | Used by | Used for | Language | Size | Description |
|---|---|---|---|---|---|
| Alpaca-COT | Phoenix | IFT,<br/> DFT,<br/> CoT | English | / | A mixture a many dataset like classic Alpaca dataset, OIG, Guanaco and some CoT(Chain-of-Thought) datasets like FLAN-CoT. May be handy to use. |
| Alpaca-GPT-4_zh-cn | / | IFT | Chinese | about 50K entries | A Chinese Alpaca-style dataset, generated by GPT-4 originally in Chinese, not translated. |
| Bactrian-X | / | Pairs | Multilingual<br/> (52 languages) | 67K entries per language | A multilingual version of **Alpaca** and **Dolly-15K**. |
| COIG | / | IFT | Chinese,<br/>code | 200K entries | A Chinese-based dataset. It contains domains like general purpose QA, Chinese exams, code. Its quality is checked by human annotators. |
| ELI5 | MiniLM series | FT,<br/>RLHF | English | 270K entries | Questions and Answers collected from Reddit, including score. Might be used for RLHF reward model training. |
| evol_instruct_70k | WizardLM | IFT | English | | An instruction finetune dataset derived from Alpaca-52K, using the **evolution** method in [this paper](https://arxiv.org/pdf/2304.12244.pdf) |
| Firefly(流萤) | Firefly(流萤) | IFT | Chinese | 1.1M entries<br/>1.17GB | A Chinese instruction-tuning dataset with 1.1 million human-written examples across 23 tasks, but no conversation. |
| GPT-4all Dataset | GPT-4all | IFT | English, <br/> Might have <br/> a translated version | 400k entries | A combination of some subsets of OIG, P3 and Stackoverflow. Covers topics like general QA, customized creative questions. |
| GuanacoDataset | Guanaco | DFT,<br/> IFT | English,<br/> Chinese,<br/> Japanese | 534,530 entries | A multilingual instruction dataset for enhancing language models' capabilities in various linguistic tasks, such as natural language understanding and explicit content recognition. |
| h2oai/h2ogpt-fortune2000-personalized | h2ogpt | IFT | English | 11363 entries | A instruction finetune developed by h2oai, covered various topics. |
| LaMini-Instruction | / | Pairs | English | 2.8M entries | A dataset distilled from flan collection, p3 and self-instruction. |
| Luotuo-QA-A CoQA-Chinese | Luotuo project | Context | Chinese | 127K QA pairs | A dataset built upon translated CoQA. Augmented by using OpenAI API. |
| OASST1 | OpenAssistant | IFT,<br/> DFT | Multilingual<br/>(English, Spanish, etc.) | 66,497 conversation trees | A large, human-written, human-annotated high quality conversation dataset. It aims at making LLM generates more natural response. |
| OIG | Pythia-Chat-Base-7B, GPT-NeoXT-Chat-Base-20B, Koala | DFT,<br/> IFT | English,<br/> code | 44M entries | A large conversational instruction dataset with medium and high quality subsets *(OIG-small-chip2)* for multi-task learning. |
| OpenAI Summarization Comparison | Koala | RLHF | English | ~93K entries<br/>420MB | A dataset of human feedback which helps training a reward model. The reward model was then used to train a summarization model to align with human preferences. |
| OpenAI WebGPT | WebGPT's reward model, Koala | RLHF | English | 19,578 pairs | Data set used in WebGPT paper. Used for training reward model in RLHF. |
| Panther-dataset_v1 | Panther | Pairs | English | 377 entries | A dataset comes from the hh-rlhf. It rewrite hh-rlhf into the form of input-output pairs. |
| RedPajama-Data-1T | RedPajama | PT | Primarily English | 1.2T tokens <br/> 5TB | A fully open pretraining dataset follows the LLaMA's method. |
| ShareGPT52K | Koala, Stable LLM | IFT | Multilingual | 52K | This dataset comprises conversations collected from ShareGPT, with a specific focus on customized creative conversation. |
| SHP | StableVicuna,<br/>chat-opt,<br/>, SteamSHP | RLHF | English | 385K entries | An RLHF dataset different from previously mentioned ones, it use scores+timestamps to infer the users' preferences. Covers 18 domains, collected by Stanford. |
| WizardLM evol_instruct_70k | WizardLM | IFT | English | | An instruction finetune dataset derived from Alpaca-52K, using the **evolution** method in [this paper](https://arxiv.org/pdf/2304.12244.pdf) |
| xP3 | BLOOMZ, mT0 | IFT | Multilingual,<br/> code | 79M entries<br/>88GB | An instruction dataset for improving language models' generalization ability, similar to *Natural Instruct*. |
| Zhihu-KOL | Open Assistant | Pairs | Chinese | 1.5GB | QA data on well-know Chinese Zhihu QA platform. |

### <div id="hf-pretraining">Pretraining</div>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| C4 | Google T5 Series, LLaMA | PT | English | 305GB | A colossal, cleaned version of Common Crawl's web crawl corpus. Frequently be used. |
| falcon-refinedweb | tiiuae/falcon series | PT | English | / | A refined subset of CommonCrawl. |
| peS2o | / | PT | English | 7.5GB | A high quality academic paper dataset for pretraining. |
| proof-pile | proof-GPT | PT | English<br/>LaTeX | 13GB | A pretraining dataset which is similar to the pile but have LaTeX corpus to enhance LM's ability in proof. |
| ROOTS | BLOOM | PT | Multilingual,<br/> code | 1.6TB | A diverse open-source dataset consisting of sub-datasets like Wikipedia and StackExchange for language modeling. |
| SlimPajama | / | PT | Primarily<br/>English | / | A cleaned and deduplicated version of RedPajama |
| StackOverflow post | / | PT | / | 35GB | Raw StackOverflow data in markdown format, for pretraining. |

### <div id="hf-domain-specific">Domain-specific</div>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| ChatGPT-Jailbreak-Prompts | / | / | English | 163KB file size | Prompts for bypassing the safety regulation of ChatGPT. Can be use for probing the harmlessness of LLMs |
| code_instructions_120k_alpaca | / | Pairs | English/code | 121,959 entries | Code instruction dataset in instruction finetune format. |
| finance-alpaca | / | Pairs | English | 1.3K entries | An Alpaca-style dataset but focus on financial topics |
| function-invocations-25k | some MPT <br/> variants | Pairs | English code | 25K entries | A dataset aims at teaching AI models how to correctly invoke [APIsGuru](https://github.com/APIs-guru/openapi-directory) functions based on natural language prompts. |
| instructional_codesearchnet_python | / | Pairs | English &<br/> Python | 192MB | This dataset is a template generated instructional Python datastet generated from an annotated version of the code-search-net dataset for the Open-Assistant project. |
| phi-1 | phi-1 | Dialog | English | / | A dataset generated by using the method in [Textbooks Are All You Need](https://arxiv.org/abs/2306.11644). It focuses on math and CS problems. |
| starcoderdata | starcoder<br/>series | PT | code | 783GB | A large pretraining dataset for improving LM's coding ability. |
| symbolic-instruction-tuning | / | Pairs | English,<br/> code | 796 | A dataset focuses on the 'symbolic' tasks: like SQL coding, mathematical computation, etc. |
| Tapir-Cleaned | / | Pairs | English | 116k entries | This is a revised version of the DAISLab dataset of PairsTT rules, which has been thoroughly cleaned, scored, and adjusted for the purpose of instruction-tuning |
| TheoremQA | / | Pairs | English | 800 | A high quality STEM theorm QA dataset. |

### <div id="hf-multimodal">Multimodal</div>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| JourneyDB | / | image-prompt-caption | English | 4M instances | A large scale dataset comprises QA, caption, and text prompting tasks, which is based on Midjourney images. |
| LLaVA Instruction | LLaVA | instruction-image | English | 158k samples | A multimodal dataset generated upon COCO dataset by prompting GPT-4 to get instructions. |
| M3IT | Ying-VLM | instruction-image | Multilingual | 2.4M instances | A dataset comprises 40 tasks with 400 human written instruction. |
| OBELICS | idefics<br/>series | image-document | English | 141M documents | an open, massive, and curated collection of interleaved image-text web documents. |
| ShareGPT4V | / | image-prompt-caption | English | 1.2M instances | A set of GPT4-Vision-powered multi-modal captions data. |

### <div id="hf-private">Private</div>

| Dataset name | Used by | Type | Language | Size | Description |
|---|---|---|---|---|---|
| *No private HF-hosted datasets currently listed.* | | | | | |

---

## Contact 📬

To contact the original authors or contribute to the original project:

  [Junhao Zhao](zhaol9555@gmail.com) 📧 <br/>
  Advised by [Prof. Wanyun Cui](https://cuiwanyun.github.io/) [![](https://img.shields.io/badge/GitHub.io-@cuiwanyun-green.svg)](https://cuiwanyun.github.io/)

To inquire about this maintained fork, or Project Hierion: [project-hierion@proton.me](mailto:project-hierion@proton.me)

---

*With gratitude and much respect to the community, for providing such useful resources, [Project-Hierion](https://github.com/Project-Hierion) will attempt to maintain and keep this forked branch of the original [LLMDataHub](https://github.com/Zjh-819/LLMDataHub) by Junhao Zhao, up to date and current. 🙏*

---

**📌 Note on HuggingFace links:**  
Following Nvidia's acquisition of HuggingFace (September 2026), this archive no longer links directly to HF-hosted datasets. We believe in open infrastructure, not corporate consolidation. Datasets hosted exclusively on HF are marked `🤑` and quarantined in the HuggingFace-Hosted Datasets section at the bottom of this page — no links, no traffic. We encourage users to seek out mirrors, GitHub repos, or paper sources. If you find a non-HF link for a dataset, please contribute it. Let's keep open-source, open. Together.
