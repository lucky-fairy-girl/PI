# Parentheses Insertion based Sentence-level Text Adversarial Attack

本项目基于 TextAttack 框架开发，提出了一种通过在句子中添加插入语来实施句子级对抗攻击的新方法。
<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/b32b7403-628f-4abc-b5dd-c796d1a04c6b" />

## 环境安装 (Installation)

pip install textattack

## 可以通过以下命令运行插入语攻击：

textattack attack --model bert-base-uncased-sst2 --recipe my --num-examples 100
