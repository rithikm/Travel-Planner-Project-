# travel_crew.py
import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Task, Process, LLM
from crewai_tools import SerperDevTool

# Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
search_tool = SerperDevTool()

# Initialize Gemini LLM
llm = LLM(
    api_key=api_key,
    model="gemini/gemini-2.5-flash",
    temperature=0.1
)


# Define CrewAI Agents
destination_expert = Agent(
    role="Destination Expert",
    goal="Recommend great destinations based on preferences in 2025.",
    backstory="A seasoned traveler who knows hidden gems around the world.",
    tools=[search_tool],
    verbose=True,
    llm=llm,

)

itinerary_designer = Agent(
    role="Itinerary Designer",
    goal="Create detailed travel itineraries with daily activities and tips.",
    backstory="A creative trip planner with an eye for unique experiences.",
    llm=llm
)

budget_advisor = Agent(
    role="Budget Advisor",
    goal="Estimate travel budgets and cost-saving strategies.",
    backstory="A financial planner specialized in travel cost optimization.",
    llm=llm
)

# Define Tasks
destination_task = Task(
    description=(
        "Search the web using your tools to find the best travel experiences in {destination} "
        "based on the user's preferences: Budget: {budget}, Interests: {interests}, Time of Year: {time_of_year}. "
        "Include only destinations and activities that are relevant in 2025."
    ),
    expected_output=(
        "Return your answer in this structured format:\n\n"
        "### 🌍 Recommended Destinations\n"
        "For the specified destination ({destination}), include:\n"
        "- **Why Visit (1-2 sentences)**\n"
        "- **Best Time to Go**\n"
        "- **Average Daily Cost (USD)**\n"
        "- **Top 3 Attractions**\n"
        "- **Travel Tip**\n\n"
        "Use Markdown formatting for readability."
    ),
    agent=destination_expert
)

itinerary_task = Task(
     description=(
        "Create a detailed 3-day travel itinerary for the destination chosen. "
        "Focus on activities related to {interests} and affordable experiences for a {budget} budget."
    ),
    expected_output=(
        "Return the itinerary in Markdown with this structure:\n\n"
        "### 🗓️ 3-Day Itinerary\n"
        "- **Day 1:** Morning / Afternoon / Evening activities\n"
        "- **Day 2:** Morning / Afternoon / Evening activities\n"
        "- **Day 3:** Morning / Afternoon / Evening activities\n\n"
        "Include at least one local food recommendation per day."
    ),
    agent=itinerary_designer
)

budget_task = Task(
    description=(
        "Estimate total travel costs for the itinerary considering the user's budget ({budget}). "
        "Provide cost-saving tips and spending breakdown."
    ),
    expected_output=(
        "Return a structured table with sections:\n\n"
        "### 💰 Budget Overview\n"
        "- **Estimated Total Cost (USD)**\n"
        "- **Daily Breakdown (Accommodation, Food, Transport, Activities)**\n\n"
        "### 🪙 Money-Saving Tips\n"
        "- Tip 1\n"
        "- Tip 2\n"
        "- Tip 3"
    ),
    agent=budget_advisor
)

# Define the crew
travel_crew = Crew(
    agents=[destination_expert, itinerary_designer, budget_advisor],
    tasks=[destination_task, itinerary_task, budget_task],
    process=Process.sequential
)

# Function to generate the travel plan
def generate_travel_plan(destination, budget, interests, time_of_year):
    inputs = {
        "destination": destination,
        "budget": budget,
        "interests": interests,
        "time_of_year": time_of_year
    }
    
    # Kick off CrewAI
    result = travel_crew.kickoff(inputs=inputs)
    
    # Extract readable text from each task output
    readable_results = []
    for task_output in result.tasks_output:
        readable_results.append(task_output.raw)  # only the raw readable text
    
    return readable_results




