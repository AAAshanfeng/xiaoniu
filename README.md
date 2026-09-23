<p align="center">
  <h1 align="center">小牛电商 · 全栈自动化测试</h1>
  <p align="center">基于 pytest + requests + Selenium 的接口 + UI 自动化测试实践</p>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.12-blue">
  <img alt="pytest" src="https://img.shields.io/badge/pytest-9.x-007acc">
  <img alt="requests" src="https://img.shields.io/badge/API-requests-28a745">
  <img alt="Selenium" src="https://img.shields.io/badge/UI-Selenium%20(Edge)-7952b3">
  <img alt="pytest-html" src="https://img.shields.io/badge/report-pytest--html-orange">
</p>

> 📊 **测试报告**：本地 `report/api_report.html`、`report/ui_report.html`（`--self-contained-html` 单文件，双击即看）

---

## 一、项目简介

以「小牛电商」在线练习系统为被测对象，搭建的一套 **接口 + UI 双栈** 自动化测试工程，由 pytest 统一驱动。

- **被测系统**：API `http://43.133.227.52/api`　|　UI `http://ceshixiaoniu.com/ecommerce-practice-app.html`
- **测试范围**：登录 / 商品 / 购物车 / 订单（创建·支付·取消·查询）/ 权限 / 数据重置，UI 侧覆盖到端到端下单主流程。
- **用例规模**：**72 条**（接口 58 + UI 14，含参数化展开）；用例设计文档见 [`test_cases.md`](./test_cases.md)。
- **框架能力**：请求分层封装（`ApiClient`）、pytest fixture 依赖注入、`admin` 重置实现数据隔离、参数化复用、显式等待、`xfail(strict)` 缺陷钉住、pytest-html 报告。

---

## 二、技术栈

| 类别 | 选型 | 版本 |
|---|---|---|
| 测试框架 | pytest | 9.1.1 |
| 接口测试 | requests | 2.34.2 |
| Web 自动化 | Selenium（Microsoft Edge） | 4.48.0 |
| 测试报告 | pytest-html | 4.2.0 |
| 运行环境 | Python | 3.12 |

> Selenium 4.48 内置 **Selenium Manager**，自动匹配并下载 Edge 驱动，本机装有 Edge 即可，无需手动配置 `msedgedriver`。

---

## 三、目录结构

```text
.
├── api_test/                 # 接口自动化
│   ├── api_client.py         # 请求封装：统一 base_url 与各接口方法
│   ├── conftest.py           # fixture：api / reset_data / login / user_header / admin_header
│   ├── test_login.py         # 登录（成功 + 参数化异常）
│   ├── test_product.py       # 商品列表：获取 + 数据字段校验 + 未登录
│   ├── test_cart.py          # 购物车：查询 / 加入 / 删除 + 数量与库存边界
│   ├── test_order.py         # 订单：创建 / 支付 / 取消 / 查询 / 库存 / 金额 / 状态机
│   ├── test_scenario.py      # 场景串联：下单-支付、状态流转、reset 权限
│   └── test_reset.py         # 数据重置：权限校验 + 重置后数据恢复
├── ui_test/                  # UI 自动化（Selenium + Edge）
│   ├── conftest.py           # fixture：driver / reset_data / login
│   ├── test_login.py         # 登录 / 失败 / 退出
│   ├── test_cart.py          # 加购 / 删除 / 重复加购 / 库存不足禁用
│   ├── test_product.py       # 商品列表展示
│   ├── test_order.py         # 建单 / 支付 / 取消 / 空车建单
│   └── test_scenario.py      # 端到端冒烟：加购 → 建单 → 支付
├── report/                   # HTML 报告输出目录（生成物，不入库）
├── misc/                     # 测试用例 Excel 等资料
├── test_cases.md             # 用例设计文档
├── 缺陷记录.md                # 缺陷记录，与代码 xfail 标记对照
├── pytest.ini                # pytest 配置（testpaths / 命名规则 / -v）
└── .gitignore
```

---

## 四、设计要点

- **接口请求分层封装**：所有接口收敛到 `api_client.ApiClient`，用例只表达业务意图，URL / 请求细节不外溢。
- **Fixture 分层与依赖注入**：
  - `api`（session 级）：全局复用一个 `ApiClient`。
  - `reset_data`：以 `admin` 调 `POST /reset` 把订单 / 购物车 / 库存恢复初始，保证用例**互不污染、可乱序、可重复**。
  - `login` → `user_header` / `admin_header`：登录返回认证头，需要登录态的用例直接注入。
  - UI 侧 `driver` / `login`：管理浏览器生命周期与登录态。
- **参数化复用**：登录异常场景用 `@pytest.mark.parametrize` 一次覆盖密码错、用户错、空值、类型错等 7 种输入。
- **显式等待，杜绝 `sleep`**：UI 用例统一 `WebDriverWait` 等到「期望内容 / 状态」出现（按内容等待而非按元素出现等待），稳定性远高于固定等待。
- **最小充分断言**：列表类只断「数量 + 抽查一项」，不逐字复刻整页文本，避免脆弱断言。
- **反向用例验证无副作用**：如「空购物车建单」除断提示外，还断「订单数量没有变化」。
- **缺陷用 `xfail(strict=True)` 钉住**：把已确认的系统缺陷固化为用例，缺陷修复后会自动转为 `XPASS` 让构建变红，提醒维护者摘除标记（详见第八节与 [`缺陷记录.md`](./缺陷记录.md)）。

---

## 五、快速开始

### 1. 环境准备
- 安装 Python 3.12 与 **Microsoft Edge** 浏览器
- 网络可达被测系统（API 与 UI 地址见第一节）

### 2. 安装依赖
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate     macOS/Linux: source .venv/bin/activate
pip install pytest==9.1.1 requests==2.34.2 selenium==4.48.0 pytest-html==4.2.0
```
> 建议将上述依赖固化为 `requirements.txt`，便于他人一键复现。

### 3. 测试账号

| 账号 | 密码 | 用途 |
|---|---|---|
| `tester` | `123456` | 普通用户（购物车、下单、支付） |
| `admin` | `admin123` | 管理员（重置数据、权限校验） |

### 4. 运行用例
```bash
pytest                                       # 跑全部（默认收集 api_test + ui_test）
pytest api_test                              # 只跑接口
pytest ui_test                               # 只跑 UI
pytest ui_test/test_scenario.py -k checkout  # 跑单条端到端冒烟
```

---

## 六、测试报告

```bash
pytest api_test --html=report/api_report.html --self-contained-html
pytest ui_test  --html=report/ui_report.html  --self-contained-html
```

生成**自包含**单文件报告（JS/CSS/数据全部内联），`report/` 已在 `.gitignore` 中忽略——属每次运行重新生成的产物。

---

## 七、用例覆盖

### 接口（`api_test` · 58 条）

| 模块 | 用例数 | 说明 |
|---|---:|---|
| 登录 | 8 | 成功 1 条 + 参数化异常 7 条（密码错 / 用户错 / 空值 / 类型错） |
| 商品 | 3 | 登录后获取列表、未登录拦截、字段与类型校验 |
| 购物车 | 15 | 查询 / 加入 / 删除，含数量边界、库存、重复、不存在商品、未登录 |
| 订单 | 23 | 创建 / 支付 / 取消 / 查询、库存扣减、金额校验、状态机、权限、未登录 |
| 场景串联 | 6 | 下单-支付、取消后支付、支付后取消、查询不存在订单、reset 权限 |
| 数据重置 | 3 | 普通用户禁止、管理员成功、重置后数据恢复 |

### UI（`ui_test` · 14 条）

| 模块 | 用例数 | 说明 |
|---|---:|---|
| 登录 / 退出 | 4 | 成功、用户名错、密码错、退出登录 |
| 购物车 | 4 | 加购、删除、重复加购、库存不足按钮禁用 |
| 商品列表 | 1 | 数量校验 + 抽查单卡 |
| 订单 | 4 | 建单、支付、取消、空车建单 |
| 端到端冒烟 | 1 | 加购 → 建单 → 支付 全链路 |

> 完整用例设计（编号、优先级、前置、步骤、数据、预期）见 [`test_cases.md`](./test_cases.md)。

---

## 八、执行过程中发现的缺陷

以下缺陷以 `@pytest.mark.xfail(strict=True)` 钉在代码中，共 **5 处**（运行结果计入 xfailed，非失败）：

| 用例编号 | 现象 | 结论 |
|---|---|---|
| `add_cart_003` | 加购 `quantity=0` 时仍返回 `code=0` 并累加数量 | 参数校验缺失 |
| `add_cart_005` | 加购 `quantity` 过大（999）时仍成功 | 数量上限 / 库存校验缺失 |
| `delete_cart_002` | 删除不存在的商品返回 `code=0` | 应报错却"成功"，缺少存在性校验 |
| `pay_orders_004` | 重复支付已支付订单返回 `code=0` | 订单状态机缺陷 |
| `cancel_orders_004` | 取消已取消订单返回 `code=0` | 订单状态机缺陷 |

> 缺陷详情、复现步骤与期望行为见 [`缺陷记录.md`](./缺陷记录.md)。缺陷修复后，对应用例将转为 `XPASS(strict)` 让构建变红，提醒及时摘除标记。

---

## 九、亮点小结

- 从零搭建 **pytest 驱动的接口 + UI 双栈** 自动化工程，接口侧以 `ApiClient` 分层封装。
- 用 **fixture** 统一管理认证头、浏览器生命周期与登录态，`admin` 重置实现**数据隔离**。
- 参数化复用异常输入；显式等待 + 内容等待替代脆弱 `sleep`。
- 断言遵循**最小充分**与**无副作用**原则，规避假绿（如识别出 Selenium `is_disabled()` 空实现，改用 `is_enabled()`）。
- 用 `xfail(strict)` **钉住已确认缺陷**，形成缺陷生命周期闭环，而非只追求"脚本跑通"。
- 接入 **pytest-html** 生成可视化报告，接口 / UI 分档输出。

---

## 十、许可与说明

本项目为软件测试学习与求职展示用途，重点展示接口与 UI 自动化框架设计、用例编写、缺陷定位与报告能力。被测系统为「小牛电商」在线练习系统。
