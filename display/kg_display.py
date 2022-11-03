import json

from pyecharts import options as opts
from pyecharts.charts import Graph
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType


def node_add(node_name, node_category, node_symbol_size=90):
    # return opts.GraphNode(
    #     name=node_name, category=node_category, symbol_size=node_symbol_size
    # )
    return {
        "name": node_name,
        "category": node_category,
        "symbol_size": node_symbol_size,
        "symbol": 'roundRect'
    }


def rel_add(s_node_name, o_node_name, rel_type):
    # return opts.GraphLink(source=s_node_name, target=o_node_name, label_opts=opts.LabelOpts(formatter=rel_type))
    return {
        "source": s_node_name,
        "target": o_node_name,
        "value": rel_type,
    }


def category_add(category_name, category_symbol="rect", category_symbol_size=120):
    # return opts.GraphCategory(name=category_name, symbol=category_symbol)
    return {"name": category_name, "symbol": category_symbol, "symbol_size":120}


if __name__ == "__main__":
    # 将json中的数据加载到程序中
    fp = open("../data/accident.json", "r", encoding="utf-8")
    input_dict = json.load(fp)
    # 定义将作为关系的节点属性，用于构建三元组
    rel_dict = {
        "time": "Time",
        "location_province": "Province",
        "casualty_number": "Casualty_Number",
        "accident_cause": "Accident_Cause",
        "solution_method": "Method",
        "location_detail": "Detail_Location",
    }
    # 定义类别
    categories_dict = {
        "time": "Time",
        "location_province": "Province",
        "casualty_number": "Casualty_Number",
        "accident_cause": "Accident_Cause",
        "solution_method": "Method",
        "location_detail": "Detail_Location",
    }
    rel_list = rel_dict.keys()
    # 方形 rect, roundRect
    # 圆形 circle
    nodes_data = []
    nodes_dict = {}
    # 字典的键值对为节点名称：节点类别
    for node in input_dict.keys():
        # nodes_data.append(
        #     {"name": node,
        #      "category": "Accident",
        #      "symbol_size": 60}
        # )
        nodes_data.append(node_add(node_name=node,node_category="Accident"))
        accident_dict = input_dict[node]
        for ppt in accident_dict.keys():
            value = categories_dict[ppt]
            key = accident_dict[ppt]
            if type(key) == list:
                for i in key:
                    nodes_dict[i] = value
            else:
                nodes_dict[key] = value
    # 将node分别添加进nodes_data
    for node in nodes_dict.keys():
        nodes_data.append(node_add(node_name=node, node_category=nodes_dict[node]))
    # 添加links_data类数据
    links_data = []
    input_list = list(input_dict.keys())
    for node in input_list:
        element_dict = input_dict[node]
        s_name = node
        element_list = list(element_dict.keys())
        for element in element_list:
            if type(element_dict[element]) == list:
                for i in element_dict[element]:
                    o_name = i
                    links_data.append(rel_add(s_name, o_name, rel_type=element))
            else:
                o_name = element_dict[element]
                links_data.append(rel_add(s_name, o_name, rel_type=element))
    # 添加category类数据
    categories_data = []
    for i in categories_dict.values():
        categories_data.append(category_add(i))
    categories_data.append({"name": "Accident",
                            "symbol": "roundRect"})

    init_opts = opts.InitOpts(
        width="1920px",  # 图宽
        height="1080px",  # 图高
        renderer="canvas",  # 渲染模式 svg 或 canvas，即 RenderType.CANVAS 或 RenderType.SVG
        theme=ThemeType.DARK,
        # 主题风格可选：WHITE,LIGHT,DARK,CHALK,ESSOS,INFOGRAPHIC,MACARONS,PURPLE_PASSION,ROMA,ROMANTIC,SHINE,VINTAGE,WALDEN,WESTEROS,WONDERLAND
        # bg_color="#FFFFF0",  # 背景颜色
        js_host="",  # js主服务位置 留空则默认官方远程主服务
    )
    edge_label = opts.LabelOpts(
        is_show=True,
        position="middle",
        color="black",
        formatter=JsCode(
            """
        function(params){
        return params.value
        }
        """
        ),
    )
    linestyle_opts = opts.LineStyleOpts(
        width=1,
        opacity=0.9,
        curve=0.1,
        type_="dashed",  # "solid",
    )
    graph = Graph(init_opts)
    graph.add(
        "",
        nodes_data,
        links_data,
        categories_data,
        repulsion=4000,
        edge_symbol=["", "arrow"],
        is_draggable=True,
        edge_label=edge_label,
        linestyle_opts=linestyle_opts,
    )
    graph.set_global_opts(
        title_opts=opts.TitleOpts(title="示例图"),
    )
    graph.render("../output/example.html")
