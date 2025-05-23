# Generated by Django 4.2.3 on 2024-07-29 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0017_rename_areas_of_activity_profile_sub_activity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="main_of_activity",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "AGRICULTURE_FORESTRY_FISHING",
                        "Agriculture, Forestry and Fishing",
                    ),
                    ("MINING_QUARRYING", "Mining and Quarrying"),
                    ("MANUFACTURING", "Manufacturing"),
                    (
                        "ELECTRICITY_GAS_STEAM",
                        "Electricity, Gas, Steam and Air Conditioning Supply",
                    ),
                    (
                        "WATER_SUPPLY_WASTE_MANAGEMENT",
                        "Water Supply; Sewerage, Waste Management and Remediation Activities",
                    ),
                    ("CONSTRUCTION", "Construction"),
                    (
                        "WHOLESALE_RETAIL_TRADE",
                        "Wholesale and Retail Trade; Repair of Motor Vehicles and Motorcycles",
                    ),
                    ("TRANSPORTATION_STORAGE", "Transportation and Storage"),
                    (
                        "ACCOMMODATION_FOOD_SERVICE",
                        "Accommodation and Food Service Activities",
                    ),
                    ("INFORMATION_COMMUNICATION", "Information and Communication"),
                    (
                        "FINANCIAL_INSURANCE_ACTIVITIES",
                        "Financial and Insurance Activities",
                    ),
                    ("REAL_ESTATE_ACTIVITIES", "Real Estate Activities"),
                    (
                        "PROFESSIONAL_SCIENTIFIC_TECHNICAL",
                        "Professional, Scientific and Technical Activities",
                    ),
                    (
                        "ADMINISTRATIVE_SUPPORT_SERVICE",
                        "Administrative and Support Service Activities",
                    ),
                    (
                        "PUBLIC_ADMINISTRATION_DEFENCE",
                        "Public Administration and Defence; Compulsory Social Security",
                    ),
                    ("EDUCATION", "Education"),
                    (
                        "HUMAN_HEALTH_SOCIAL_WORK",
                        "Human Health and Social Work Activities",
                    ),
                    (
                        "ARTS_ENTERTAINMENT_RECREATION",
                        "Arts, Entertainment and Recreation",
                    ),
                    ("OTHER_SERVICE_ACTIVITIES", "Other Service Activities"),
                    (
                        "HOUSEHOLDS_AS_EMPLOYERS",
                        "Activities of Households as Employers; Undifferentiated Goods- and Services-Producing Activities of Households for Own Use",
                    ),
                    (
                        "EXTRATERRITORIAL_ORGANIZATIONS",
                        "Activities of Extraterritorial Organizations and Bodies",
                    ),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="sub_activity",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "01",
                        "Crop and animal production, hunting and related service activities",
                    ),
                    ("02", "Forestry and logging"),
                    ("03", "Fishing and aquaculture"),
                    ("05", "Mining of coal and lignite"),
                    ("06", "Extraction of crude petroleum and natural gas"),
                    ("07", "Mining of metal ores"),
                    ("08", "Other mining and quarrying"),
                    ("09", "Mining support service activities"),
                    ("10", "Manufacture of food products"),
                    ("11", "Manufacture of beverages"),
                    ("12", "Manufacture of tobacco products"),
                    ("13", "Manufacture of textiles"),
                    ("14", "Manufacture of wearing apparel"),
                    ("15", "Manufacture of leather and related products"),
                    (
                        "16",
                        "Manufacture of wood and of products of wood and cork, except furniture",
                    ),
                    ("17", "Manufacture of paper and paper products"),
                    ("18", "Printing and reproduction of recorded media"),
                    ("19", "Manufacture of coke and refined petroleum products"),
                    ("20", "Manufacture of chemicals and chemical products"),
                    (
                        "21",
                        "Manufacture of basic pharmaceutical products and pharmaceutical preparations",
                    ),
                    ("22", "Manufacture of rubber and plastic products"),
                    ("23", "Manufacture of other non-metallic mineral products"),
                    ("24", "Manufacture of basic metals"),
                    (
                        "25",
                        "Manufacture of fabricated metal products, except machinery and equipment",
                    ),
                    ("26", "Manufacture of computer, electronic and optical products"),
                    ("27", "Manufacture of electrical equipment"),
                    ("28", "Manufacture of machinery and equipment n.e.c."),
                    ("29", "Manufacture of motor vehicles, trailers and semi-trailers"),
                    ("30", "Manufacture of other transport equipment"),
                    ("31", "Manufacture of furniture"),
                    ("32", "Other manufacturing"),
                    ("33", "Repair and installation of machinery and equipment"),
                    ("35", "Electricity, gas, steam and air conditioning supply"),
                    ("36", "Water collection, treatment and supply"),
                    ("37", "Sewerage"),
                    (
                        "38",
                        "Waste collection, treatment and disposal activities; materials recovery",
                    ),
                    (
                        "39",
                        "Remediation activities and other waste management services",
                    ),
                    ("41", "Construction of buildings"),
                    ("42", "Civil engineering"),
                    ("43", "Specialized construction activities"),
                    (
                        "45",
                        "Wholesale and retail trade and repair of motor vehicles and motorcycles",
                    ),
                    ("46", "Wholesale trade, except of motor vehicles and motorcycles"),
                    ("47", "Retail trade, except of motor vehicles and motorcycles"),
                    ("49", "Land transport and transport via pipelines"),
                    ("50", "Water transport"),
                    ("51", "Air transport"),
                    ("52", "Warehousing and support activities for transportation"),
                    ("53", "Postal and courier activities"),
                    ("55", "Accommodation"),
                    ("56", "Food and beverage service activities"),
                    ("58", "Publishing activities"),
                    (
                        "59",
                        "Motion picture, video and television programme production, sound recording and music publishing activities",
                    ),
                    ("60", "Programming and broadcasting activities"),
                    ("61", "Telecommunications"),
                    ("62", "Computer programming, consultancy and related activities"),
                    ("63", "Information service activities"),
                    (
                        "64",
                        "Financial service activities, except insurance and pension funding",
                    ),
                    (
                        "65",
                        "Insurance, reinsurance and pension funding, except compulsory social security",
                    ),
                    (
                        "66",
                        "Activities auxiliary to financial services and insurance activities",
                    ),
                    ("68", "Real estate activities"),
                    ("69", "Legal and accounting activities"),
                    (
                        "70",
                        "Activities of head offices; management consultancy activities",
                    ),
                    (
                        "71",
                        "Architectural and engineering activities; technical testing and analysis",
                    ),
                    ("72", "Scientific research and development"),
                    ("73", "Advertising and market research"),
                    ("74", "Other professional, scientific and technical activities"),
                    ("75", "Veterinary activities"),
                    ("77", "Rental and leasing activities"),
                    ("78", "Employment activities"),
                    (
                        "79",
                        "Travel agency, tour operator and other reservation service and related activities",
                    ),
                    ("80", "Security and investigation activities"),
                    ("81", "Services to buildings and landscape activities"),
                    (
                        "82",
                        "Office administrative, office support and other business support activities",
                    ),
                    (
                        "84",
                        "Public administration and defence; compulsory social security",
                    ),
                    ("85", "Education"),
                    ("86", "Human health activities"),
                    ("87", "Residential care activities"),
                    ("88", "Social work activities without accommodation"),
                    ("90", "Creative, arts and entertainment activities"),
                    (
                        "91",
                        "Libraries, archives, museums and other cultural activities",
                    ),
                    ("92", "Gambling and betting activities"),
                    ("93", "Sports activities and amusement and recreation activities"),
                    ("94", "Activities of membership organizations"),
                    ("95", "Repair of computers and personal and household goods"),
                    ("96", "Other personal service activities"),
                    (
                        "97",
                        "Activities of households as employers of domestic personnel",
                    ),
                    (
                        "98",
                        "Undifferentiated goods- and services-producing activities of private households for own use",
                    ),
                    ("99", "Activities of extraterritorial organizations and bodies"),
                ],
                null=True,
            ),
        ),
    ]
