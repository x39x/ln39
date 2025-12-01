# ln39

**ln39** 是一个基于 Python 与 Git 的dotfiles 管理工具

## 特性

- **零依赖**
  无需额外安装工具。只需 Python 与 Git（大多数系统已预装）。

- **配置灵活**
  直接使用 Python 作为配置文件，轻松处理不同场景

- **跨平台**
  支持 Linux、macOS、Windows、BSD。

- **安全操作**
  需要移动文件时自动备份到指定目录(~/ln39.bak/)，不会进行删除操作造成文件丢失

## 安装

在你的 dotfiles 目录中添加子模块：

```sh
git submodule add https://github.com/x39x/ln39
git commit -a -m "add submodule ln39"
```

## 快速上手

示例：

在 dotfiles 目录中新建 `config.py`：

```python
from ln39 import M, utils

default = [
    M("git", "~/.config/git"),
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

## `M` 对象

用于声明一条 dotfile 映射：把仓库中的文件链接到系统中的实际路径。

```python
M(src, dest, enabled=True, before_ln=None, after_ln=None)
```

### 参数

- **`src`**
  dotfiles 仓库中的文件路径（相对当前定义 `M()` 的文件所在目录）。支持 `~` 和环境变量。

- **`dest`**
  系统中的目标路径（将被创建 symlink 的位置）。支持 `~` 和环境变量。

- **`enabled`**（可选，默认 `True`）
  是否启用这条映射

```python
from ln39 import M, utils

def is_arch():
    result = utils.run(["cat", "/etc/*-release"])
    if "arch" in result.stdout.lower():
        return True
    else:
        return False

linux = [
    M("xkb", "~/.config/xkb"),
    M("sway", "~/.config/sway"),
    M("arch.config","~/.config/archconfig",enabled=is_arch()),
]

if utils.get_os_name() == "Linux":
    utils.ln(linux)
```

- **`before_ln`**
  在创建 symlink **之前**执行的函数（可选）。
  会收到一个对象参数：`opts.src`、`opts.dest`、`opts.basedir`，分别对应源文件路径，目标路径，ln39所在目录

```python
from ln39 import M, utils

def print_info(opts):
    print("opts.src:", opts.src)
    print("opts.dest:", opts.dest)
    print("opts.basedir:", opts.basedir)

default = [
    M("git", "~/.config/git"),
    M("nvim", "~/.config/nvim",before_ln=print_info),
]

utils.ln(default)
```

执行：

```sh
python config.py
```

- **`after_ln`**
  在创建 symlink **之后**执行的函数（可选）。
  同上

## Example

如果你愿意分享自己的 dotfiles 配置，可以在 issue 或 PR 中添加

- [https://github.com/x39x/dotfiles](https://github.com/x39x/dotfiles)

## utils

ln39 提供一组简单但实用的工具函数

### 环境变量

```python
utils.get_env("SHELL") # 返回环境变量的值
utils.env_exists("SHELL") # 环境变量是否存在
utils.env_equals("SHELL", "/bin/zsh") # 判断环境变量的值
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
result=utils.run(["ls", "-a"], cwd="~/Desktop")
print(result.stdout)
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
