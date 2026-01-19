# HealthSync Project Repository Initialization

# Create a README.md file for the HealthSync project
echo "# HealthSync" > README.md
echo "HealthSync is a web application built with FastAPI, Next.js, PostgreSQL, LangChain, and OpenAI." >> README.md
echo "" >> README.md
echo "## Project Structure" >> README.md
echo "" >> README.md
echo "HealthSync/" >> README.md
echo "├── backend/" >> README.md
echo "│   ├── main.py" >> README.md
echo "│   └── requirements.txt" >> README.md
echo "└── frontend/" >> README.md
echo "    ├── pages/" >> README.md
echo "    ├── public/" >> README.md
echo "    └── package.json" >> README.md
echo "" >> README.md
echo "" >> README.md
echo "## Installation" >> README.md
echo "1. Clone the repository." >> README.md
echo "2. Navigate to the backend directory and install dependencies." >> README.md
echo "3. Navigate to the frontend directory and install dependencies." >> README.md
echo "" >> README.md
echo "## Usage" >> README.md
echo "Run the FastAPI backend and Next.js frontend." >> README.md
echo "" >> README.md
echo "## License" >> README.md
echo "This project is licensed under the MIT License." >> README.md

# Initialize Git repository
git init
git add README.md
git commit -m "Initial commit: Set up project repository and README"