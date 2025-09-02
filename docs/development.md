# 开发指南

本文档介绍如何设置开发环境并参与 rimetool 的开发。

## 环境要求

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (推荐的包管理工具)
- Git

## 快速开始

### 1. 克隆项目

```bash
git clone git@github.com:whitewatercn/rimetool.git
cd rimetool
```

### 2. 设置开发环境

推荐使用 uv 管理虚拟环境与包依赖：

```bash
# 创建虚拟环境并安装依赖
uv init
uv sync

# 激活虚拟环境
source .venv/bin/activate

# 以开发模式安装项目
uv pip install -e .
```

### 3. 验证安装

```bash
# 测试命令行工具
rimetool --help

# 启动 Web 界面（开发模式）
rimetool web --debug
```

## 项目结构

```
rimetool/
├── rimetool/                 # 主要源代码
│   ├── main.py              # 主入口文件
│   ├── rimetool_core/       # 核心功能模块
│   │   └── utils/           # 工具函数
│   │       ├── vcf.py       # VCF 联系人处理
│   │       ├── simple_*.py  # 简单文本处理
│   │       ├── tosougou.py  # 搜狗词库转换
│   │       └── Epub_Processor.py  # EPUB 处理
│   └── rimetool_gui/        # Web 界面
│       ├── new_app.py       # Flask 应用
│       ├── templates/       # HTML 模板
│       ├── logs/           # 日志文件
│       ├── uploads/        # 上传文件
│       └── outputs/        # 输出文件
├── docs/                    # 文档
├── examples/                # 示例文件
└── pyproject.toml          # 项目配置
```

## 开发流程

### 日志系统

项目使用带时间戳的日志系统：

- 日志文件格式：`rimetool_gui_YYYYMMDD_HHMMSS.log`
- 自动清理：保留最新 20 个日志文件
- 日志级别：DEBUG（开发阶段获取详细信息）

### 调试模式

```bash
# 启用 Flask 调试模式
rimetool web --debug --host 127.0.0.1 --port 8000
```

调试模式特性：

- 代码修改后自动重载
- 详细错误页面
- 交互式调试器
- 实时模板更新

### 代码修改

由于使用了开发模式安装 (`-e`)，代码修改会立即生效，无需重新安装。

### 构建和测试

```bash
# 构建包
uv build

# 手动安装到虚拟环境测试
uv pip install dist/rimetool-*.whl
```

## 功能模块说明

### 1. 命令行工具

主要功能通过 `rimetool` 命令提供：

- `--tool vcf`: VCF 联系人文件转 Rime 词库
- `--tool simple-english/se`: 英文文本转 Rime 词库
- `--tool simple-chinese/sc`: 中文文本转 Rime 词库
- `--tool tosougou`: Rime 词库转搜狗格式
- `--tool epub`: EPUB 电子书处理

### 2. Web 界面

通过 `rimetool web` 启动 Flask Web 应用：

- 文件上传和处理
- 实时进度显示
- 结果下载
- 操作日志记录

### 3. EPUB 处理模式

支持多种 EPUB 处理模式：

- `epub_to_txt`: EPUB 转纯文本
- `txt_to_short_long`: 文本分句处理
- `txt_to_rime`: 文本转 Rime 格式
- `epub_to_rime`: 完整转换流程

## 贡献指南

1. Fork 项目到你的 GitHub 账户
2. 创建功能分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -am 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 创建 Pull Request

## 常见问题

### Q: 虚拟环境中的 pip 指向错误位置？

```bash
# 安装 pip 到虚拟环境
uv pip install pip

# 清除命令缓存
hash -r

# 验证 pip 路径
which pip
```

### Q: 模板文件没有被打包？

确保 `pyproject.toml` 中包含：

```toml
[tool.setuptools.package-data]
"rimetool.rimetool_gui" = ["templates/*", "templates/**/*"]
```

### Q: 如何查看应用日志？

开发模式下，日志会输出到控制台和文件：

```bash
# 查看项目日志目录
ls rimetool/rimetool_gui/logs/

# 实时查看最新日志
tail -f rimetool/rimetool_gui/logs/rimetool_gui_*.log
```
