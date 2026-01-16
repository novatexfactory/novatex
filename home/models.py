from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel

# --- 1. HERO BLOCK ---
class HeroBlock(blocks.StructBlock):
    """
    Hero Section with background image, title, and CTA button.
    """
    image = ImageChooserBlock(required=True, label="Background Image")
    title = blocks.CharBlock(required=True, max_length=60, label="Title (e.g. TEXARINE)")
    subtitle = blocks.TextBlock(required=False, label="Subtitle")
    
    # Changed to CharBlock to allow anchors like '#' or relative paths
    button_text = blocks.CharBlock(required=False, default="Try it now", label="Button Text")
    button_url = blocks.CharBlock(required=False, label="Button URL")

    class Meta:
        template = "home/blocks/hero_block.html"
        icon = "image"
        label = "Hero Banner"

# --- 2. BENEFITS BLOCK (New) ---
class BenefitsBlock(blocks.StructBlock):
    """
    Section with a title and a grid of 3 features with icons.
    """
    title = blocks.CharBlock(required=True, label="Section Title (e.g. WHY TEXARINE?)")
    
    # List of benefits (Icon + Title + Description)
    items = blocks.ListBlock(blocks.StructBlock([
        ('icon', blocks.CharBlock(label="Emoji Icon (e.g. ⚡, 🧠, 🛡️)")),
        ('title', blocks.CharBlock(label="Benefit Title")),
        ('text', blocks.TextBlock(label="Benefit Description")),
    ]), label="Benefits List")

    class Meta:
        template = "home/blocks/benefits_block.html"
        icon = "list-ul"
        label = "Benefits Section"

# --- 3. FEATURE BLOCK (Image + Text) ---
class FeatureBlock(blocks.StructBlock):
    """
    Block with Image on one side and Text on the other.
    Ideal for 'Science' or 'About' sections.
    """
    heading = blocks.CharBlock(required=True, label="Heading (e.g. THE SCIENCE)")
    description = blocks.RichTextBlock(required=True, label="Text Content")
    image = ImageChooserBlock(required=True, label="Image")
    
    # Checkbox to switch image position (Left/Right)
    reverse_layout = blocks.BooleanBlock(required=False, label="Image on the Right? (Default is Left)", help_text="Check this to swap image and text positions")

    button_text = blocks.CharBlock(required=False, label="Button Text")
    button_url = blocks.CharBlock(required=False, label="Button URL")

    class Meta:
        template = "home/blocks/feature_block.html"
        icon = "doc-full-inverse"
        label = "Feature / Science Block"

# --- 4. PRODUCT BLOCK (SHOP) ---
class ProductBlock(blocks.StructBlock):
    """
    Block to showcase the product with price and CTA.
    """
    heading = blocks.CharBlock(required=True, label="Product Name (e.g. STARTER PACK)")
    price = blocks.CharBlock(required=True, label="Price (e.g. $14.99)")
    description = blocks.TextBlock(required=False, label="Short Description")
    image = ImageChooserBlock(required=True, label="Product Image")
    
    # List of bullet points (e.g. "20 Tablets", "Orange Flavor")
    features = blocks.ListBlock(blocks.CharBlock(label="Feature point"), label="Key Features List")
    
    button_text = blocks.CharBlock(default="ADD TO CART", label="Button Text")
    button_url = blocks.CharBlock(required=False, label="Button URL")

    class Meta:
        template = "home/blocks/product_block.html"
        icon = "cart"
        label = "Product Showcase"

# --- X. HOME PAGE ---
class HomePage(Page):
    """
    The main landing page model.
    """
    # StreamField allows adding blocks in any order
    body = StreamField([
        ('hero', HeroBlock()), 
        ('benefits', BenefitsBlock()),
        ('feature', FeatureBlock()),
        ('product', ProductBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]