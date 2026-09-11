import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def generate():
    # 1. Carregar dados consolidados da fonte oficial
    src_path = 'C:/Users/a.alves/Downloads/data (5).xlsx'
    wb_src = openpyxl.load_workbook(src_path, data_only=True)
    ws_src = wb_src.active
    rows = list(ws_src.iter_rows(values_only=True))
    header = rows[0]
    raw_data = rows[1:-3] # 64 registros reais
    
    df = pd.DataFrame(raw_data, columns=header)
    df['emp_Empresa_chr'] = df['emp_Empresa_chr'].astype(str).str.strip()
    df['sup_Supervisor_chr'] = df['sup_Supervisor_chr'].astype(str).str.strip()
    df['Vendedor'] = df['Vendedor'].astype(str).str.strip()
    df['ICE'] = df['ICE'].fillna(0).astype(int)
    df['CLI ICE'] = df['CLI ICE'].fillna(0).astype(int)
    df['ULTRA'] = df['ULTRA'].fillna(0).astype(int)
    df['CLI ULTRA'] = df['CLI ULTRA'].fillna(0).astype(int)
    df['ACAO'] = df['ACAO'].fillna(0).astype(int)
    df['CLI ACAO'] = df['CLI ACAO'].fillna(0).astype(int)
    
    print(f"Total registros: {len(df)}")
    print(f"Total ULTRA: {df['ULTRA'].sum()} | ICE: {df['ICE'].sum()} | AÇÃO: {df['ACAO'].sum()} | CLI AÇÃO: {df['CLI ACAO'].sum()}")
    
    # -------------------------------------------------------------
    # 2. GERAR PLANILHA EXCEL (Vendedores_Bonus_RH_ICE_ULTRA.xlsx)
    # -------------------------------------------------------------
    excel_path = 'C:/Users/a.alves/Downloads/ICE_ULTRA/Vendedores_Bonus_RH_ICE_ULTRA.xlsx'
    wb_out = openpyxl.Workbook()
    
    # Estilos reutilizáveis Excel
    font_header = Font(name='Segoe UI', size=11, bold=True, color='FFFFFF')
    fill_header = PatternFill(start_color='164E35', end_color='164E35', fill_type='solid') # Verde Floresta Escuro
    fill_header_blue = PatternFill(start_color='1E3A5F', end_color='1E3A5F', fill_type='solid') # Azul Petróleo para Clientes
    fill_zebra = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')
    
    font_data = Font(name='Segoe UI', size=10)
    font_bold = Font(name='Segoe UI', size=10, bold=True)
    font_total = Font(name='Segoe UI', size=11, bold=True, color='FFFFFF')
    fill_total = PatternFill(start_color='0F291E', end_color='0F291E', fill_type='solid')
    
    thin_border = Border(
        left=Side(style='thin', color='E2E8F0'),
        right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='E2E8F0'),
        bottom=Side(style='thin', color='E2E8F0')
    )
    
    # --- ABA 1: Ranking Geral - Volume ---
    ws1 = wb_out.active
    ws1.title = "Ranking Geral - Volume"
    ws1.views.sheetView[0].showGridLines = True
    
    ws1.merge_cells('A1:J1')
    ws1['A1'] = "FECHAMENTO OFICIAL DE VENDAS — AÇÃO CRYSTAL ICE & PETRA ULTRA (AGO/2026)"
    ws1['A1'].font = Font(name='Segoe UI', size=14, bold=True, color='164E35')
    ws1['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws1.row_dimensions[1].height = 35
    
    ws1.merge_cells('A2:J2')
    ws1['A2'] = "Base auditada de vendas faturadas por RCA do Pedido (VEND-PED) • Ordenado por Volume Total (Caixas)"
    ws1['A2'].font = Font(name='Segoe UI', size=10, italic=True, color='64748B')
    ws1['A2'].alignment = Alignment(horizontal='center', vertical='center')
    ws1.row_dimensions[2].height = 20
    
    headers_ws1 = [
        "Pos.", "Empresa / Filial", "Supervisor", "Vendedor (RCA)", 
        "QTD Ultra", "QTD Ice", "QTD Ação (Total)", 
        "CLI Ultra", "CLI Ice", "CLI Ação (Total)"
    ]
    
    ws1.row_dimensions[4].height = 26
    for col_idx, h in enumerate(headers_ws1, 1):
        cell = ws1.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = thin_border
        
    df_vol = df.sort_values(by=['ACAO', 'ULTRA', 'ICE'], ascending=[False, False, False]).reset_index(drop=True)
    
    start_row = 5
    for idx, row in df_vol.iterrows():
        current_row = start_row + idx
        ws1.row_dimensions[current_row].height = 20
        is_even = (idx % 2 == 0)
        row_fill = fill_zebra if is_even else PatternFill(fill_type=None)
        
        pos_medal = str(idx + 1)
        if idx == 0: pos_medal = "🥇 1º"
        elif idx == 1: pos_medal = "🥈 2º"
        elif idx == 2: pos_medal = "🥉 3º"
        else: pos_medal = f"{idx+1}º"
        
        values = [
            pos_medal,
            row['emp_Empresa_chr'],
            row['sup_Supervisor_chr'],
            row['Vendedor'],
            row['ULTRA'],
            row['ICE'],
            row['ACAO'],
            row['CLI ULTRA'],
            row['CLI ICE'],
            row['CLI ACAO']
        ]
        
        for col_idx, val in enumerate(values, 1):
            cell = ws1.cell(row=current_row, column=col_idx, value=val)
            cell.border = thin_border
            
            if col_idx == 1:
                cell.font = font_bold
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.fill = row_fill
            elif col_idx in [2, 3, 4]:
                cell.font = font_data
                cell.alignment = Alignment(horizontal='left', vertical='center')
                cell.fill = row_fill
            elif col_idx in [5, 6, 7]:
                cell.font = font_bold if col_idx == 7 else font_data
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal='right', vertical='center')
                cell.fill = row_fill
            elif col_idx in [8, 9, 10]:
                cell.font = font_bold if col_idx == 10 else font_data
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal='right', vertical='center')
                cell.fill = row_fill
                
    # Linha de Totais Volume
    total_row = start_row + len(df_vol)
    ws1.row_dimensions[total_row].height = 24
    ws1.cell(row=total_row, column=1, value="TOTAL").alignment = Alignment(horizontal='center', vertical='center')
    ws1.cell(row=total_row, column=2, value=f"{len(df_vol)} Vendedores").alignment = Alignment(horizontal='left', vertical='center')
    ws1.cell(row=total_row, column=3, value="")
    ws1.cell(row=total_row, column=4, value="")
    
    ws1.cell(row=total_row, column=5, value=f"=SUM(E{start_row}:E{total_row-1})").number_format = '#,##0'
    ws1.cell(row=total_row, column=6, value=f"=SUM(F{start_row}:F{total_row-1})").number_format = '#,##0'
    ws1.cell(row=total_row, column=7, value=f"=SUM(G{start_row}:G{total_row-1})").number_format = '#,##0'
    ws1.cell(row=total_row, column=8, value=f"=SUM(H{start_row}:H{total_row-1})").number_format = '#,##0'
    ws1.cell(row=total_row, column=9, value=f"=SUM(I{start_row}:I{total_row-1})").number_format = '#,##0'
    ws1.cell(row=total_row, column=10, value=f"=SUM(J{start_row}:J{total_row-1})").number_format = '#,##0'
    
    for col_idx in range(1, 11):
        c = ws1.cell(row=total_row, column=col_idx)
        c.fill = fill_total
        c.font = font_total
        c.border = thin_border
        
    # --- ABA 2: Ranking Geral - Clientes (NOVA) ---
    ws_cli = wb_out.create_sheet(title="Ranking Geral - Clientes")
    ws_cli.views.sheetView[0].showGridLines = True
    
    ws_cli.merge_cells('A1:J1')
    ws_cli['A1'] = "RANKING GERAL POR COBERTURA DE CLIENTES — AÇÃO CRYSTAL ICE & PETRA ULTRA (AGO/2026)"
    ws_cli['A1'].font = Font(name='Segoe UI', size=14, bold=True, color='1E3A5F')
    ws_cli['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws_cli.row_dimensions[1].height = 35
    
    ws_cli.merge_cells('A2:J2')
    ws_cli['A2'] = "Base auditada de vendas faturadas por RCA do Pedido (VEND-PED) • Ordenado por Clientes Únicos Atendidos (CLI Ação)"
    ws_cli['A2'].font = Font(name='Segoe UI', size=10, italic=True, color='64748B')
    ws_cli['A2'].alignment = Alignment(horizontal='center', vertical='center')
    ws_cli.row_dimensions[2].height = 20
    
    headers_cli = [
        "Pos.", "Empresa / Filial", "Supervisor", "Vendedor (RCA)", 
        "CLI Ação (Total)", "CLI Ultra", "CLI Ice", 
        "QTD Ação (Total)", "QTD Ultra", "QTD Ice"
    ]
    
    ws_cli.row_dimensions[4].height = 26
    for col_idx, h in enumerate(headers_cli, 1):
        cell = ws_cli.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header_blue
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = thin_border
        
    df_cli = df.sort_values(by=['CLI ACAO', 'ACAO', 'ULTRA'], ascending=[False, False, False]).reset_index(drop=True)
    
    for idx, row in df_cli.iterrows():
        current_row = start_row + idx
        ws_cli.row_dimensions[current_row].height = 20
        is_even = (idx % 2 == 0)
        row_fill = fill_zebra if is_even else PatternFill(fill_type=None)
        
        pos_medal = str(idx + 1)
        if idx == 0: pos_medal = "🥇 1º"
        elif idx == 1: pos_medal = "🥈 2º"
        elif idx == 2: pos_medal = "🥉 3º"
        else: pos_medal = f"{idx+1}º"
        
        values = [
            pos_medal,
            row['emp_Empresa_chr'],
            row['sup_Supervisor_chr'],
            row['Vendedor'],
            row['CLI ACAO'],
            row['CLI ULTRA'],
            row['CLI ICE'],
            row['ACAO'],
            row['ULTRA'],
            row['ICE']
        ]
        
        for col_idx, val in enumerate(values, 1):
            cell = ws_cli.cell(row=current_row, column=col_idx, value=val)
            cell.border = thin_border
            
            if col_idx == 1:
                cell.font = font_bold
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.fill = row_fill
            elif col_idx in [2, 3, 4]:
                cell.font = font_data
                cell.alignment = Alignment(horizontal='left', vertical='center')
                cell.fill = row_fill
            elif col_idx in [5, 6, 7]:
                cell.font = font_bold if col_idx == 5 else font_data
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal='right', vertical='center')
                cell.fill = row_fill
            elif col_idx in [8, 9, 10]:
                cell.font = font_bold if col_idx == 8 else font_data
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal='right', vertical='center')
                cell.fill = row_fill
                
    # Linha de Totais Clientes
    tot_row_cli = start_row + len(df_cli)
    ws_cli.row_dimensions[tot_row_cli].height = 24
    ws_cli.cell(row=tot_row_cli, column=1, value="TOTAL").alignment = Alignment(horizontal='center', vertical='center')
    ws_cli.cell(row=tot_row_cli, column=2, value=f"{len(df_cli)} Vendedores").alignment = Alignment(horizontal='left', vertical='center')
    ws_cli.cell(row=tot_row_cli, column=3, value="")
    ws_cli.cell(row=tot_row_cli, column=4, value="")
    
    ws_cli.cell(row=tot_row_cli, column=5, value=f"=SUM(E{start_row}:E{tot_row_cli-1})").number_format = '#,##0'
    ws_cli.cell(row=tot_row_cli, column=6, value=f"=SUM(F{start_row}:F{tot_row_cli-1})").number_format = '#,##0'
    ws_cli.cell(row=tot_row_cli, column=7, value=f"=SUM(G{start_row}:G{tot_row_cli-1})").number_format = '#,##0'
    ws_cli.cell(row=tot_row_cli, column=8, value=f"=SUM(H{start_row}:H{tot_row_cli-1})").number_format = '#,##0'
    ws_cli.cell(row=tot_row_cli, column=9, value=f"=SUM(I{start_row}:I{tot_row_cli-1})").number_format = '#,##0'
    ws_cli.cell(row=tot_row_cli, column=10, value=f"=SUM(J{start_row}:J{tot_row_cli-1})").number_format = '#,##0'
    
    fill_total_blue = PatternFill(start_color='112233', end_color='112233', fill_type='solid')
    for col_idx in range(1, 11):
        c = ws_cli.cell(row=tot_row_cli, column=col_idx)
        c.fill = fill_total_blue
        c.font = font_total
        c.border = thin_border
        
    # --- ABA 3: Por Filial e Supervisor ---
    ws2 = wb_out.create_sheet(title="Por Filial e Supervisor")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2.merge_cells('A1:I1')
    ws2['A1'] = "DETALHAMENTO POR FILIAL E SUPERVISOR — VENDEDORES ORDENADOS POR VOLUME TOTAL"
    ws2['A1'].font = Font(name='Segoe UI', size=13, bold=True, color='164E35')
    ws2['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws2.row_dimensions[1].height = 30
    
    headers_ws2 = ["Empresa / Filial", "Supervisor", "Vendedor", "QTD Ultra", "QTD Ice", "QTD Ação (Total)", "CLI Ultra", "CLI Ice", "CLI Ação (Total)"]
    ws2.row_dimensions[3].height = 24
    for col_idx, h in enumerate(headers_ws2, 1):
        cell = ws2.cell(row=3, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = thin_border
        
    row_cursor = 4
    empresas = sorted(df['emp_Empresa_chr'].unique())
    for emp in empresas:
        df_emp = df[df['emp_Empresa_chr'] == emp]
        supervisores = sorted(df_emp['sup_Supervisor_chr'].unique())
        
        # Banner Filial
        ws2.merge_cells(f'A{row_cursor}:I{row_cursor}')
        b_cell = ws2.cell(row=row_cursor, column=1, value=f"🏢 FILIAL: {emp}  (Total: {df_emp['ACAO'].sum():,} cx • {df_emp['CLI ACAO'].sum():,} clis • {len(df_emp)} Vendedores)")
        b_cell.font = Font(name='Segoe UI', size=11, bold=True, color='FFFFFF')
        b_cell.fill = PatternFill(start_color='1E3A2F', end_color='1E3A2F', fill_type='solid')
        b_cell.alignment = Alignment(horizontal='left', vertical='center')
        ws2.row_dimensions[row_cursor].height = 24
        row_cursor += 1
        
        for sup in supervisores:
            df_sup = df_emp[df_emp['sup_Supervisor_chr'] == sup].sort_values(by=['ACAO', 'CLI ACAO'], ascending=[False, False])
            
            # Banner Supervisor
            ws2.merge_cells(f'A{row_cursor}:I{row_cursor}')
            s_cell = ws2.cell(row=row_cursor, column=1, value=f"  👤 Supervisor: {sup}  ({df_sup['ACAO'].sum():,} cx • {df_sup['CLI ACAO'].sum():,} clis • {len(df_sup)} vendedores)")
            s_cell.font = Font(name='Segoe UI', size=10, bold=True, color='164E35')
            s_cell.fill = PatternFill(start_color='E2EFE7', end_color='E2EFE7', fill_type='solid')
            s_cell.alignment = Alignment(horizontal='left', vertical='center')
            ws2.row_dimensions[row_cursor].height = 20
            row_cursor += 1
            
            for _, r in df_sup.iterrows():
                vals = [r['emp_Empresa_chr'], r['sup_Supervisor_chr'], r['Vendedor'], r['ULTRA'], r['ICE'], r['ACAO'], r['CLI ULTRA'], r['CLI ICE'], r['CLI ACAO']]
                ws2.row_dimensions[row_cursor].height = 19
                for c_idx, val in enumerate(vals, 1):
                    c = ws2.cell(row=row_cursor, column=c_idx, value=val)
                    c.border = thin_border
                    c.font = font_data
                    if c_idx in [4, 5, 6, 7, 8, 9]:
                        c.number_format = '#,##0'
                        c.alignment = Alignment(horizontal='right', vertical='center')
                        if c_idx == 6: c.font = font_bold
                row_cursor += 1
                
    # --- ABA 4: Resumo Filiais ---
    ws3 = wb_out.create_sheet(title="Resumo Filiais")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3.merge_cells('A1:I1')
    ws3['A1'] = "RESUMO CONSOLIDADO POR FILIAL / EMPRESA"
    ws3['A1'].font = Font(name='Segoe UI', size=13, bold=True, color='164E35')
    ws3['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws3.row_dimensions[1].height = 30
    
    h3 = [
        "Filial / Empresa", "Vendedores", "QTD Ultra", "QTD Ice", 
        "QTD Ação (Total)", "% Part. Volume", "Clientes Positivados", 
        "Média cx / Vendedor", "Média Clis / Vendedor"
    ]
    ws3.row_dimensions[3].height = 24
    for c_idx, text in enumerate(h3, 1):
        cell = ws3.cell(row=3, column=c_idx, value=text)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = thin_border
        
    filial_group = df.groupby('emp_Empresa_chr').agg(
        Vendedores=('Vendedor', 'count'),
        ULTRA=('ULTRA', 'sum'),
        ICE=('ICE', 'sum'),
        ACAO=('ACAO', 'sum'),
        CLI_ACAO=('CLI ACAO', 'sum')
    ).sort_values(by='ACAO', ascending=False).reset_index()
    
    total_acao_geral = df['ACAO'].sum()
    for idx, r in filial_group.iterrows():
        c_row = 4 + idx
        ws3.row_dimensions[c_row].height = 21
        pct = (r['ACAO'] / total_acao_geral)
        media_cx = r['ACAO'] / r['Vendedores']
        media_cli = r['CLI_ACAO'] / r['Vendedores']
        
        vals = [
            r['emp_Empresa_chr'], 
            r['Vendedores'], 
            r['ULTRA'], 
            r['ICE'], 
            r['ACAO'], 
            pct, 
            r['CLI_ACAO'],
            media_cx,
            media_cli
        ]
        for c_idx, val in enumerate(vals, 1):
            c = ws3.cell(row=c_row, column=c_idx, value=val)
            c.border = thin_border
            c.font = font_data
            if c_idx == 1:
                c.font = font_bold
            elif c_idx in [2, 3, 4, 5, 7]:
                c.number_format = '#,##0'
                c.alignment = Alignment(horizontal='right', vertical='center')
                if c_idx == 5: c.font = font_bold
            elif c_idx == 6:
                c.number_format = '0.0%'
                c.alignment = Alignment(horizontal='right', vertical='center')
            elif c_idx in [8, 9]:
                c.number_format = '#,##0.0'
                c.alignment = Alignment(horizontal='right', vertical='center')
                
    # Total Resumo
    tot_row_3 = 4 + len(filial_group)
    ws3.row_dimensions[tot_row_3].height = 24
    ws3.cell(row=tot_row_3, column=1, value="TOTAL GERAL").alignment = Alignment(horizontal='center', vertical='center')
    ws3.cell(row=tot_row_3, column=2, value=f"=SUM(B4:B{tot_row_3-1})").number_format = '#,##0'
    ws3.cell(row=tot_row_3, column=3, value=f"=SUM(C4:C{tot_row_3-1})").number_format = '#,##0'
    ws3.cell(row=tot_row_3, column=4, value=f"=SUM(D4:D{tot_row_3-1})").number_format = '#,##0'
    ws3.cell(row=tot_row_3, column=5, value=f"=SUM(E4:E{tot_row_3-1})").number_format = '#,##0'
    ws3.cell(row=tot_row_3, column=6, value=f"=SUM(F4:F{tot_row_3-1})").number_format = '0.0%'
    ws3.cell(row=tot_row_3, column=7, value=f"=SUM(G4:G{tot_row_3-1})").number_format = '#,##0'
    ws3.cell(row=tot_row_3, column=8, value=f"=AVERAGE(H4:H{tot_row_3-1})").number_format = '#,##0.0'
    ws3.cell(row=tot_row_3, column=9, value=f"=AVERAGE(I4:I{tot_row_3-1})").number_format = '#,##0.0'
    
    for c_idx in range(1, 10):
        c = ws3.cell(row=tot_row_3, column=c_idx)
        c.fill = fill_total
        c.font = font_total
        c.border = thin_border
        
    # Autoajuste de colunas para todas as abas
    for ws in [ws1, ws_cli, ws2, ws3]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or '')
                if not str(cell.coordinate) in ws.merged_cells:
                    max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)
            
    ws1.column_dimensions['D'].width = 38 # Vendedor
    ws1.column_dimensions['C'].width = 34 # Supervisor
    ws1.column_dimensions['B'].width = 18 # Empresa
    
    ws_cli.column_dimensions['D'].width = 38
    ws_cli.column_dimensions['C'].width = 34
    ws_cli.column_dimensions['B'].width = 18
    
    ws2.column_dimensions['C'].width = 38
    ws2.column_dimensions['B'].width = 34
    ws2.column_dimensions['A'].width = 18
    
    wb_out.save(excel_path)
    print(f"Excel salvo com sucesso em: {excel_path}")
    
    # -------------------------------------------------------------
    # 3. GERAR APRESENTAÇÃO PPTX (Apresentacao_Bonus_RH_ICE_ULTRA.pptx)
    # -------------------------------------------------------------
    ppt_path = 'C:/Users/a.alves/Downloads/ICE_ULTRA/Apresentacao_Bonus_RH_ICE_ULTRA.pptx'
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333) # 16:9 widescreen
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Cores PPT
    c_dark_green = RGBColor(15, 56, 34)
    c_mid_green = RGBColor(22, 78, 53)
    c_gold = RGBColor(201, 151, 56)
    c_gold_light = RGBColor(245, 230, 195)
    c_slate = RGBColor(30, 41, 59)
    c_gray_bg = RGBColor(248, 250, 252)
    c_white = RGBColor(255, 255, 255)
    c_table_header = RGBColor(22, 78, 53)
    c_table_header_blue = RGBColor(30, 58, 95)
    c_zebra = RGBColor(245, 248, 246)
    c_border = RGBColor(226, 232, 240)
    
    def add_header(slide, title_text, subtitle_text, banner_color=c_dark_green):
        # Background slide
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = c_gray_bg
        bg.line.fill.background()
        
        # Header banner
        header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        header.fill.solid()
        header.fill.fore_color.rgb = banner_color
        header.line.fill.background()
        
        # Dourado line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.08), Inches(13.333), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = c_gold
        line.line.fill.background()
        
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.85))
        tf = tx_box.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title_text
        p1.font.name = 'Segoe UI'
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = c_white
        
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.name = 'Segoe UI'
        p2.font.size = Pt(11)
        p2.font.color.rgb = c_gold_light
        
        # Footer
        ft_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.3))
        ft_tf = ft_box.text_frame
        fp = ft_tf.paragraphs[0]
        fp.text = "Campanha Crystal ICE & Petra Ultra • Vendas apuradas por RCA do Pedido (VEND-PED) • Fechamento Oficial (AGO/2026)"
        fp.font.name = 'Segoe UI'
        fp.font.size = Pt(9)
        fp.font.color.rgb = RGBColor(148, 163, 184)
        
    # SLIDE 1: Capa Executiva
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(12, 40, 25) # Verde escuro nobre
    bg1.line.fill.background()
    
    # Detalhe visual dourado na capa
    gold_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.8), Inches(0.15), Inches(3.6))
    gold_bar.fill.solid()
    gold_bar.fill.fore_color.rgb = c_gold
    gold_bar.line.fill.background()
    
    tb_title = slide1.shapes.add_textbox(Inches(1.6), Inches(1.7), Inches(10.5), Inches(3.8))
    tf1 = tb_title.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "AÇÃO COMERCIAL REGIONAL"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_gold
    
    p = tf1.add_paragraph()
    p.text = "CRYSTAL ICE & PETRA ULTRA"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = c_white
    
    p = tf1.add_paragraph()
    p.text = "Relatório Oficial de Fechamento de Vendas & Desempenho Comercial (RH)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(226, 232, 240)
    
    p = tf1.add_paragraph()
    p.text = "\n✦ Período Oficial da Campanha (Agosto/2026)  |  ✦ 64 Vendedores  |  ✦ 2.320 Caixas Faturadas  |  ✦ 875 Clientes Atendidos"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(13)
    p.font.color.rgb = c_gold_light
    
    # Badge na capa (Sem menção a meta 50)
    badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.6), Inches(5.6), Inches(10.2), Inches(0.9))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(22, 60, 40)
    badge.line.color.rgb = c_gold
    badge_tf = badge.text_frame
    badge_p = badge_tf.paragraphs[0]
    badge_p.text = "Critério de Apuração: RCA que emitiu o pedido (VEND-PED) • Rankings Oficiais por Volume e Positivação de Clientes"
    badge_p.alignment = PP_ALIGN.CENTER
    badge_p.font.name = 'Segoe UI'
    badge_p.font.size = Pt(12)
    badge_p.font.bold = True
    badge_p.font.color.rgb = c_white
    
    # SLIDE 2: Resumo Executivo / KPIs Gerais
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "RESUMO EXECUTIVO CONSOLIDADO DA CAMPANHA", "Visão geral de faturamento, participação de marcas e distribuição de clientes por filial")
    
    # 4 Cartões KPI
    kpis = [
        ("TOTAL GERAL AÇÃO", f"{df['ACAO'].sum():,} cx", "100% do Volume Total", c_dark_green),
        ("PETRA ULTRA", f"{df['ULTRA'].sum():,} cx", f"{(df['ULTRA'].sum()/df['ACAO'].sum())*100:.1f}% do Volume Total", RGBColor(161, 98, 7)),
        ("CRYSTAL ICE", f"{df['ICE'].sum():,} cx", f"{(df['ICE'].sum()/df['ACAO'].sum())*100:.1f}% do Volume Total", RGBColor(185, 28, 28)),
        ("CLIENTES ATENDIDOS", f"{df['CLI ACAO'].sum():,} clis", "Positivações no Período", RGBColor(3, 105, 161)),
    ]
    
    for i, (kpi_label, kpi_val, kpi_sub, kpi_color) in enumerate(kpis):
        kpi_x = Inches(0.8 + i * 2.95)
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, kpi_x, Inches(1.4), Inches(2.8), Inches(1.5))
        card.fill.solid()
        card.fill.fore_color.rgb = c_white
        card.line.color.rgb = c_border
        
        tb = slide2.shapes.add_textbox(kpi_x, Inches(1.45), Inches(2.8), Inches(1.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = kpi_label
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = RGBColor(100, 116, 139)
        p.alignment = PP_ALIGN.CENTER
        
        p = tf.add_paragraph()
        p.text = kpi_val
        p.font.name = 'Segoe UI'
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = kpi_color
        p.alignment = PP_ALIGN.CENTER
        
        p = tf.add_paragraph()
        p.text = kpi_sub
        p.font.name = 'Segoe UI'
        p.font.size = Pt(9)
        p.font.color.rgb = RGBColor(71, 85, 105)
        p.alignment = PP_ALIGN.CENTER
        
    # Tabela Resumo das Filiais no Slide 2
    table_shape2 = slide2.shapes.add_table(7, 7, Inches(0.8), Inches(3.2), Inches(11.7), Inches(3.5))
    t2 = table_shape2.table
    t2_headers = ["Filial / Empresa", "Vendedores", "Petra Ultra (cx)", "Crystal Ice (cx)", "Volume Total (cx)", "% Part.", "Clientes Atendidos"]
    t2_col_widths = [Inches(2.5), Inches(1.3), Inches(1.6), Inches(1.6), Inches(1.7), Inches(1.3), Inches(1.7)]
    for i, w in enumerate(t2_col_widths): t2.columns[i].width = w
    
    for j, h in enumerate(t2_headers):
        cell = t2.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_table_header
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = c_white
        p.alignment = PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT
        
    for idx, r in filial_group.iterrows():
        t_vals = [
            r['emp_Empresa_chr'], 
            f"{r['Vendedores']}", 
            f"{r['ULTRA']:,}", 
            f"{r['ICE']:,}", 
            f"{r['ACAO']:,}", 
            f"{(r['ACAO']/total_acao_geral)*100:.1f}%",
            f"{r['CLI_ACAO']:,}"
        ]
        for j, val in enumerate(t_vals):
            c = t2.cell(idx+1, j)
            c.fill.solid()
            c.fill.fore_color.rgb = c_zebra if idx % 2 == 0 else c_white
            p = c.text_frame.paragraphs[0]
            p.text = val
            p.font.name = 'Segoe UI'
            p.font.size = Pt(10)
            p.font.bold = (j in [0, 4, 6])
            p.font.color.rgb = c_slate
            p.alignment = PP_ALIGN.RIGHT if j in [1, 2, 3, 4, 5, 6] else PP_ALIGN.LEFT
            
    # SLIDE 3: TOP 10 RANKING GERAL — MAIORES VOLUMES (CAIXAS)
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "TOP 10 RANKING GERAL — MAIORES VOLUMES (CAIXAS)", "Os 10 vendedores com maior volume faturado na campanha de Crystal Ice & Petra Ultra")
    
    top10_vol = df.sort_values(by=['ACAO', 'ULTRA', 'ICE'], ascending=[False, False, False]).head(10).reset_index(drop=True)
    table_shape3 = slide3.shapes.add_table(11, 8, Inches(0.8), Inches(1.45), Inches(11.7), Inches(5.3))
    t3 = table_shape3.table
    t3_headers = ["Colocação", "Empresa / Filial", "Supervisor", "Vendedor", "QTD Ultra", "QTD Ice", "Total Ação (cx)", "Clientes Atend."]
    t3_widths = [Inches(1.1), Inches(1.8), Inches(2.4), Inches(2.7), Inches(0.9), Inches(0.9), Inches(1.0), Inches(0.9)]
    for i, w in enumerate(t3_widths): t3.columns[i].width = w
    
    for j, h in enumerate(t3_headers):
        cell = t3.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_table_header
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = c_white
        p.alignment = PP_ALIGN.CENTER if j in [0, 4, 5, 6, 7] else PP_ALIGN.LEFT
        
    for idx, r in top10_vol.iterrows():
        pos_txt = f"{idx+1}º"
        if idx == 0: pos_txt = "🥇 1º"
        elif idx == 1: pos_txt = "🥈 2º"
        elif idx == 2: pos_txt = "🥉 3º"
        
        vals = [pos_txt, r['emp_Empresa_chr'], r['sup_Supervisor_chr'], r['Vendedor'], f"{r['ULTRA']:,}", f"{r['ICE']:,}", f"{r['ACAO']:,}", f"{r['CLI ACAO']:,}"]
        for j, val in enumerate(vals):
            c = t3.cell(idx+1, j)
            c.fill.solid()
            c.fill.fore_color.rgb = c_zebra if idx % 2 == 0 else c_white
            p = c.text_frame.paragraphs[0]
            p.text = val
            p.font.name = 'Segoe UI'
            p.font.size = Pt(9.5)
            p.font.bold = (j in [0, 6])
            p.font.color.rgb = c_slate
            p.alignment = PP_ALIGN.RIGHT if j in [4, 5, 6, 7] else (PP_ALIGN.CENTER if j == 0 else PP_ALIGN.LEFT)
            
    # SLIDE 4 (NOVO): TOP 10 RANKING GERAL — MAIOR COBERTURA DE CLIENTES (POSITIVAÇÃO)
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "TOP 10 RANKING GERAL — MAIOR COBERTURA DE CLIENTES (POSITIVAÇÃO)", "Os 10 vendedores com maior número de clientes atendidos e positivados na campanha", banner_color=c_table_header_blue)
    
    top10_cli = df.sort_values(by=['CLI ACAO', 'ACAO', 'ULTRA'], ascending=[False, False, False]).head(10).reset_index(drop=True)
    table_shape4 = slide4.shapes.add_table(11, 8, Inches(0.8), Inches(1.45), Inches(11.7), Inches(5.3))
    t4 = table_shape4.table
    t4_headers = ["Colocação", "Empresa / Filial", "Supervisor", "Vendedor", "Clientes Ação", "CLI Ultra", "CLI Ice", "Total Volume (cx)"]
    t4_widths = [Inches(1.1), Inches(1.8), Inches(2.4), Inches(2.7), Inches(1.0), Inches(0.9), Inches(0.9), Inches(0.9)]
    for i, w in enumerate(t4_widths): t4.columns[i].width = w
    
    for j, h in enumerate(t4_headers):
        cell = t4.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_table_header_blue
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = c_white
        p.alignment = PP_ALIGN.CENTER if j in [0, 4, 5, 6, 7] else PP_ALIGN.LEFT
        
    for idx, r in top10_cli.iterrows():
        pos_txt = f"{idx+1}º"
        if idx == 0: pos_txt = "🥇 1º"
        elif idx == 1: pos_txt = "🥈 2º"
        elif idx == 2: pos_txt = "🥉 3º"
        
        vals = [pos_txt, r['emp_Empresa_chr'], r['sup_Supervisor_chr'], r['Vendedor'], f"{r['CLI ACAO']:,}", f"{r['CLI ULTRA']:,}", f"{r['CLI ICE']:,}", f"{r['ACAO']:,}"]
        for j, val in enumerate(vals):
            c = t4.cell(idx+1, j)
            c.fill.solid()
            c.fill.fore_color.rgb = c_zebra if idx % 2 == 0 else c_white
            p = c.text_frame.paragraphs[0]
            p.text = val
            p.font.name = 'Segoe UI'
            p.font.size = Pt(9.5)
            p.font.bold = (j in [0, 4])
            p.font.color.rgb = c_slate
            p.alignment = PP_ALIGN.RIGHT if j in [4, 5, 6, 7] else (PP_ALIGN.CENTER if j == 0 else PP_ALIGN.LEFT)
            
    # FUNÇÃO HELPER: Adicionar Slide de Tabela por Filial (Sem Bônus, com Clientes Ação)
    def add_branch_slide(title, subtitle, branch_df):
        slide = prs.slides.add_slide(blank_layout)
        add_header(slide, title, subtitle)
        
        # Montar lista ordenada de linhas com agrupamento por supervisor
        rows_to_render = []
        supervisores = sorted(branch_df['sup_Supervisor_chr'].unique())
        
        for sup in supervisores:
            df_sup = branch_df[branch_df['sup_Supervisor_chr'] == sup].sort_values(by=['ACAO', 'CLI ACAO'], ascending=[False, False])
            # Linha de cabeçalho do supervisor
            rows_to_render.append({
                'is_sup_header': True,
                'sup_name': sup,
                'total_sup': df_sup['ACAO'].sum(),
                'total_cli': df_sup['CLI ACAO'].sum(),
                'count_sup': len(df_sup)
            })
            for _, r in df_sup.iterrows():
                rows_to_render.append({
                    'is_sup_header': False,
                    'emp': r['emp_Empresa_chr'],
                    'sup': r['sup_Supervisor_chr'],
                    'vend': r['Vendedor'],
                    'ultra': r['ULTRA'],
                    'ice': r['ICE'],
                    'acao': r['ACAO'],
                    'cli_acao': r['CLI ACAO']
                })
                
        num_rows = len(rows_to_render) + 1
        table_height = min(Inches(5.6), Inches(0.32 * num_rows + 0.3))
        table_shape = slide.shapes.add_table(num_rows, 6, Inches(0.8), Inches(1.4), Inches(11.7), table_height)
        t = table_shape.table
        
        headers = ["Supervisor", "Vendedor", "QTD Ultra", "QTD Ice", "Total Ação (cx)", "Clientes Ação"]
        widths = [Inches(3.2), Inches(3.7), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.2)]
        for i, w in enumerate(widths): t.columns[i].width = w
        
        for j, h in enumerate(headers):
            cell = t.cell(0, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_table_header
            p = cell.text_frame.paragraphs[0]
            p.text = h
            p.font.name = 'Segoe UI'
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = c_white
            p.alignment = PP_ALIGN.CENTER if j in [2, 3, 4, 5] else PP_ALIGN.LEFT
            
        for i, item in enumerate(rows_to_render):
            row_idx = i + 1
            if item['is_sup_header']:
                # Linha destacada do supervisor
                c0 = t.cell(row_idx, 0)
                c0.fill.solid()
                c0.fill.fore_color.rgb = RGBColor(226, 239, 231)
                p0 = c0.text_frame.paragraphs[0]
                p0.text = f"👤 {item['sup_name']}"
                p0.font.name = 'Segoe UI'
                p0.font.size = Pt(9.5)
                p0.font.bold = True
                p0.font.color.rgb = c_dark_green
                
                c1 = t.cell(row_idx, 1)
                c1.fill.solid()
                c1.fill.fore_color.rgb = RGBColor(226, 239, 231)
                p1 = c1.text_frame.paragraphs[0]
                p1.text = f"Subtotal da equipe ({item['count_sup']} vendedores):"
                p1.font.name = 'Segoe UI'
                p1.font.size = Pt(9)
                p1.font.italic = True
                p1.font.color.rgb = RGBColor(71, 85, 105)
                
                for j in range(2, 6):
                    cj = t.cell(row_idx, j)
                    cj.fill.solid()
                    cj.fill.fore_color.rgb = RGBColor(226, 239, 231)
                    pj = cj.text_frame.paragraphs[0]
                    if j == 4:
                        pj.text = f"{item['total_sup']:,}"
                        pj.font.bold = True
                        pj.alignment = PP_ALIGN.RIGHT
                    elif j == 5:
                        pj.text = f"{item['total_cli']:,}"
                        pj.font.bold = True
                        pj.alignment = PP_ALIGN.RIGHT
                    else:
                        pj.text = ""
                    pj.font.name = 'Segoe UI'
                    pj.font.size = Pt(9.5)
                    pj.font.color.rgb = c_dark_green
            else:
                vals = [
                    "",
                    item['vend'],
                    f"{item['ultra']:,}",
                    f"{item['ice']:,}",
                    f"{item['acao']:,}",
                    f"{item['cli_acao']:,}"
                ]
                for j, val in enumerate(vals):
                    cell = t.cell(row_idx, j)
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = c_zebra if row_idx % 2 == 0 else c_white
                    p = cell.text_frame.paragraphs[0]
                    p.text = val
                    p.font.name = 'Segoe UI'
                    p.font.size = Pt(9)
                    p.font.bold = (j in [4, 5])
                    p.font.color.rgb = c_slate
                    p.alignment = PP_ALIGN.RIGHT if j in [2, 3, 4, 5] else PP_ALIGN.LEFT
                    
    # SLIDE 5: CD-BOA VISTA
    df_bv = df[df['emp_Empresa_chr'] == 'CD-BOA VISTA']
    add_branch_slide(
        "FILIAL: CD-BOA VISTA — RESULTADOS POR SUPERVISOR E VENDEDOR",
        f"Total da Filial: {df_bv['ACAO'].sum():,} caixas faturadas  •  {df_bv['CLI ACAO'].sum():,} clientes atendidos  •  {len(df_bv)} Vendedores",
        df_bv
    )
    
    # SLIDE 6: CD-ITACOATIARA
    df_ita = df[df['emp_Empresa_chr'] == 'CD-ITACOATIARA']
    add_branch_slide(
        "FILIAL: CD-ITACOATIARA — RESULTADOS POR SUPERVISOR E VENDEDOR",
        f"Total da Filial: {df_ita['ACAO'].sum():,} caixas faturadas  •  {df_ita['CLI ACAO'].sum():,} clientes atendidos  •  {len(df_ita)} Vendedores",
        df_ita
    )
    
    # SLIDE 7: CD-MACAPA
    df_mcp = df[df['emp_Empresa_chr'] == 'CD-MACAPA']
    add_branch_slide(
        "FILIAL: CD-MACAPÁ — RESULTADOS POR SUPERVISOR E VENDEDOR",
        f"Total da Filial: {df_mcp['ACAO'].sum():,} caixas faturadas  •  {df_mcp['CLI ACAO'].sum():,} clientes atendidos  •  {len(df_mcp)} Vendedores",
        df_mcp
    )
    
    # SLIDES 8, 9 e 10: CD-MANAUS (Dividido em 3 slides equilibrados para máxima legibilidade)
    df_mao = df[df['emp_Empresa_chr'] == 'CD-MANAUS']
    sups_p1 = ['EDIOMAR GRIJO', 'RAFAEL DA SILVA OLIVEIRA']
    sups_p2 = ['MARCONE CARVALHO', 'THIAGO LUIZ NEGREIROS', 'JARLISON JUNIOR SOUZA AUZIER']
    sups_p3 = ['JHONISON DE SOUZA SERRAO', 'ERMESON BARBOSA DE SOUZA', 'BRUNO RENAN BADEIRA GOMES']
    
    df_mao_p1 = df_mao[df_mao['sup_Supervisor_chr'].isin(sups_p1)]
    df_mao_p2 = df_mao[df_mao['sup_Supervisor_chr'].isin(sups_p2)]
    df_mao_p3 = df_mao[df_mao['sup_Supervisor_chr'].isin(sups_p3)]
    
    add_branch_slide(
        "FILIAL: CD-MANAUS (PARTE 1/3) — RESULTADOS POR SUPERVISOR E VENDEDOR",
        f"Supervisores: Ediomar Grijó & Rafael Oliveira  •  Subtotal: {df_mao_p1['ACAO'].sum():,} caixas ({df_mao_p1['CLI ACAO'].sum():,} clientes)",
        df_mao_p1
    )
    
    add_branch_slide(
        "FILIAL: CD-MANAUS (PARTE 2/3) — RESULTADOS POR SUPERVISOR E VENDEDOR",
        f"Supervisores: Marcone Carvalho, Thiago Negreiros & Jarlison Auzier  •  Subtotal: {df_mao_p2['ACAO'].sum():,} caixas ({df_mao_p2['CLI ACAO'].sum():,} clientes)",
        df_mao_p2
    )

    add_branch_slide(
        "FILIAL: CD-MANAUS (PARTE 3/3) — RESULTADOS POR SUPERVISOR E VENDEDOR",
        f"Supervisores: Jhonison Serrão, Ermeson Barbosa & Bruno Renan  •  Subtotal: {df_mao_p3['ACAO'].sum():,} caixas ({df_mao_p3['CLI ACAO'].sum():,} clientes)",
        df_mao_p3
    )
    
    # SLIDE 11: CD-PARINTINS & CD-TABATINGA
    df_interior = df[df['emp_Empresa_chr'].isin(['CD-PARINTINS', 'CD-TABATINGA'])]
    add_branch_slide(
        "FILIAIS: CD-PARINTINS & CD-TABATINGA — RESULTADOS POR SUPERVISOR E VENDEDOR",
        f"Parintins: {df[df['emp_Empresa_chr']=='CD-PARINTINS']['ACAO'].sum():,} cx  •  Tabatinga: {df[df['emp_Empresa_chr']=='CD-TABATINGA']['ACAO'].sum():,} cx",
        df_interior
    )
    
    # SLIDE 12: Conclusão & Próximos Passos RH
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "NOTAS TÉCNICAS, AUDITORIA & DIRETRIZES OPERACIONAIS (RH)", "Conclusão da apuração de desempenho comercial e critérios de validação")
    
    card_rh = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    card_rh.fill.solid()
    card_rh.fill.fore_color.rgb = c_white
    card_rh.line.color.rgb = c_border
    
    tb_rh = slide12.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.9), Inches(4.6))
    tf_rh = tb_rh.text_frame
    tf_rh.word_wrap = True
    
    p = tf_rh.paragraphs[0]
    p.text = "NOTAS TÉCNICAS E VALIDAÇÃO DA APURAÇÃO"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_dark_green
    
    bullets = [
        ("Critério de Vendedor Válido (VEND-PED):", " A apuração considera estritamente o RCA que emitiu o pedido (IDRCA_PED no Winthor Histórico e IDRCA no Winthor Atual), garantindo que todo o esforço de venda seja creditado com exatidão a quem efetivamente gerou o faturamento."),
        ("Duplo Critério de Reconhecimento:", " A apuração apresenta tanto o Ranking Geral por Volume Faturado (caixas) quanto o Ranking Geral por Cobertura de Mercado (positivação de clientes), permitindo uma avaliação abrangente do esforço comercial sem corte arbitrário."),
        ("Totais Consolidados Auditados:", " Foram faturadas 1.557 caixas de Petra Ultra e 763 caixas de Crystal Ice, totalizando 2.320 caixas e 875 positivações de clientes no período oficial da campanha em toda a regional."),
        ("Arquivos Completos em Excel:", " O arquivo em Excel ('Vendedores_Bonus_RH_ICE_ULTRA.xlsx') contém 4 abas estruturadas (Ranking por Volume, Ranking por Clientes, Detalhamento por Supervisor e Resumo por Filial) com fórmulas dinâmicas para conciliação com o RH."),
        ("Atualização no Power BI:", " O modelo PBIP ('ICE_ULTRA.SemanticModel') e a página 'Info' ('ICE_ULTRA.Report') estão sincronizados com as medidas ativas USERELATIONSHIP e a tabela expandida de vendedores com ordenação decrescente por volume para consulta contínua.")
    ]
    
    for b_title, b_desc in bullets:
        p = tf_rh.add_paragraph()
        p.text = f"\n• {b_title}"
        p.font.name = 'Segoe UI'
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = c_slate
        
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.color.rgb = RGBColor(71, 85, 105)
        
    prs.save(ppt_path)
    print(f"PowerPoint salvo com sucesso em: {ppt_path}")

if __name__ == '__main__':
    generate()
