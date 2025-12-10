# 2026年工作日历处理工具

从PDF格式的2026年工作日历表中提取休息日和工作日信息，生成ICS日历文件和CSV文件。

## 功能特性

- ✅ 解析PDF中的日历表格
- ✅ 识别黄色高亮的休息日（节假日）
- ✅ 识别周末工作日（周六/周日需要上班的日子）
- ✅ 生成标准ICS日历文件，可导入到Google Calendar、Outlook、Apple Calendar等
- ✅ 生成CSV文件，方便数据分析和导入其他系统

## 文件说明

| 文件名 | 描述 |
|--------|------|
| `附件：2026年工作日历表.pdf` | 源PDF文件 |
| `generate_calendar.py` | 主处理脚本，生成ICS和CSV文件 |
| `extract_pdf.py` | PDF文本提取测试脚本 |
| `inspect_pdf_colors.py` | PDF颜色检测脚本 |
| `test_tables.py` / `test_tables_2.py` | 表格解析测试脚本 |
| `calendar_2026.ics` | 生成的ICS日历文件 |
| `calendar_2026.csv` | 生成的CSV数据文件 |
| `requirements.txt` | Python依赖包列表 |

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行主脚本

```bash
python generate_calendar.py
```

运行后将在当前目录生成：
- `calendar_2026.ics` - ICS日历文件
- `calendar_2026.csv` - CSV数据文件

### 3. 导入日历

- **ICS文件**：直接双击或导入到日历应用
- **CSV文件**：使用Excel、Google Sheets等打开

### 4. 导入到Google Calendar

将生成的ICS文件导入Google Calendar的步骤：

1. **访问Google Calendar**
   - 打开 [calendar.google.com](https://calendar.google.com)
   - 确保已登录Google账号

2. **进入导入界面**
   - 在左侧面板中找到"其他日历"
   - 点击旁边的"+"图标
   - 选择"导入"

3. **选择文件**
   - 点击"选择文件"按钮
   - 浏览并选择生成的 `calendar_2026.ics` 文件

4. **选择目标日历**
   - 在下拉菜单中选择要将事件添加到哪个日历（或新建日历）
   - 建议新建一个日历，如"2026工作日历"

5. **开始导入**
   - 点击"导入"按钮
   - 等待导入完成

6. **验证导入结果**
   - 在日历视图中查看2026年的日期
   - 检查黄色休息日和周末工作日是否正确显示
   - 事件标题应显示为"休息"或"班"（带描述）

**注意事项**：

- 导入的日历事件是只读的，如需修改需重新生成并导入
- 建议在导入前备份现有日历数据
- 如果日历中已有相同日期的其他事件，它们会共存

## 数据处理规则

脚本根据以下规则处理日期：

1. **黄色高亮日期** → 休息日（节假日）
2. **周六/周日无黄色高亮** → 工作日（需要上班）
3. **周一至周五无黄色高亮** → 正常工作日（不标记）

## 输出格式

### ICS文件包含的事件
- 休息日：标题为"休息"或"休息: [描述]"
- 周末工作日：标题为"班"或"班: [描述]"

### CSV文件字段
- `Subject`: 事件标题
- `Start Date`: 开始日期 (YYYY-MM-DD)
- `All Day Event`: 全天事件标记
- `Description`: 事件描述（如有）
- `Type`: 事件类型 (Rest/Work)

## 开发说明

### 测试脚本

项目中包含多个测试脚本，用于PDF解析调试：

```bash
# 测试PDF表格提取
python extract_pdf.py

# 检查PDF颜色信息
python inspect_pdf_colors.py

# 测试表格解析
python test_tables.py
python test_tables_2.py
```

### 主要依赖库

- **pdfplumber**: PDF解析和表格提取
- **ics**: ICS日历文件生成

## 注意事项

1. 确保PDF文件名为`附件：2026年工作日历表.pdf`并放置在项目根目录
2. 如果PDF格式有变化，可能需要调整表格解析逻辑
3. 生成的ICS文件使用UTF-8编码，支持中文字符

## 许可证

本项目代码采用MIT许可证。

## 贡献

欢迎提交Issue和Pull Request改进此工具。