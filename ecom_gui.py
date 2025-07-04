import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog

def scrape_and_save():
    base_url = url_entry.get().strip()
    
    if not base_url.startswith("http"):
        messagebox.showwarning("Input Error", "Please enter a valid URL (starting with http:// or https://).")
        return

    product_names = []
    product_prices = []
    product_ratings = []

    try:
        for page in range(1, 4):  # Change range to scrape more pages
            full_url = f"{base_url}/catalogue/page-{page}.html"
            response = requests.get(full_url)
            soup = BeautifulSoup(response.text, "html.parser")

            products = soup.find_all("article", class_="product_pod")

            for product in products:
                name = product.h3.a["title"]
                price = product.find("p", class_="price_color").text.strip()
                rating_class = product.find("p", class_="star-rating")["class"]
                rating = rating_class[1] if len(rating_class) > 1 else "No rating"

                product_names.append(name)
                product_prices.append(price)
                product_ratings.append(rating)

        df = pd.DataFrame({
            "Product Name": product_names,
            "Price": product_prices,
            "Rating": product_ratings
        })

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")],
                                                 title="Save CSV as")
        if file_path:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", f"✅ Data saved to:\n{file_path}")
        else:
            messagebox.showinfo("Cancelled", "Save operation was cancelled.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while scraping:\n\n{str(e)}")

# Setup GUI
root = tk.Tk()
root.title("🛍️ E-Commerce Product Scraper")
root.geometry("500x230")
root.resizable(False, False)

# Widgets
tk.Label(root, text="Enter the base URL of the e-commerce site:", font=("Arial", 11)).pack(pady=10)

url_entry = tk.Entry(root, width=60, font=("Arial", 12))
url_entry.insert(0, "http://books.toscrape.com")
url_entry.pack(pady=5)

scrape_button = tk.Button(root, text="Scrape and Save to CSV", font=("Arial", 12), bg="lightgreen", command=scrape_and_save)
scrape_button.pack(pady=20)

# Run the application
root.mainloop()