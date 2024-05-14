import os
from PIL import Image, ImageDraw, ImageFont
from py_avataaars import PyAvataaar
from py_avataaars import AvatarStyle, SkinColor, TopType, HairColor, FacialHairType, ClotheType, Color, EyesType, \
    EyebrowType, MouthType
import random
from applicant.models import Applicant, Experience, Education, Recommendation
from company.models import Company
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


def generate_logo(company_name: Company) -> str:
    """
    Generate a logo image with random background color, text, and shapes.

    Args:
        company_name (str): The name of the company.

    Returns:
        str: The path to the generated logo image.
    """

    # Create image
    width, height = 400, 300
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Background color
    bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    image.paste(bg_color, [0, 0, width, height])

    # Font
    try:
        font = ImageFont.truetype("arial.ttf", random.randint(300, 400))  # Random font size
    except IOError:
        font = ImageFont.load_default(random.randint(30, 40))

    #  Text
    text_width, text_height = draw.textbbox((0, 0), company_name, font=font)[2:]
    text_position = ((width - text_width) / 2, (height - text_height) / 2)
    text_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    draw.text(text_position, company_name, font=font, fill=text_color)

    # Shapes
    for _ in range(random.randint(1, 5)):
        shape_type = random.choice(['rectangle', 'ellipse'])
        x0, x1 = sorted([random.randint(0, width), random.randint(0, width)])
        y0, y1 = sorted([random.randint(0, height), random.randint(0, height)])
        shape_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if shape_type == 'rectangle':
            draw.rectangle([x0, y0, x1, y1], outline=shape_color, width=2)
        elif shape_type == 'ellipse':
            draw.ellipse([x0, y0, x1, y1], outline=shape_color, width=2)

    # Save
    logo_directory = os.path.join('media/logos')
    if not os.path.exists(logo_directory):
        os.makedirs(logo_directory)
    logo_filename = f'{company_name.replace(" ", "_")}.png'
    logo_path = os.path.join(logo_directory, logo_filename)
    image.save(logo_path)

    return os.path.join('logos', logo_filename)


def generate_avatar(applicant: Applicant) -> str:
    """
     Generate an avatar image for an applicant.

     Args:
         applicant: An object representing the applicant.

     Returns:
         str: The path to the generated avatar image.
     """
    # Remove undesireable attributes
    eye_types = [eye for eye in EyesType if eye not in [EyesType.CLOSE, EyesType.DIZZY, EyesType.SQUINT, EyesType.CRY, EyesType.HEARTS]]
    mouth_types = [mouth for mouth in MouthType if mouth not in [MouthType.SERIOUS, MouthType.SCREAM_OPEN, MouthType.SAD, MouthType.VOMIT]]

    # Create an avatar with randomized attributes
    avatar = PyAvataaar(
        style=AvatarStyle.CIRCLE,
        skin_color=random.choice(list(SkinColor)),
        top_type=random.choice(list(TopType)),
        hair_color=random.choice(list(HairColor)),
        facial_hair_type=random.choice(list(FacialHairType)),
        facial_hair_color=random.choice(list(HairColor)),
        clothe_type=random.choice(list(ClotheType)),
        clothe_color=random.choice(list(Color)),
        eye_type=random.choice(list(eye_types)),
        eyebrow_type=random.choice(list(EyebrowType)),
        mouth_type=random.choice(list(mouth_types))
    )

    # Save
    avatar_directory = os.path.join('media', 'images')

    if not os.path.exists(avatar_directory):
        os.makedirs(avatar_directory)
    avatar_filename = f'{applicant.user.first_name}_{applicant.user.last_name}.png'
    avatar_path = os.path.join(avatar_directory, avatar_filename)

    avatar.render_png_file(avatar_path)
    return os.path.join('images', avatar_filename)





def generate_pdf_resume(applicant: Applicant, fake, num) -> str:
    # File path
    resume_filename = f"{applicant.user.username}_{num}_resume.pdf"
    resume_filepath = os.path.join(MEDIA_ROOT, 'resumes', resume_filename)
    os.makedirs(os.path.dirname(resume_filepath), exist_ok=True)

    # PDF canvas
    c = canvas.Canvas(resume_filepath, pagesize=letter)
    width, height = letter

    # Text
    c.setFont("Helvetica", 12)
    text = c.beginText(40, height - 40)

    # Applicant Info
    text.setFont("Helvetica-Bold", 16)
    text.textLine(f"{applicant.user.first_name} {applicant.user.last_name}")
    text.setFont("Helvetica", 12)
    text.textLine(f"Email: {applicant.user.email}")
    text.textLine(f"Phone: {applicant.phone_number}")
    text.textLine(
        f"Address: {applicant.house_number} {applicant.street_name}, {applicant.city}, {applicant.country.name}, {applicant.postal_code}")
    text.textLine("")

    # Summary
    text.setFont("Helvetica-Bold", 14)
    text.textLine("Summary")
    text.setFont("Helvetica", 12)
    text.textLine(fake.paragraph(nb_sentences=5))

    # Education
    text.setFont("Helvetica-Bold", 14)
    text.textLine("Education")
    educations = Education.objects.filter(applicant=applicant)
    for education in educations:
        text.setFont("Helvetica-Bold", 12)
        text.textLine(education.school)
        text.setFont("Helvetica", 12)
        text.textLine(f"{education.level} ({education.start_date} - {education.end_date})")
        text.textLine(education.location)
        text.textLine(education.additional_info)
        text.textLine("")

    # Experience
    text.setFont("Helvetica-Bold", 14)
    text.textLine("Experience")
    experiences = Experience.objects.filter(applicant=applicant)
    for experience in experiences:
        text.setFont("Helvetica-Bold", 12)
        text.textLine(experience.company_name)
        text.setFont("Helvetica", 12)
        text.textLine(f"({experience.start_date} - {experience.end_date})")
        text.textLine(experience.main_responsibility)
        text.textLine("")

    # Recommendations
    text.setFont("Helvetica-Bold", 14)
    text.textLine("Recommendations")
    recommendations = Recommendation.objects.filter(applicant=applicant)
    for recommendation in recommendations:
        text.setFont("Helvetica-Bold", 12)
        text.textLine(recommendation.name)
        text.setFont("Helvetica", 12)
        text.textLine(f"{recommendation.company_name}")
        text.textLine(f"Phone: {recommendation.phone_number}")
        text.textLine("")

    # Save
    c.drawText(text)
    c.showPage()
    c.save()

    return os.path.join('resumes', resume_filename)
