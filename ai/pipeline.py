from ai.gemini import ai_decide
from tools.router import route_tool


def ai_action_decide(user_input):

    decision = ai_decide(user_input)


    # if decision['tool'] is None:
    #     return """
    #
    #     """

    print("Decision:", decision)
    print("Tool:", decision["tool"])


    result = route_tool(decision["tool"], decision["args"])

    return result

