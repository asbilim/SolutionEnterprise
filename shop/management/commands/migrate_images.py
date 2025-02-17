from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from shop.models import Product, ImageGallery, Testimonial
from blog.models import Article, Category
import requests
import tempfile
import os
from django.core.files import File

class Command(BaseCommand):
    help = 'Migrate existing images to new storage configuration'

    def download_image(self, url):
        """Download image from URL."""
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                # Create a temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=True)
                # Write the content to the temporary file
                for block in response.iter_content(1024 * 8):
                    if not block:
                        break
                    temp_file.write(block)
                temp_file.flush()
                return temp_file
            return None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error downloading image: {str(e)}'))
            return None

    def migrate_model_images(self, model, field_name):
        """Migrate images for a specific model and field."""
        self.stdout.write(f'Migrating images for {model.__name__}...')
        for instance in model.objects.all():
            field = getattr(instance, field_name)
            if field and field.name:
                try:
                    # Get the current URL
                    current_url = field.url
                    self.stdout.write(f'Processing {current_url}')

                    # Download the image
                    temp_file = self.download_image(current_url)
                    if temp_file:
                        # Get original filename
                        original_name = os.path.basename(field.name)
                        
                        # Clear the current field
                        field.delete(save=False)
                        
                        # Save the new file
                        field.save(
                            original_name,
                            File(temp_file),
                            save=False
                        )
                        
                        instance.save()
                        self.stdout.write(self.style.SUCCESS(
                            f'Successfully migrated {original_name}'
                        ))
                        
                        # Close and delete temp file
                        temp_file.close()
                    else:
                        self.stdout.write(self.style.WARNING(
                            f'Could not download {current_url}'
                        ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Error processing {field.name}: {str(e)}'
                    ))

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting image migration...')

        # Migrate Product images
        self.migrate_model_images(Product, 'image')

        # Migrate ImageGallery images
        self.migrate_model_images(ImageGallery, 'image')

        # Migrate Testimonial images
        self.migrate_model_images(Testimonial, 'image')

        # Migrate Category images
        self.migrate_model_images(Category, 'image')

        # Migrate Article images
        self.migrate_model_images(Article, 'image')

        self.stdout.write(self.style.SUCCESS('Image migration completed!')) 