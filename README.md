# Chai & Chapter Café – PHP + MySQL SEO site

A 3-page (Home, About, Blog) website for a fictional Mumbai café. Blog posts and every page's meta title and description live in MySQL.

## Setup (XAMPP / any Apache + PHP 8+ + MySQL)
1. Copy this folder into `htdocs` (e.g. `htdocs/chai-cafe`). Enable `mod_rewrite` and `AllowOverride All`.
2. Import the database: `mysql -u root -p < database/schema.sql` (or import in phpMyAdmin).
3. Edit DB credentials in `config.php` (or set `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS` env vars).
4. Open `http://localhost/chai-cafe/`.

Routes: `/`, `/about`, `/blog`, `/blog/{slug}`, `/sitemap.xml`, `/robots.txt`.

## SEO choices
- Unique `<title>`, meta description and canonical URL per page, read from MySQL (`pages` and `posts` tables).
- One `<h1>` per page with a clean h1 → h2 → h3 order; semantic landmarks (`header`, `nav`, `main`, `article`, `footer`).
- Clean slug URLs via `.htaccess`; invalid slugs return a real 404 with `noindex`.
- `sitemap.xml` is generated from the DB (with `lastmod`), `robots.txt` points to it; all images have alt text plus width/height to avoid layout shift.
- Bonus: `CafeOrCoffeeShop` (LocalBusiness) JSON-LD with address, geo and opening hours on Home.

## Lighthouse
Chrome DevTools → Lighthouse → Mobile → run on the Home page, save the screenshot as `lighthouse-home.png` in the repo.
