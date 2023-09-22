import http.client
import urllib.parse
import requests
from bs4 import BeautifulSoup

# Replace with your Pushover API token and user key
app_token = "YOUR_APP_TOKEN"
user_key = "YOUR_USER_KEY"

# Define the Pushover API endpoint and parameters
api_url = "/1/messages.json"
api_host = "api.pushover.net"
api_port = 443

# Function to send a Pushover notification
def send_pushover_notification(title, message):
    # Create a dictionary with the message parameters
    message_data = {
        "token": app_token,
        "user": user_key,
        "title": title,
        "message": message,
    }

    # Encode the message data
    encoded_data = urllib.parse.urlencode(message_data)

    # Create a connection to the Pushover API server
    conn = http.client.HTTPSConnection(api_host, api_port)

    # Send a POST request to the Pushover API
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn.request("POST", api_url, encoded_data, headers)

    # Get the response from the API (you can handle it as needed)
    response = conn.getresponse()

    # Close the connection
    conn.close()

# URL of the webpage / Replace with the URL you are using
url = "YOUR_URL"

# Set a user-agent header to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Send an HTTP GET request to the webpage with the user-agent header
response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all product listings on the webpage
    product_listings = soup.find_all("div", class_="listing-row")

    # Initialize a flag to check if any products meet the criteria
    found_matching_product = False

    # Iterate through the listings to check for your criteria
    for listing in product_listings:
        # Find the product title
        product_title = listing.find("h2", class_="listing-title").text.strip()

        # Find the product price
        product_price = listing.find("span", class_="price").text.strip()
        # Remove "$" and any commas in the price and convert it to a float
        product_price = float(product_price.replace("$", "").replace(",", ""))

        # Manually print product information for debugging
        print(f"Product Title: {product_title}")
        print(f"Product Price: {product_price}")

        # Check if the product meets your criteria / Replace with your specifications
        if "your laptop" in product_title.lower() and "your specification" in product_title.lower() and product_price < 1000:
            found_matching_product = True
            send_pushover_notification("Your Product Available!", f"Product Found: {product_title} - Price: ${product_price}")

    # Check if no matching products were found
    if not found_matching_product:
        send_pushover_notification("No Matching Products Found", "No products meeting the criteria were found.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
