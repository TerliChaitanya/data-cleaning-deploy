# 🧹 Data Cleaning App

A powerful and user-friendly Streamlit application for data cleaning and preprocessing.

## Features

- 📂 **Upload Data** - Import CSV files for analysis
- 🔍 **Data Overview** - View dataset statistics and distributions
- 🧹 **Handle Missing Values** - Remove or fill missing data using various strategies
- 🔁 **Handle Duplicates** - Detect and remove duplicate rows
- 📊 **Outlier Detection** - Identify and handle outliers using IQR method
- 📝 **Fix Categories** - Clean up inconsistent categorical values
- 💾 **Download Data** - Export cleaned datasets

## Installation

### Local Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/data-cleaning-app.git
cd data-cleaning-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Deployment on Render

### Prerequisites
- GitHub account with your repository
- Render.com account (free tier available)

### Steps to Deploy

1. **Push to GitHub**
   - Create a new repository on GitHub
   - Push this project to your GitHub repo

2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select this repository

3. **Configure Deployment**
   - **Name**: Choose a name for your service
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
   - **Plan**: Select Free or Paid

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - Your app will be live at: `https://your-service-name.onrender.com`

## Project Structure

```
data-cleaning-app/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment configuration
├── .gitignore            # Git ignore patterns
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md             # This file
```

## Requirements

- Python 3.8+
- streamlit==1.28.1
- pandas==2.1.3
- numpy==1.24.3
- plotly==5.17.0

## Usage

1. **Upload Data**: Go to "Upload Data" tab and select a CSV file
2. **Explore**: Use "Data Overview" to understand your dataset
3. **Clean**: Apply cleaning operations from different tabs
4. **Download**: Save your cleaned dataset in "Download Data" tab

## Troubleshooting

### App not loading on Render
- Check build logs in Render dashboard
- Ensure `Procfile` exists and is correctly formatted
- Verify all dependencies are in `requirements.txt`

### Memory issues
- Render free tier has limited memory
- For large datasets, consider upgrading to a paid plan

### Changes not showing
- Push changes to GitHub
- Render will automatically redeploy on new commits

## Features & Strategies

### Missing Values
- Remove affected rows
- Fill with Mean (numeric only)
- Fill with Median (numeric only)
- Fill with Mode (any type)

### Outlier Detection
- IQR (Interquartile Range) method
- Remove outliers
- Replace with NaN
- Clip to boundaries

## License

MIT License - Feel free to use this project freely

## Support

For issues or questions, please create an issue on GitHub.

## Author

Created with ❤️ for data enthusiasts

---

**Happy Data Cleaning! 🎉**
