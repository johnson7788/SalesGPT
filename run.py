import argparse
import json
import os
from salesgpt.agents import SalesGPT
from langchain.chat_models import ChatLiteLLM
from dotenv import load_dotenv
load_dotenv() # loads .env file 

from salesgpt.agents import SalesGPT

if __name__ == "__main__":
    # Initialize aSalrgparse
    parser = argparse.ArgumentParser(description="Description of your program")

    # Add arguments
    parser.add_argument(
        "--config", type=str, help="Path to agent config file", default=""
    )
    parser.add_argument("--verbose", type=bool, help="Verbosity", default=False)
    parser.add_argument(
        "--max_num_turns",
        type=int,
        help="Maximum number of turns in the sales conversation",
        default=10,
    )
    parser.add_argument('-ut',"--use_tools", action='store_true', help='是否使用工具')

    # Parse arguments
    args = parser.parse_args()

    # Access arguments
    config_path = args.config
    verbose = args.verbose
    max_num_turns = args.max_num_turns
    use_tools = args.use_tools

    llm = ChatLiteLLM(temperature=0.2)
    if config_path == "":
        print("No agent config specified, using a standard config")
        if use_tools:
            sales_agent = SalesGPT.from_llm(
                llm,
                use_tools=use_tools,
                product_catalog="examples/sample_product_catalog.txt",
                salesperson_name="Ted Lasso",
                verbose=verbose,
            )
        else:
            sales_agent = SalesGPT.from_llm(llm, verbose=verbose)
    else:
        print(f"使用配置文件: {config_path}，构建Agent")
        with open(config_path, "r", encoding="UTF-8") as f:
            config = json.load(f)
        sales_agent = SalesGPT.from_llm(llm, use_tools=use_tools, verbose=verbose, **config)
    # 设置对话的历史
    sales_agent.seed_agent()
    print("=" * 10)
    cnt = 0
    print(f"开始进行对话")
    while cnt != max_num_turns:
        cnt += 1
        if cnt == max_num_turns:
            print("Maximum number of turns reached - ending the conversation.")
            break
        sales_agent.step()

        # end conversation
        if "<END_OF_CHAT>" in sales_agent.conversation_history[-1]:
            print("Agent determined it is time to end the conversation.")
            break
        human_input = input("Your response: ")
        sales_agent.human_step(human_input)
        print("=" * 10)
