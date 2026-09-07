#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
党政机关公文生成器 - 基于 GB/T 9704-2012 国家标准
生成符合规范的党政机关公文 docx 文件
"""

import json
import sys
import argparse
import os
from docx import Document
from docx.shared import Pt, Mm, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from copy import deepcopy


# ============================================================
# 字号对照表 (中文字号 -> 磅值)
# ============================================================
FONT_SIZE_MAP = {
    '初号': 42, '小初': 36, '一号': 26, '小一': 24,
    '二号': 22, '小二': 18, '三号': 16, '小三': 15,
    '四号': 14, '小四': 12, '五号': 10.5, '小五': 9,
}

# 结构层次对应的字体
LEVEL_FONT_MAP = {
    1: '黑体',    # 一、二、三、
    2: '楷体',    # （一）（二）（三）
    3: '仿宋',    # 1. 2. 3.
    4: '仿宋',    # （1）（2）（3）
}


def set_font(run, font_name, font_size_pt, bold=False, color=None, east_asia_font=None):
    """设置run的字体属性"""
    run.font.name = font_name
    run.font.size = Pt(font_size_pt)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color
    # 设置中文字体
    ea = east_asia_font or font_name
    rpr = run._element.get_or_add_rPr()
    rFonts = rpr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:eastAsia="{ea}"/>')
        rpr.insert(0, rFonts)
    else:
        rFonts.set(qn('w:eastAsia'), ea)


def set_paragraph_spacing(paragraph, before=0, after=0, line_spacing=None, line_rule=None):
    """设置段落间距"""
    pf = paragraph.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if line_spacing:
        pf.line_spacing = Pt(line_spacing)


def add_empty_lines(doc, count=1, font_size_pt=16):
    """添加空行"""
    for _ in range(count):
        p = doc.add_paragraph()
        set_paragraph_spacing(p, line_spacing=font_size_pt * 1.75)
        run = p.add_run('')
        set_font(run, '仿宋', font_size_pt)


def setup_page(doc):
    """设置A4页面，符合GB/T 9704-2012要求"""
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.orientation = WD_ORIENT.PORTRAIT
    # 天头 37mm，订口 28mm
    section.top_margin = Mm(37)
    section.bottom_margin = Mm(35)   # 下白边约35mm
    section.left_margin = Mm(28)
    section.right_margin = Mm(26)    # 右白边约26mm
    return section


def add_red_line(doc, width_mm=156, thickness_pt=1.5):
    """添加红色分隔线（版头分隔线）"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before=0, after=0)
    # 使用底部边框模拟红色分隔线
    pPr = p._element.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="{int(thickness_pt * 8)}" '
        f'    w:space="1" w:color="FF0000"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)
    run = p.add_run('')
    run.font.size = Pt(2)
    return p


def add_thick_line(doc):
    """添加粗分隔线（版记首条/末条，0.35mm）"""
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=0, after=0)
    pPr = p._element.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="10" '
        f'    w:space="1" w:color="000000"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)
    run = p.add_run('')
    run.font.size = Pt(2)
    return p


def add_thin_line(doc):
    """添加细分隔线（版记中间，0.25mm）"""
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=0, after=0)
    pPr = p._element.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="6" '
        f'    w:space="1" w:color="000000"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)
    run = p.add_run('')
    run.font.size = Pt(2)
    return p


def build_header(doc, header_data, format_type='general'):
    """构建版头区域"""
    # 份号
    copy_number = header_data.get('copy_number')
    if copy_number:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_paragraph_spacing(p, line_spacing=28)
        run = p.add_run(str(copy_number))
        set_font(run, 'Times New Roman', 16)  # 三号

    # 密级和保密期限
    security_level = header_data.get('security_level')
    if security_level:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_paragraph_spacing(p, line_spacing=28)
        security_period = header_data.get('security_period', '')
        text = f'{security_level}★{security_period}年' if security_period else security_level
        run = p.add_run(text)
        set_font(run, '黑体', 16, bold=True)  # 三号黑体

    # 紧急程度
    urgency = header_data.get('urgency')
    if urgency:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_paragraph_spacing(p, line_spacing=28)
        run = p.add_run(urgency)
        set_font(run, '黑体', 16, bold=True)  # 三号黑体

    # 发文机关标志（红色小标宋体）
    issuer_mark = header_data.get('issuer_mark', '')
    if issuer_mark:
        add_empty_lines(doc, 1, 22)  # 留出上方空间
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(p, before=0, after=0, line_spacing=42)
        run = p.add_run(issuer_mark)
        set_font(run, '小标宋体', 26, color=RGBColor(0xFF, 0x00, 0x00))  # 红色，约小标宋大小

    # 发文字号
    doc_number = header_data.get('doc_number', {})
    if doc_number:
        prefix = doc_number.get('prefix', '')
        year = doc_number.get('year', '')
        seq = doc_number.get('sequence', '')
        doc_num_text = f'{prefix}〔{year}〕{seq}号'

        signers = header_data.get('signer', [])
        if signers:
            # 上行文：发文字号居左，签发人居右
            p = doc.add_paragraph()
            set_paragraph_spacing(p, line_spacing=28)
            # 发文字号左空一字
            run = p.add_run(f'\u3000{doc_num_text}')
            set_font(run, '仿宋', 16)
            # 签发人居右
            signer_text = '、'.join(signers)
            run2 = p.add_run(f'    签发人：{signer_text}')
            set_font(run2, '仿宋', 16)
        else:
            # 下行文/平行文：发文字号居中
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_paragraph_spacing(p, line_spacing=28)
            run = p.add_run(doc_num_text)
            set_font(run, '仿宋', 16)  # 三号仿宋

    # 红色分隔线
    add_empty_lines(doc, 1, 8)
    add_red_line(doc)

    return doc


def build_body(doc, subject_data):
    """构建主体区域"""
    # 标题 - 二号小标宋体，居中
    title = subject_data.get('title', '')
    if title:
        add_empty_lines(doc, 2, 22)  # 红色分隔线下空二行
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(p, line_spacing=32)
        run = p.add_run(title)
        set_font(run, '小标宋体', 22)  # 二号 = 22pt

    # 主送机关 - 三号仿宋，顶格
    recipients = subject_data.get('recipients', [])
    if recipients:
        p = doc.add_paragraph()
        set_paragraph_spacing(p, line_spacing=28)
        recipient_text = '、'.join(recipients) + '：'
        run = p.add_run(recipient_text)
        set_font(run, '仿宋', 16)  # 三号仿宋

    # 正文
    body = subject_data.get('body', [])
    for item in body:
        if isinstance(item, str):
            # 简单段落 - 三号仿宋，首行缩进2字
            p = doc.add_paragraph()
            pf = p.paragraph_format
            pf.first_line_indent = Pt(32)  # 三号字16pt × 2 = 32pt
            set_paragraph_spacing(p, line_spacing=28)
            run = p.add_run(item)
            set_font(run, '仿宋', 16)
        elif isinstance(item, dict):
            level = item.get('level', 1)
            text = item.get('text', '')
            paragraphs = item.get('paragraphs', [])

            # 层次标题
            font_name = LEVEL_FONT_MAP.get(level, '仿宋')
            p = doc.add_paragraph()
            pf = p.paragraph_format
            pf.first_line_indent = Pt(32)
            set_paragraph_spacing(p, line_spacing=28)
            run = p.add_run(text)
            set_font(run, font_name, 16)

            # 层次下的段落
            for para_text in paragraphs:
                p = doc.add_paragraph()
                pf = p.paragraph_format
                pf.first_line_indent = Pt(32)
                set_paragraph_spacing(p, line_spacing=28)
                run = p.add_run(para_text)
                set_font(run, '仿宋', 16)

    # 附件说明
    attachments = subject_data.get('attachments', [])
    if attachments:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.first_line_indent = Pt(32)
        set_paragraph_spacing(p, line_spacing=28)
        att_texts = []
        for i, att in enumerate(attachments, 1):
            att_name = att.get('name', f'附件{i}') if isinstance(att, dict) else str(att)
            att_texts.append(f'{i}.{att_name}')
        run = p.add_run('附件：' + '\n      '.join(att_texts))
        set_font(run, '仿宋', 16)

    # 发文机关署名和成文日期
    issuer_name = subject_data.get('issuer_name', '')
    issue_date = subject_data.get('issue_date', '')
    seal = subject_data.get('seal', True)

    if issuer_name or issue_date:
        add_empty_lines(doc, 1, 16)

    if issuer_name:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        set_paragraph_spacing(p, line_spacing=28)
        run = p.add_run(issuer_name)
        set_font(run, '仿宋', 16)

    if issue_date:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        set_paragraph_spacing(p, line_spacing=28)
        # 右空四字
        run = p.add_run(f'{issue_date}    ')
        set_font(run, '仿宋', 16)

    # 附注
    notes = subject_data.get('notes')
    if notes:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.first_line_indent = Pt(32)
        set_paragraph_spacing(p, line_spacing=28)
        run = p.add_run(f'（{notes}）')
        set_font(run, '仿宋', 16)

    return doc


def build_footer(doc, footer_data):
    """构建版记区域"""
    if not footer_data:
        return doc

    cc_list = footer_data.get('cc', [])
    print_org = footer_data.get('print_org', '')
    print_date = footer_data.get('print_date', '')

    if not cc_list and not print_org:
        return doc

    # 版记首条粗分隔线
    add_thick_line(doc)

    # 抄送机关
    if cc_list:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.first_line_indent = Pt(28)  # 左右各空一字
        set_paragraph_spacing(p, line_spacing=24)
        cc_text = '抄送：' + '、'.join(cc_list) + '。'
        run = p.add_run(cc_text)
        set_font(run, '仿宋', 14)  # 四号仿宋

    # 印发机关和印发日期之间的细分隔线
    if cc_list and print_org:
        add_thin_line(doc)

    # 印发机关和印发日期
    if print_org or print_date:
        p = doc.add_paragraph()
        set_paragraph_spacing(p, line_spacing=24)
        if print_org:
            run = p.add_run(f' {print_org}')
            set_font(run, '仿宋', 14)  # 四号仿宋
        if print_date:
            # 印发日期右空一字
            remaining = 28 - len(print_org or '') - len(print_date) - 2
            spaces = ' ' * max(remaining, 1)
            run = p.add_run(f'{spaces}{print_date} 印发 ')
            set_font(run, '仿宋', 14)

    # 版记末条粗分隔线
    add_thick_line(doc)

    return doc


def add_page_numbers(doc):
    """添加页码 - 四号半角宋体，单页右空一字，双页左空一字"""
    for section in doc.sections:
        footer = section.footer
        footer.is_linked_to_previous = False
        p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # 使用域代码实现页码
        run = p.add_run()
        set_font(run, '宋体', 14)  # 四号宋体
        fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
        run._element.append(fldChar1)
        run2 = p.add_run()
        instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
        run2._element.append(instrText)
        run3 = p.add_run()
        fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
        run3._element.append(fldChar2)


def generate_gov_document(input_data, output_path):
    """主函数：生成公文"""
    doc = Document()

    # 1. 页面设置
    setup_page(doc)

    # 2. 获取各区域数据
    header_data = input_data.get('header', {})
    subject_data = input_data.get('subject', {})
    footer_data = input_data.get('footer', {})
    format_type = input_data.get('format_type', input_data.get('doc_type', 'general'))
    show_page_number = input_data.get('page_number', True)

    # 3. 构建版头
    build_header(doc, header_data, format_type)

    # 4. 构建主体
    build_body(doc, subject_data)

    # 5. 构建版记
    build_footer(doc, footer_data)

    # 6. 添加页码
    if show_page_number:
        add_page_numbers(doc)

    # 7. 保存文档
    doc.save(output_path)
    print(f'公文已生成: {output_path}')
    return output_path


def main():
    parser = argparse.ArgumentParser(description='党政机关公文生成器 (GB/T 9704-2012)')
    parser.add_argument('--input', '-i', required=True, help='JSON输入文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出docx文件路径')
    args = parser.parse_args()

    # 读取JSON输入
    with open(args.input, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    # 确保输出路径以.docx结尾
    output_path = args.output
    if not output_path.endswith('.docx'):
        output_path += '.docx'

    generate_gov_document(input_data, output_path)


if __name__ == '__main__':
    main()
