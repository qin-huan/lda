import pyecharts.options as opts
from pyecharts.charts import Line
import pandas as pd
import os
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot

def main(inputFile, sheetName, chartTitle, outputDir, outName):
    folder = os.path.exists(outputDir)
    if not folder:
        os.makedirs(outputDir)

    xlsx = pd.read_excel(inputFile,sheet_name=sheetName,header=None)
    dates = xlsx.values[1:,0]
    themes = xlsx.values[0,1:11]
    line = (
        Line(init_opts=opts.InitOpts(
            width='1280px',
            height='720px',
        ))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=chartTitle,
                pos_top='bottom',
                pos_left='center',
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger='axis',
                background_color='#808080',
                textstyle_opts=opts.TextStyleOpts(
                    color='#ffffff',
                ),
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(is_show=True),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axisline_opts=opts.AxisLineOpts(is_show=True)
            ),
        )
    .add_xaxis(xaxis_data=dates))
    for index in range(len(themes)):
        name = themes[index]
        value = xlsx.values[1:,index+1]
        line.add_yaxis(
            series_name=name, 
            y_axis=value, 
            label_opts=opts.LabelOpts(
                is_show=False,
                position='top',
            ),
            is_connect_nones=True,
            is_smooth=False,
        )
    line.render(outputDir+outName)
    # make_snapshot(snapshot, line.render(), outputDir+outName)

class Arg:
    def __init__(self, inFile, sheet, title, outDir):
        self.inFile = inFile
        self.sheet = sheet
        self.title = title
        self.outDir = outDir

args = [
Arg('./in_3_11/jiangsu_all/all_attention.xlsx', 'all_attention', '江苏省所有', './out_3_11/江苏省所有/'),
Arg('./in_3_11/jiangsu_all_city/city_all_attention.xlsx', 'city_all_attention', '江苏省所有市级', './out_3_11/江苏省所有市级/'),
Arg('./in_3_11/jiangsu_all_county/county_all_attention.xlsx', 'county_all_attention', '江苏省所有县级', './out_3_11/江苏省所有县级/'),
Arg('./in_3_11/jiangsu_city_with_county/changzhou/changzhou_all_attention.xlsx', 'changzhou_all_attention', '江苏省常州市（包含该市区县级数据）', './out_3_11/江苏省市级所有(包含市级)/常州/'),
Arg('./in_3_11/jiangsu_county_without_city/changzhou/changzhou_all_attention.xlsx', 'changzhou_all_attention', '江苏省常州市所有(不包含市级数据)', './out_3_11/江苏省市级所有(不包含市级)/常州/'),
Arg('./in_3_11/jiangsu_province_city/changzhou.csv_attention.xlsx', 'changzhou.csv_attention', "江苏省常州市", './out_3_11/江苏省省市/常州/'),
Arg('./in_3_11/jiangsu_city_with_county/huaian/huaian_all_attention.xlsx', 'huaian_all_attention', '江苏省淮安市（包含该市区县级数据）', './out_3_11/江苏省市级所有(包含市级)/淮安/'),
Arg('./in_3_11/jiangsu_county_without_city/huaian/huaian_all_attention.xlsx', 'huaian_all_attention', '江苏省淮安市所有(不包含市级数据)', './out_3_11/江苏省市级所有(不包含市级)/淮安/'),
Arg('./in_3_11/jiangsu_province_city/huaian.csv_attention.xlsx', 'huaian.csv_attention', "江苏省淮安市", './out_3_11/江苏省省市/淮安/'),
Arg('./in_3_11/jiangsu_city_with_county/lianyungang/lianyungang_all_attention.xlsx', 'lianyungang_all_attention', '江苏省连云港市（包含该市区县级数据）', './out_3_11/江苏省市级所有(包含市级)/连云港/'),
Arg('./in_3_11/jiangsu_county_without_city/lianyungang/lianyungang_all_attention.xlsx', 'lianyungang_all_attention', '江苏省连云港市所有(不包含市级数据)', './out_3_11/江苏省市级所有(不包含市级)/连云港/'),
Arg('./in_3_11/jiangsu_province_city/lianyungang.csv_attention.xlsx', 'lianyungang.csv_attention', "江苏省连云港市", './out_3_11/江苏省省市/连云港/'),
Arg('./in_3_11/jiangsu_city_with_county/nanjing/nanjing_all_attention.xlsx', 'nanjing_all_attention', '江苏省南京市（包含该市区县级数据）', './out_3_11/江苏省市级所有(包含市级)/南京/'),
Arg('./in_3_11/jiangsu_county_without_city/nanjing/nanjing_all_attention.xlsx', 'nanjing_all_attention', '江苏省南京市所有(不包含市级数据)', './out_3_11/江苏省市级所有(不包含市级)/南京/'),
Arg('./in_3_11/jiangsu_province_city/nanjing.csv_attention.xlsx', 'nanjing.csv_attention', "江苏省南京市", './out_3_11/江苏省省市/南京/'),
Arg('./in_3_11/jiangsu_city_with_county/nantong/nantong_all_attention.xlsx', 'nantong_all_attention', '江苏省南通市（包含该市区县级数据）', './out_3_11/江苏省市级所有(包含市级)/南通/'),
Arg('./in_3_11/jiangsu_county_without_city/nantong/nantong_all_attention.xlsx', 'nantong_all_attention', '江苏省南通市所有(不包含市级数据)', './out_3_11/江苏省市级所有(不包含市级)/南通/'),
Arg('./in_3_11/jiangsu_province_city/nantong.csv_attention.xlsx', 'nantong.csv_attention', "江苏省南通市", './out_3_11/江苏省省市/南通/'),
Arg('./in_3_11/jiangsu_city_with_county/suzhou/suzhou_all_attention.xlsx', 'suzhou_all_attention', '江苏省苏州市（包含该市区县级数据）', './out_3_11/江苏省市级所有(包含市级)/苏州/'),
Arg('./in_3_11/jiangsu_county_without_city/suzhou/suzhou_all_attention.xlsx', 'suzhou_all_attention', '江苏省苏州市所有(不包含市级数据)', './out_3_11/江苏省市级所有(不包含市级)/苏州/'),
Arg('./in_3_11/jiangsu_province_city/suzhou.csv_attention.xlsx', 'suzhou.csv_attention', "江苏省苏州市", './out_3_11/江苏省省市/苏州/'),
Arg('./in_3_11/jiangsu_city_with_county/suqian/suqian_all_attention.xlsx', 'suqian_all_attention', '江苏省宿迁市（包含该市区县级数据）', './out_3_11/江苏省市级所有(包含市级)/宿迁/'),
Arg('./in_3_11/jiangsu_county_without_city/suqian/suqian_all_attention.xlsx', 'suqian_all_attention', '江苏省宿迁市所有(不包含市级数据)', './out_3_11/江苏省市级所有(不包含市级)/宿迁/'),
Arg('./in_3_11/jiangsu_province_city/suqian.csv_attention.xlsx', 'suqian.csv_attention', "江苏省宿迁市", './out_3_11/江苏省省市/宿迁/'),
Arg('./in_3_11/jiangsu_city_with_county/taizhou/taizhou_all_attention.xlsx', 'taizhou_all_attention', '江苏省泰州市（包含该市区县级数据）', './out_3_11/江苏省市级所有(包含市级)/泰州/'),
Arg('./in_3_11/jiangsu_county_without_city/taizhou/taizhou_all_attention.xlsx', 'taizhou_all_attention', '江苏省泰州市所有(不包含市级数据)', './out_3_11/江苏省市级所有(不包含市级)/泰州/'),
Arg('./in_3_11/jiangsu_province_city/taizhou.csv_attention.xlsx', 'taizhou.csv_attention', "江苏省泰州市", './out_3_11/江苏省省市/泰州/'),
Arg('./in_3_11/jiangsu_city_with_county/wuxi/wuxi_all_attention.xlsx', 'wuxi_all_attention', '江苏省无锡市（包含该市区县级数据）', './out_3_11/江苏省市级所有(包含市级)/无锡/'),
Arg('./in_3_11/jiangsu_county_without_city/wuxi/wuxi_all_attention.xlsx', 'wuxi_all_attention', '江苏省无锡市所有(不包含市级数据)', './out_3_11/江苏省市级所有(不包含市级)/无锡/'),
Arg('./in_3_11/jiangsu_province_city/wuxi.csv_attention.xlsx', 'wuxi.csv_attention', "江苏省无锡市", './out_3_11/江苏省省市/无锡/'),
Arg('./in_3_11/jiangsu_city_with_county/xuzhou/xuzhou_all_attention.xlsx', 'xuzhou_all_attention', '江苏省徐州市（包含该市区县级数据）', './out_3_11/江苏省市级所有(包含市级)/徐州/'),
Arg('./in_3_11/jiangsu_county_without_city/xuzhou/xuzhou_all_attention.xlsx', 'xuzhou_all_attention', '江苏省徐州市所有(不包含市级数据)', './out_3_11/江苏省市级所有(不包含市级)/徐州/'),
Arg('./in_3_11/jiangsu_province_city/xuzhou.csv_attention.xlsx', 'xuzhou.csv_attention', "江苏省徐州市", './out_3_11/江苏省省市/徐州/'),
Arg('./in_3_11/jiangsu_city_with_county/yancheng/yancheng_all_attention.xlsx', 'yancheng_all_attention', '江苏省盐城市（包含该市区县级数据）', './out_3_11/江苏省市级所有(包含市级)/盐城/'),
Arg('./in_3_11/jiangsu_county_without_city/yancheng/yancheng_all_attention.xlsx', 'yancheng_all_attention', '江苏省盐城市所有(不包含市级数据)', './out_3_11/江苏省市级所有(不包含市级)/盐城/'),
Arg('./in_3_11/jiangsu_province_city/yancheng.csv_attention.xlsx', 'yancheng.csv_attention', "江苏省盐城市", './out_3_11/江苏省省市/盐城/'),
Arg('./in_3_11/jiangsu_city_with_county/yangzhou/yangzhou_all_attention.xlsx', 'yangzhou_all_attention', '江苏省扬州市（包含该市区县级数据）', './out_3_11/江苏省市级所有(包含市级)/扬州/'),
Arg('./in_3_11/jiangsu_county_without_city/yangzhou/yangzhou_all_attention.xlsx', 'yangzhou_all_attention', '江苏省扬州市所有(不包含市级数据)', './out_3_11/江苏省市级所有(不包含市级)/扬州/'),
Arg('./in_3_11/jiangsu_province_city/yangzhou.csv_attention.xlsx', 'yangzhou.csv_attention', "江苏省扬州市", './out_3_11/江苏省省市/扬州/'),
Arg('./in_3_11/jiangsu_city_with_county/zhenjiang/zhenjiang_all_attention.xlsx', 'zhenjiang_all_attention', '江苏省镇江市（包含该市区县级数据）', './out_3_11/江苏省市级所有(包含市级)/镇江/'),
Arg('./in_3_11/jiangsu_county_without_city/zhenjiang/zhenjiang_all_attention.xlsx', 'zhenjiang_all_attention', '江苏省镇江市所有(不包含市级数据)', './out_3_11/江苏省市级所有(不包含市级)/镇江/'),
Arg('./in_3_11/jiangsu_province_city/zhenjiang.csv_attention.xlsx', 'zhenjiang.csv_attention', "江苏省镇江市", './out_3_11/江苏省省市/镇江/'),
Arg('./in_3_11/only_jiangsu_province/weibojiangsu_attention.xlsx', 'weibojiangsu_attention', "江苏省政府", './out_3_11/江苏省省市/江苏省/'),
]

for arg in args:
    sheetName1 = arg.sheet+'1'
    sheetName2 = arg.sheet+'2'
    filename1 = sheetName1+'.html'
    filename2 = sheetName2+'.html'
    main(arg.inFile, sheetName1, arg.title, arg.outDir, filename1)
    main(arg.inFile, sheetName2, arg.title, arg.outDir, filename2)

