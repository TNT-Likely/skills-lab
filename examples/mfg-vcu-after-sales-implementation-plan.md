# 售后 VCU 换件纵向实施计划

这份计划只覆盖一个可验收的纵向切片：`售后工单 → VIN 查询 → 新 VCU 校验 → UDS/蓝牙写入 → 读回校验 → Melon 换件事务 → 飞书任务关闭 → 反向追溯`。先让一条真实流程跑通，再复制到 T-Box 和其他零部件。

## 1. 目标和边界

### 目标

- 售后人员可以在飞书任务中发起一张 VCU 换件任务。
- App 通过 Melon 查询 VIN 当前 VCU，扫描新件 PN/SN，并得到明确的校验结果。
- 设备写入成功且读回一致后，Melon 原子地完成旧件解除、新件绑定和换件履历追加。
- 飞书只回写任务进度、结果摘要和 Melon 记录引用；Melon 是车辆关系和换件事实的唯一写入方。

### 明确不做

- 本阶段不建设完整采购、WMS、MES 或售后工单平台。
- 本阶段不允许飞书和 Melon 双向修改当前 VCU 关系。
- 真实 UDS/蓝牙驱动可以先用模拟适配器替代，但设备结果接口必须保留成功、失败、超时和读回不一致状态。

## 2. 业务主流程

```text
飞书创建售后任务
  → App 输入/扫描 VIN
  → Melon 查询车辆和当前 VCU
  → App 扫描新 VCU PN/SN
  → Melon 校验车型适配、SN 唯一、验收、库存和重复任务
  → Melon 创建换件会话并保存旧件快照
  → UDS / 蓝牙写入车辆配置
  → 读回 SN / 配置并校验
  → Melon 提交换件事务
  → 解除旧 VCU 当前关系，绑定新 VCU
  → 追加 PART_REPLACED 追溯事件
  → 飞书回写完成并关闭任务
```

异常路径必须可恢复：

- 校验失败：不创建关系变更，修正候选 SN 或换件后重试。
- 写入失败或超时：会话保留为 `DEVICE_FAILED`，当前关系不变，允许重试。
- 读回不一致：会话进入 `READBACK_MISMATCH`，禁止提交关系切换。
- 重复提交：使用幂等键返回已完成结果，不能重复写履历。

## 3. 职责和数据主权

| 场景 | 飞书 | Melon | 最终事实来源 |
| --- | --- | --- | --- |
| 创建售后任务 | 任务、负责人、服务站、故障描述、优先级 | 接收外部任务号 | 飞书 |
| 查询车辆和当前件 | 展示关联结果 | VIN、车辆状态、当前 VCU 关系查询 | Melon |
| 扫描新件 | 承载任务入口或 App 页面 | 接收 PN/SN 候选输入并校验 | Melon |
| 设备写入 | 展示执行进度 | 保存设备命令结果、超时和重试 | Melon |
| 换件提交 | 接收结果摘要和链接 | 原子更新当前关系、零件状态、追溯事件 | Melon |
| 任务关闭 | 更新任务状态、备注、通知 | 提供完成结果和 `replacement_id` | 飞书展示，Melon 事实 |
| 反向追溯 | 通过引用打开结果 | 按 VIN、旧 SN、新 SN、工单查询履历 | Melon |

原则：一个业务事实只能有一个写入方。飞书记录 `source_system=feishu` 和 `source_record_id`，但飞书记录 ID 不能成为 Melon 领域主键。

## 4. 候选领域模型和 API

### 主要实体

| 实体 | 关键字段 | 候选 Melon 表 |
| --- | --- | --- |
| 售后任务引用 | `ticket_id`, `source_record_id`, `vin`, `reason` | `service_ticket_ref` |
| 车辆 | `vehicle_id`, `vin`, `model` | 已有车辆主数据 |
| 零部件实物 | `part_id`, `pn`, `sn`, `status` | 已有 `mfg_vehicle_part` / 扩展实物表 |
| 换件会话 | `replacement_id`, `old_sn`, `new_sn`, `idempotency_key`, `status` | `mfg_replacement_session` |
| 追溯事件 | `event_id`, `event_type`, `vin`, `part_sn`, `occurred_at`, `operator_id` | `mfg_trace_event` |

### 接口顺序

```text
GET  /mfg/vehicles/{vin}/current-parts?partType=VCU
POST /mfg/replacements/validate
POST /mfg/replacements/sessions
POST /mfg/replacements/{id}/device-write
POST /mfg/replacements/{id}/readback
POST /mfg/replacements/{id}/commit
GET  /mfg/replacements/{id}
GET  /mfg/vehicles/{vin}/trace?partType=VCU
```

关键校验：VIN 存在且属于当前服务范围；PN 适配车型版本；新 SN 已登记并通过验收；新 SN 未装在其他车辆；没有冲突的进行中会话；提交时读回值与目标值一致；所有命令支持 `idempotency_key`。

## 5. 分阶段实施

### 阶段 0：飞书流程验证

在飞书建立最小任务字段：工单号、VIN、车型、旧 VCU SN、新 VCU PN、新 VCU SN、换件原因、服务站、技师、状态、Melon 会话号、结果链接。用合成数据验证成功、校验失败、设备失败、重复提交四种状态。

验收：业务人员不看代码也能完成一条任务；字段名称和状态不会出现两套含义。

### 阶段 1：Melon 影子接口

复用已有零件登记、安装和装配查询能力，先实现查询、校验、会话和模拟设备结果；不修改当前生产关系，只记录影子换件会话和事件。

验收：相同请求可幂等重放；错误 PN、已占用 SN、错误 VIN 都返回可理解的失败原因。

### 阶段 2：单工位真实闭环

选择一个车型、一个服务站工位、一个 VCU 型号。接入真实 UDS/蓝牙适配器，执行写入和读回。只有读回成功才允许 `commit`。

验收：成功后 VIN 当前 VCU 变为新 SN；旧 SN 仍可在历史查询；失败、超时、断网重试不会产生半条关系。

### 阶段 3：飞书回写和反查

Melon 通过受控同步适配器回写任务状态、完成时间、结果摘要、`replacement_id` 和结果链接。飞书页面提供按 VIN 和工单号打开 Melon 追溯详情的入口。

验收：飞书状态落后时不影响 Melon 事实；重复 webhook 不重复产生事件；人工可从 VIN 追到旧件、新件、设备结果和原工单。

### 阶段 4：复制到 T-Box

复用会话、幂等、追溯和同步边界，只替换部件类型、设备协议和适配规则。VCU 通过验收后再扩展，不提前抽象成无法验证的通用平台。

## 6. 测试矩阵

| 场景 | 预期 |
| --- | --- |
| 正常换件 | 写入、读回、commit 成功，当前关系切换，任务关闭 |
| PN 不适配 | 校验失败，旧关系保持不变 |
| 新 SN 已被其他车占用 | 校验失败，可更换候选件重试 |
| UDS 写入失败 | 会话失败，可重试，不产生换件履历 |
| 读回不一致 | 禁止 commit，保留设备日志 |
| commit 重复 | 返回同一结果，不重复更新或写事件 |
| 飞书回写失败 | Melon 事实已完成，补偿同步可重试 |
| 反向追溯 | VIN 能看到工单、旧 SN、新 SN、操作者和时间 |

## 7. 原型到代码的迁移说明

原型中的按钮只模拟 API 返回和状态更新；`VCU-OLD-0042`、`VCU-NEW-0098`、`VIN-LEMON-001` 等均为合成 fixture。迁移时保留节点名称、状态、命令和事件类型，删除浏览器内存状态，改为 Melon 数据库事务和真实设备适配器。

建议先落地一个领域命令：`CommitReplacement`。它接收 `replacement_id`、`old_part_id`、`new_part_id`、`vin`、`operator_id`、`idempotency_key` 和设备读回证据，在一个事务中更新当前关系并追加事件。
