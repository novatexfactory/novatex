from wagtail import blocks

class AccordionItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True, 
        help_text="Title of the section (e.g., SHIPPING & RETURNS)"
    )
    content = blocks.RichTextBlock(
        required=True, 
        help_text="The hidden content that expands when clicked"
    )

    class Meta:
        icon = 'plus'
        label = "Accordion Item"

class AccordionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        required=False, 
        help_text="Optional section heading (e.g., PRODUCT INTELLIGENCE)"
    )
    items = blocks.ListBlock(
        AccordionItemBlock(), 
        label="Accordion Items"
    )

    class Meta:
        template = 'home/blocks/accordion_block.html'
        icon = 'list-ul'
        label = "FAQ / Product Details"