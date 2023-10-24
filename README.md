# CS50-Commerce

# eBay-like E-commerce Auction Site

This project is an eBay-like e-commerce auction site that allows users to post auction listings, place bids on listings, comment on those listings, and add listings to a "watchlist."

## Project Components

### URL Configuration

The URL configuration for this project is defined in the `auctions/urls.py` file. It includes routes for the default index, login, logout, and register pages.

### Views

The views associated with the routes are defined in `auctions/views.py`. These include views for the index, login, logout, and registration processes. The views handle user authentication and rendering of forms.

### Templates

Templates for the project can be found in the `auctions/templates` directory. The primary template, `layout.html`, defines the overall structure of the pages. The `index.html` template displays auction listings.

### Models

The `auctions/models.py` file contains the models used in the project. You will find the User model, which inherits from AbstractUser, and you can add additional models to represent auction listings, bids, comments, and categories.

## Key Functionality

1. **Models**: You must define at least three additional models besides the User model. These models should represent auction listings, bids, and comments. The fields and types of these models are at your discretion, and you can add more models if needed.

2. **Create Listing**: Users should be able to create new auction listings. They can provide a title, description, starting bid, an optional image URL, and category for the listing.

3. **Active Listings Page**: The default route of your web application should display all currently active auction listings. The displayed information should include at least the title, description, current price, and listing photo (if available).

4. **Listing Page**: Clicking on a listing should lead to a dedicated page with full details. Users should be able to:
   - Add the listing to their "Watchlist."
   - Place bids (meeting certain criteria).
   - Close an auction (if the user is the creator).
   - View if they've won an auction.
   - Add comments to the listing.

5. **Watchlist**: Users can view a Watchlist page, displaying all listings they've added. Clicking on a listing leads to its dedicated page.

6. **Categories**: Users should be able to visit a page displaying all listing categories. Clicking on a category displays active listings in that category.

7. **Django Admin Interface**: Site administrators can use the Django admin interface to manage listings, comments, and bids on the site.

## Usage

1. Start the Django development server: `python manage.py runserver`.

2. Access the project in your web browser.

3. Register for an account and explore the auction listings.
