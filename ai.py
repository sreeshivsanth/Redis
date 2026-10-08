from typing import Annotated, TypedDict
from dotenv import load_dotenv
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.tools import tool

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# 2. GRAPH STATE
# ============================================================

class GraphState(TypedDict):
    messages: Annotated[list, add_messages]


# ============================================================
# 3. STUDENT DATABASE
# ============================================================

students = {
    "101": {
        "name": "Arun",
        "department": "CSE",
        "attendance": 82
    },
    "102": {
        "name": "Priya",
        "department": "AI",
        "attendance": 91
    },
    "103": {
        "name": "Rahul",
        "department": "ECE",
        "attendance": 76
    },
    "104": {
        "name": "Ananya",
        "department": "CSE",
        "attendance": 88
    }
}


# ============================================================
# 4. CALCULATOR TOOL
# ============================================================

@tool
def calculator(expression: str) -> str:
    """
    Perform basic mathematical calculations.
    """

    try:
        allowed_characters = "0123456789+-*/(). "

        if not all(char in allowed_characters for char in expression):
            return "Invalid mathematical expression."

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return f"{result:.2f}"

    except ZeroDivisionError:
        return "Cannot divide by zero."

    except Exception:
        return "Sorry, I could not calculate that expression."


# ============================================================
# 5. STUDENT INFORMATION TOOL
# ============================================================

@tool
def student_information(name: str) -> str:
    """
    Find a student's department.
    """

    for student in students.values():

        if student["name"].lower() == name.lower():

            return (
                f"{student['name']} is from the "
                f"{student['department']} department."
            )

    return f"No student named {name} was found."


# ============================================================
# 6. ATTENDANCE TOOL
# ============================================================

@tool
def attendance(name: str) -> str:
    """
    Find a student's attendance percentage.
    """

    for student in students.values():

        if student["name"].lower() == name.lower():

            return (
                f"{student['name']}'s current attendance "
                f"is {student['attendance']}%."
            )

    return f"No student named {name} was found."


# ============================================================
# 7. DATE AND TIME TOOL
# ============================================================

@tool
def get_date_time() -> str:
    """
    Get the current date and time.
    """

    current_time = datetime.now()

    return current_time.strftime(
        "Current date: %d-%m-%Y, Current time: %I:%M:%S %p"
    )

# ============================================================
# 7. CREATE LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# ============================================================
# 8. CONNECT TOOLS TO LLM
# ============================================================

tools = [
    calculator,
    student_information,
    attendance,
    get_date_time
]

llm_with_tools = llm.bind_tools(tools)


# ============================================================
# 9. CHAT NODE
# ============================================================

def chat_node(state: GraphState) -> dict:

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# ============================================================
# 10. CREATE LANGGRAPH
# ============================================================

builder = StateGraph(GraphState)

builder.add_node(
    "chat",
    chat_node
)

builder.add_node(
    "tools",
    ToolNode(tools)
)

builder.add_edge(
    START,
    "chat"
)

builder.add_conditional_edges(
    "chat",
    tools_condition
)

builder.add_edge(
    "tools",
    "chat"
)


# IMPORTANT:
# This creates the graph variable
graph = builder.compile()


# ============================================================
# 11. MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 55)
    print("       AGENTIC AI STUDENT ASSISTANT")
    print("=" * 55)

    print("\nAvailable Tools:")
    print("1. Calculator")
    print("2. Student Information")
    print("3. Attendance")
    print("4. Get Date and Time")

    print("\nType 'exit' to quit.")

    # Conversation memory
    conversation_history = []

    while True:

        user_input = input("\nUser: ").strip()

        if user_input.lower() in ("exit", "quit", "q"):

            print("Agent: Goodbye!")
            break

        if not user_input:
            continue

        try:

            # Add user message
            conversation_history.append(
                ("user", user_input)
            )

            # Run the graph
            result = graph.invoke({
                "messages": conversation_history
            })

            # Save updated conversation
            conversation_history = result["messages"]

            # Display response
            print(
                "\nAgent:",
                result["messages"][-1].content
            )

        except Exception as e:

            print("\nError:", e)