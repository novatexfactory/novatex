from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail import blocks


# -------------------------
# Home (top-level site root)
# -------------------------

class HomePage(Page):
    """
    The real site homepage (top level).
    Keep it simple: brand + navigation + CTA.
    """
    template = "home/home_page.html"

    hero_title = models.CharField(max_length=140, blank=True)
    hero_subtitle = models.CharField(max_length=255, blank=True)
    intro = RichTextField(blank=True)

    cta_primary_text = models.CharField(max_length=60, blank=True)
    cta_primary_url = models.URLField(blank=True)

    cta_secondary_text = models.CharField(max_length=60, blank=True)
    cta_secondary_url = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_subtitle"),
                FieldPanel("intro"),
            ],
            heading="Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel("cta_primary_text"),
                FieldPanel("cta_primary_url"),
                FieldPanel("cta_secondary_text"),
                FieldPanel("cta_secondary_url"),
            ],
            heading="Call to action",
        ),
    ]

    # Only allow the Texarine hub under the homepage
    subpage_types = [
        "home.TexarineLandingPage",
    ]


# -------------------------
# Texarine hub (main product site)
# -------------------------

class TexarineLandingPage(Page):
    """
    The Texarine hub page (separate from HomePage).
    All product/supporting pages live under this.
    """
    template = "home/texarine_landing_page.html"

    hero_title = models.CharField(max_length=140, blank=True)
    hero_subtitle = models.CharField(max_length=255, blank=True)

    what_it_is = RichTextField(blank=True)
    what_its_not = RichTextField(blank=True)
    who_its_for = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("hero_title"), FieldPanel("hero_subtitle")],
            heading="Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel("what_it_is"),
                FieldPanel("what_its_not"),
                FieldPanel("who_its_for"),
            ],
            heading="Core content",
        ),
    ]

    parent_page_types = ["home.HomePage"]

    # IMPORTANT: this must list children, otherwise you can't add anything under TexarineLandingPage
    subpage_types = [
        "home.ProductIndexPage",
        "home.IngredientsPage",
        "home.QualityCompliancePage",
        "home.HowToUsePage",
        "home.FAQPage",
        "home.ContactPage",
        "home.LegalIndexPage",
        "home.BlogIndexPage",
    ]


# -------------------------
# Products
# -------------------------

class ProductIndexPage(Page):
    """
    Container for product listing.
    """
    template = "home/product_index_page.html"

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["home.TexarineLandingPage"]
    subpage_types = ["home.ProductPage"]


class ProductPage(Page):
    """
    Product detail page.
    Uses Page.title as product name.
    """
    template = "home/product_page.html"

    sku = models.CharField(max_length=64, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)

    format_note = models.CharField(
        max_length=120,
        blank=True,
        help_text="Example: Sublingual tablets (non-nicotine).",
    )

    short_description = models.CharField(max_length=240, blank=True)
    description = RichTextField(blank=True)

    # Optional pricing placeholder for future commerce
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    warnings = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("sku"),
                FieldPanel("subtitle"),
                FieldPanel("format_note"),
                FieldPanel("price"),
            ],
            heading="Product basics",
        ),
        MultiFieldPanel(
            [
                FieldPanel("short_description"),
                FieldPanel("description"),
            ],
            heading="Description",
        ),
        MultiFieldPanel(
            [
                FieldPanel("warnings"),
            ],
            heading="Warnings / disclaimers",
        ),
    ]

    parent_page_types = ["home.ProductIndexPage"]
    subpage_types = []


# -------------------------
# Supporting / compliance pages (under TexarineLandingPage)
# -------------------------

class IngredientsPage(Page):
    template = "home/ingredients_page.html"

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("body")]

    parent_page_types = ["home.TexarineLandingPage"]
    subpage_types = []


class QualityCompliancePage(Page):
    template = "home/quality_compliance_page.html"

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("body")]

    parent_page_types = ["home.TexarineLandingPage"]
    subpage_types = []


class HowToUsePage(Page):
    template = "home/how_to_use_page.html"

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("body")]

    parent_page_types = ["home.TexarineLandingPage"]
    subpage_types = []


class FAQPage(Page):
    template = "home/faq_page.html"

    intro = RichTextField(blank=True)
    faqs = StreamField(
        [
            (
                "faq",
                blocks.StructBlock(
                    [
                        ("question", blocks.CharBlock(required=True, max_length=140)),
                        ("answer", blocks.RichTextBlock(required=True)),
                    ],
                    icon="help",
                    label="FAQ item",
                ),
            )
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("faqs"),
    ]

    parent_page_types = ["home.TexarineLandingPage"]
    subpage_types = []


class ContactPage(Page):
    template = "home/contact_page.html"

    intro = RichTextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=40, blank=True)
    note = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        MultiFieldPanel(
            [FieldPanel("contact_email"), FieldPanel("contact_phone")],
            heading="Contact details",
        ),
        FieldPanel("note"),
    ]

    parent_page_types = ["home.TexarineLandingPage"]
    subpage_types = []


# -------------------------
# Legal
# -------------------------

class LegalIndexPage(Page):
    template = "home/legal_index_page.html"

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    parent_page_types = ["home.TexarineLandingPage"]
    subpage_types = [
        "home.DisclaimerPage",
        "home.PrivacyPolicyPage",
        "home.TermsPage",
        "home.ReturnsShippingPage",
    ]


class DisclaimerPage(Page):
    template = "home/disclaimer_page.html"

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("body")]

    parent_page_types = ["home.LegalIndexPage"]
    subpage_types = []


class PrivacyPolicyPage(Page):
    template = "home/privacy_policy_page.html"

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("body")]

    parent_page_types = ["home.LegalIndexPage"]
    subpage_types = []


class TermsPage(Page):
    template = "home/terms_page.html"

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("body")]

    parent_page_types = ["home.LegalIndexPage"]
    subpage_types = []


class ReturnsShippingPage(Page):
    template = "home/returns_shipping_page.html"

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("body")]

    parent_page_types = ["home.LegalIndexPage"]
    subpage_types = []


# -------------------------
# Blog (optional)
# -------------------------

class BlogIndexPage(Page):
    template = "home/blog_index_page.html"

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    parent_page_types = ["home.TexarineLandingPage"]
    subpage_types = ["home.BlogPage"]


class BlogPage(Page):
    template = "home/blog_page.html"

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("body")]

    parent_page_types = ["home.BlogIndexPage"]
    subpage_types = []
