from tools.stock_tools import add_stock, search_stock, delete_stock


def route_tool(tool_name, args):

    if tool_name == "add_stock":
        return add_stock(args)
    elif tool_name == "search_stock":
        return search_stock(args["semantic_query"], args["filters"])
    elif tool_name == "delete_stock":
        try:
            print(1)
            return delete_stock(args["Code"])
        except:
            print(2)
            return {
                "tool": "delete_stock",
                "success": False,
                "message": "missing code argument"
            }
    else:
        return {
            "tool": None,
            "success": False,
            "message": "Unknown tool"
        }