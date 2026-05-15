<h1>AI Travel Planner</h1>

<p>
AI Travel Planner is a console-based multi-tool travel planning assistant built in Python. It accepts a natural-language travel request such as <code>Plan a 3 day trip from Delhi to Goa with a budget of 15000</code>, extracts the important trip details, calls multiple travel-related tools, and generates a structured travel plan containing trip summary, flight details, hotel options, places to visit, weather forecast, and estimated budget.
</p>

<h2>Project Purpose</h2>

<p>
This project is designed to demonstrate practical AI-agent workflow skills rather than production-grade booking accuracy. The main goal is to show that a single travel agent can take one user query, break it into useful sub-tasks, call specialized tools, combine their outputs, and present a readable final plan in the terminal.
</p>

<h2>Main Features</h2>

<ul>
  <li>Natural-language travel query input from the terminal.</li>
  <li>Trip summary extraction from a free-text prompt.</li>
  <li>Flight search using a dedicated flight tool.</li>
  <li>Hotel recommendation generation using a hotel tool.</li>
  <li>Tourist place suggestions using a places tool.</li>
  <li>3-day weather forecast using Open-Meteo weather data.</li>
  <li>Readable weather labels such as Clear sky, Mainly clear, Light drizzle, and Thunderstorm.</li>
  <li>Budget estimation using available tool outputs and fallback values where needed.</li>
  <li>Simple terminal-friendly output format suitable for demos and viva-style explanation.</li>
</ul>

<h2>How the Project Works</h2>

<ol>
  <li>The user runs the travel agent from the terminal.</li>
  <li>The program asks for a travel query.</li>
  <li>The query is parsed to identify source city, destination city, duration, and budget.</li>
  <li>The agent calls individual tools for flights, hotels, places, and weather.</li>
  <li>The responses from those tools are combined into one final travel plan.</li>
  <li>The program estimates total trip cost based on available flight cost, hotel price, and local expenses.</li>
  <li>The final result is printed in a structured format inside the terminal.</li>
</ol>

<h2>Expected Project Structure</h2>

<pre><code>ai-travel-planner/
├── agents/
│   └── travel_agent.py
├── tools/
│   ├── flight_tool.py
│   ├── hotel_tool.py
│   ├── places_tool.py
│   └── weather_tool.py
├── data/                 (optional, if local datasets are used)
├── requirements.txt
├── README.md
└── .gitignore
</code></pre>

<p>
The exact structure in your local repository may vary slightly, but the main working files are the agent file inside <code>agents/</code> and the tool files inside <code>tools/</code>.
</p>

<h2>Core Files Explained</h2>

<h3><code>agents/travel_agent.py</code></h3>
<p>
This is the main controller of the project. It collects the user query, extracts trip details, calls all required tools, and builds the final terminal output.
</p>

<h3><code>tools/flight_tool.py</code></h3>
<p>
This file is responsible for finding matching flight information between source and destination. If no route exists in the current dataset or logic, the final output shows that no flight was found.
</p>

<h3><code>tools/hotel_tool.py</code></h3>
<p>
This file returns recommended hotel options for the destination city along with hotel ID, city, rating, price per night, and amenities.
</p>

<h3><code>tools/places_tool.py</code></h3>
<p>
This file returns tourist places or attractions for the destination city. It typically includes place name, place ID, category, city, and rating.
</p>

<h3><code>tools/weather_tool.py</code></h3>
<p>
This tool fetches weather forecast data using the Open-Meteo API. It converts the destination city into coordinates, calls the weather API, and prints a readable 3-day forecast. Numeric weather codes are converted into human-friendly text labels.
</p>

<h2>Technologies Used</h2>

<ul>
  <li>Python</li>
  <li>LangChain tool decorator pattern</li>
  <li>Requests library</li>
  <li>Open-Meteo API for weather forecast</li>
  <li>Git and GitHub for version control</li>
  <li>Git Bash / terminal-based workflow</li>
</ul>

<h2>Environment Setup</h2>

<h3>1. Clone the repository</h3>

<pre><code>git clone &lt;your-repository-url&gt;
cd ai-travel-planner
</code></pre>

<h3>2. Create a virtual environment</h3>

<pre><code>python -m venv venv
</code></pre>

<h3>3. Activate the virtual environment</h3>

<p><strong>Windows Git Bash:</strong></p>
<pre><code>source venv/Scripts/activate
</code></pre>

<p><strong>Windows CMD:</strong></p>
<pre><code>venv\Scripts\activate
</code></pre>

<p><strong>PowerShell:</strong></p>
<pre><code>venv\Scripts\Activate.ps1
</code></pre>

<h3>4. Install dependencies</h3>

<pre><code>pip install -r requirements.txt
</code></pre>

<p>
If <code>requirements.txt</code> is missing or incomplete, install the main dependencies manually:
</p>

<pre><code>pip install requests langchain
</code></pre>

<h2>How to Run the Project</h2>

<p>
After activating the virtual environment and installing dependencies, run the agent using:
</p>

<pre><code>python agents/travel_agent.py
</code></pre>

<p>
When prompted with <code>Enter your travel query:</code>, type a natural-language request.
</p>

<h3>Example Input</h3>

<pre><code>Plan a 3 day trip from Delhi to Goa with a budget of 15000
</code></pre>

<h3>What the Output Shows</h3>

<ul>
  <li>Trip summary: source, destination, duration, and user budget.</li>
  <li>Flight details: matching flights if available, otherwise a no-flight message.</li>
  <li>Hotel options: recommended hotels with price and amenities.</li>
  <li>Top places to visit in the destination.</li>
  <li>Weather forecast for the next 3 days.</li>
  <li>Budget estimate combining flights, hotel cost, and local expenses.</li>
</ul>

<h2>How to Test Each Part Separately</h2>

<h3>Test the full agent</h3>
<pre><code>python agents/travel_agent.py
</code></pre>

<h3>Test the weather tool only</h3>
<pre><code>python -c "from tools.weather_tool import weather_tool; print(weather_tool.run('Delhi'))"
</code></pre>

<h3>Expected weather test behavior</h3>
<ul>
  <li>It should print a weather forecast for 3 days.</li>
  <li>It should show readable labels such as <code>Mainly clear</code>, <code>Light drizzle</code>, or <code>Thunderstorm</code>.</li>
  <li>It should not print only raw weather code values.</li>
</ul>

<h3>Test with another city</h3>
<pre><code>python -c "from tools.weather_tool import weather_tool; print(weather_tool.run('Goa'))"
</code></pre>

<h3>Test invalid city handling</h3>
<pre><code>python -c "from tools.weather_tool import weather_tool; print(weather_tool.run('UnknownCity'))"
</code></pre>

<p>
This should return a message like coordinates not found, depending on your current implementation.
</p>

<h2>How to Demonstrate the Project</h2>

<p>
If you want to show this project during interview, portfolio review, internship discussion, or classroom demo, follow this order:
</p>

<ol>
  <li>Open the project in VS Code.</li>
  <li>Open the terminal in the root folder.</li>
  <li>Activate the virtual environment.</li>
  <li>Run <code>python agents/travel_agent.py</code>.</li>
  <li>Enter a travel query such as <code>Plan a 3 day trip from Delhi to Goa with a budget of 15000</code>.</li>
  <li>Explain that the agent takes one natural-language prompt and coordinates multiple tools behind the scenes.</li>
  <li>Show the final output sections one by one: summary, hotels, places, weather, and budget.</li>
  <li>Optionally run the weather tool separately to prove that tools can also be tested independently.</li>
</ol>

<h2>Sample Demo Flow</h2>

<pre><code>python agents/travel_agent.py
</code></pre>

<p>Enter this:</p>

<pre><code>Plan a 3 day trip from Delhi to Goa with a budget of 15000
</code></pre>

<p>
Then explain the result like this:
</p>

<ul>
  <li>The query parser extracts Delhi as source, Goa as destination, 3 days as duration, and 15000 as budget.</li>
  <li>The flight tool checks whether a route is available.</li>
  <li>The hotel tool recommends suitable stays.</li>
  <li>The places tool lists important attractions.</li>
  <li>The weather tool fetches real forecast data and prints readable weather descriptions.</li>
  <li>The budget section combines costs into an estimated total trip amount.</li>
</ul>

<h2>Current Example Result</h2>

<p>
A successful sample run currently shows:
</p>

<ul>
  <li>Trip summary from Delhi to Goa for 3 days.</li>
  <li>No matching flights found in the current flight data for that route.</li>
  <li>Hotel recommendations such as Royal Heritage, Comfort Suites, and Budget Stay Inn.</li>
  <li>Top places to visit in Goa.</li>
  <li>Weather forecast showing readable labels like Thunderstorm.</li>
  <li>Total estimated cost of Rs.11696.00 for the sample trip output that was tested.</li>
</ul>

<h2>Budget Logic</h2>

<p>
The project estimates budget using three main parts:
</p>

<ul>
  <li>Flight cost</li>
  <li>Hotel cost</li>
  <li>Local expenses</li>
</ul>

<p>
If a flight is not found, the current implementation may use a fallback flight estimate. Hotel cost is generally derived from the selected hotel price and number of nights. Local expenses are added as a simple daily estimate.
</p>

<h2>Weather Logic</h2>

<p>
The weather tool uses city-to-coordinate mapping first. Then it calls Open-Meteo using latitude and longitude and requests daily temperature and weather-code data. After receiving the weather code, it converts it into a readable description so the output becomes user-friendly.
</p>

<h2>Example Weather Labels</h2>

<ul>
  <li>0 = Clear sky</li>
  <li>1 = Mainly clear</li>
  <li>2 = Partly cloudy</li>
  <li>3 = Overcast</li>
  <li>51 = Light drizzle</li>
  <li>61 = Slight rain</li>
  <li>63 = Moderate rain</li>
  <li>95 = Thunderstorm</li>
</ul>

<h2>Common Commands</h2>

<pre><code># run the main project
python agents/travel_agent.py

# test only weather tool
python -c "from tools.weather_tool import weather_tool; print(weather_tool.run('Delhi'))"

# check git status
git status

# view recent commits
git log --oneline -5
</code></pre>

<h2>Troubleshooting</h2>

<h3>1. Module not found error</h3>
<p>
Make sure the virtual environment is activated and dependencies are installed.
</p>

<h3>2. No flights found</h3>
<p>
This may be expected if the route does not exist in the current local flight dataset or logic. It does not necessarily mean the project is broken.
</p>

<h3>3. Coordinates not found for a city</h3>
<p>
The city may not exist in the manually defined coordinate dictionary inside <code>weather_tool.py</code>. Add the new city with latitude and longitude if needed.
</p>

<h3>4. Weather API request failed</h3>
<p>
Check your internet connection and confirm that the Open-Meteo API is reachable from your machine.
</p>

<h3>5. Output formatting issues</h3>
<p>
Re-run the script from the root directory of the project to avoid import-path issues.
</p>

<h2>How to Extend the Project</h2>

<ul>
  <li>Add more cities and coordinates.</li>
  <li>Improve query parsing for more complex travel requests.</li>
  <li>Connect to real hotel and flight APIs.</li>
  <li>Add a Streamlit or web frontend.</li>
  <li>Export results to PDF or HTML itinerary pages.</li>
  <li>Add date-based planning instead of only duration-based planning.</li>
  <li>Improve budget calculation with transport, food, and activity categories.</li>
</ul>

<h2>Why This Project Is Good for Portfolio</h2>

<ul>
  <li>It shows practical Python project structuring.</li>
  <li>It demonstrates tool-based agent design.</li>
  <li>It shows API integration through weather forecasting.</li>
  <li>It includes parsing, formatting, and reporting logic in one project.</li>
  <li>It is easy to explain during interviews because input and output are visible in the terminal.</li>
</ul>

<h2>Suggested Interview Explanation</h2>

<p>
This project is a Python-based AI travel planner that takes a natural-language travel request and turns it into a structured trip plan. The system is built using an agent-controller approach where one central file handles the user request and multiple tool files handle specialized tasks such as flights, hotels, places, and weather. The project demonstrates prompt-style input handling, modular tool architecture, API integration, and readable terminal output for end-user travel planning.
</p>

<h2>Final Notes</h2>

<p>
This project is best presented as a skill-demonstration project. It is not intended to be a complete production booking platform, but it successfully proves the ability to design a modular AI-style workflow, test individual tools, combine outputs, and deliver a clear result from one user prompt.
</p>
