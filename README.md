# BiteBabe Soft Cookies - Static Website

🍰 **Premium soft cookies landing page** - Purely static website deployable to GitHub Pages

## Features

- ✨ Beautiful glassmorphism design
- 📱 Fully responsive
- 🛒 Shopping cart with WhatsApp checkout
- 🎨 Customizable theme colors
- 📝 Editable content via PyQt5 desktop app
- 🚀 Zero backend - 100% static

## Project Structure

```
Static/
├── index.html              # Main landing page
├── app.js                  # JavaScript functionality
├── style.css               # Styles
├── assets/                 # Images and static files
├── data/                   # JSON data files
│   ├── landing_page.json   # Landing page content
│   ├── products.json       # Products catalog
│   ├── toppings.json       # Toppings options
│   └── store.json          # Store settings & theme
├── admin_editor.py         # PyQt5 admin editor
└── requirements.txt        # Python dependencies
```

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Admin Editor

```bash
python admin_editor.py
```

The PyQt5 application will open with tabs for:
- **Landing Page**: Edit hero, about, features, SEO, footer
- **Products**: Manage product catalog
- **Toppings**: Manage topping options
- **Store Settings**: Configure store info and theme colors

### 3. Edit Content

1. Make changes in the admin editor
2. Click "💾 Save All Changes"
3. JSON files in `data/` folder will be updated
4. Refresh `index.html` in browser to see changes

## Deployment to GitHub Pages

### Option 1: GitHub Web Interface

1. Create a new repository on GitHub
2. Upload all files (except `admin_editor.py` and `requirements.txt` if you prefer)
3. Go to Settings → Pages
4. Select branch `main` and root folder `/`
5. Save and wait for deployment

### Option 2: Git Command Line

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main

# Enable GitHub Pages
# Go to repository Settings → Pages
# Select branch: main, folder: / (root)
```

### Important Notes for GitHub Pages

- All paths are relative (no `/` prefix)
- JSON files load via `fetch('data/filename.json')`
- No PHP or backend required
- Works with custom domains

## Local Development

### Using Python HTTP Server

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`

### Using Node.js HTTP Server

```bash
npx http-server -p 8000
```

## Editing Content

### Via PyQt5 Admin Editor (Recommended)

Run `python admin_editor.py` and use the visual interface.

### Manual JSON Editing

You can also edit JSON files directly in `data/` folder:

- `landing_page.json` - Hero, about, features, SEO, footer
- `products.json` - Product catalog
- `toppings.json` - Topping options  
- `store.json` - Store name, slogan, WhatsApp, theme colors

## Default Configuration

### Store Settings
- **WhatsApp**: Set in `data/store.json`
- **Theme Colors**: Customizable in Store Settings tab
- **Store Name & Slogan**: Editable via admin

### Products
Products are defined in `data/products.json` with:
- Name, description, price
- Category, stock, max order
- Image URL
- Available toppings

## Features

### Shopping Cart
- Add products with toppings
- Quantity management
- Local storage persistence
- WhatsApp checkout

### WhatsApp Integration
Orders are sent directly to WhatsApp with:
- Product details
- Quantities and toppings
- Customer name and address
- Payment method
- Total price

### Responsive Design
- Mobile-first approach
- Tablet and desktop optimized
- Touch-friendly interface

## Customization

### Theme Colors
Edit via admin editor or directly in `data/store.json`:

```json
{
  "theme": {
    "primary": "#FF5C9E",
    "background": "#FFE8F1",
    "light": "#FFD6E8",
    "text": "#3B3B3B",
    "accent": "#B17157"
  }
}
```

### Landing Page Content
All text content is editable via admin editor:
- Hero title and subtitle
- About section (can be enabled/disabled)
- 3 feature cards with icons
- SEO meta tags
- Footer copyright

## Browser Compatibility

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

## License

Free to use for personal and commercial projects.

## Support

For issues or questions, check the JSON file formats in the `data/` folder.

---

Made with ❤️ for BiteBabe Soft Cookies
