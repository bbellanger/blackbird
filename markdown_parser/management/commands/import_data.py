import os
import yaml
import markdown
from django.core.management.base import BaseCommand
from django.core.files import File
from markdown_parser.models import Article
from config.settings import BASE_DIR

# Define a function that deletes the .md files after import
def mdfiles_delete():
    path = os.path.join(BASE_DIR, "notes")
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")



class Command(BaseCommand):
    help = 'Import notes from Markdown files'

    def handle(self, *args, **kwargs):
        article_path = os.path.join(BASE_DIR, "notes")
        
        for root, dirs, files in os.walk(article_path):
            for file in files:
                if file.endswith('.md'):
                    self.import_markdown_file(os.path.join(root, file))

    def import_markdown_file(self, file_path):
        with open(file_path, 'r') as f:
            content = f.read()

        # Separate YAML front matter and Markdown content
        front_matter, markdown_content = content.split('---\n', 1)[1].split('---\n', 1)
        
        # Parse the YAML front matter
        metadata = yaml.safe_load(front_matter)

        # Convert Markdown content to HTML (optional)
        html_content = markdown.markdown(markdown_content)

        # Create a new Article object
        article = Article(
            title=metadata.get('title', 'Untitled'),
            date = metadata.get('date', '2024-01-01'),
            tags=','.join(metadata.get('tags', [])),
            content=html_content if html_content else 'Default content',
            slug=os.path.splitext(os.path.basename(file_path))[0],
        )
        
        # Handle the image
        if 'image' in metadata and metadata['image']:
            image_path = os.path.join(os.path.dirname(file_path), metadata['image'])
            if os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    # Save image to the ImageField in the Article model
                    article.image.save(os.path.basename(image_path), File(img_file), save=False)

        # Save the article object to the database
        article.save()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {article.title}'))
        
# Delete .md files from the directory
#mdfiles_delete()
