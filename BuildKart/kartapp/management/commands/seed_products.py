from django.core.management.base import BaseCommand
from kartapp.models import Category, Brand, Product, Testimonial


class Command(BaseCommand):
    help = 'Seeds the database with sample products for BuildKart'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with sample data...')
        
        # Create Categories
        categories_data = [
            {'name': 'Cement', 'slug': 'cement', 'icon': 'fa-box', 'description': 'Premium quality cement for all construction needs'},
            {'name': 'Sand', 'slug': 'sand', 'icon': 'fa-layer-group', 'description': 'Fine and coarse sand for construction'},
            {'name': 'Bricks', 'slug': 'bricks', 'icon': 'fa-th-large', 'description': 'Red bricks and AAC blocks'},
            {'name': 'Steel', 'slug': 'steel', 'icon': 'fa-gavel', 'description': 'TMT bars and steel reinforcement'},
            {'name': 'Aggregates', 'slug': 'aggregates', 'icon': 'fa-cubes', 'description': 'Gravel and crushed stone'},
            {'name': 'Concrete Blocks', 'slug': 'blocks', 'icon': 'fa-border-all', 'description': 'Solid and hollow concrete blocks'},
            {'name': 'Tools & Equipment', 'slug': 'tools', 'icon': 'fa-tools', 'description': 'Construction tools and safety equipment'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = cat
            if created:
                self.stdout.write(f'Created category: {cat.name}')
        
        # Create Brands
        brands_data = [
            {'name': 'UltraTech Cement', 'slug': 'ultratech'},
            {'name': 'Ambuja Cement', 'slug': 'ambuja'},
            {'name': 'ACC Cement', 'slug': 'acc'},
            {'name': 'Birla Corp', 'slug': 'birla'},
            {'name': 'JSW Steel', 'slug': 'jsw'},
            {'name': 'Tata Steel', 'slug': 'tata-steel'},
            {'name': 'SAIL', 'slug': 'sail'},
            {'name': 'Vindhya', 'slug': 'vindhya'},
            {'name': 'Swan', 'slug': 'swan'},
            {'name': 'Kalinga', 'slug': 'kalinga'},
        ]
        
        brands = {}
        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(
                slug=brand_data['slug'],
                defaults=brand_data
            )
            brands[brand_data['slug']] = brand
            if created:
                self.stdout.write(f'Created brand: {brand.name}')
        
        # Create Products
        products_data = [
            # Cement Products
            {
                'name': 'UltraTech PPC Cement - 50kg Bag',
                'slug': 'ultratech-ppc-cement-50kg',
                'category': 'cement',
                'brand': 'ultratech',
                'short_description': 'Premium Portland Pozzolana Cement for durable construction',
                'description': 'UltraTech PPC Cement is a blended cement with excellent workability and strength. Ideal for residential, commercial, and industrial construction.',
                'specifications': 'Grade: PPC | Weight: 50kg | Compressive Strength: 33 MPa',
                'price': 380,
                'discount_percentage': 10,
                'unit': 'bag',
                'stock': 500,
                'rating': 4.5,
                'num_reviews': 128,
                'is_featured': True,
            },
            {
                'name': 'Ambuja OPC Cement - 50kg Bag',
                'slug': 'ambuja-opc-cement-50kg',
                'category': 'cement',
                'brand': 'ambuja',
                'short_description': 'Ordinary Portland Cement for general construction',
                'description': 'Ambuja OPC Cement provides high early strength and is ideal for all types of construction work.',
                'specifications': 'Grade: OPC 43 | Weight: 50kg | Compressive Strength: 43 MPa',
                'price': 420,
                'discount_percentage': 8,
                'unit': 'bag',
                'stock': 450,
                'rating': 4.3,
                'num_reviews': 95,
                'is_featured': True,
            },
            {
                'name': 'ACC Gold Cement - 50kg Bag',
                'slug': 'acc-gold-cement-50kg',
                'category': 'cement',
                'brand': 'acc',
                'short_description': 'Premium quality cement with Quick Strength Technology',
                'description': 'ACC Gold Cement with Quick Strength Technology ensures faster construction with superior durability.',
                'specifications': 'Grade: PPC | Weight: 50kg | Setting Time: 30 mins',
                'price': 395,
                'discount_percentage': 5,
                'unit': 'bag',
                'stock': 400,
                'rating': 4.4,
                'num_reviews': 76,
                'is_featured': False,
            },
            {
                'name': 'Birla Uttam Cement - 50kg Bag',
                'slug': 'birla-uttam-cement-50kg',
                'category': 'cement',
                'brand': 'birla',
                'short_description': 'Premium PPC Cement for robust structures',
                'description': 'Birla Uttam Cement offers excellent strength and durability for all construction needs.',
                'specifications': 'Grade: PPC | Weight: 50kg | Fineness: 3200 cm2/g',
                'price': 375,
                'discount_percentage': 12,
                'unit': 'bag',
                'stock': 380,
                'rating': 4.2,
                'num_reviews': 64,
                'is_featured': False,
            },
            
            # Sand Products
            {
                'name': 'River Sand - 1 Cubic Feet',
                'slug': 'river-sand-1-cubic-feet',
                'category': 'sand',
                'brand': None,
                'short_description': 'Clean river sand for plastering and masonry',
                'description': 'High quality river sand free from impurities. Ideal for plastering, masonry, and concrete work.',
                'specifications': 'Type: River Sand | Grade: A | Moisture Content: < 5%',
                'price': 45,
                'discount_percentage': 0,
                'unit': 'cubic_feet',
                'stock': 1000,
                'rating': 4.1,
                'num_reviews': 45,
                'is_featured': True,
            },
            {
                'name': 'M-Sand (Manufactured Sand) - 1 Ton',
                'slug': 'm-sand-1-ton',
                'category': 'sand',
                'brand': None,
                'short_description': 'Premium manufactured sand for concrete',
                'description': 'Engineered sand produced from crushed rock. Excellent alternative to river sand with better consistency.',
                'specifications': 'Type: M-Sand | Grade: I | FM Value: 2.5-3.0',
                'price': 1200,
                'discount_percentage': 5,
                'unit': 'ton',
                'stock': 500,
                'rating': 4.4,
                'num_reviews': 38,
                'is_featured': False,
            },
            {
                'name': 'Pit Sand - 1 Cubic Feet',
                'slug': 'pit-sand-1-cubic-feet',
                'category': 'sand',
                'brand': None,
                'short_description': 'Natural pit sand for construction',
                'description': 'Clean pit sand suitable for all types of masonry and concrete work.',
                'specifications': 'Type: Pit Sand | Grade: B | Particle Size: 0.075-4.75mm',
                'price': 35,
                'discount_percentage': 0,
                'unit': 'cubic_feet',
                'stock': 800,
                'rating': 3.9,
                'num_reviews': 22,
                'is_featured': False,
            },
            
            # Bricks Products
            {
                'name': 'Red Clay Bricks - 1000 Pieces',
                'slug': 'red-clay-bricks-1000',
                'category': 'bricks',
                'brand': None,
                'short_description': 'Traditional red clay bricks for walls',
                'description': 'Quality red clay bricks with consistent size and strength. Perfect for load-bearing and non-load-bearing walls.',
                'specifications': 'Size: 230x115x75mm | Compressive Strength: 10 MPa | Water Absorption: < 15%',
                'price': 8500,
                'discount_percentage': 8,
                'unit': 'piece',
                'stock': 50000,
                'rating': 4.0,
                'num_reviews': 156,
                'is_featured': True,
            },
            {
                'name': 'AAC Blocks - 1 Cubic Feet',
                'slug': 'aac-blocks-1-cubic-feet',
                'category': 'bricks',
                'brand': 'vindhya',
                'short_description': 'Lightweight AAC blocks for fast construction',
                'description': 'Autoclaved Aerated Concrete blocks are lightweight, fire-resistant, and provide excellent thermal insulation.',
                'specifications': 'Size: 600x200x200mm | Density: 550 kg/m3 | Compressive Strength: 4 MPa',
                'price': 120,
                'discount_percentage': 10,
                'unit': 'piece',
                'stock': 25000,
                'rating': 4.6,
                'num_reviews': 89,
                'is_featured': True,
            },
            {
                'name': 'Fly Ash Bricks - 500 Pieces',
                'slug': 'fly-ash-bricks-500',
                'category': 'bricks',
                'brand': 'swan',
                'short_description': 'Eco-friendly fly ash bricks',
                'description': 'Bricks made from fly ash, cement, and sand. Eco-friendly with consistent quality.',
                'specifications': 'Size: 230x100x75mm | Compressive Strength: 10-12 MPa',
                'price': 4200,
                'discount_percentage': 5,
                'unit': 'piece',
                'stock': 30000,
                'rating': 4.2,
                'num_reviews': 67,
                'is_featured': False,
            },
            
            # Steel Products
            {
                'name': 'JSW Steel TMT Bars - 1 Ton (12mm)',
                'slug': 'jsw-tmt-bars-12mm-1-ton',
                'category': 'steel',
                'brand': 'jsw',
                'short_description': 'High-strength TMT bars for reinforcement',
                'description': 'JSW Thermex TMT Bars with superior strength and ductility. Earthquake resistant and corrosion proof.',
                'specifications': 'Grade: Fe 500D | Diameter: 12mm | Length: 12m',
                'price': 58000,
                'discount_percentage': 8,
                'unit': 'ton',
                'stock': 200,
                'rating': 4.7,
                'num_reviews': 234,
                'is_featured': True,
            },
            {
                'name': 'TATA Steel TMT Bars - 1 Ton (16mm)',
                'slug': 'tata-tmt-bars-16mm-1-ton',
                'category': 'steel',
                'brand': 'tata-steel',
                'short_description': 'Premium TMT bars from Tata',
                'description': 'TATA Tiscon TMT Bars with advanced rib design for better bonding with concrete.',
                'specifications': 'Grade: Fe 500D | Diameter: 16mm | Length: 12m',
                'price': 62000,
                'discount_percentage': 10,
                'unit': 'ton',
                'stock': 150,
                'rating': 4.8,
                'num_reviews': 189,
                'is_featured': True,
            },
            {
                'name': 'SAIL Steel TMT Bars - 1 Ton (10mm)',
                'slug': 'sail-tmt-bars-10mm-1-ton',
                'category': 'steel',
                'brand': 'sail',
                'short_description': 'Government quality TMT bars',
                'description': 'SAIL TMT Bars manufactured by Steel Authority of India. Trusted quality at affordable price.',
                'specifications': 'Grade: Fe 415 | Diameter: 10mm | Length: 12m',
                'price': 52000,
                'discount_percentage': 5,
                'unit': 'ton',
                'stock': 180,
                'rating': 4.5,
                'num_reviews': 145,
                'is_featured': False,
            },
            {
                'name': 'Steel Binding Wire - 5kg Bundle',
                'slug': 'steel-binding-wire-5kg',
                'category': 'steel',
                'brand': None,
                'short_description': 'GI binding wire for reinforcement',
                'description': 'Galvanized iron binding wire for tying TMT bars. Soft and easy to use.',
                'specifications': 'Gauge: 20-22 | Material: GI | Weight: 5kg',
                'price': 350,
                'discount_percentage': 3,
                'unit': 'kg',
                'stock': 500,
                'rating': 4.1,
                'num_reviews': 34,
                'is_featured': False,
            },
            
            # Aggregates Products
            {
                'name': '20mm Crushed Stone Aggregate - 1 Cubic Meter',
                'slug': '20mm-crushed-stone-1-cubic-meter',
                'category': 'aggregates',
                'brand': None,
                'short_description': 'Quality crushed stone for concrete',
                'description': '20mm graded crushed stone aggregate suitable for concrete and road work.',
                'specifications': 'Size: 20mm | Type: Crushed | Shape: Angular',
                'price': 1800,
                'discount_percentage': 5,
                'unit': 'cubic_meter',
                'stock': 300,
                'rating': 4.3,
                'num_reviews': 56,
                'is_featured': False,
            },
            {
                'name': '40mm Crushed Stone Aggregate - 1 Cubic Meter',
                'slug': '40mm-crushed-stone-1-cubic-meter',
                'category': 'aggregates',
                'brand': None,
                'short_description': 'Coarse aggregate for mass concrete',
                'description': '40mm crushed stone for RCC work, foundations, and mass concrete.',
                'specifications': 'Size: 40mm | Type: Crushed | Shape: Angular',
                'price': 1600,
                'discount_percentage': 5,
                'unit': 'cubic_meter',
                'stock': 250,
                'rating': 4.2,
                'num_reviews': 42,
                'is_featured': False,
            },
            {
                'name': '10mm Crushed Stone Aggregate - 1 Cubic Meter',
                'slug': '10mm-crushed-stone-1-cubic-meter',
                'category': 'aggregates',
                'brand': None,
                'short_description': 'Fine aggregate for concrete',
                'description': '10mm crushed stone for RCC, plastering, and finishing work.',
                'specifications': 'Size: 10mm | Type: Crushed | Shape: Angular',
                'price': 1950,
                'discount_percentage': 3,
                'unit': 'cubic_meter',
                'stock': 280,
                'rating': 4.4,
                'num_reviews': 38,
                'is_featured': False,
            },
            
            # Concrete Blocks
            {
                'name': 'Solid Concrete Block - 4 Inch',
                'slug': 'solid-concrete-block-4-inch',
                'category': 'blocks',
                'brand': None,
                'short_description': 'Solid concrete blocks for load-bearing walls',
                'description': 'High strength solid concrete blocks. Eco-friendly alternative to bricks.',
                'specifications': 'Size: 400x200x100mm | Compressive Strength: 5-7 MPa',
                'price': 45,
                'discount_percentage': 8,
                'unit': 'piece',
                'stock': 40000,
                'rating': 4.3,
                'num_reviews': 78,
                'is_featured': False,
            },
            {
                'name': 'Hollow Concrete Block - 6 Inch',
                'slug': 'hollow-concrete-block-6-inch',
                'category': 'blocks',
                'brand': None,
                'short_description': 'Hollow blocks for partition walls',
                'description': 'Lightweight hollow concrete blocks with excellent thermal insulation.',
                'specifications': 'Size: 400x200x150mm | Compressive Strength: 3-5 MPa',
                'price': 55,
                'discount_percentage': 5,
                'unit': 'piece',
                'stock': 35000,
                'rating': 4.1,
                'num_reviews': 45,
                'is_featured': False,
            },
            {
                'name': 'Pavers Block - 230x115x60mm',
                'slug': 'paver-block-230x115x60mm',
                'category': 'blocks',
                'brand': 'kalinga',
                'short_description': 'Interlocking pavers for driveways',
                'description': 'Colorful interlocking paver blocks for driveways, walkways, and parking areas.',
                'specifications': 'Size: 230x115x60mm | Strength: 30-40 MPa',
                'price': 35,
                'discount_percentage': 10,
                'unit': 'piece',
                'stock': 50000,
                'rating': 4.5,
                'num_reviews': 92,
                'is_featured': True,
            },
            
            # Tools & Equipment
            {
                'name': 'Construction Helmet - Yellow',
                'slug': 'construction-helmet-yellow',
                'category': 'tools',
                'brand': None,
                'short_description': 'Safety helmet for construction workers',
                'description': 'ISI marked safety helmet with adjustable strap. Lightweight and comfortable.',
                'specifications': 'Material: HDPE | Size: Adjustable | ISI Marked',
                'price': 150,
                'discount_percentage': 15,
                'unit': 'piece',
                'stock': 500,
                'rating': 4.4,
                'num_reviews': 67,
                'is_featured': True,
            },
            {
                'name': 'Wheelbarrow - 90 Liter',
                'slug': 'wheelbarrow-90-liter',
                'category': 'tools',
                'brand': None,
                'short_description': 'Heavy duty wheelbarrow for material handling',
                'description': 'Sturdy wheelbarrow with pneumatic wheel. Perfect for transporting sand, cement, and debris.',
                'specifications': 'Capacity: 90 Liters | Frame: Steel | Wheel: Pneumatic',
                'price': 1200,
                'discount_percentage': 10,
                'unit': 'piece',
                'stock': 100,
                'rating': 4.5,
                'num_reviews': 45,
                'is_featured': False,
            },
            {
                'name': 'Trowel Set - 5 Pieces',
                'slug': 'trowel-set-5-pieces',
                'category': 'tools',
                'brand': None,
                'short_description': 'Professional trowel set for plastering',
                'description': 'Stainless steel trowel set with wooden handles. Includes pointing, brick, and finishing trowels.',
                'specifications': 'Material: Stainless Steel | Pieces: 5 | Handle: Wooden',
                'price': 450,
                'discount_percentage': 8,
                'unit': 'piece',
                'stock': 200,
                'rating': 4.3,
                'num_reviews': 34,
                'is_featured': False,
            },
            {
                'name': 'Measuring Tape - 10 Meters',
                'slug': 'measuring-tape-10-meters',
                'category': 'tools',
                'brand': None,
                'short_description': 'Fiber measuring tape for construction',
                'description': 'Durable fiber measuring tape with metric markings. Water resistant and break resistant.',
                'specifications': 'Length: 10m | Material: Fiber | Type: Metric',
                'price': 85,
                'discount_percentage': 5,
                'unit': 'piece',
                'stock': 400,
                'rating': 4.2,
                'num_reviews': 56,
                'is_featured': False,
            },
            {
                'name': 'Safety Gloves - Pair',
                'slug': 'safety-gloves-pair',
                'category': 'tools',
                'brand': None,
                'short_description': 'Leather safety gloves for workers',
                'description': 'Heavy duty leather gloves with reinforced palm. Protects hands during construction work.',
                'specifications': 'Material: Leather | Size: Free | Type: Reinforced',
                'price': 120,
                'discount_percentage': 10,
                'unit': 'piece',
                'stock': 600,
                'rating': 4.1,
                'num_reviews': 89,
                'is_featured': False,
            },
        ]
        
        for prod_data in products_data:
            category = categories[prod_data.pop('category')]
            brand_slug = prod_data.pop('brand', None)
            brand = brands.get(brand_slug) if brand_slug else None
            
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults={
                    **prod_data,
                    'category': category,
                    'brand': brand,
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        # Create Testimonials
        testimonials_data = [
            {
                'name': 'Rajesh Kumar',
                'company': 'Rajesh Construction',
                'message': 'BuildKart has made procurement of construction materials so much easier. Great quality and timely delivery!',
                'rating': 5,
            },
            {
                'name': 'Priya Sharma',
                'company': 'Sharma Builders',
                'message': 'Excellent platform for bulk orders. The TMT bars quality is top-notch and prices are competitive.',
                'rating': 5,
            },
            {
                'name': 'Mohammad Khan',
                'company': 'Khan Contractors',
                'message': 'Very reliable service. Ordered cement and steel for my project - always on time and good quality.',
                'rating': 4,
            },
            {
                'name': 'Anita Desai',
                'company': 'Desai Infrastructure',
                'message': 'Great customer support and amazing product range. Highly recommended for all construction needs!',
                'rating': 5,
            },
        ]
        
        for test_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=test_data['name'],
                defaults=test_data
            )
            if created:
                self.stdout.write(f'Created testimonial: {testimonial.name}')
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write(f'Categories: {len(categories)}')
        self.stdout.write(f'Brands: {len(brands)}')
        self.stdout.write(f'Products: {Product.objects.count()}')
        self.stdout.write(f'Testimonials: {Testimonial.objects.count()}')
