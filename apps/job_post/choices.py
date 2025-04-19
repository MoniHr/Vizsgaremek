from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

# TODO:remove
class IndustryChoices(TextChoices):
    ACCOUNTANCY = "ACCOUNTANCY", _("Accountancy & Finance")
    AGRICULTURE_ENVIRONMENT = "AGRICULTURE_ENVIRONMENT", _("Agriculture, Environment")
    APPRENTICESHIP = "APPRENTICESHIP", _("Apprenticeship, Internship")
    ARTS_ENTERTAINMENT = "ARTS_ENTERTAINMENT", _("Arts & Entertainment")
    BANK_INSURANCE_BROKER = "BANK_INSURANCE_BROKER", _("Bank, Insurance, Broker")
    CONSTRUCTION = "CONSTRUCTION", _("Construction & Building Industry")
    CUSTOMER_SERVICE = "CUSTOMER_SERVICE", _("Customer Relation, Customer Service")
    EDUCATION = "EDUCATION", _("Education")
    ENERGY = "ENERGY", _("Energy")
    ENGINEERING = "ENGINEERING", _("Engineering")
    HEALTHCARE = "HEALTHCARE", _("Healthcare")
    HOSPITALITY = "HOSPITALITY", _("Hospitality & Tourism")
    HUMAN_RESOURCES = "HUMAN_RESOURCES", _("Human Resources & Labor Case")
    IT_AND_TELCO = "IT_AND_TELCO", _("IT & Telecom")
    LEGAL = "LEGAL", _("Law & Legal Cases")
    LOGISTICS = "LOGISTICS", _("Logistics, Duty, Customs Clearance")
    MANUFACTURING = "MANUFACTURING", _("Manufacturing")
    MARKETING = "MARKETING", _("Marketing, PR, Advertisement")
    MEDIA = "MEDIA", _("Media")
    NONPROFIT = "NONPROFIT", _("Nonprofit")
    PROJECT_MANAGEMENT = "PROJECT_MANAGEMENT", _("Project Management")
    PUBLIC_ADMINISTRATION = "PUBLIC_ADMINISTRATION", _("Office Jobs, Administration")
    PUBLIC_RELATIONS = "PUBLIC_RELATIONS", _("Public Relations")
    REAL_ESTATE = "REAL_ESTATE", _("Real Estate")
    RETAIL = "RETAIL", _("Retail")
    SALES = "SALES", _("Sales, Trade, Commerce, Economics")
    SCIENCE_RESEARCH = "SCIENCE_RESEARCH", _("Science & Research")
    SECURITY = "SECURITY", _("Security")
    SPORT = "SPORT", _("Sport")
    SUPPLY_CHAIN = "SUPPLY_CHAIN", _("Supply Chain & Logistics")
    TECHNOLOGY = "TECHNOLOGY", _("Technology")
    TRAINED_UNSKILLED_WORKERS = "TRAINED_UNSKILLED_WORKERS", _("Trained or Unskilled Jobs")
    TRANSPORTATION = "TRANSPORTATION", _("Transportation")
    WAREHOUSE = "WAREHOUSE", _("Warehouse")

class SubIndustryChoices(TextChoices):
    # Agriculture, Environment
    ADMINISTRATION = "ADMINISTRATION", _("Administration, Administrator")
    FACTORY_WORKER = "FACTORY_WORKER", _("Factory Worker")
    WASTE_MANAGEMENT = "WASTE_MANAGEMENT", _("Waste Management")
    ENVIRONMENTAL_PROTECTION = "ENVIRONMENTAL_PROTECTION", _("Environmental Protection")
    ENVIRONMENTAL_SUSTAINABILITY = "ENVIRONMENTAL_SUSTAINABILITY", _("Environmental Sustainability")
    PROFESSIONAL_CONSULTANT = "PROFESSIONAL_CONSULTANT", _("Professional Consultant")
    FARM_HELP = "FARM_HELP", _("Farm Help")
    GROWING_PLANTS = "GROWING_PLANTS", _("Growing Plants")
    FRUIT_VEGETABLE_PICKING = "FRUIT_VEGETABLE_PICKING", _("Fruits and Vegetables Picking, Harvesting")
    PRODUCTION = "PRODUCTION", _("Production, Product Management")
    COMPONENT_EQUIPMENT_RESOURCES = "COMPONENT_EQUIPMENT_RESOURCES", _("Component, Equipment Resources")
    COMPONENT_EQUIPMENT_WAREHOUSE = "COMPONENT_EQUIPMENT_WAREHOUSE", _("Component and Equipment Warehouse, Delivery")
    PRODUCT_MANAGEMENT = "PRODUCT_MANAGEMENT", _("Product Management, Assistant")
    SALES = "SALES", _("Sales, Seller, Agricultural Sales Person")
    ENGINEER = "ENGINEER", _("Engineer, Food Engineer")
    MECHANICAL_ENGINEER = "MECHANICAL_ENGINEER", _("Mechanical Engineer")
    QUALITY_CONTROL = "QUALITY_CONTROL", _("Quality, Quality Control")
    TECHNICIAN = "TECHNICIAN", _("Technician, Experimental Technician, Consultant")
    COMMERCIAL_COORDINATOR = "COMMERCIAL_COORDINATOR", _("Commercial Coordinator, Sales")
    REGIONAL_REPRESENTATIVE = "REGIONAL_REPRESENTATIVE", _("Regional Representative")
    LAB = "LAB", _("Lab, Labor")
    NATURE_CONSERVATION = "NATURE_CONSERVATION", _("Nature Conservation Officer")
    FOREST_MANAGEMENT = "FOREST_MANAGEMENT", _("Forest Management, Forestry")
    PLANT_ANIMAL_PROTECTION = "PLANT_ANIMAL_PROTECTION", _("Plant and Animal Protection, Agronomist")
    VETERINARIAN = "VETERINARIAN", _("Veterinarian")
    HERBALIST = "HERBALIST", _("Herbalist")
    SITE_MANAGER = "SITE_MANAGER", _("Site Manager")
    FORKLIFT_DRIVER = "FORKLIFT_DRIVER", _("Forklift Driver")
    SEED_PLANT_STOREKEEPER = "SEED_PLANT_STOREKEEPER", _("Seed Plant, Storekeeper, Shift Manager")

    # Banking, Insurance, Broker
    BANK_INSURANCE_MANAGEMENT = "BANK_INSURANCE_MANAGEMENT", _("Bank and Insurance Management")
    INVESTMENT_ANALYST = "INVESTMENT_ANALYST", _("Investment, Investment Analyst")
    ANALYST = "ANALYST", _("Analyst")
    DATA_MINER = "DATA_MINER", _("Data Miner, Database Manager, SQL")
    SAP = "SAP", _("SAP")
    ACCOUNT = "ACCOUNT", _("Account, Account Management, Manager")
    BANK_CARD_MANAGEMENT = "BANK_CARD_MANAGEMENT", _("Bank Card Management")
    CREDIT_CONTROL = "CREDIT_CONTROL", _("Credit, Credit Control")
    UNIVERSAL_CONSULTANT = "UNIVERSAL_CONSULTANT", _("Universal Consultant")
    PROPERTY_LIABILITY_INSURANCE = "PROPERTY_LIABILITY_INSURANCE", _("Property and Liability Insurance")
    INSURANCE = "INSURANCE", _("Insurance")
    PRODUCT_SPECIALIST = "PRODUCT_SPECIALIST", _("Product Specialist, Product Manager, Product Development Manager")
    CORPORATE_CUSTOMER_CONTACT = "CORPORATE_CUSTOMER_CONTACT", _("Corporate Customer Contact")
    PROCESS_SPECIALIST = "PROCESS_SPECIALIST", _("Process Specialist, Process Development")
    COACH_AGILE_TEAM_LEADER = "COACH_AGILE_TEAM_LEADER", _("Coach, Agile Team Leader")
    BANK_INSURANCE_INFORMATICS = "BANK_INSURANCE_INFORMATICS", _("Bank and Insurance Informatics, Programmer")
    WEBDESIGN = "WEBDESIGN", _("Web Design, Web Developer")
    THREE_D_DEVELOPMENT = "THREE_D_DEVELOPMENT", _("3D Development")
    CREDIT_RISK = "CREDIT_RISK", _("Credit Risk, Risk Controller")
    CONSULTANT = "CONSULTANT", _("Consultant")
    CUSTOMER_REPRESENTATIVE = "CUSTOMER_REPRESENTATIVE", _("Customer Representative, CRM, CSS")
    ADMINISTRATION_OFFICE_JOB = "ADMINISTRATION_OFFICE_JOB", _("Administration, Office Job, Office Assistant")
    TELEPHONE_CLERK = "TELEPHONE_CLERK", _("Telephone Clerk, Telephone Salesperson")
    CASHIER = "CASHIER", _("Cashier, Changer, Money Change")
    FINANCIAL_ADVISOR = "FINANCIAL_ADVISOR", _("Financial Advisor")
    COMPLIANCE = "COMPLIANCE", _("Compliance, Complaint Clerk")
    REGIONAL_REPRESENTATIVE_BANK = "REGIONAL_REPRESENTATIVE_BANK", _("Regional Representative")
    BUSINESS_MANAGER = "BUSINESS_MANAGER", _("Business Manager")
    RECEPTIONIST = "RECEPTIONIST", _("Receptionist")
    SECURITY = "SECURITY", _("Security")
    LOGISTICS = "LOGISTICS", _("Logistics, Transport, Delivery")
    SMALL_BUSINESS_CONSULTANT = "SMALL_BUSINESS_CONSULTANT", _("Small Business Consultant, Salesperson")
    MEDIUM_SIZED_BUSINESS_CONSULTANT = "MEDIUM_SIZED_BUSINESS_CONSULTANT", _("Medium-Sized Company, Business Consultant, Salesperson")
    LARGE_CORPORATE_SALES = "LARGE_CORPORATE_SALES", _("Large Corporate Business Consultant, Salesperson")
    CLAIMS_ADJUSTER = "CLAIMS_ADJUSTER", _("Claims Adjuster")
    MONEY_LAUNDERING_PREVENTION = "MONEY_LAUNDERING_PREVENTION", _("Money Laundering Prevention, Officer")
    BROKER = "BROKER", _("Broker")

    # Technology
    CSHARP = "CSHARP", _("C#")
    JAVA = "JAVA", _("Java")

    # Construction
    CONSTRUCTION_ENGINEER = "CONSTRUCTION_ENGINEER", _("Construction Engineer")

__SubIndustryChoicesByIndustry = {
    IndustryChoices.ENGINEERING: {
        SubIndustryChoices.CSHARP,
        SubIndustryChoices.JAVA
    },
    IndustryChoices.CONSTRUCTION: {
        SubIndustryChoices.CONSTRUCTION_ENGINEER
    },
    IndustryChoices.AGRICULTURE_ENVIRONMENT: {
        SubIndustryChoices.ADMINISTRATION,
        SubIndustryChoices.FACTORY_WORKER,
        SubIndustryChoices.WASTE_MANAGEMENT,
        SubIndustryChoices.ENVIRONMENTAL_PROTECTION,
        SubIndustryChoices.ENVIRONMENTAL_SUSTAINABILITY,
        SubIndustryChoices.PROFESSIONAL_CONSULTANT,
        SubIndustryChoices.FARM_HELP,
        SubIndustryChoices.GROWING_PLANTS,
        SubIndustryChoices.FRUIT_VEGETABLE_PICKING,
        SubIndustryChoices.PRODUCTION,
        SubIndustryChoices.COMPONENT_EQUIPMENT_RESOURCES,
        SubIndustryChoices.COMPONENT_EQUIPMENT_WAREHOUSE,
        SubIndustryChoices.PRODUCT_MANAGEMENT,
        SubIndustryChoices.SALES,
        SubIndustryChoices.ENGINEER,
        SubIndustryChoices.MECHANICAL_ENGINEER,
        SubIndustryChoices.QUALITY_CONTROL,
        SubIndustryChoices.TECHNICIAN,
        SubIndustryChoices.COMMERCIAL_COORDINATOR,
        SubIndustryChoices.REGIONAL_REPRESENTATIVE,
        SubIndustryChoices.LAB,
        SubIndustryChoices.NATURE_CONSERVATION,
        SubIndustryChoices.FOREST_MANAGEMENT,
        SubIndustryChoices.PLANT_ANIMAL_PROTECTION,
        SubIndustryChoices.VETERINARIAN,
        SubIndustryChoices.HERBALIST,
        SubIndustryChoices.SITE_MANAGER,
        SubIndustryChoices.FORKLIFT_DRIVER,
        SubIndustryChoices.SEED_PLANT_STOREKEEPER
    },
    IndustryChoices.BANK_INSURANCE_BROKER: {
        SubIndustryChoices.BANK_INSURANCE_MANAGEMENT,
        SubIndustryChoices.INVESTMENT_ANALYST,
        SubIndustryChoices.ANALYST,
        SubIndustryChoices.DATA_MINER,
        SubIndustryChoices.SAP,
        SubIndustryChoices.ACCOUNT,
        SubIndustryChoices.BANK_CARD_MANAGEMENT,
        SubIndustryChoices.CREDIT_CONTROL,
        SubIndustryChoices.UNIVERSAL_CONSULTANT,
        SubIndustryChoices.PROPERTY_LIABILITY_INSURANCE,
        SubIndustryChoices.INSURANCE,
        SubIndustryChoices.PRODUCT_SPECIALIST,
        SubIndustryChoices.CORPORATE_CUSTOMER_CONTACT,
        SubIndustryChoices.PROCESS_SPECIALIST,
        SubIndustryChoices.COACH_AGILE_TEAM_LEADER,
        SubIndustryChoices.BANK_INSURANCE_INFORMATICS,
        SubIndustryChoices.WEBDESIGN,
        SubIndustryChoices.THREE_D_DEVELOPMENT,
        SubIndustryChoices.CREDIT_RISK,
        SubIndustryChoices.CONSULTANT,
        SubIndustryChoices.CUSTOMER_REPRESENTATIVE,
        SubIndustryChoices.ADMINISTRATION_OFFICE_JOB,
        SubIndustryChoices.TELEPHONE_CLERK,
        SubIndustryChoices.CASHIER,
        SubIndustryChoices.FINANCIAL_ADVISOR,
        SubIndustryChoices.COMPLIANCE,
        SubIndustryChoices.REGIONAL_REPRESENTATIVE_BANK,
        SubIndustryChoices.BUSINESS_MANAGER,
        SubIndustryChoices.RECEPTIONIST,
        SubIndustryChoices.SECURITY,
        SubIndustryChoices.LOGISTICS,
        SubIndustryChoices.SMALL_BUSINESS_CONSULTANT,
        SubIndustryChoices.MEDIUM_SIZED_BUSINESS_CONSULTANT,
        SubIndustryChoices.LARGE_CORPORATE_SALES,
        SubIndustryChoices.CLAIMS_ADJUSTER,
        SubIndustryChoices.MONEY_LAUNDERING_PREVENTION,
        SubIndustryChoices.BROKER
    }
}





SubIndustryChoicesByIndustry = {}
for key, value in __SubIndustryChoicesByIndustry.items():
    SubIndustryChoicesByIndustry[key.name] = []
    for item in value:
        SubIndustryChoicesByIndustry[key.name].append(
            {
                "value": item.name,
                "label": item.label,
            }
        )
