# JSON输入格式说明

生成公文时，需要提供一个JSON文件作为输入，格式如下：

## 完整JSON结构

```json
{
  "doc_type": "general",
  "paper_size": "A4",
  "header": {
    "copy_number": "000001",
    "security_level": "秘密",
    "security_period": "5",
    "urgency": "特急",
    "issuer_mark": "国务院文件",
    "doc_number": {
      "prefix": "国发",
      "year": "2026",
      "sequence": "1"
    },
    "signer": ["张三", "李四"]
  },
  "subject": {
    "title": "关于XXX的通知",
    "recipients": ["各省、自治区、直辖市人民政府", "国务院各部委"],
    "body": [
      "正文第一段内容...",
      "正文第二段内容...",
      {
        "level": 1,
        "text": "一级标题",
        "paragraphs": ["该标题下的段落..."]
      },
      {
        "level": 2,
        "text": "（一）二级标题",
        "paragraphs": ["该标题下的段落..."]
      }
    ],
    "attachments": [
      {"name": "附件一名称", "file": "path/to/file1.docx"},
      {"name": "附件二名称"}
    ],
    "issuer_name": "国务院",
    "issue_date": "2026年8月12日",
    "seal": true,
    "notes": "（此件公开发布）"
  },
  "footer": {
    "cc": ["国务院办公厅", "国家发展改革委"],
    "print_org": "国务院办公厅秘书局",
    "print_date": "2026年8月12日"
  },
  "page_number": true,
  "format_type": "general"
}
```

## 字段说明

### 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `doc_type` | string | 否 | 公文类型: general(通用)/letter(信函)/order(命令)/minutes(纪要)，默认general |
| `paper_size` | string | 否 | 纸张尺寸，默认A4 |
| `header` | object | 是 | 版头要素 |
| `subject` | object | 是 | 主体要素 |
| `footer` | object | 否 | 版记要素 |
| `page_number` | boolean | 否 | 是否显示页码，默认true |
| `format_type` | string | 否 | 格式类型: general/letter/order/minutes |

### header 对象

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `copy_number` | string | 否 | 份号，6位数字 |
| `security_level` | string | 否 | 密级: 秘密/机密/绝密 |
| `security_period` | string | 否 | 保密期限(年) |
| `urgency` | string | 否 | 紧急程度: 急件/特急 |
| `issuer_mark` | string | 是 | 发文机关标志，如"国务院文件" |
| `doc_number` | object | 是 | 发文字号 |
| `doc_number.prefix` | string | 是 | 机关代字，如"国发" |
| `doc_number.year` | string | 是 | 年份 |
| `doc_number.sequence` | string | 是 | 顺序号 |
| `signer` | array | 否 | 签发人姓名列表 |

### subject 对象

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 是 | 公文标题 |
| `recipients` | array | 是 | 主送机关列表 |
| `body` | array | 是 | 正文内容(字符串或结构化段落) |
| `attachments` | array | 否 | 附件列表 |
| `issuer_name` | string | 是 | 发文机关署名 |
| `issue_date` | string | 是 | 成文日期，格式"YYYY年M月D日" |
| `seal` | boolean | 否 | 是否加盖印章，默认true |
| `notes` | string | 否 | 附注内容 |

### body 数组元素

正文可以是简单字符串数组，也可以包含结构化层次:

**简单格式:**
```json
["第一段内容...", "第二段内容..."]
```

**结构化格式:**
```json
[
  "普通段落...",
  {"level": 1, "text": "一、一级标题(黑体)", "paragraphs": ["段落..."]},
  {"level": 2, "text": "（一）二级标题(楷体)", "paragraphs": ["段落..."]},
  {"level": 3, "text": "1.三级标题(仿宋)", "paragraphs": ["段落..."]},
  {"level": 4, "text": "（1）四级标题(仿宋)", "paragraphs": ["段落..."]}
]
```

### footer 对象

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `cc` | array | 否 | 抄送机关列表 |
| `print_org` | string | 否 | 印发机关 |
| `print_date` | string | 否 | 印发日期 |

## 简化示例（最简输入）

```json
{
  "header": {
    "issuer_mark": "XX市人民政府文件",
    "doc_number": {
      "prefix": "X政发",
      "year": "2026",
      "sequence": "1"
    }
  },
  "subject": {
    "title": "关于做好2026年度工作的通知",
    "recipients": ["各县区人民政府"],
    "body": ["正文内容..."],
    "issuer_name": "XX市人民政府",
    "issue_date": "2026年8月12日"
  }
}
```
