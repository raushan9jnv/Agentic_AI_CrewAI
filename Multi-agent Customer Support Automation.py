# import warnings
# warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

# llm = ChatGroq(
#     api_key="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",
#     model ="mixtral-8x7b-32768"
# )

llm = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key= "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",
    model_name = "mixtral-8x7b-32768"
)

#Role playing, Focus and cooperation
#agent-1
support_agent = Agent(
    role =" Senior Support Representative",
    goal = " Be the most friendly and helpful"
            "support representative in your team",
    backstory= (
            " You work at crewAI (https://crewai.com) and "
            " are now working on providing "
            "support to {customer}, a super important customer "
            "for your company "
            "You need to make sure that you provide the best support! "
            "MAke sure to provide full complete answers,"
            " and make no assumptions."
            ),
    allow_delegation = False,
    verbose = True
)

# By not setting allow_delegation = False, allow_delegation takes it defualt value of being True
#This means the agent can delegtae its work to another agent which is better suited to do a particular task.

#agent-2

support_quality_assurance_agent = Agent(
    role = "Supportt Quality Assurance Specialist",
    goal ="get recognition for providing the"
         "best support quality assurance in your team",
    backstory= (
        "You work at crewAI (https://crewai.com) and "
        "are now working with team "
        " on a request from {customer} ensuring that"
        " the support representative is "
        "providing best support possible.\n"
        "you need to make sure that the support representative "
        "is providing full "
        "complete answers, and make no assumptions."
    ),
    verbose = True
)

# Role playing: both agents have been given a role, goal and backstory
# Focus: Both agents have been prompted to get into the character of the roles they are playing.
# Cooperation : Support Quality Assurance Agent can delegate work back to the support Agent, allowing for these agents to work together.

# Tools, Guardrails and Memory

#tools
 
# possible custom tools: Load customer data, Tap into previous conversations, Load data from a CRM, checking existing bug reports,
# checking existing feature requests, checking ongoing tickets and ....more.

docs_scrape_tool = ScrapeWebsiteTool( website_url = "https://docs.crewai.com/guides/crews/first-crew")

#Different ways to give agents tools
 # -Agent level: The agent can use the tool(s) on any task it performs.
 # - Task Level: The agent will only use the tool(s) when performing that specific task.
 # Note: Task tools override the Agent Tools.

 #creating task 
 # - here passing the tool on Task level

#task-1
inquiry_resolution = Task(
        description = (
         "{customer} just reached out with a super important ask:\n"
         "{inquiry} \n\n"
         "{person} from {customer} is the one that reached out."
         "Make sure to use everything you know "
         "to provide the best support possible."
         "You must strive to provide a complete "
         "and accurate response to the customer's inquiry."
        ),
        expected_output= (
            "A detailed, informative response to the "
            "customer's inquiry that addresses "
            "all aspects of thier question.\n"
            "The response should include references "
            "to everything you used to find the answer, "
            "including external data or solutions. "
            "ensure the answer is complete, "
            "leaving no questions unanswered, and maintain a helpful and friendly "
            "tone throghout."
        ),
        tools =[docs_scrape_tool],
        agent = support_agent,
 )

#quality_assurance_review is not using any Tool(s).
# Here the QA Agent will only review the work of the support agent.

#task-2
quality_assurance_review = Task(
    description=(
        "Review the response drafted by the senior Support Representative for {cusomer}'s inquiry."
        "Ensure that the answer is comprehensive, accurate, and adheres to the "
        "high-quality standards expected for customer support. \n"
        "verify that all parts of the customer's inquiry "
        "have been addressed"
        "thoroughly, with a helpful and friendly tone.\n"
        "Check for references and sources used to "
        "find the information, "
        "ensuring the response is well-supported and "
        "leaves no questions unanswered."
    ),
    expected_output=(
        "A final, detailed, and informative response "
        "ready to be sent to the customer.\n"
        "This response should fully address the "
        "customer's inquiry, incorporating all "
        "relevant feedback and improvements.\n"
        "Don't be too formal, we are a chill and cool comapny "
        "but maintain a professional and friendly tone thoughout."
    ),
    agent= support_quality_assurance_agent,
)

#creating the crew

#setting memory=True when putting the crew together enables memory.

crew = Crew(
    agents = [support_agent, support_quality_assurance_agent],
    tasks = [inquiry_resolution,quality_assurance_review],
    verbose = 2,
    memory = True,
    llm =llm
)

# Running the crew
#By running the execution below, we can see that the agents and the responses are within the scope of what we expect from them.

inputs ={
    "customer": "Infosys",
    "person": "Raushan",
    "Inquiry": "I need help with setting up a Crew"
                " and kicking it off, specifically "
                "how can i add memory to my crew?"
                "Can you provide guidance?"
}

result = crew.kickoff(inputs = inputs)