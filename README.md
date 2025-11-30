# ln39

**ln39** 是一个基于 Python 与 Git 的 _零依赖 dotfiles 管理工具_

## ✨ 特性

- **零依赖**
  无需额外安装工具。只需 Python 与 Git（大多数系统已预装）。

- **配置灵活**
  直接使用 Python 作为配置文件，轻松处理不同系统、不同路径、条件逻辑等场景。

- **跨平台**
  支持 Linux、macOS、Windows、BSD。

- **安全操作**
  需要移动文件时自动备份到指定目录(~/ln39.bak/)，不会造成文件丢失

## 📦 安装

在你的 dotfiles 目录中添加子模块：

```sh
git submodule add https://github.com/x39x/ln39
git commit -a -m "add submodule ln39"
```

## 🚀 快速上手

示例：

在 dotfiles 目录中新建 `config.py`：

```python
from ln39 import M, utils

default = [
    M("git", "~/.config/git"),
    M("ghostty", "~/.config/ghostty"),
    M("bat", "~/.config/bat/config"),
    M(
        "vscode/settings.json",
        utils.path_for(
            macos="~/Library/Application Support/Code/User/settings.json",
            linux="~/.config/Code/User/settings.json",
        ),
    ),
]

linux = [
    M("xkb", "~/.config/xkb"),
    M("sway", "~/.config/sway"),
]

macos = [
    M("hammerspoon", "~/.hammerspoon"),
    M("karabiner", "~/.config/karabiner"),
]

osname = utils.get_os_name()

if osname == "Linux":
    utils.ln(linux)

if osname == "Darwin":
    utils.ln(macos)

# 公共配置
utils.ln(default)
```

执行：

```sh
python config.py
```

你的配置将自动链接到系统对应路径。

---

## 📁 示例仓库

如果你愿意分享自己的 ln39 配置，可以在 issue 或 PR 中添加

- [https://github.com/x39x/dotfiles](https://github.com/x39x/dotfiles)

## M 对象

`M(source, target)` 用于描述一个映射关系：

- `src`: 配置文件在dotfiles 仓库中的路径
- `dest`: 系统中的实际路径（可用 `~`）

## 🛠️ 工具函数（utils）

ln39 提供一组简单但实用的工具函数

### 环境变量

```python
utils.get_env("SHELL")
utils.env_exists("SHELL")
utils.env_equals("SHELL", "/bin/zsh")
```

### 系统名称

```python
utils.get_os_name()  # Darwin / Linux / Windows / ...
```

### 路径选择

根据系统返回配置路径，其中 "FreeBSD", "OpenBSD", "NetBSD", "DragonFly"都会返回 bsd

```python
utils.path_for(
    macos="~/Library/.../path",
    linux="~/.config/.../path",
    windows="C:\\Users\\...\\path",
    bsd="~/.config/bsd/path",
)
```

### 执行命令

```python
utils.run(["ls", "-a"], cwd="~/Desktop")
```

对 `subprocess.run` 的包装，默认捕获输出。

支持参数：

- `command`: 列表或字符串（必填）
- `cwd`: 工作目录（默认当前脚本所在目录）
- `capture_output`: 是否捕获输出
- `check`: 是否在失败时抛异常
- `shell`: 是否通过 shell 执行

### 备份文件

```python
utils.backup("~/.vim")
```

将文件移动至 `~/ln39.bak/`。

### Git 操作

```python
utils.init_submodules("/abs/path/to/repo")
utils.clone_repo("/abs/path/to/repo")
utils.pull_repo("/abs/path/to/repo")
utils.update_ln39()
```
