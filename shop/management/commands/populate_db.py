from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from shop.models import Product, ImageGallery, Testimonial, Contact, Request
from blog.models import Article, Category
import random
import requests
from faker import Faker
from django.utils.text import slugify
import io

fake = Faker()

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def download_image(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return ContentFile(response.content)
        return None

    def save_image(self, instance, field_name, image_content, filename):
        if image_content:
            # Get the field's upload_to path
            field = instance._meta.get_field(field_name)
            upload_to = field.upload_to

            # Construct the full path
            full_path = f"{upload_to}/{filename}" if upload_to else filename
            
            # Save using default storage (R2)
            file_name = default_storage.save(full_path, image_content)
            
            # Update the model's field
            setattr(instance, field_name, file_name)
            instance.save()

    def generate_medical_article_content(self):
        """Generate medical-themed article content with CKEditor5 formatting"""
        medical_topics = [
            "Latest Advances in Medical Technology",
            "Healthcare Innovation",
            "Patient Care Improvements",
            "Medical Research Breakthroughs",
            "Healthcare Industry Trends"
        ]
        
        paragraphs = []
        # Add a main heading
        paragraphs.append(f"<h2>{random.choice(medical_topics)}</h2>")
        
        # Add introduction
        paragraphs.append(f"<p>{fake.paragraph(nb_sentences=3)}</p>")
        
        # Add subheadings with content
        for _ in range(3):
            paragraphs.append(f"<h3>{fake.catch_phrase()}</h3>")
            paragraphs.append(f"<p>{fake.paragraph(nb_sentences=4)}</p>")
            
            # Add a list sometimes
            if random.choice([True, False]):
                list_items = [f"<li>{fake.sentence()}</li>" for _ in range(3)]
                list_html = f"<ul>{''.join(list_items)}</ul>"
                paragraphs.append(list_html)
        
        # Add a quote
        paragraphs.append(f'<blockquote><p>"{fake.sentence()}"</p></blockquote>')
        
        # Add conclusion
        paragraphs.append(f"<h3>Conclusion</h3>")
        paragraphs.append(f"<p>{fake.paragraph(nb_sentences=2)}</p>")
        
        return '\n'.join(paragraphs)

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database population...')

        # Create Categories
        categories = [
            {
                'title': 'Medical Equipment',
                'description': 'Essential medical equipment for healthcare facilities',
                'image_url': 'https://images.unsplash.com/photo-1583324113626-70df0f4deaab'
            },
            {
                'title': 'Laboratory Supplies',
                'description': 'High-quality laboratory supplies and equipment',
                'image_url': 'https://images.unsplash.com/photo-1579154204601-01588f351e67'
            },
            {
                'title': 'Healthcare News',
                'description': 'Latest updates in healthcare and medical technology',
                'image_url': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d'
            },
        ]

        for cat_data in categories:
            category = Category.objects.create(
                title=cat_data['title'],
                description=cat_data['description']
            )
            image_content = self.download_image(cat_data['image_url'])
            if image_content:
                self.save_image(category, 'image', image_content, f"{slugify(cat_data['title'])}.jpg")
            self.stdout.write(f'Created category: {category.title}')

        # Create Products
        product_images = [
            'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae',  # Stethoscope
            'https://images.unsplash.com/photo-1603398938378-e54eab446dde',  # Microscope
            'https://images.unsplash.com/photo-1581595220892-b0739db3ba8c',  # Blood pressure monitor
        ]

        for i in range(10):
            product = Product.objects.create(
                name=f"{fake.company()} {fake.word().title()} {random.choice(['Monitor', 'Scanner', 'Device'])}",
                description=fake.paragraph(nb_sentences=5),
                price=random.uniform(100, 10000),
                quantity=random.randint(1, 100),
                sizable=random.choice([True, False]),
                downloadable=random.choice([True, False])
            )
            image_content = self.download_image(random.choice(product_images))
            self.save_image(product, 'image', image_content, f"product_{i}.jpg")
            self.stdout.write(f'Created product: {product.name}')

        # Create Articles
        article_images = [
            'https://images.unsplash.com/photo-1576091160550-2173dba999ef',
            'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d',
            'https://images.unsplash.com/photo-1587854692152-cbe660dbde88',
            'https://images.unsplash.com/photo-1631248055158-edec7a3c072b',
            'https://images.unsplash.com/photo-1530497610245-94d3c16cda28',
            'https://images.unsplash.com/photo-1666214280557-f1b5022eb634'
        ]

        article_titles = [
            "Breakthrough in Medical Imaging Technology",
            "The Future of Healthcare: AI and Machine Learning",
            "Understanding Modern Laboratory Equipment",
            "Advances in Patient Care Technology",
            "Medical Equipment Maintenance Best Practices",
            "Healthcare Technology: A 2025 Perspective"
        ]

        for i in range(len(article_titles)):
            article = Article.objects.create(
                title=article_titles[i],
                content=self.generate_medical_article_content(),
                description=fake.paragraph(nb_sentences=2),
                likes=random.randint(50, 2000),
                shares=random.randint(20, 1000),
                category=Category.objects.order_by('?').first()
            )
            image_content = self.download_image(article_images[i])
            self.save_image(article, 'image', image_content, f"article_{i}.jpg")
            self.stdout.write(f'Created article: {article.title}')

        # Create Testimonials
        testimonial_images = [
            'https://images.unsplash.com/photo-1559839734-2b71ea197ec2',
            'https://images.unsplash.com/photo-1494790108377-be9c29b29330',
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d'
        ]

        for i in range(5):
            testimonial = Testimonial.objects.create(
                author=fake.name(),
                message=fake.paragraph(),
                position=fake.job()
            )
            image_content = self.download_image(random.choice(testimonial_images))
            if image_content:
                self.save_image(testimonial, 'image', image_content, f"testimonial_{i}.jpg")
            self.stdout.write(f'Created testimonial from: {testimonial.author}')

        # Create Contacts
        for _ in range(8):
            Contact.objects.create(
                subject=fake.sentence(),
                email=fake.email(),
                message=fake.paragraph()
            )

        # Create Requests
        for _ in range(5):
            Request.objects.create(
                email=fake.email(),
                phone_number=fake.phone_number(),
                product=Product.objects.order_by('?').first()
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated database!')) 