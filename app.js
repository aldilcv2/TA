// State
let products = [];
let toppings = [];
let storeConfig = {};
let landingPageData = {};
let cart = JSON.parse(localStorage.getItem('bitebabe_cart')) || [];

// DOM Elements
const productsGrid = document.getElementById('productsGrid');
const cartOverlay = document.getElementById('cartOverlay');
const cartItemsContainer = document.getElementById('cartItems');
const cartTotalElement = document.getElementById('cartTotal');
const cartBadge = document.getElementById('cartBadge');
const modal = document.getElementById('productModal');
const modalBody = document.getElementById('modalBody');

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await loadData();
    await loadLandingPageData();
    renderProducts();
    updateCartUI();
    renderStoreInfo();
    renderLandingPage();
});

// Load Data
async function loadData() {
    try {
        const responses = await Promise.all([
            fetch('data/products.json'),
            fetch('data/toppings.json'),
            fetch('data/store.json')
        ]);

        if (responses.some(r => !r.ok)) {
            throw new Error('One or more JSON files failed to load');
        }

        const [prodRes, topRes, storeRes] = responses;

        products = await prodRes.json();
        toppings = await topRes.json();
        storeConfig = await storeRes.json();
    } catch (error) {
        console.warn('JSON files not available, loading mock data for UI demo.', error);

        // Mock Data for UI Verification/Demo
        products = [
            {
                id: '1',
                name: 'Classic Choco Walnut',
                description: 'Our signature soft cookie with belgian dark chocolate and roasted walnuts. Melted perfection.',
                price: 25000,
                category: 'Best Seller',
                image: 'https://images.unsplash.com/photo-1499636138143-bd649043ea52?q=80&w=800&auto=format&fit=crop',
                toppings: ['1', '2'],
                max_order: 10
            },
            {
                id: '2',
                name: 'Red Velvet Oreo',
                description: 'Red velvet dough filled with cream cheese and topped with oreo crumbs.',
                price: 28000,
                category: 'Special',
                image: 'https://images.unsplash.com/photo-1624356853128-48f1850f6fa2?q=80&w=800&auto=format&fit=crop',
                toppings: ['1'],
                max_order: 10
            },
            {
                id: '3',
                name: 'Matcha White Choco',
                description: 'Premium matcha cookie with white chocolate chunks.',
                price: 27000,
                category: 'New',
                image: 'https://images.unsplash.com/photo-1597733336794-12d05021d510?q=80&w=800&auto=format&fit=crop',
                toppings: [],
                max_order: 10
            }
        ];

        toppings = [
            { id: '1', name: 'Extra Sauce', price: 5000 },
            { id: '2', name: 'Ice Cream', price: 8000 },
            { id: '3', name: 'Almonds', price: 4000 }
        ];

        storeConfig = {
            name: 'BiteBabe Demo',
            slogan: 'Premium Soft Cookies (Demo Mode)',
            whatsapp: '628123456789'
        };
    }
}

// Load Landing Page Data
async function loadLandingPageData() {
    try {
        const response = await fetch('data/landing_page.json');
        if (response.ok) {
            landingPageData = await response.json();
        }
    } catch (error) {
        console.warn('Could not load landing page data:', error);
        // Use defaults if loading fails
        landingPageData = {
            hero: {
                title: "Softness in Every Bite",
                subtitle: "Premium homemade soft cookies with belgian chocolate.",
                buttonText: "Order Now"
            },
            about: {
                enabled: false
            },
            features: [],
            seo: {
                title: "BiteBabe Soft Cookies",
                description: "Softness in every bite. Premium soft cookies homemade."
            },
            footer: {
                copyright: "2024 BiteBabe Soft Cookies. All rights reserved."
            }
        };
    }
}

// Render Landing Page Content
function renderLandingPage() {
    // Update Hero Section
    if (landingPageData.hero) {
        const heroTitle = document.querySelector('.hero-title');
        const heroSubtitle = document.querySelector('.hero-subtitle');
        const heroButton = document.querySelector('.hero a.btn');

        if (heroTitle && landingPageData.hero.title) {
            heroTitle.textContent = landingPageData.hero.title;
        }
        if (heroSubtitle && landingPageData.hero.subtitle) {
            heroSubtitle.textContent = landingPageData.hero.subtitle;
        }
        if (heroButton && landingPageData.hero.buttonText) {
            heroButton.innerHTML = `${landingPageData.hero.buttonText} <i class="fa-solid fa-arrow-right"></i>`;
        }
    }

    // Update About Section
    if (landingPageData.about && landingPageData.about.enabled) {
        const aboutSection = document.getElementById('about');
        const aboutTitle = document.getElementById('aboutTitle');
        const aboutDescription = document.getElementById('aboutDescription');

        if (aboutSection) {
            aboutSection.style.display = 'block';
        }
        if (aboutTitle && landingPageData.about.title) {
            aboutTitle.textContent = landingPageData.about.title;
        }
        if (aboutDescription && landingPageData.about.description) {
            aboutDescription.textContent = landingPageData.about.description;
        }
    }

    // Render Features
    if (landingPageData.features && landingPageData.features.length > 0) {
        const featuresGrid = document.getElementById('featuresGrid');
        if (featuresGrid) {
            featuresGrid.innerHTML = landingPageData.features.map((feature, index) => `
                <div class="feature-card animate-in delay-${(index % 3) + 1}">
                    <div class="feature-icon">${feature.icon || '✨'}</div>
                    <h3>${feature.title || ''}</h3>
                    <p>${feature.description || ''}</p>
                </div>
            `).join('');
        }
    }

    // Update SEO Meta Tags
    if (landingPageData.seo) {
        if (landingPageData.seo.title) {
            document.title = landingPageData.seo.title;
        }

        let metaDescription = document.querySelector('meta[name="description"]');
        if (metaDescription && landingPageData.seo.description) {
            metaDescription.setAttribute('content', landingPageData.seo.description);
        }
    }

    // Update Footer
    if (landingPageData.footer && landingPageData.footer.copyright) {
        const footerText = document.querySelector('.footer p');
        if (footerText) {
            footerText.innerHTML = landingPageData.footer.copyright;
        }
    }
}

// Render Store Info
function renderStoreInfo() {
    if (storeConfig.name) {
        document.querySelector('.brand-name').textContent = storeConfig.name;
    }

    // Apply Theme Colors
    if (storeConfig.theme) {
        const root = document.documentElement;
        if (storeConfig.theme.primary) root.style.setProperty('--primary', storeConfig.theme.primary);
        if (storeConfig.theme.background) root.style.setProperty('--bg-soft', storeConfig.theme.background);
        if (storeConfig.theme.light) root.style.setProperty('--bg-light', storeConfig.theme.light);
        // Note: variable names in CSS might need adjustment if they don't match exactly, 
        // assuming standard names based on the JSON. 
        // If the CSS uses --text-light etc, we map them here.
        if (storeConfig.theme.text) root.style.setProperty('--text-dark', storeConfig.theme.text);
        if (storeConfig.theme.accent) root.style.setProperty('--accent', storeConfig.theme.accent);
    }
}

// Render Products
function renderProducts() {
    console.log('Rendering products array:', JSON.stringify(products));
    if (!products.length) console.warn('Products array is empty!');
    productsGrid.innerHTML = products.map((product, index) => `
        <div class="product-card animate-in delay-${(index % 3) + 1}">
            <div class="product-image-wrapper">
                <img src="${product.image}" alt="${product.name}" class="product-image" onerror="this.src='https://placehold.co/400x400/e0f2fe/0087F7?text=Cookie'">
            </div>
            <div class="product-info">
                <div class="product-category">${product.category}</div>
                <h3 class="product-title">${product.name}</h3>
                <div class="product-footer">
                    <div class="product-price">${formatRupiah(product.price)}</div>
                    <button class="btn-add-mini" onclick="openProductModal('${product.id}')">
                        <i class="fa-solid fa-plus"></i>
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Product Modal
function openProductModal(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;

    const productToppings = toppings.filter(t => (product.toppings || []).includes(t.id));

    modalBody.innerHTML = `
        <div style="text-align: center; margin-bottom: 24px;">
            <img src="${product.image}" style="width: 120px; height: 120px; object-fit: cover; border-radius: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); margin-bottom: 16px;" onerror="this.src='https://placehold.co/400x400/eeeeee/999999?text=Cookie'">
            <h2 style="font-family: var(--font-display); font-size: 1.8rem; margin-bottom: 8px;">${product.name}</h2>
            <p style="color: var(--text-medium); line-height: 1.5; font-size: 0.95rem;">${product.description}</p>
            <h3 style="color: var(--primary); font-size: 1.5rem; margin-top: 12px; font-weight: 700;">${formatRupiah(product.price)}</h3>
        </div>

        <div class="form-group" style="text-align: center;">
            <label>Quantity</label>
            <div class="qty-control">
                <button class="qty-btn" onclick="adjustModalQty(-1)">-</button>
                <span id="modalQty" style="font-weight: 700; font-size: 1.2rem; min-width: 24px;">1</span>
                <button class="qty-btn" onclick="adjustModalQty(1, ${product.max_order})">+</button>
            </div>
        </div>

        ${productToppings.length > 0 ? `
            <div class="form-group">
                <label style="margin-bottom: 12px; display: block;">Extra Toppings</label>
                <div class="toppings-list">
                    ${productToppings.map(t => `
                        <label class="topping-option">
                            <span style="display: flex; align-items: center; gap: 8px;">
                                <i class="fa-solid fa-cookie-bite" style="color: var(--accent); opacity: 0.7;"></i>
                                ${t.name}
                            </span>
                            <span style="font-weight: 600; color: var(--text-medium);">+${formatRupiah(t.price)}</span>
                            <input type="checkbox" value="${t.id}" data-price="${t.price}" data-name="${t.name}" onchange="toggleToppingSelection('${t.id}', this)">
                        </label>
                    `).join('')}
                </div>
            </div>
        ` : ''}

        <button class="btn btn-primary" style="width: 100%; margin-top: 24px; padding: 18px;" onclick="addToCart('${product.id}')">
            Add to Order &bull; <span id="modalTotal" style="margin-left: 5px;">${formatRupiah(product.price)}</span>
        </button>
    `;

    modal.classList.add('active');
    window.currentModalProduct = product;
    window.currentModalQty = 1;
    window.currentModalToppings = [];
}

function closeModal() {
    modal.classList.remove('active');
}

function adjustModalQty(delta, max) {
    let newQty = window.currentModalQty + delta;
    if (newQty < 1) newQty = 1;
    if (max && newQty > max) newQty = max;

    window.currentModalQty = newQty;
    document.getElementById('modalQty').textContent = newQty;
    updateModalTotal();
}

function toggleToppingSelection(toppingId, checkboxElement) {
    // Toggle selected class on parent label
    const label = checkboxElement.closest('.topping-option');
    if (checkboxElement.checked) {
        label.classList.add('selected');
    } else {
        label.classList.remove('selected');
    }

    const topping = toppings.find(t => t.id === toppingId);
    if (checkboxElement.checked) {
        window.currentModalToppings.push(topping);
    } else {
        window.currentModalToppings = window.currentModalToppings.filter(t => t.id !== toppingId);
    }
    updateModalTotal();
}

function updateModalTotal() {
    const basePrice = window.currentModalProduct.price;
    const toppingsPrice = window.currentModalToppings.reduce((sum, t) => sum + t.price, 0);
    const total = (basePrice + toppingsPrice) * window.currentModalQty;
    document.getElementById('modalTotal').textContent = formatRupiah(total);
}

// Cart Logic
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    const cartItem = {
        id: Date.now(), // Unique ID for cart item
        productId: product.id,
        name: product.name,
        price: product.price,
        image: product.image,
        qty: window.currentModalQty,
        toppings: [...window.currentModalToppings]
    };

    cart.push(cartItem);
    saveCart();
    closeModal();
    toggleCart(); // Open cart to show item added
}

function removeFromCart(cartItemId) {
    cart = cart.filter(item => item.id !== cartItemId);
    saveCart();
}

function updateCartQty(cartItemId, delta) {
    const item = cart.find(i => i.id === cartItemId);
    if (!item) return;

    const product = products.find(p => p.id === item.productId);
    let newQty = item.qty + delta;

    if (newQty < 1) {
        removeFromCart(cartItemId);
        return;
    }
    if (product.max_order && newQty > product.max_order) return;

    item.qty = newQty;
    saveCart();
}

function saveCart() {
    localStorage.setItem('bitebabe_cart', JSON.stringify(cart));
    updateCartUI();
}

function updateCartUI() {
    cartBadge.textContent = cart.reduce((sum, item) => sum + item.qty, 0);

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<div class="empty-cart">Your cart is empty.</div>';
        cartTotalElement.textContent = formatRupiah(0);
        return;
    }

    let total = 0;
    cartItemsContainer.innerHTML = cart.map(item => {
        const toppingsPrice = item.toppings.reduce((sum, t) => sum + t.price, 0);
        const itemTotal = (item.price + toppingsPrice) * item.qty;
        total += itemTotal;

        return `
            <div class="cart-item">
                <img src="${item.image}" class="cart-item-img" onerror="this.src='https://placehold.co/100x100/FFD6E8/FF5C9E?text=Cookie'">
                <div class="cart-item-details">
                    <div class="cart-item-title">${item.name}</div>
                    <div class="cart-item-price">${formatRupiah(item.price)}</div>
                    ${item.toppings.length ? `
                        <div class="cart-item-toppings">
                            + ${item.toppings.map(t => t.name).join(', ')}
                        </div>
                    ` : ''}
                    <div class="cart-controls">
                        <button class="qty-btn" onclick="updateCartQty(${item.id}, -1)">-</button>
                        <span>${item.qty}</span>
                        <button class="qty-btn" onclick="updateCartQty(${item.id}, 1)">+</button>
                        <button class="remove-btn" onclick="removeFromCart(${item.id})"><i class="fa-solid fa-trash"></i></button>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    cartTotalElement.textContent = formatRupiah(total);
}

function toggleCart() {
    cartOverlay.classList.toggle('active');

    // Staggered animation for cart items
    if (cartOverlay.classList.contains('active')) {
        const items = document.querySelectorAll('.cart-item');
        items.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.animation = `fadeUp 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards ${index * 0.1 + 0.2}s`;
        });
    }
}

// Checkout
async function checkoutWhatsApp() {
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }

    const name = document.getElementById('customerName').value;
    const address = document.getElementById('customerAddress').value;
    const payment = document.getElementById('paymentMethod').value;

    if (!name || !address) {
        alert('Please fill in your name and address.');
        return;
    }

    // Calculate total first
    let total = 0;
    const orderItems = cart.map(item => {
        const toppingsPrice = item.toppings.reduce((sum, t) => sum + t.price, 0);
        const itemTotal = (item.price + toppingsPrice) * item.qty;
        total += itemTotal;
        return {
            name: item.name,
            qty: item.qty,
            price: item.price,
            toppings: item.toppings
        };
    });

    // Static website mode: Skip database save
    // In a full version, we would save to a backend here.
    console.log('Proceeding to WhatsApp checkout (Static Mode)');

    // Construct WhatsApp Message
    let message = `Halo, saya ingin pesan:\n\n`;

    cart.forEach(item => {
        const toppingsPrice = item.toppings.reduce((sum, t) => sum + t.price, 0);
        const itemTotal = (item.price + toppingsPrice) * item.qty;

        message += `🍪 ${item.name} x${item.qty} — ${formatRupiah(itemTotal)}\n`;
        if (item.toppings.length) {
            message += `   + Topping: ${item.toppings.map(t => t.name).join(', ')}\n`;
        }
        message += `\n`;
    });

    message += `Total: ${formatRupiah(total)}\n\n`;
    message += `Nama: ${name}\n`;
    message += `Alamat: ${address}\n`;
    message += `Metode Pembayaran: ${payment}`;

    const whatsappNumber = storeConfig.whatsapp || '628123456789';
    const url = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;

    // Clear cart after successful checkout initiation
    cart = [];
    saveCart();
    toggleCart();

    window.open(url, '_blank');
}

// Utility
function formatRupiah(number) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(number);
}
