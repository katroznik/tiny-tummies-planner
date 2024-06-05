import altair as alt
import numpy as np
import streamlit as st
import pandas as pd
import pdfkit
import base64
import os
from datetime import datetime

# Verify wkhtmltopdf installation
if os.system('which wkhtmltopdf') != 0:
    raise EnvironmentError('wkhtmltopdf not installed or not found in PATH.')

# Specify the path to wkhtmltopdf
path_to_wkhtmltopdf = '/usr/bin/wkhtmltopdf'  # Update this path based on your environment
pdfkit_config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# Path to the log file
log_file = "food_log.csv"

# Function to load the log file
def load_log():
    if os.path.exists(log_file):
        log = pd.read_csv(log_file)
        log['Date'] = pd.to_datetime(log['Date']).dt.date
        return log.sort_values(by='Date').reset_index(drop=True)
    else:
        return pd.DataFrame(columns=["Date", "Food", "Notes"])

# Function to save the log file
def save_log(log):
    log.to_csv(log_file, index=False)

# Define your food items with categories
food_items = {
    "Chia seeds": ["digestion aid", "energy-rich", "iron-rich"],
    "Pear": ["digestion aid", "fruit"],
    "Tofu": ["allergen", "energy-rich", "iron-rich"],
    "Lentil pasta": ["iron-rich"],
    "Turkey": ["energy-rich", "iron-rich"],
    "Yogurt": ["allergen", "energy-rich"],
    "Steak": ["iron-rich"],
    "Shrimp": ["allergen"],
    "Lobster": ["allergen", "energy-rich"],
    "Salmon": ["allergen", "energy-rich", "iron-rich"],
    "Ground turkey": ["energy-rich", "iron-rich"],
    "Eggs": ["allergen", "energy-rich", "iron-rich"],
    "Coconut oil": ["energy-rich"],
    "Bacon": ["energy-rich"],
    "Lamb": ["iron-rich"],
    "Bison": ["iron-rich"],
    "Cod": ["iron-rich"],
    "Duck": ["iron-rich"],
    "Herring": ["iron-rich"],
    "Trout": ["iron-rich"],
    "Pollock": ["iron-rich"],
    "Flounder": ["iron-rich"],
    "Hummus": ["iron-rich", "energy-rich"],
    "Crab": ["allergen"],
    "Bulgur": ["allergen"],
    "Olives": ["iron-rich"],
    "Corn": ["energy-rich"],
    "Clams": ["iron-rich"],
    "Tahini": ["allergen", "iron-rich"],
    "Sesame": ["allergen", "iron-rich"],
    "Noodles": ["allergen"],
    "Avocado": ["energy-rich", "iron-rich", "fruit"],
    "Oatmeal": ["energy-rich", "digestion aid", "iron-rich"],
    "Almonds": ["allergen", "iron-rich", "energy-rich"],
    "Almond butter": ["allergen", "iron-rich", "energy-rich"],
    "Cashews": ["allergen", "iron-rich", "energy-rich"],
    "Cashew butter": ["allergen", "iron-rich", "energy-rich"],
    "Walnuts": ["allergen", "iron-rich", "energy-rich"],
    "Peanuts": ["allergen", "iron-rich", "energy-rich"],
    "Peanut butter": ["allergen", "iron-rich", "energy-rich"],
    "Pecans": ["allergen", "iron-rich", "energy-rich"],
    "Hazelnuts": ["allergen", "iron-rich", "energy-rich"],
    "Hazelnut spread": ["allergen", "iron-rich", "energy-rich"],
    "Macadamia nuts": ["iron-rich", "energy-rich"],
    "Pistachios": ["allergen", "iron-rich", "energy-rich"],
    "Pine nuts": ["allergen", "iron-rich", "energy-rich"],
    "Brazil nuts": ["iron-rich", "energy-rich"],
    "Pancakes": ["energy-rich"],
    "Muffin": ["energy-rich"],
    "French toast": ["energy-rich"],
    "Greek yogurt": ["allergen", "energy-rich"],
    "Ricotta": ["allergen", "energy-rich"],
    "Mozzarella": ["allergen", "energy-rich"],
    "Mascarpone": ["allergen", "energy-rich"],
    "Pecorino": ["allergen", "energy-rich"],
    "Goat cheese": ["allergen", "energy-rich"],
    "Quark": ["allergen", "energy-rich"],
    "Crème fraiche": ["allergen", "energy-rich"],
    "Swiss": ["allergen", "energy-rich"],
    "Parmesan": ["allergen", "energy-rich"],
    "Cheese": ["allergen", "energy-rich"],
    "Cotija cheese": ["allergen", "energy-rich"],
    "Cottage cheese": ["allergen", "energy-rich"],
    "Edamame": ["allergen", "iron-rich"],
    "Broccoli": ["veggie"],
    "Banana": ["fruit", "energy-rich"],
    "Chicken": ["energy-rich", "iron-rich"],
    "Rabbit": ["iron-rich"],
    "Pork": ["energy-rich", "iron-rich"],
    "Rice": ["energy-rich"],
    "Brown rice": ["energy-rich"],
    "Ground beef": ["iron-rich"],
    "Apple": ["fruit", "digestion aid"],
    "Applesauce": ["fruit", "digestion aid"],
    "Prunes": ["fruit", "digestion aid"],
    "Plum": ["fruit", "digestion aid"],
    "Yellow peach": ["fruit", "digestion aid"],
    "White peach": ["fruit", "digestion aid"],
    "Peach": ["fruit", "digestion aid"],
    "Asian pear": ["fruit", "digestion aid"],
    "Squash": ["veggie"],
    "Blueberries": ["fruit", "digestion aid"],
    "Flaxseed": ["digestion aid"],
    "Papaya": ["fruit", "digestion aid"],
    "Lentils": ["digestion aid", "iron-rich"],
    "Olive oil": ["digestion aid", "energy-rich"],
    "Figs": ["fruit", "digestion aid"],
    "Raisins": ["fruit", "digestion aid"],
    "Kiwi": ["fruit", "digestion aid"],
    "Orange": ["fruit", "digestion aid"],
    "Grapefruit": ["fruit", "digestion aid"],
    "Pomelo": ["fruit", "digestion aid"],
    "Mandarin orange": ["fruit", "digestion aid"],
    "Clementine": ["fruit", "digestion aid"],
    "Spinach": ["digestion aid", "iron-rich"],
    "Cherries": ["fruit", "digestion aid"],
    "Bell pepper": ["veggie"],
    "Sweet potato": ["energy-rich", "veggie"],
    "Yam": ["veggie"],
    "Cassava": ["veggie"],
    "Tomato": ["veggie"],
    "Potato": ["veggie"],
    "Garlic": ["veggie"],
    "Onion": ["veggie"],
    "Tomato sauce": ["veggie"],
    "Asparagus": ["veggie"],
    "Green beans": ["veggie"],
    "Turnip": ["veggie"],
    "Chickpea": ["iron-rich"],
    "Peas": ["veggie"],
    "Watermelon": ["fruit"],
    "Pineapple": ["fruit"],
    "Mango": ["fruit"],
    "Strawberries": ["fruit"],
    "Cinnamon": ["spice"],
    "Thyme": ["spice"],
    "Nutmeg": ["spice"],
    "Allspice": ["spice"],
    "Ginger": ["spice"],
    "Parsley": ["herb"],
    "Cumin": ["spice"],
    "Carrot": ["veggie"],
    "Cantaloupe": ["fruit"],
    "Melon": ["fruit"],
    "Beets": ["veggie"],
    "Bread": ["allergen"],
    "Apricot": ["fruit", "digestion aid"],
    "Cauliflower": ["veggie"],
    "Pumpkin": ["veggie"],
    "Artichoke": ["veggie"],
    "Kale": ["veggie"],
    "Bok choy": ["veggie"],
    "Collard greens": ["veggie"],
    "Cabbage": ["veggie"],
    "Kohlrabi": ["veggie"],
    "Lettuce": ["veggie"],
    "Mustard greens": ["veggie"],
    "Leek": ["veggie"],
    "Quinoa": ["energy-rich", "iron-rich"],
    "Cous cous": ["allergen"],
    "Tuna": ["allergen", "energy-rich", "iron-rich"],
    "Anchovy": ["allergen", "energy-rich", "iron-rich"],
    "Haddock": ["allergen"],
    "Tilapia": ["allergen"],
    "Rice noodles": ["allergen", "energy-rich"],
    "Chickpea pasta": ["energy-rich", "iron-rich"],
    "Pumpkin seeds": ["energy-rich", "iron-rich"],
    "Hemp seeds": ["energy-rich", "iron-rich"],
    "Sunflower seeds": ["energy-rich", "iron-rich"],
    "Tempeh": ["allergen", "energy-rich", "iron-rich"],
    "Barley": ["allergen", "energy-rich"],
    "Farro": ["allergen", "energy-rich"],
    "Guava": ["fruit"],
    "Mulberries": ["fruit"],
    "Lychee": ["fruit"],
    "Gooseberries": ["fruit"],
    "Cranberries": ["fruit", "digestion aid"],
    "Pomegranate": ["fruit", "digestion aid"],
    "Raspberries": ["fruit", "digestion aid"],
    "Grapes": ["fruit"],
    "Celery": ["veggie"],
    "Parsnip": ["veggie"],
    "Zucchini": ["veggie"],
    "Eggplant": ["veggie"],
    "Butternut squash": ["veggie"],
    "Brussel sprouts": ["veggie"],
    "Basil": ["herb"],
    "Parsley": ["herb"],
    "Cilantro": ["herb"],
    "Mint": ["herb"],
    "Rosemary": ["herb"],
    "Thyme": ["herb"],
    "Oregano": ["herb"],
    "Sage": ["herb"],
    "Dill": ["herb"],
    "Tarragon": ["herb"],
    "Chives": ["herb"],
    "Bay leaves": ["herb"],
    "Marjoram": ["herb"],
    "Lemongrass": ["herb"],
    "Fennel": ["herb"],
    "Lavender": ["herb"],
    "Black pepper": ["spice"],
    "Cumin": ["spice"],
    "Coriander": ["spice"],
    "Turmeric": ["spice"],
    "Paprika": ["spice"],
    "Chili powder": ["spice"],
    "Cinnamon": ["spice"],
    "Nutmeg": ["spice"],
    "Cloves": ["spice"],
    "Cardamom": ["spice"],
    "Allspice": ["spice"],
    "Ginger": ["spice"],
    "Mustard seeds": ["spice"],
    "Fenugreek": ["spice"],
    "Caraway seeds": ["spice"],
    "Saffron": ["spice"],
    "Vanilla": ["spice"],
    "Star anise": ["spice"],
    "Sumac": ["spice"],
    "Cayenne pepper": ["spice"],
    "Ancho chili powder": ["spice"],
    "Bay leaf": ["spice"],
    "Fennel seeds": ["spice"],
    "Garam masala": ["spice"],
    "Tandoori masala": ["spice"],
    "Chinese five spice": ["spice"],
    "Za'atar": ["spice"],
    "Smoked paprika": ["spice"],
    "White pepper": ["spice"],
    "Mace": ["spice"],
    "Fenugreek": ["spice"],
    "Curry powder": ["spice"],
    "Ground coriander": ["spice"],
    "Ground cumin": ["spice"],
    "Ground turmeric": ["spice"],
    "Ground ginger": ["spice"],
    "Ground cinnamon": ["spice"],
    "Ground nutmeg": ["spice"],
    "Ground cloves": ["spice"],
    "Golden beets": ["veggie"],
    "Feijoa": ["fruit"],
    "Persimmon": ["fruit"],
    "Pitaya/Dragon fruit": ["fruit"] }

# Define meals in the preferred order
meals = ["Breakfast", "Snack 1", "Lunch", "Snack 2", "Dinner"]

# Function to get categories of selected items
def get_categories(selected_items):
    categories = {"allergen": [], "iron-rich": [], "energy-rich": [], "veggie": [], "fruit": [], "digestion aid": [], "herb": [], "spice": []}
    for item in selected_items:
        for category in food_items[item]:
            categories[category].append(item)
    return categories

# Function to generate HTML for PDF
def generate_html(meal_plans):
    html = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            h1, h2, h3 {
                color: #333;
            }
            p {
                color: #555;
            }
        </style>
    </head>
    <body>
        <h1>Tiny Tummies Planner</h1>
    """
    for date, meal_plan in meal_plans.items():
        html += f"<h2>{date}</h2>"
        for meal, items in meal_plan.items():
            if items:  # Only include meals with selected items
                html += f"<h3>{meal}</h3>"
                for item in items:
                    html += f"<p>- {item}</p>"
    html += """
    </body>
    </html>
    """
    return html

# Streamlit app layout
st.set_page_config(page_title="Tiny Tummies Planner", page_icon=":baby_bottle:")

# Custom CSS for fonts and light grey selection
st.markdown("""
    <style>
        body, .stApp {
            font-family: 'Arial', sans-serif;
        }
        .stMultiSelect div[data-baseweb="select"] > div {
            background-color: #D3D3D3 !important;
        }
        .stMultiSelect div[data-baseweb="select"] > div:has(div[class*="selected"]) {
            background-color: #D3D3D3 !important;
            color: white !important;
        }
        .stMultiSelect div[data-baseweb="select"] > div div[aria-selected="true"] {
            background-color: #D3D3D3 !important;
            color: white !important;
        }
        .tried-food {
            color: #FF4500 !important;
        }
        .new-food {
            color: #000000 !important;
        }
        .delete-btn {
            color: red;
            cursor: pointer;
        }
        .dataframe-table {
            max-width: 80%;
            margin: 0 auto;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Tiny Tummies Planner")
st.markdown("Plan a nutritious and balanced menu for your little one.")

# About section
st.sidebar.title("About")
st.sidebar.markdown("My name is Kat and I made this app for myself to streamline meal prep for my son. Hope you also find it helpful! Check out my Substack Baby Saavy")

# Initialize meal plans
meal_plans = {}

# Load the log
log = load_log()

# Sidebar navigation
st.sidebar.title("About")
st.sidebar.title("Navigation")
st.sidebar.markdown("[Your Meal Plans](#your-meal-plans)")
st.sidebar.markdown("[Categories of Selected Items](#categories-of-selected-items)")
st.sidebar.markdown("[Shopping List](#shopping-list)")
st.sidebar.markdown("[Save as PDF](#save-as-pdf)")
st.sidebar.markdown("[Food Log](#food-log)")
st.sidebar.markdown("[Food Statistics](#food-statistics)")

# Sidebar selection
plan_option = st.sidebar.radio("Choose an option:", ("Quick plan for one day", "Plan for multiple days"))

if plan_option == "Quick plan for one day":
    selected_date = st.date_input("Select date for the meal plan", value=datetime.now(), min_value=datetime(2020, 1, 1), max_value=datetime(2030, 12, 31))
    selected_dates = [selected_date]
else:
    selected_dates = st.date_input("Select dates for the meal plan", value=[datetime.now()], min_value=datetime(2020, 1, 1), max_value=datetime(2030, 12, 31))

# Ensure selected_dates is a list
if isinstance(selected_dates, datetime):
    selected_dates = [selected_dates]

# Create a dropdown menu for each meal for each selected date
for date in selected_dates:
    date_str = date.strftime("%B %d, %Y")
    meal_plans[date_str] = {}
    st.header(date_str)
    for meal in meals:
        tried_items = log["Food"].unique()
        selected_items = st.multiselect(
            f"Select items for {meal} on {date_str} (categories in parentheses)", 
            [f"{item} ({', '.join(cats)})" + (" - Tried" if item in tried_items else "") for item, cats in food_items.items()],
            key=f"{date_str}_{meal}"
        )
        # Extract the item names from the selections
        meal_plans[date_str][meal] = [item.split(" (")[0] for item in selected_items]

# Display the meal plans
st.header("Your Meal Plans")
st.markdown('<a name="your-meal-plans"></a>', unsafe_allow_html=True)
for date, meal_plan in meal_plans.items():
    st.subheader(date)
    for meal, items in meal_plan.items():
        if items:  # Only display meals with selected items
            st.write(f"**{meal}:** {', '.join(items)}")

# Generate shopping list
shopping_list = set()
for meal_plan in meal_plans.values():
    for items in meal_plan.values():
        shopping_list.update(items)

# Toggle visibility of the shopping list
if 'show_shopping_list' not in st.session_state:
    st.session_state.show_shopping_list = False

if st.button("Add Shopping List"):
    st.session_state.show_shopping_list = not st.session_state.show_shopping_list

if st.session_state.show_shopping_list:
    st.header("Shopping List")
    st.markdown('<a name="shopping-list"></a>', unsafe_allow_html=True)
    for item in shopping_list:
        st.write(f"- {item}")

# Display categories of selected items
st.header("Categories of Selected Items")
st.markdown('<a name="categories-of-selected-items"></a>', unsafe_allow_html=True)
categories = get_categories(shopping_list)
for category, items in categories.items():
    st.subheader(category.capitalize())
    st.write(', '.join(items))

# Function to create a download link for the PDF
def create_download_link(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    b64 = base64.b64encode(pdf_bytes).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="meal_plan.pdf">Download PDF</a>'

# Add button to save as PDF
st.header("Save as PDF")
st.markdown('<a name="save-as-pdf"></a>', unsafe_allow_html=True)
if st.button("Save as PDF"):
    html = generate_html(meal_plans)
    pdf_path = '/tmp/meal_plan.pdf'
    pdfkit.from_string(html, pdf_path, configuration=pdfkit_config)
    st.success("PDF saved!")
    st.markdown(create_download_link(pdf_path), unsafe_allow_html=True)

# Food log section
st.header("Food Log")
st.markdown('<a name="food-log"></a>', unsafe_allow_html=True)

# Function to delete an entry from the log
def delete_entry(index):
    global log
    log = log.drop(index)
    save_log(log)

# Display the log with delete buttons
for i, row in log.iterrows():
    col1, col2, col3, col4 = st.columns([2, 2, 3, 1.5])
    with col1:
        st.write(row["Date"])
    with col2:
        st.write(row["Food"])
    with col3:
        st.write(row["Notes"])
    with col4:
        if st.button("Delete", key=f"delete_{i}"):
            delete_entry(i)
            st.experimental_rerun()

# Add new entry to the log
with st.form(key="add_food_log"):
    new_food = st.selectbox("Enter a new food", list(food_items.keys()))
    log_date = st.date_input("Date", value=datetime.now())
    notes = st.selectbox("Notes", ["loved", "thumbs up", "unsure", "didn't like", "allergy"])
    submit_button = st.form_submit_button(label="Add to Log")
    if submit_button and new_food:
        new_entry = pd.DataFrame({"Date": [log_date.strftime("%Y-%m-%d")], "Food": [new_food], "Notes": [notes]})
        log = pd.concat([log, new_entry], ignore_index=True)
        save_log(log)
        st.success(f"Added {new_food} to the log")

# Food statistics section
st.header("Food Statistics")
st.markdown('<a name="food-statistics"></a>', unsafe_allow_html=True)

# Count the number of times each food has been eaten
food_counts = log['Food'].value_counts().reset_index()
food_counts.columns = ['Food', 'Count']

# Display the count of each food item
st.subheader("Food Count")
st.dataframe(food_counts.style.set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}, {'selector': 'td', 'props': [('text-align', 'center')]}]), use_container_width=False)

# Identify items that haven't been eaten for a while
last_eaten = log.groupby('Food')['Date'].max().reset_index()
last_eaten.columns = ['Food', 'Last Eaten']
last_eaten = last_eaten.sort_values(by='Last Eaten')

# Display items that haven't been eaten for a while
st.subheader("Foods Not Eaten Recently")
st.dataframe(last_eaten.style.set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}, {'selector': 'td', 'props': [('text-align', 'center')]}]), use_container_width=False)

