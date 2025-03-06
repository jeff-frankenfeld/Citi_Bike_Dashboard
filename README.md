# Citi Bike Usage Analysis & Dashboard

## Project Overview  
This project analyzes **New York City's Citi Bike usage patterns** to **identify distribution inefficiencies and improve bike availability** across the city. Using **Python, Pandas, Plotly, and Streamlit**, I developed an **interactive dashboard** that visualizes key insights, such as:  
- **How weather impacts ridership**  
- **Most frequently used bike stations**  
- **Aggregated trip patterns across the city**  
- **Differences in weekday vs. weekend trip activity**  
- **Data-driven recommendations to optimize Citi Bike operations**  

---

## **Key Features**
### **Interactive Dashboard**
- **Built using Python & Streamlit** for seamless user interaction.
- **Modular navigation**: Users can explore Citi Bike data through different analytical sections.
- **Data filters for seasonality**: View how station usage changes across different seasons.

### **Analytical Insights**
- **Seasonal Trends:** Warmer months see increased ridership, while winter months show a decline.
- **Most Popular Stations:** `W 21 St & 6 Ave` is the most frequently used start station year-round.
- **Commuter vs. Recreational Usage:**  
  - **Work commuters** dominate ridership in **Chelsea & Midtown Manhattan**.
  - **Casual riders & tourists** use Citi Bikes heavily in **Central Park & Roosevelt Island**.
- **Hourly Usage Trends:**  
  - **Weekday peaks:** 8 AM & 5-7 PM (work commutes).  
  - **Weekend usage:** Evenly distributed, peaking mid-afternoon.

### **Data-Driven Recommendations**
- **Redistribute bikes based on seasonal demand** to prevent shortages.
- **Expand docking stations in high-tourism areas (Central Park, Roosevelt Island).**
- **Use real-time data for smarter bike rebalancing.**
- **Offer winter promotions to encourage year-round ridership.**

---

## **Project Structure**
/Citi_Bike_Dashboard
│── 01 Project Management  # Documentation & project plan
│── 02 Data
│   ├── Prepared Data  # Cleaned dataset for analysis
│── 03 Scripts
│   ├── Citi_Dashboard.py  # First draft Streamlit dashboard script
│   ├── Citi_Dashboard_pt2.py  # Final draft dashboard
│   ├── Various jupyterlab notebook scripts for data analysis  # Data preparation & transformation
│── 04 Analysis
│   ├── Visualizations  # Stored plots
│   ├── Reports  # Stored reports
│── README.md  # Project overview & details
