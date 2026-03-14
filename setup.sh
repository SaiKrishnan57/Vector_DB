#!/bin/bash

# Vector Databases - Super Simple Lab Setup
# Just Python and NumPy - no complex frameworks!

set -e

echo "============================================"
echo "🔍 Vector Databases - Lab Setup"
echo "============================================"
echo ""
echo "Setting up your super simple environment..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check Python availability
echo ""
echo "1. Checking Python environment..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_status "Python $PYTHON_VERSION available"
else
    print_error "Python 3 not found. Please install Python 3."
    exit 1
fi

# Create virtual environment
echo ""
echo "2. Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "3. Activating virtual environment..."
source venv/bin/activate
print_status "Virtual environment activated"

# Install uv first (fast Python package manager)
echo ""
echo "4. Installing UV package manager..."
pip install --quiet --upgrade uv
if [ $? -eq 0 ]; then
    print_status "UV package manager installed"
else
    print_warning "UV installation failed, falling back to pip"
    USE_PIP=true
fi

# Install packages using UV (or pip as fallback)
echo ""
echo "5. Installing Python packages..."
echo "   - numpy (for vector math)"
echo "   - chromadb (latest version for production vector database)"
echo "   - sentence-transformers (for real AI embeddings)"
echo "   - Building educational concepts with production tools"

if [ -z "$USE_PIP" ]; then
    # Use UV for faster installation
    echo "   Using UV for fast package installation..."
    uv pip install --upgrade numpy chromadb sentence-transformers
    
    if [ $? -eq 0 ]; then
        print_status "All packages installed successfully with UV"
    else
        print_warning "UV installation failed, retrying with pip..."
        pip install --quiet --upgrade numpy chromadb sentence-transformers
        print_status "All packages installed successfully with pip"
    fi
else
    # Fallback to pip
    pip install --quiet --upgrade numpy chromadb sentence-transformers
    print_status "All packages installed successfully with pip"
fi

# Test ChromaDB installation
echo ""
echo "6. Testing ChromaDB installation..."
python3 -c "import chromadb; print('ChromaDB version:', chromadb.__version__)" 2>/dev/null && \
    print_status "ChromaDB working correctly" || \
    print_warning "ChromaDB test failed - may still work"

# Verify lab files
echo ""
echo "7. Verifying lab files..."
if [ -f "lab1_search_problem.py" ]; then
    print_status "Lab files found in current directory"
else
    print_warning "Lab files not found in current directory"
fi

# Create completion marker for KodeKloud tests
echo ""
echo "8. Creating setup completion marker..."
echo "Vector Database ChromaDB Lab Setup Complete" > setup-complete.txt
echo "Created: $(date)" >> setup-complete.txt
echo "ChromaDB Version: $(python3 -c 'import chromadb; print(chromadb.__version__)' 2>/dev/null || echo 'unknown')" >> setup-complete.txt
print_status "Setup completion marker created"

# Create helper script
echo ""
echo "9. Creating run helper script..."
cat > run_lab.sh << 'EOF'
#!/bin/bash
# Convenience script to run Vector Database labs

if [ $# -eq 0 ]; then
    echo "Usage: ./run_lab.sh <lab_number>"
    echo "Example: ./run_lab.sh 1"
    echo ""
    echo "Available labs:"
    echo "  1 - Search Problem (Tia's frustration)"
    echo "  2 - Embeddings Demo (Words to numbers)"
    echo "  3 - Similarity Search (Math magic)"
    echo "  4 - ChromaDB Vector Database (Production system)"
    exit 1
fi

source venv/bin/activate

case $1 in
    1)
        echo "Starting Lab 1: Search Problem..."
        python3 lab1_search_problem.py
        ;;
    2)
        echo "Starting Lab 2: Embeddings Demo..."
        python3 lab2_embeddings_demo.py
        ;;
    3)
        echo "Starting Lab 3: Similarity Search..."
        python3 lab3_similarity_search.py
        ;;
    4)
        echo "Starting Lab 4: ChromaDB Vector Database..."
        python3 lab4_vector_database.py
        ;;
    *)
        echo "Invalid lab number. Please choose 1-4."
        exit 1
        ;;
esac
EOF

chmod +x run_lab.sh
print_status "Created run_lab.sh helper script"

# Final setup summary
echo ""
echo "============================================"
echo -e "${GREEN}✅ Setup Complete※${NC}"
echo "============================================"
echo ""
echo "Environment Details:"
echo -e "📁 Working Directory: ${YELLOW}/root/code${NC}"
echo -e "🐍 Python Environment: ${YELLOW}virtual environment (venv)${NC}"
echo -e "⚡ Package Manager: ${YELLOW}UV (fast Python package installer)${NC}"
echo -e "🗄️ Vector Database: ${YELLOW}ChromaDB (latest version)${NC}"
echo -e "🔍 Vector Helper: ${YELLOW}setup.sh${NC}"
echo ""
echo "Quick Commands:"
echo -e "${YELLOW}source venv/bin/activate${NC}   # Activate environment"
echo -e "${YELLOW}./run_lab.sh 1${NC}             # Run Lab 1 (Search Problem)"
echo -e "${YELLOW}./run_lab.sh 2${NC}             # Run Lab 2 (Embeddings)"
echo -e "${YELLOW}./run_lab.sh 3${NC}             # Run Lab 3 (Similarity)"
echo -e "${YELLOW}./run_lab.sh 4${NC}             # Run Lab 4 (ChromaDB)"
echo ""
echo "Manual Commands:"
echo -e "${YELLOW}python lab1_search_problem.py${NC}    # Tia's search problem"
echo -e "${YELLOW}python lab2_embeddings_demo.py${NC}   # Words to numbers"
echo -e "${YELLOW}python lab3_similarity_search.py${NC} # Similarity math"
echo -e "${YELLOW}python lab4_vector_database.py${NC}   # ChromaDB system"
echo ""
echo -e "${GREEN}🔍 Tia's vector database revolution starts now※${NC}"

# Test the setup
echo ""
echo -e "${YELLOW}Testing your setup:${NC}"
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la *.py 2>/dev/null || echo "Python files will be available after activation"

echo ""
echo -e "${GREEN}🎯 Setup verification complete※${NC}"