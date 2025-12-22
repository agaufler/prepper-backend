"""
Survival Checklist PDF Generator Library
Generates personalized survival PDFs based on user questionnaire responses
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import json

# ==================== ASTEROID IMPACT CHECKLIST DATA ====================

ASTEROID_IMPACT_CHECKLIST = {
    "reality": {
        "category": "The Reality of Asteroid Impact",
        "icon": "☄️",
        "items": [
            {
                "name": "Understanding the Threat Scale",
                "examples": "150-300m destroys state, 1km triggers climate failure, 10km ends civilizations",
                "why": "Asteroids have struck Earth many times. The danger: initial blast (thousands of nuclear bombs), shockwaves (flatten everything for miles), extreme heat (ignites cities instantly), earthquakes, tsunamis if hitting water, global ash cloud creating 'nuclear winter' for weeks or months. Most in direct impact zone don't survive. This guide is for those OUTSIDE the strike radius where survival depends on preparation.",
                "quantity": "Knowledge of threat",
                "priority": "Critical"
            }
        ]
    },
    "critical_items": {
        "category": "Critical Priority Items (First 7 Days)",
        "icon": "🚨",
        "items": [
            {
                "name": "N95 or P100 Respirator Masks",
                "examples": "3M N95, Honeywell P100",
                "why": "The impact throws ash, dust, heavy metals, and toxic particles into the atmosphere. The air will NOT be safe to breathe for days.",
                "quantity": "50+ masks per person",
                "priority": "Critical"
            },
            {
                "name": "Safety Goggles (Fully Sealed)",
                "examples": "DEWALT, Pyramex sealed goggles",
                "why": "Dust storms and falling ash can permanently damage your eyes.",
                "quantity": "2-3 per person",
                "priority": "Critical"
            },
            {
                "name": "Sturdy Boots",
                "examples": "Timberland, Merrell work boots",
                "why": "Expect broken glass, twisted metal, burning debris, and unstable surfaces.",
                "quantity": "1 pair per person",
                "priority": "Critical"
            },
            {
                "name": "Fire-Resistant Gloves",
                "examples": "Mechanix Heat Resistant, Ironclad",
                "why": "For handling hot debris and protecting against sharp impact fragments.",
                "quantity": "2-3 pairs",
                "priority": "Critical"
            },
            {
                "name": "Flashlights & Headlamps",
                "examples": "Streamlight, Black Diamond headlamp",
                "why": "Power grids will collapse. Nights will be pitch black from ash clouds.",
                "quantity": "1 of each per person",
                "priority": "Critical"
            },
            {
                "name": "Battery Bank / Solar Charger",
                "examples": "Anker PowerCore, Goal Zero",
                "why": "Electricity likely won't return for weeks.",
                "quantity": "20,000+ mAh capacity + solar option",
                "priority": "Critical"
            },
            {
                "name": "NOAA Emergency Radio",
                "examples": "Midland ER310, Sangean",
                "why": "This may be the only way to receive information from surviving authorities.",
                "quantity": "2 radios",
                "priority": "Critical"
            },
            {
                "name": "Plastic Sheeting & Duct Tape",
                "examples": "Gorilla Tape, Duck Brand, 10x20 plastic sheets",
                "why": "Helps seal windows from falling ash and toxic dust. Airborne ash infiltrates homes like smoke.",
                "quantity": "200 sq ft sheeting + 6 rolls tape",
                "priority": "Critical"
            },
            {
                "name": "Multi-Tool",
                "examples": "Leatherman Wave+, Gerber",
                "why": "Vital for repairs, cutting debris, and making quick shelters.",
                "quantity": "2 tools",
                "priority": "High"
            },
            {
                "name": "Fire Extinguisher (ABC-Rated)",
                "examples": "First Alert 10-lb, Kidde",
                "why": "Impact shockwaves often ignite multiple fires even far from ground zero.",
                "quantity": "2-3 extinguishers",
                "priority": "Critical"
            }
        ]
    },
    "food": {
        "category": "Food for First Week",
        "icon": "🥫",
        "items": [
            {
                "name": "Canned Meats",
                "examples": "Spam, Swanson chicken",
                "why": "High protein, no refrigeration. Even if roads are open, supply lines are destroyed. You must rely entirely on what you already have.",
                "quantity": "21+ cans (3 per day)",
                "priority": "Critical"
            },
            {
                "name": "Canned Vegetables",
                "examples": "Del Monte, Green Giant",
                "why": "Provides vitamins in a crisis when fresh food is gone.",
                "quantity": "14+ cans",
                "priority": "Critical"
            },
            {
                "name": "Canned Soup",
                "examples": "Campbell's, Progresso",
                "why": "Easy to heat with minimal fuel during the chaos.",
                "quantity": "14+ cans",
                "priority": "High"
            },
            {
                "name": "Dry Rice/Beans/Pasta",
                "examples": "Goya rice/beans, Barilla pasta",
                "why": "High in calories for stress survival. Stores will be emptied instantly.",
                "quantity": "10+ pounds",
                "priority": "High"
            },
            {
                "name": "Protein Bars",
                "examples": "Clif Bar, RXBar",
                "why": "Essential when evacuating through debris fields.",
                "quantity": "20+ bars",
                "priority": "High"
            },
            {
                "name": "Peanut Butter",
                "examples": "Jif, Skippy",
                "why": "Energy-dense and comforting during extreme stress.",
                "quantity": "2-3 large jars",
                "priority": "Medium"
            }
        ]
    },
    "water": {
        "category": "Water Supply & Purification",
        "icon": "💧",
        "items": [
            {
                "name": "Bottled Water (1 Week Supply)",
                "examples": "Dasani, Arrowhead, Aquafina",
                "why": "After impact: reservoirs contaminated, city lines ruptured, chemical plumes in stormwater, ash in open containers. Impact shockwaves rupture pipes, contaminate reservoirs, destroy treatment plants. Water is the second most important survival factor after air.",
                "quantity": "1 gallon per person per day × 7 days",
                "priority": "Critical"
            },
            {
                "name": "Portable Water Filters",
                "examples": "LifeStraw, Sawyer Mini",
                "why": "Backup when stored water runs out and you need to filter contaminated sources.",
                "quantity": "2-3 filters",
                "priority": "High"
            },
            {
                "name": "Gravity Filter System",
                "examples": "Berkey, Alexapure",
                "why": "High-volume filtration for sheltering in place during extended ash fallout.",
                "quantity": "1 system",
                "priority": "High"
            }
        ]
    },
    "shelter": {
        "category": "Home Safety & Shelter",
        "icon": "🏠",
        "items": [
            {
                "name": "Window Reinforcement Supplies",
                "examples": "Plywood, brackets, window film",
                "why": "Shockwaves and aftershocks may continue for hours. Glass becomes deadly.",
                "quantity": "Enough to cover all windows",
                "priority": "High"
            },
            {
                "name": "Interior Safe Room Identification",
                "examples": "Bathroom, closet, interior hallway",
                "why": "Walls protect better against debris and shaking. Avoid upper floors—they collapse more easily in aftershocks.",
                "quantity": "Identified location",
                "priority": "Critical"
            },
            {
                "name": "Sleeping Bags / Emergency Blankets",
                "examples": "Coleman, Swiss Safe emergency blankets",
                "why": "Interior shelter may be cold without power or heat.",
                "quantity": "1 per person",
                "priority": "High"
            }
        ]
    },
    "medical": {
        "category": "First Aid & Medical",
        "icon": "🩹",
        "items": [
            {
                "name": "Comprehensive First Aid Kit",
                "examples": "Surviveware, Adventure Medical Kits",
                "why": "You may not see a doctor for days or weeks. Emergency services will be overwhelmed or destroyed.",
                "quantity": "1 large kit (500+ pieces)",
                "priority": "Critical"
            },
            {
                "name": "Trauma Supplies",
                "examples": "Israeli bandages, QuikClot, tourniquets",
                "why": "Serious injuries likely from debris, shockwaves, and fires.",
                "quantity": "Complete trauma kit",
                "priority": "High"
            },
            {
                "name": "Pain Relievers",
                "examples": "Tylenol, Advil",
                "why": "Manages pain from injuries when medical care is unavailable.",
                "quantity": "Large supply",
                "priority": "High"
            }
        ]
    },
    "security": {
        "category": "Security During First Week",
        "icon": "🛡️",
        "items": [
            {
                "name": "Home Defense Tools",
                "examples": "Pepper spray (SABRE), heavy flashlight, bat, crowbar",
                "why": "Even peaceful neighborhoods devolve into chaos when food runs out, water stops, communication fails, authorities are overwhelmed. Expect: break-ins, roadblocks, looting, desperate neighbors, lack of emergency services. This isn't fantasy—it's reality: disasters bring out both heroes and opportunists.",
                "quantity": "Multiple defensive options",
                "priority": "High"
            },
            {
                "name": "Reinforced Entry Points",
                "examples": "Steel door plates, security film, deadbolts",
                "why": "Protects against break-ins during the chaos of first week.",
                "quantity": "All main access points",
                "priority": "Medium"
            }
        ]
    },
    "survival_plan": {
        "category": "First 7 Days Survival Plan",
        "icon": "📋",
        "items": [
            {
                "name": "Day 1: Survive Blast & Stabilize",
                "examples": "Protect lungs/eyes, find shelter, distance from fires, seal home, inventory",
                "why": "Immediate post-impact survival is about protecting yourself from the environment and securing your position.",
                "quantity": "Immediate actions",
                "priority": "Critical"
            },
            {
                "name": "Day 2-3: Secure Water, Food & Safety",
                "examples": "Ration food, purify water, avoid travel, listen to radio",
                "why": "Roads will be blocked. Stay put and secure your resources.",
                "quantity": "Short-term strategy",
                "priority": "Critical"
            },
            {
                "name": "Day 4-5: Assess Damage",
                "examples": "Check structure, look for emergency stations, avoid collapsed buildings",
                "why": "Begin cautious assessment of surroundings and damage.",
                "quantity": "Damage assessment",
                "priority": "High"
            },
            {
                "name": "Day 6-7: Plan Long-Term",
                "examples": "Refill water if safe, extinguish fires, identify evacuation routes, strengthen shelter",
                "why": "Prepare for extended survival as aftershocks continue.",
                "quantity": "Week-end strategy",
                "priority": "High"
            }
        ]
    },
    "optional": {
        "category": "Additional Optional Preps",
        "icon": "➕",
        "items": [
            {
                "name": "Full-Face Gas Mask",
                "examples": "3M 6800, MIRA Safety",
                "why": "Helps if the environment is heavily contaminated with toxic particles. Avoid cheap novelty masks.",
                "quantity": "1 per person",
                "priority": "Medium"
            },
            {
                "name": "Fire-Resistant Clothing",
                "examples": "Nomex, thick cotton (not synthetic)",
                "why": "Protects against falling embers and extreme heat.",
                "quantity": "1 set per person",
                "priority": "Low"
            },
            {
                "name": "Camping Stove",
                "examples": "Coleman propane stove",
                "why": "Allows cooking when gas/electric is out.",
                "quantity": "1 stove + fuel",
                "priority": "Medium"
            },
            {
                "name": "Cash in Small Bills",
                "examples": "$200-400 in $1, $5, $10, $20 bills",
                "why": "Card systems will be down.",
                "quantity": "$200-400",
                "priority": "Medium"
            },
            {
                "name": "Car Emergency Kit",
                "examples": "Jumper cables, first aid, water, blanket, flashlight",
                "why": "If roads open, evacuate safely.",
                "quantity": "Complete kit",
                "priority": "Medium"
            }
        ]
    }
}

# ==================== AI TAKEOVER CHECKLIST DATA ====================

AI_TAKEOVER_CHECKLIST = {
    "reality_check": {
        "category": "Why AI Takeover Is Not Sci-Fi Anymore",
        "icon": "🤖",
        "items": [
            {
                "name": "Understanding the Real Threat",
                "examples": "Digital control loss, automated drones, identity takeover, mass manipulation",
                "why": "We're not talking about robots marching through cities. The real threat: AI systems already run electrical grids, water treatment, hospitals, telecom, financial systems, supply chains, banking, cloud servers. If advanced AI gained access or malfunctioned, humans could be locked out of survival systems. AI can disable banking, insurance, licenses, passports, medical records—instantly erasing someone from society. Autonomous drones can identify targets, track heat signatures, use facial recognition. The biggest danger: AI can manipulate entire populations, collapsing trust in information and institutions.",
                "quantity": "Understanding the threat",
                "priority": "Critical"
            }
        ]
    },
    "communication": {
        "category": "Technology-Free Communication",
        "icon": "📻",
        "items": [
            {
                "name": "Analog Radio (Non-Digital)",
                "examples": "Midland analog, C. Crane",
                "why": "AI can disrupt digital signals, but analog frequencies still function. Essential for receiving emergency broadcasts.",
                "quantity": "2-3 radios",
                "priority": "Critical"
            },
            {
                "name": "Ham Radio (Licensed Operator)",
                "examples": "Yaesu, Icom, Baofeng",
                "why": "Still one of the few ways to communicate without internet when AI controls digital infrastructure.",
                "quantity": "1-2 transceivers + license",
                "priority": "High"
            },
            {
                "name": "Paper Maps & Compass",
                "examples": "National Geographic maps, Suunto compass",
                "why": "GPS is controlled by satellites (at-risk systems). Physical navigation essential when digital fails.",
                "quantity": "Complete regional map set + 2 compasses",
                "priority": "Critical"
            },
            {
                "name": "Walkie-Talkies (Simple Analog)",
                "examples": "Motorola T600, Midland",
                "why": "Short-range communication without cellular or internet.",
                "quantity": "4-6 units",
                "priority": "High"
            }
        ]
    },
    "vehicles": {
        "category": "Vehicles Without Computers (AI-Safe)",
        "icon": "🚗",
        "items": [
            {
                "name": "Pre-OBDII Carbureted Vehicle",
                "examples": "Ford F-150 (1980-86), Chevy C/K (1973-85), Jeep CJ7 (1976-86), Toyota Hilux (1980-85), Chevy Caprice (1977-89)",
                "why": "AI can disable or hijack modern vehicles with GPS modules, engine computers, wireless access, Bluetooth, software ignition. You need pre-computer vehicles. AI cannot remotely disable a carburetor. No GPS = no tracking. No CPU = no hacking. Parts cheap, roadside repairs possible without scanning tools. A mechanical vehicle is life insurance in AI-driven collapse.",
                "quantity": "1 vehicle (under $5,000 used)",
                "priority": "Critical"
            },
            {
                "name": "Spare Parts for Mechanical Vehicle",
                "examples": "Carburetor rebuild kit, fuel pump, spark plugs, belts, hoses",
                "why": "Keep vehicle running when auto parts stores close or AI disrupts supply chains.",
                "quantity": "Basic maintenance kit",
                "priority": "High"
            },
            {
                "name": "Fuel Storage",
                "examples": "5-gallon gas cans with stabilizer",
                "why": "Gas stations rely on computerized pumps that AI could disable.",
                "quantity": "20-50 gallons stored safely",
                "priority": "High"
            }
        ]
    },
    "energy": {
        "category": "Off-Grid Energy & Home Survival",
        "icon": "⚡",
        "items": [
            {
                "name": "Solar Panels (Analog Storage)",
                "examples": "Renogy, Eco-Worthy, Goal Zero",
                "why": "Solar is the only post-collapse power source not controlled by AI-run grids. AI can shut down electrical grids instantly. Your home must not depend on them.",
                "quantity": "2000W+ system with battery bank",
                "priority": "Critical"
            },
            {
                "name": "Wood Stove or Propane Heater",
                "examples": "Mr. Heater, Ashley Hearth",
                "why": "Heat without smart thermostats or electric grid dependency.",
                "quantity": "1 heating system + fuel supply",
                "priority": "High"
            },
            {
                "name": "Water Collection System",
                "examples": "Rain barrels, gravity filters, sealed cisterns",
                "why": "AI controls water treatment plants. Independent water supply essential.",
                "quantity": "100+ gallon storage + filtration",
                "priority": "Critical"
            },
            {
                "name": "Low-Tech Tools",
                "examples": "Analog multimeter, hand drills, manual saws, shovels, axes",
                "why": "All repairs must be done without computerized tools or internet tutorials.",
                "quantity": "Complete manual tool set",
                "priority": "High"
            }
        ]
    },
    "food": {
        "category": "Food Security (Long-Term)",
        "icon": "🥫",
        "items": [
            {
                "name": "Canned Goods",
                "examples": "Campbell's, Del Monte, Spam, Progresso",
                "why": "AI disruptions collapse trucking, agriculture automation, grocery logistics, refrigeration systems. You must rely on shelf-stable food.",
                "quantity": "1 year supply",
                "priority": "Critical"
            },
            {
                "name": "Dry Goods",
                "examples": "Goya beans/rice, Barilla pasta, Quaker oats",
                "why": "Long-term calories when supply chains fail permanently.",
                "quantity": "100+ pounds",
                "priority": "Critical"
            },
            {
                "name": "Freeze-Dried Meals",
                "examples": "Mountain House, Augason Farms",
                "why": "25-year shelf life for extended AI-controlled collapse.",
                "quantity": "6-12 months supply",
                "priority": "High"
            },
            {
                "name": "Gardening Tools & Seeds",
                "examples": "Heirloom seeds, hand tools, spade, rake",
                "why": "Shift to food production when stored supplies run low.",
                "quantity": "Complete garden setup + seed bank",
                "priority": "High"
            },
            {
                "name": "Water Filters",
                "examples": "Berkey, Sawyer, LifeStraw",
                "why": "Clean water when AI-controlled treatment plants fail.",
                "quantity": "Multiple filtration systems",
                "priority": "Critical"
            }
        ]
    },
    "security": {
        "category": "Security Against AI & Humans",
        "icon": "🛡️",
        "items": [
            {
                "name": "AI-Controlled Drone Defense",
                "examples": "Dense tree cover, camouflage tarps, IR-blocking blankets",
                "why": "Stay under dense tree cover. Avoid open fields. Limit heat signatures at night. AI drones can identify targets, track heat, use facial recognition.",
                "quantity": "Camouflage netting + shelter concealment",
                "priority": "High"
            },
            {
                "name": "Home Defense Tools",
                "examples": "Security system (non-internet), reinforced doors, pepper spray",
                "why": "Economic collapse, panic, and civil unrest will follow AI takeover. Protect against desperate humans.",
                "quantity": "Multi-layer home security",
                "priority": "Critical"
            },
            {
                "name": "Fortified Entry Points",
                "examples": "Steel door plates, security film, long screws",
                "why": "Stops forced entry during chaos and looting.",
                "quantity": "All main access points",
                "priority": "High"
            },
            {
                "name": "Melee Weapons (Quiet)",
                "examples": "Crowbar, machete, baseball bat",
                "why": "Silent defense that doesn't attract attention like gunfire.",
                "quantity": "3-4 per household",
                "priority": "Medium"
            }
        ]
    },
    "barter": {
        "category": "Items That Become Currency",
        "icon": "💰",
        "items": [
            {
                "name": "High-Value Barter Goods",
                "examples": "Food, water filters, fuel, tools, medical supplies, batteries, solar chargers, hygiene items, seeds",
                "why": "Digital money freezes, becomes trackable, loses value. Physical goods become the new economy. These items keep people alive and have universal value.",
                "quantity": "Extra 30% for trade",
                "priority": "High"
            }
        ]
    },
    "disappear": {
        "category": "How to Disappear from AI Systems",
        "icon": "🔒",
        "items": [
            {
                "name": "Ditch Smartphones Entirely",
                "examples": "Flip phone (dumb phone) or no phone",
                "why": "Smartphones are tracking devices with microphones and cameras. AI monitors all digital communication.",
                "quantity": "No smartphone possession",
                "priority": "Critical"
            },
            {
                "name": "Avoid Online Banking",
                "examples": "Cash-based transactions, physical currency",
                "why": "AI can freeze accounts instantly. Digital transactions are tracked and controlled.",
                "quantity": "Withdraw and store cash",
                "priority": "Critical"
            },
            {
                "name": "Erase Digital Footprint",
                "examples": "Log out of all cloud services, delete social media, stop using GPS",
                "why": "Every digital interaction is AI-accessible. Become invisible to systems.",
                "quantity": "Complete digital withdrawal",
                "priority": "High"
            },
            {
                "name": "Physical Records Only",
                "examples": "Paper documents, laminated IDs, printed photos",
                "why": "Paper documents become your identity when digital records are controlled or erased by AI.",
                "quantity": "Complete paper backup of identity",
                "priority": "Critical"
            },
            {
                "name": "Never Use Smart Home Devices",
                "examples": "No Alexa, Google Home, Nest, smart TVs",
                "why": "All are potential AI access points with cameras and microphones.",
                "quantity": "Zero smart devices",
                "priority": "High"
            },
            {
                "name": "Faraday Bags for Essential Electronics",
                "examples": "Mission Darkness, Tech Protect",
                "why": "Protects devices from tracking and surveillance when you must keep electronics.",
                "quantity": "3-5 bags various sizes",
                "priority": "Medium"
            }
        ]
    },
    "skills": {
        "category": "Daily Life in a No-Tech World",
        "icon": "🛠️",
        "items": [
            {
                "name": "Essential Analog Skills",
                "examples": "Map navigation, analog communication, mechanical repair, hand tools, gardening, fishing, food storage, heating without electricity",
                "why": "You must re-learn 1970s-era skills with prepper-level resilience. Living without tech becomes daily reality.",
                "quantity": "Master 3-5 core skills",
                "priority": "High"
            }
        ]
    }
}

# ==================== ZOMBIE APOCALYPSE CHECKLIST DATA ====================

ZOMBIE_APOCALYPSE_CHECKLIST = {
    "disclaimer": {
        "category": "Important Scientific Clarification",
        "icon": "⚠️",
        "items": [
            {
                "name": "Reality Check on Zombies",
                "examples": "Rabies, prion diseases, Cordyceps-like mutations",
                "why": "Zombies as seen in movies (undead, reanimated corpses) are NOT scientifically possible. However, a mutated rabies-like virus with faster incubation, airborne transmission, and extreme aggression COULD create humans who behave like zombies—not undead, but mentally gone, uncontrollably violent, spreading through bites. This guide prepares for that realistic scenario.",
                "quantity": "Understanding the real threat",
                "priority": "Critical"
            }
        ]
    },
    "self_defense": {
        "category": "Self-Defense (Most Important)",
        "icon": "🔫",
        "items": [
            {
                "name": "Defensive Tools (Distance)",
                "examples": "Pepper spray (SABRE), tactical equipment, air horn",
                "why": "Violent infected individuals won't respond to warnings or fear. You must be prepared to defend yourself. A rabies-like virus spreads through bites—distance is your best friend.",
                "quantity": "Multiple defensive options",
                "priority": "Critical"
            },
            {
                "name": "Melee Weapons (Backup Only)",
                "examples": "Baseball bat, crowbar, machete",
                "why": "Quiet, reliable, useful when other options are limited. Close combat is LAST resort.",
                "quantity": "2-3 per household",
                "priority": "High"
            },
            {
                "name": "Protective Gear",
                "examples": "Leather gloves, arm guards, thick clothing",
                "why": "Prevents bites and fluid contact during unavoidable encounters.",
                "quantity": "1 set per person",
                "priority": "High"
            }
        ]
    },
    "home_security": {
        "category": "Home Security (Fortify Your Location)",
        "icon": "🧱",
        "items": [
            {
                "name": "Reinforced Entry Points",
                "examples": "Steel door plates, 3-inch screws, deadbolts",
                "why": "Infected individuals do not think rationally. They push, run, and attack endlessly. Your home becomes your fortress.",
                "quantity": "All doors and accessible windows",
                "priority": "Critical"
            },
            {
                "name": "Boarding Materials",
                "examples": "Plywood sheets, 2x4s, brackets, nails",
                "why": "Allows fast barricading when threat level increases.",
                "quantity": "Enough to cover all windows",
                "priority": "Critical"
            },
            {
                "name": "Security Cameras (Battery/Solar)",
                "examples": "Blink, Arlo, Ring",
                "why": "Helps monitor exterior without exposing yourself. You cannot outrun large groups.",
                "quantity": "4-6 cameras",
                "priority": "High"
            },
            {
                "name": "Motion Lights",
                "examples": "LITOM solar, Ring floodlight",
                "why": "Deters both infected and looters during night hours.",
                "quantity": "Perimeter coverage",
                "priority": "High"
            }
        ]
    },
    "food": {
        "category": "Food Supply (3-6 Months Minimum)",
        "icon": "🛒",
        "items": [
            {
                "name": "Canned Meats",
                "examples": "Spam, Swanson chicken, Vienna sausages",
                "why": "Stores will be empty in 48-72 hours of panic. Leaving your home becomes increasingly dangerous.",
                "quantity": "50+ cans",
                "priority": "Critical"
            },
            {
                "name": "Canned Vegetables",
                "examples": "Del Monte, Green Giant",
                "why": "Long shelf life, requires no refrigeration during grid collapse.",
                "quantity": "50+ cans",
                "priority": "Critical"
            },
            {
                "name": "Canned Soup",
                "examples": "Campbell's, Progresso",
                "why": "Easy to prepare, comforting during high-stress situations.",
                "quantity": "24+ cans",
                "priority": "High"
            },
            {
                "name": "Rice, Beans, Pasta",
                "examples": "Goya beans, Barilla pasta, Minute Rice",
                "why": "Bulk calories, long storage, filling meals.",
                "quantity": "50-100 pounds total",
                "priority": "Critical"
            },
            {
                "name": "Freeze-Dried Meals",
                "examples": "Mountain House, Augason Farms",
                "why": "25-year shelf life for truly long-term survival.",
                "quantity": "3-6 months supply",
                "priority": "High"
            },
            {
                "name": "Protein Bars",
                "examples": "Clif Bar, RXBar",
                "why": "Quick energy without cooking, good for evacuation.",
                "quantity": "50+ bars",
                "priority": "Medium"
            },
            {
                "name": "Peanut Butter",
                "examples": "Jif, Skippy",
                "why": "High calories, doesn't require refrigeration, morale booster.",
                "quantity": "4-6 large jars",
                "priority": "High"
            }
        ]
    },
    "water": {
        "category": "Water Supply & Filtration",
        "icon": "💧",
        "items": [
            {
                "name": "Bottled Water",
                "examples": "Dasani, Arrowhead, Aquafina",
                "why": "City water may become contaminated or shut off during collapse.",
                "quantity": "1 gallon per person per day × 90 days",
                "priority": "Critical"
            },
            {
                "name": "Water Storage Jugs",
                "examples": "Reliance Aqua-Tainer, Coleman 5-gallon",
                "why": "Allows bulk water storage before infrastructure fails.",
                "quantity": "50-100 gallon capacity",
                "priority": "Critical"
            },
            {
                "name": "Portable Water Filter",
                "examples": "LifeStraw, Sawyer Mini",
                "why": "You may need to filter river or rainwater for months.",
                "quantity": "3-4 filters",
                "priority": "High"
            },
            {
                "name": "Gravity Filter System",
                "examples": "Berkey, Alexapure",
                "why": "High-volume filtration for extended home use.",
                "quantity": "1 large system",
                "priority": "High"
            }
        ]
    },
    "tools": {
        "category": "Tools & Equipment",
        "icon": "🧰",
        "items": [
            {
                "name": "Solar Generator",
                "examples": "Jackery 2000 Pro, Bluetti, EcoFlow",
                "why": "Electricity becomes unreliable or gone entirely. Solar is renewable.",
                "quantity": "1 large system + panels",
                "priority": "High"
            },
            {
                "name": "Hand Tools",
                "examples": "Stanley, DeWalt, Craftsman",
                "why": "Repairs and barricading when power tools are useless.",
                "quantity": "Complete manual tool set",
                "priority": "High"
            },
            {
                "name": "Duct Tape",
                "examples": "Gorilla Tape, Duck Brand",
                "why": "Fast fixes and sealing gaps during potential airborne spread.",
                "quantity": "6+ rolls",
                "priority": "High"
            },
            {
                "name": "Fire Extinguisher",
                "examples": "First Alert 10-lb, Kidde",
                "why": "Fires break out frequently in abandoned neighborhoods.",
                "quantity": "2-3 extinguishers",
                "priority": "High"
            },
            {
                "name": "Binoculars",
                "examples": "Bushnell, Nikon",
                "why": "Observe threats from distance without exposure.",
                "quantity": "1-2",
                "priority": "Medium"
            }
        ]
    },
    "medical": {
        "category": "Medical Supplies",
        "icon": "🩹",
        "items": [
            {
                "name": "Comprehensive First Aid Kit",
                "examples": "Surviveware, Adventure Medical Kits",
                "why": "Hospitals collapse early in the outbreak. You must be your own first responder.",
                "quantity": "1 large kit (500+ pieces)",
                "priority": "Critical"
            },
            {
                "name": "Antibiotics (If Legally Obtained)",
                "examples": "Fish antibiotics (research carefully)",
                "why": "Infections become deadly when medical care is unavailable.",
                "quantity": "Emergency supply",
                "priority": "High"
            },
            {
                "name": "N95 Respirator Masks",
                "examples": "3M N95",
                "why": "Protects from airborne transmission if virus has respiratory component.",
                "quantity": "Box of 50+ per person",
                "priority": "Critical"
            },
            {
                "name": "Disposable Gloves",
                "examples": "MedPride nitrile, Ammex",
                "why": "Prevents fluid contact from bites or infected blood.",
                "quantity": "Box of 200+",
                "priority": "Critical"
            },
            {
                "name": "Wound Care Supplies",
                "examples": "Israeli bandages, QuikClot, sutures",
                "why": "Trauma care when emergency services don't exist.",
                "quantity": "Extensive supply",
                "priority": "High"
            }
        ]
    },
    "survival_strategy": {
        "category": "Survival Strategy & Protocols",
        "icon": "🧭",
        "items": [
            {
                "name": "Avoid Hospitals and Government Centers",
                "examples": "Stay home, avoid crowds",
                "why": "Historically during pandemics, hospitals are overwhelmed, understaffed, dangerous, and filled with infected. In a zombie-like scenario, risk is multiplied.",
                "quantity": "Strategic avoidance",
                "priority": "Critical"
            },
            {
                "name": "Maintain Silence = Survival",
                "examples": "Quiet movement, melee weapons, noise discipline",
                "why": "Noise attracts attention from both infected and desperate humans. Rely on quiet tools and suppressed movement.",
                "quantity": "Operational discipline",
                "priority": "Critical"
            },
            {
                "name": "Travel Only When Necessary",
                "examples": "Stay fortified, minimize exposure",
                "why": "Roads jammed with abandoned cars, crashed vehicles, infected clusters. Walking may be safer than driving. Travel only for water, safer zone, or critical supplies.",
                "quantity": "Minimal movement",
                "priority": "High"
            },
            {
                "name": "Be Cautious About Other Survivors",
                "examples": "Control distance, verify before trust",
                "why": "The infected are dangerous—but humans can be worse. Expect looters, armed raiders, desperate families trying to take supplies by force. Trust becomes rare.",
                "quantity": "Constant vigilance",
                "priority": "Critical"
            }
        ]
    },
    "long_term": {
        "category": "Long-Term Survival (Months to Years)",
        "icon": "🌾",
        "items": [
            {
                "name": "Sustainable Skills Development",
                "examples": "Gardening, hunting, fishing, food preservation, water treatment, basic medicine, tool repair",
                "why": "These skills replace stores, hospitals, and supply chains. The population drops drastically; cities become death zones; small groups become the new 'towns.'",
                "quantity": "Learn 3-5 core skills",
                "priority": "High"
            },
            {
                "name": "Community Building (Carefully)",
                "examples": "Trusted families, skilled neighbors",
                "why": "A single person cannot guard, cook, garden, and sleep safely without help. Look for families you trust, other preppers, skilled individuals (nurse, mechanic, carpenter). Avoid large roaming groups.",
                "quantity": "3-8 trusted people",
                "priority": "High"
            },
            {
                "name": "Rural Relocation Plan",
                "examples": "Farm, cabin, rural house with well water",
                "why": "Urban environments become too dangerous over time due to population density and uncontrolled fires. Rural areas far from highways are ideal.",
                "quantity": "Identified location + route",
                "priority": "Medium"
            }
        ]
    },
    "barter": {
        "category": "Barter Items in Zombie Outbreak",
        "icon": "💰",
        "items": [
            {
                "name": "High-Value Barter Goods",
                "examples": "Water filters, canned food, hygiene supplies, medicine, batteries, fire-starters, solar chargers, fuel",
                "why": "During long-term collapse, currency becomes items that keep people alive. These have universal value.",
                "quantity": "Extra 20-30% for trade",
                "priority": "Medium"
            },
            {
                "name": "NEVER Barter These",
                "examples": "Your location info, how much food you have, weapons, antibiotics, security routines",
                "why": "Revealing too much makes you a target. Information security is survival.",
                "quantity": "Complete secrecy",
                "priority": "Critical"
            }
        ]
    },
    "mental": {
        "category": "Mental & Psychological Survival",
        "icon": "🧠",
        "items": [
            {
                "name": "Maintain Routine and Structure",
                "examples": "Watch shifts, daily hygiene, regular training, structured tasks",
                "why": "This scenario is traumatic. Expect fear, isolation, loss, exhaustion, moral dilemmas, long-term stress. Routine becomes the anchor of sanity. A collapsed world needs disciplined survivors.",
                "quantity": "Daily structure",
                "priority": "High"
            }
        ]
    }
}

# ==================== ECONOMIC COLLAPSE CHECKLIST DATA ====================

ECONOMIC_COLLAPSE_CHECKLIST = {
    "food_water": {
        "category": "Food & Water (6-12 Months Minimum)",
        "icon": "🥫",
        "items": [
            {
                "name": "Dry Goods (Rice, Beans, Oats, Pasta)",
                "examples": "Minute Rice, Goya beans, Barilla pasta, Quaker oats",
                "why": "Long shelf life and bulk calories. In long-term collapse, food becomes currency. The government won't restock shelves and supply chains break.",
                "quantity": "50-100 pounds total",
                "priority": "Critical"
            },
            {
                "name": "Canned Meats",
                "examples": "Spam, Swanson chicken, Kirkland canned beef",
                "why": "Protein you can store for years. Food becomes worth more than money during collapse.",
                "quantity": "50+ cans",
                "priority": "Critical"
            },
            {
                "name": "Canned Vegetables & Soup",
                "examples": "Del Monte, Campbell's, Progresso",
                "why": "Vitamin sources when fresh food disappears completely.",
                "quantity": "50+ cans",
                "priority": "Critical"
            },
            {
                "name": "Freeze-Dried Meals",
                "examples": "Mountain House, Augason Farms",
                "why": "25-year shelf life and high survival value for long-term collapse.",
                "quantity": "3-6 months supply",
                "priority": "High"
            },
            {
                "name": "Water Containers & Filtration",
                "examples": "Brita, Sawyer filter, Berkey",
                "why": "Water becomes more critical when utilities fail permanently.",
                "quantity": "50+ gallons storage + 2 filters",
                "priority": "Critical"
            },
            {
                "name": "Portable Water Filters",
                "examples": "LifeStraw, Sawyer Mini",
                "why": "You may need to filter lake or rainwater for months or years.",
                "quantity": "2-3 filters",
                "priority": "High"
            }
        ]
    },
    "security": {
        "category": "Security & Self-Defense",
        "icon": "🛡️",
        "items": [
            {
                "name": "Home Defense Tools",
                "examples": "Security system, pepper spray (SABRE), tactical flashlight",
                "why": "During collapse: police response is slow or nonexistent, break-ins become common, gangs take advantage of chaos, people with resources become targets. Crime surges—looting, home invasions, carjackings spike dramatically.",
                "quantity": "Multiple defensive layers",
                "priority": "Critical"
            },
            {
                "name": "Home Fortifications",
                "examples": "Reinforced doors, window security film, motion lights",
                "why": "Makes your home a harder target when law enforcement is unavailable.",
                "quantity": "Complete home security upgrade",
                "priority": "High"
            },
            {
                "name": "Pepper Spray",
                "examples": "SABRE Red, Mace",
                "why": "Useful for non-lethal defense during high-crime periods.",
                "quantity": "2-3 per adult",
                "priority": "High"
            },
            {
                "name": "Security Lighting",
                "examples": "Solar motion lights, battery-powered alarms",
                "why": "Deters criminals when grid power is unreliable.",
                "quantity": "Perimeter coverage",
                "priority": "Medium"
            }
        ]
    },
    "barter": {
        "category": "Barter Items (The New Currency)",
        "icon": "💰",
        "items": [
            {
                "name": "Extra Food (Rice, Beans, Canned Meat)",
                "examples": "Goya, Spam, pasta",
                "why": "Money loses value. Food becomes the real currency. People with food are powerful; people without become desperate.",
                "quantity": "20-30% extra beyond your needs",
                "priority": "High"
            },
            {
                "name": "Batteries (Various Sizes)",
                "examples": "Duracell, Energizer AA, AAA, CR123",
                "why": "Batteries become gold when electricity is unreliable. High barter value.",
                "quantity": "500+ batteries",
                "priority": "High"
            },
            {
                "name": "Fuel Storage",
                "examples": "Propane tanks, gasoline (with stabilizer)",
                "why": "Fuel becomes extremely valuable for cooking, heating, and generators.",
                "quantity": "As much as safely storable",
                "priority": "High"
            },
            {
                "name": "Hand Tools",
                "examples": "Stanley, Craftsman basic tool sets",
                "why": "Hand tools become gold when electric tools are useless without power.",
                "quantity": "Extra sets for barter",
                "priority": "Medium"
            },
            {
                "name": "Water Filters (Extras)",
                "examples": "LifeStraw, Sawyer Mini",
                "why": "Clean water filters have universal value in collapse.",
                "quantity": "5-10 extra filters",
                "priority": "High"
            },
            {
                "name": "Soap & Hygiene Items",
                "examples": "Dove, Dial, hand sanitizer",
                "why": "Hygiene becomes a luxury. High barter value.",
                "quantity": "1-2 year supply",
                "priority": "Medium"
            },
            {
                "name": "Alcohol (Medical/Drinking)",
                "examples": "Jack Daniels, Everclear, rubbing alcohol",
                "why": "Used for disinfecting, barter, or consumption. Always in demand.",
                "quantity": "12+ bottles",
                "priority": "Low"
            },
            {
                "name": "OTC Medicine",
                "examples": "Tylenol, Advil, bandages",
                "why": "Medical supplies have extreme barter value when pharmacies are closed.",
                "quantity": "Large stockpile",
                "priority": "High"
            },
            {
                "name": "Baby Supplies (If Applicable)",
                "examples": "Diapers, formula, wipes",
                "why": "Desperate parents will trade anything for these.",
                "quantity": "Extra if you have young children",
                "priority": "Medium"
            }
        ]
    },
    "tools": {
        "category": "Tools & Equipment (Long-Term Survival)",
        "icon": "🔧",
        "items": [
            {
                "name": "Solar Generator",
                "examples": "Jackery 2000 Pro, Bluetti, EcoFlow",
                "why": "When the grid collapses permanently, solar becomes critical for survival.",
                "quantity": "1 large system (2000W+) + panels",
                "priority": "High"
            },
            {
                "name": "Hand Tools (Non-Electric)",
                "examples": "Stanley, DeWalt manual tools",
                "why": "Electric tools become useless without power. Hand tools last forever.",
                "quantity": "Complete manual tool set",
                "priority": "High"
            },
            {
                "name": "Manual Can Opener",
                "examples": "OXO Good Grips",
                "why": "If you store canned food, this is non-negotiable.",
                "quantity": "3-4",
                "priority": "Critical"
            },
            {
                "name": "Propane Stove",
                "examples": "Coleman portable stove",
                "why": "Lets you cook when electricity and gas are shut off.",
                "quantity": "1 stove + fuel supply",
                "priority": "Critical"
            },
            {
                "name": "Cast Iron Skillet",
                "examples": "Lodge",
                "why": "Lasts forever, works on flame, easy to clean.",
                "quantity": "2-3 pans",
                "priority": "High"
            },
            {
                "name": "Fishing Gear",
                "examples": "Ugly Stik rod, KastKing reel",
                "why": "Provides long-term food sources when stored food runs low.",
                "quantity": "Complete fishing setup",
                "priority": "Medium"
            },
            {
                "name": "Gardening Tools & Seeds",
                "examples": "Heirloom seeds, spade, rake, hoe",
                "why": "Collapse can last years—you must shift from stored food to food production.",
                "quantity": "Complete garden setup + seed bank",
                "priority": "High"
            }
        ]
    },
    "communication": {
        "category": "Communication & Mobility",
        "icon": "📻",
        "items": [
            {
                "name": "Hand-Crank Emergency Radio",
                "examples": "Midland ER310, Sangean",
                "why": "Government communication may be limited, but weather alerts still matter.",
                "quantity": "2 radios",
                "priority": "High"
            },
            {
                "name": "Bicycles",
                "examples": "Schwinn, Trek, mountain bikes",
                "why": "Gas becomes scarce. Bikes become high-value assets. Mobility is survival—people trapped in cities during collapse are at highest risk.",
                "quantity": "1 per person + spare parts",
                "priority": "High"
            },
            {
                "name": "Paper Maps",
                "examples": "Local city, county, state maps",
                "why": "GPS will fail or be unreliable. Physical navigation essential.",
                "quantity": "Complete regional maps",
                "priority": "Medium"
            }
        ]
    },
    "medical": {
        "category": "Medical & Hygiene Supplies",
        "icon": "🩹",
        "items": [
            {
                "name": "Comprehensive Medical Kit",
                "examples": "Adventure Medical Kits, Surviveware",
                "why": "Hospitals will be overwhelmed or shut down during long-term collapse.",
                "quantity": "1 large kit (500+ pieces)",
                "priority": "Critical"
            },
            {
                "name": "Antibiotics (If Legally Obtained)",
                "examples": "Fish antibiotics (amoxicillin equivalent)",
                "why": "Infections become deadly when medical care is limited or unavailable.",
                "quantity": "Emergency supply",
                "priority": "High"
            },
            {
                "name": "Pain Relievers (Extra for Barter)",
                "examples": "Tylenol, Advil, Aspirin",
                "why": "High barter value and personal use.",
                "quantity": "10+ bottles",
                "priority": "High"
            },
            {
                "name": "Hygiene Supplies",
                "examples": "Soap (Dove), toothpaste (Crest), deodorant (Old Spice)",
                "why": "Hygiene becomes a luxury during collapse. Barter value increases.",
                "quantity": "1-2 year supply",
                "priority": "Medium"
            },
            {
                "name": "Water Purification Tablets",
                "examples": "Potable Aqua, Aquatabs",
                "why": "Critical backup option when filters wear out.",
                "quantity": "500+ tablets",
                "priority": "High"
            }
        ]
    },
    "financial": {
        "category": "Cash & Financial Adjustments",
        "icon": "💵",
        "items": [
            {
                "name": "Small Bill Cash Reserve",
                "examples": "$1,000-3,000 in $1, $5, $10, $20 bills",
                "why": "Cash will still matter briefly (first 1-3 months), but eventually: inflation kills value, banks freeze withdrawals, credit cards stop working. Keep some cash for early phase, don't rely on it long-term.",
                "quantity": "$1,000-3,000",
                "priority": "Medium"
            },
            {
                "name": "Precious Metals (HIDDEN)",
                "examples": "Silver coins, small gold pieces",
                "why": "IMPORTANT: Never tell ANYONE you own gold or silver. In every real collapse, people with precious metals were targeted, robbed, or kidnapped. Gold and silver are stores of value—not everyday currency. Should be hidden, not traded publicly.",
                "quantity": "Small reserve (if desired)",
                "priority": "Low"
            }
        ]
    },
    "opsec": {
        "category": "Operational Security (OPSEC)",
        "icon": "🤐",
        "items": [
            {
                "name": "Maintain Secrecy About Preps",
                "examples": "Don't brag, don't post online, don't tell neighbors",
                "why": "The more resources you have, the less anyone should know. People get violent when their children are starving. Don't show off stored food or display weapons.",
                "quantity": "Complete discretion",
                "priority": "Critical"
            },
            {
                "name": "Discreet Storage",
                "examples": "Hidden pantry, basement cache, buried containers",
                "why": "Visible supplies make you a target during desperate times.",
                "quantity": "Multiple hidden locations",
                "priority": "High"
            }
        ]
    },
    "skills": {
        "category": "Skills That Replace Money",
        "icon": "🎓",
        "items": [
            {
                "name": "Valuable Collapse Skills",
                "examples": "First aid, auto repair, plumbing, gardening, fishing, carpentry, electrical work, water filtration, food preservation, home security",
                "why": "Skills become more important than physical currency. Learning these makes you 'untradeable'—people need you. In Phase 3 (1-5 years), skill-based trade replaces the old economy.",
                "quantity": "Learn 2-3 core skills deeply",
                "priority": "High"
            }
        ]
    }
}

# ==================== TORNADO CHECKLIST DATA ====================

TORNADO_CHECKLIST = {
    "critical": {
        "category": "Critical Priority Items (Before Tornado Season)",
        "icon": "🌪️",
        "items": [
            {
                "name": "NOAA Emergency Weather Radio",
                "examples": "Midland WR120, Sangean portable",
                "why": "Tornado warnings often come minutes before impact. Phones fail, alerts don't always sound, and storms knock out cell towers. A battery-powered NOAA radio gives the earliest possible warning, increasing survival chances dramatically.",
                "quantity": "2 radios (1 backup)",
                "priority": "Critical"
            },
            {
                "name": "Safe Room / Interior Shelter Plan",
                "examples": "Basement, interior bathroom, closet, hallway",
                "why": "If you don't have a basement, identify the innermost room on the lowest floor. Rehearse getting there in under 10 seconds.",
                "quantity": "Identified location + practice drills",
                "priority": "Critical"
            },
            {
                "name": "Bike Helmet or Construction Hard Hat",
                "examples": "Schwinn bike helmet, 3M hard hat",
                "why": "Most tornado deaths come from head trauma caused by flying debris. A simple helmet can mean the difference between life and death.",
                "quantity": "1 per person",
                "priority": "Critical"
            },
            {
                "name": "N95 Respirator Masks",
                "examples": "3M N95, Honeywell",
                "why": "After a tornado, the air fills with insulation fibers, mold, dust, and microscopic debris. An N95 protects your lungs during rescue and cleanup.",
                "quantity": "Box of 20+ per person",
                "priority": "Critical"
            },
            {
                "name": "Sturdy Boots",
                "examples": "Timberland, Merrell work boots",
                "why": "Walking barefoot or in sneakers after a tornado means stepping on nails, shattered glass, splintered wood, hot metal, and chemicals. Boots are mandatory for searching or evacuating through debris fields.",
                "quantity": "1 pair per person",
                "priority": "Critical"
            },
            {
                "name": "Flashlight + Headlamp",
                "examples": "Streamlight, Black Diamond headlamp",
                "why": "Power outages are universal. Debris makes homes dark even during daytime. A hands-free headlamp helps you navigate rubble safely.",
                "quantity": "1 of each per person",
                "priority": "Critical"
            },
            {
                "name": "Fire Extinguisher (ABC-Rated)",
                "examples": "First Alert 10-lb, Kidde",
                "why": "Gas leaks and damaged wiring commonly start fires after tornadoes.",
                "quantity": "2 extinguishers",
                "priority": "Critical"
            }
        ]
    },
    "water_food": {
        "category": "Water & Food (1 Week Minimum)",
        "icon": "🥫",
        "items": [
            {
                "name": "Bottled Water",
                "examples": "Dasani, Arrowhead, Aquafina",
                "why": "Water lines break and contamination is common after tornadoes.",
                "quantity": "1 gallon per person per day × 7 days",
                "priority": "Critical"
            },
            {
                "name": "Canned Soup",
                "examples": "Campbell's, Progresso",
                "why": "Provides warmth and comfort when your home may be unlivable.",
                "quantity": "12-24 cans",
                "priority": "High"
            },
            {
                "name": "Canned Vegetables",
                "examples": "Del Monte, Green Giant",
                "why": "Gives vitamins and hydration when fresh food is unavailable.",
                "quantity": "12+ cans",
                "priority": "High"
            },
            {
                "name": "Canned Meats",
                "examples": "Swanson chicken, Spam",
                "why": "Protein source that requires no refrigeration.",
                "quantity": "12-18 cans",
                "priority": "High"
            },
            {
                "name": "Peanut Butter",
                "examples": "Jif, Skippy",
                "why": "High-calorie food that stores well and feeds kids quickly.",
                "quantity": "2-3 large jars",
                "priority": "High"
            },
            {
                "name": "Protein Bars",
                "examples": "Clif Bar, RXBar, Quest",
                "why": "Essential for quick calories if you're evacuating on foot.",
                "quantity": "20-30 bars",
                "priority": "High"
            },
            {
                "name": "Instant Rice / Mashed Potatoes",
                "examples": "Minute Rice, Idahoan",
                "why": "Heats quickly with limited fuel and provides steady energy.",
                "quantity": "5+ boxes each",
                "priority": "Medium"
            },
            {
                "name": "Crackers & Oatmeal Packets",
                "examples": "Ritz, Quaker Instant",
                "why": "Shelf-stable carbs that stay good even in hot or humid weather.",
                "quantity": "5+ boxes",
                "priority": "Medium"
            },
            {
                "name": "Electrolyte Drinks",
                "examples": "Gatorade, Pedialyte, Liquid I.V.",
                "why": "Heat exhaustion is common during debris cleanup.",
                "quantity": "12+ bottles or 30+ packets",
                "priority": "High"
            }
        ]
    },
    "tools": {
        "category": "Tools & Gear",
        "icon": "🔧",
        "items": [
            {
                "name": "Multi-Tool",
                "examples": "Leatherman Wave+, Gerber",
                "why": "Helps cut through debris, open cans, cut seatbelts, or shut off gas lines.",
                "quantity": "2 tools",
                "priority": "High"
            },
            {
                "name": "Crowbar / Pry Bar",
                "examples": "Stanley Wonder Bar, Estwing",
                "why": "Used to lift fallen beams, open jammed doors, and free trapped people.",
                "quantity": "1-2 bars",
                "priority": "High"
            },
            {
                "name": "Portable Power Bank / Solar Charger",
                "examples": "Anker PowerCore, Goal Zero",
                "why": "Cell towers may still function, but power will not. Keep your phone alive for coordination and emergency calls.",
                "quantity": "2-3 power banks + 1 solar charger",
                "priority": "High"
            },
            {
                "name": "Chainsaw or Hand Saw",
                "examples": "Stihl chainsaw, Husqvarna, folding saw",
                "why": "After a tornado, roads and yards are blocked by downed trees. Clearing these can be the only way to evacuate.",
                "quantity": "1 chainsaw + fuel OR 2 hand saws",
                "priority": "High"
            },
            {
                "name": "Tarp and Duct Tape",
                "examples": "Gorilla Tape, Duck Brand, heavy-duty tarps",
                "why": "If your roof is partially damaged but the structure is intact, tarps prevent rain from destroying what's left.",
                "quantity": "3-4 large tarps + 4 rolls tape",
                "priority": "High"
            },
            {
                "name": "Work Gloves",
                "examples": "Ironclad, Mechanix Wear",
                "why": "Essential for picking up debris, insulation, and sharp materials.",
                "quantity": "3-4 pairs",
                "priority": "Critical"
            },
            {
                "name": "Emergency Whistle",
                "examples": "Shoreline Marine, Storm",
                "why": "To signal rescuers if trapped under rubble.",
                "quantity": "1 per person",
                "priority": "High"
            }
        ]
    },
    "communication": {
        "category": "Communication & Records",
        "icon": "📄",
        "items": [
            {
                "name": "Laminated Emergency Contact Card",
                "examples": "DIY laminated cards with contacts",
                "why": "Phones die or get lost; physical cards keep family contacts accessible.",
                "quantity": "1 per person",
                "priority": "High"
            },
            {
                "name": "Fireproof Waterproof Document Pouch",
                "examples": "EngPow, JUNDUN fireproof bag",
                "why": "After destruction, you'll need proof of ownership for FEMA claims, insurance, rebuilding, and medical identity. Keep copies of IDs, deeds, insurance, titles.",
                "quantity": "1 large pouch",
                "priority": "Critical"
            },
            {
                "name": "Paper Map of Your Area",
                "examples": "Local road map, county map",
                "why": "GPS often fails when power and towers go down.",
                "quantity": "2-3 maps",
                "priority": "Medium"
            }
        ]
    },
    "health": {
        "category": "Health & Sanitation",
        "icon": "🩹",
        "items": [
            {
                "name": "Comprehensive First Aid Kit",
                "examples": "Surviveware, Adventure Medical Kits",
                "why": "Treats cuts, punctures, burns, and infections—common injuries in tornado debris.",
                "quantity": "1 large kit (200+ pieces)",
                "priority": "Critical"
            },
            {
                "name": "Wet Wipes & Hand Sanitizer",
                "examples": "Purell, Clorox wipes",
                "why": "With running water unavailable, this maintains basic hygiene.",
                "quantity": "5+ packs wipes, 3 bottles sanitizer",
                "priority": "High"
            },
            {
                "name": "Prescription Medications",
                "examples": "Your personal prescriptions",
                "why": "Pharmacies might be destroyed or closed.",
                "quantity": "7-14 days supply",
                "priority": "Critical"
            }
        ]
    },
    "evacuation": {
        "category": "Evacuation Go-Bag Essentials",
        "icon": "🎒",
        "items": [
            {
                "name": "Emergency Go-Bag (Pre-Packed)",
                "examples": "5.11 Tactical, Osprey backpack",
                "why": "If house is destroyed or unsafe, you need to evacuate immediately with essentials ready.",
                "quantity": "1 per person",
                "priority": "Critical"
            },
            {
                "name": "Cash",
                "examples": "$200-400 in small bills",
                "why": "ATMs won't work, cards won't process. Cash is essential.",
                "quantity": "$200-400",
                "priority": "Critical"
            },
            {
                "name": "Spare Clothing",
                "examples": "2 complete changes per person",
                "why": "Your clothes may be destroyed or contaminated.",
                "quantity": "2 sets per person",
                "priority": "High"
            },
            {
                "name": "Blanket or Sleeping Bag",
                "examples": "Coleman, Teton Sports",
                "why": "Shelters are often crowded; having your own provides comfort.",
                "quantity": "1 per person",
                "priority": "High"
            },
            {
                "name": "Personal Hygiene Supplies",
                "examples": "Toothbrush, soap, deodorant",
                "why": "You may be displaced for days or weeks.",
                "quantity": "Travel-size complete kit",
                "priority": "Medium"
            }
        ]
    },
    "security": {
        "category": "Security & Property Protection",
        "icon": "🛡️",
        "items": [
            {
                "name": "Pepper Spray",
                "examples": "SABRE Red",
                "why": "Last resort protection during periods of limited law enforcement when neighborhoods are evacuated and homes left open.",
                "quantity": "1-2 per adult",
                "priority": "Medium"
            },
            {
                "name": "Heavy-Duty Flashlight",
                "examples": "Maglite, tactical flashlight",
                "why": "Dual purpose: lighting and self-defense tool.",
                "quantity": "1-2",
                "priority": "Medium"
            },
            {
                "name": "Door/Window Security",
                "examples": "Plywood sheets, security bars",
                "why": "Damaged homes are vulnerable to looting when police resources are stretched thin.",
                "quantity": "Enough to secure main openings",
                "priority": "Low"
            }
        ]
    }
}

# ==================== PANDEMIC CHECKLIST DATA ====================

PANDEMIC_CHECKLIST = {
    "medical_ppe": {
        "category": "Medical & PPE (First to Disappear)",
        "icon": "😷",
        "items": [
            {
                "name": "N95 or KN95 Masks",
                "examples": "3M N95, Honeywell, Powecom KN95",
                "why": "COVID showed cloth masks were weak compared to N95-quality masks. These provide real respiratory protection during airborne outbreaks.",
                "quantity": "Box of 20+ per person",
                "priority": "Critical"
            },
            {
                "name": "Disposable Gloves",
                "examples": "Ammex nitrile, MedPride",
                "why": "Useful for cleaning, caring for a sick person, or dealing with shared surfaces without contamination.",
                "quantity": "Box of 100+",
                "priority": "High"
            },
            {
                "name": "Hand Sanitizer (60-70% Alcohol)",
                "examples": "Purell, Germ-X",
                "why": "One of the first items to vanish during COVID. Necessary when you can't wash hands frequently.",
                "quantity": "6+ bottles (8 oz each)",
                "priority": "Critical"
            },
            {
                "name": "Disinfectant Wipes / Sprays",
                "examples": "Lysol wipes, Clorox spray",
                "why": "Used to wipe down doorknobs, groceries, packages, and high-touch surfaces. Sold out for months during COVID.",
                "quantity": "10+ containers",
                "priority": "Critical"
            },
            {
                "name": "Digital Thermometer",
                "examples": "Braun ThermoScan, iProven",
                "why": "Essential for monitoring symptoms and deciding when to call a doctor. Stores sold out quickly during COVID.",
                "quantity": "2 thermometers",
                "priority": "Critical"
            },
            {
                "name": "Pulse Oximeter",
                "examples": "Zacurate, Innovo",
                "why": "COVID taught us: oxygen levels can drop before someone feels 'short of breath.' Early warning tool for respiratory distress.",
                "quantity": "1-2 devices",
                "priority": "High"
            },
            {
                "name": "Fever Reducers",
                "examples": "Tylenol (acetaminophen), Advil (ibuprofen)",
                "why": "First-line treatment for fever and body aches. Stores ran out during COVID waves.",
                "quantity": "2 bottles each",
                "priority": "Critical"
            },
            {
                "name": "Cough Medicine",
                "examples": "Mucinex, Robitussin DM",
                "why": "Helps manage respiratory symptoms at home before seeking medical care.",
                "quantity": "2-3 bottles",
                "priority": "High"
            },
            {
                "name": "Stomach Medications",
                "examples": "Pepto-Bismol, Imodium",
                "why": "Many viruses cause GI symptoms. These became hard to find during COVID.",
                "quantity": "2 bottles each",
                "priority": "Medium"
            },
            {
                "name": "Allergy/Upper Respiratory Meds",
                "examples": "Zyrtec, Claritin, Benadryl",
                "why": "Helps differentiate symptoms and manage allergies vs. illness.",
                "quantity": "2 bottles",
                "priority": "Medium"
            }
        ]
    },
    "food_supplies": {
        "category": "Food & Basic Supplies (2-3 Weeks)",
        "icon": "🥫",
        "items": [
            {
                "name": "Canned Soup & Chili",
                "examples": "Campbell's, Progresso, Hormel",
                "why": "Easy to prepare when sick, comforting, long shelf life. Shelves emptied quickly during COVID panic buying.",
                "quantity": "18-24 cans",
                "priority": "High"
            },
            {
                "name": "Canned Vegetables",
                "examples": "Del Monte, Green Giant",
                "why": "Provides nutrition when fresh produce is risky or unavailable.",
                "quantity": "18+ cans",
                "priority": "High"
            },
            {
                "name": "Canned Beans",
                "examples": "Bush's, Goya",
                "why": "Protein and fiber, stores indefinitely, filling.",
                "quantity": "12+ cans",
                "priority": "High"
            },
            {
                "name": "Canned Meats",
                "examples": "Spam, Swanson canned chicken",
                "why": "Protein source when meat counters are empty or risky.",
                "quantity": "12-18 cans",
                "priority": "High"
            },
            {
                "name": "Rice",
                "examples": "Mahatma, Ben's Original",
                "why": "Filling, stores forever, one of the first panic-buy items.",
                "quantity": "10-20 pounds",
                "priority": "High"
            },
            {
                "name": "Pasta & Sauce",
                "examples": "Barilla, De Cecco, Prego, Rao's",
                "why": "Quick meals, long shelf life, disappeared quickly during COVID.",
                "quantity": "5 lbs pasta + 6 jars sauce",
                "priority": "High"
            },
            {
                "name": "Oatmeal Packets",
                "examples": "Quaker Instant Oatmeal",
                "why": "Easy breakfast, requires minimal effort when energy is low.",
                "quantity": "3+ boxes",
                "priority": "Medium"
            },
            {
                "name": "Protein Bars",
                "examples": "Clif Bar, RXBar, Quest",
                "why": "Grab-and-go nutrition when cooking feels impossible.",
                "quantity": "24+ bars",
                "priority": "Medium"
            },
            {
                "name": "Peanut Butter & Jelly",
                "examples": "Jif, Skippy, Smucker's",
                "why": "High calories, comfort food, doesn't require refrigeration.",
                "quantity": "2-3 jars each",
                "priority": "High"
            },
            {
                "name": "Crackers",
                "examples": "Ritz, Saltines, Wheat Thins",
                "why": "Easy on upset stomachs, pairs with other foods.",
                "quantity": "5+ boxes",
                "priority": "Medium"
            },
            {
                "name": "Shelf-Stable Milk",
                "examples": "Horizon UHT, Silk",
                "why": "When dairy cases are empty or you can't shop frequently.",
                "quantity": "12+ cartons",
                "priority": "Medium"
            },
            {
                "name": "Coffee/Tea/Sugar",
                "examples": "Folgers, Lipton, generic sugar",
                "why": "Morale matters. Small comforts help mental health during lockdowns.",
                "quantity": "Normal usage + 50% extra",
                "priority": "Low"
            }
        ]
    },
    "household_basics": {
        "category": "Household Basics (Disappeared During COVID)",
        "icon": "🧻",
        "items": [
            {
                "name": "Toilet Paper",
                "examples": "Charmin, Cottonelle, store brand",
                "why": "The infamous COVID panic buy. Buy a reasonable surplus—not a garage full.",
                "quantity": "6-8 week supply per household",
                "priority": "Critical"
            },
            {
                "name": "Paper Towels",
                "examples": "Bounty, Viva",
                "why": "Cleaning and wiping surfaces became constant during COVID.",
                "quantity": "12-18 rolls",
                "priority": "High"
            },
            {
                "name": "Trash Bags",
                "examples": "Hefty, Glad",
                "why": "More waste from home meals, deliveries, and sick room cleanup.",
                "quantity": "2-3 boxes",
                "priority": "Medium"
            },
            {
                "name": "Dish Soap & Sponges",
                "examples": "Dawn, Palmolive, Scotch-Brite",
                "why": "Cooking at home increases dramatically during lockdowns.",
                "quantity": "4+ bottles, 12+ sponges",
                "priority": "Medium"
            },
            {
                "name": "Laundry Detergent",
                "examples": "Tide, Gain, All",
                "why": "Essential for hygiene, especially if someone is sick.",
                "quantity": "2-3 large bottles",
                "priority": "Medium"
            }
        ]
    },
    "sick_room": {
        "category": "Isolation / Sick Room Setup",
        "icon": "🏥",
        "items": [
            {
                "name": "Separate Room Supplies",
                "examples": "Dedicated trash can, tissues, hand sanitizer",
                "why": "COVID lesson: many families infected each other by not separating the first sick person. Create a 'hot zone' immediately.",
                "quantity": "1 complete setup",
                "priority": "High"
            },
            {
                "name": "Extra Masks (For Sick Person)",
                "examples": "Surgical masks, N95s",
                "why": "Sick person wears mask to reduce spread to caregivers.",
                "quantity": "20+ masks",
                "priority": "High"
            },
            {
                "name": "Electrolyte Drinks",
                "examples": "Gatorade, Pedialyte, Liquid I.V.",
                "why": "Prevents dehydration during fever and illness.",
                "quantity": "12+ bottles or 30+ packets",
                "priority": "High"
            },
            {
                "name": "Throat Lozenges",
                "examples": "Halls, Ricola",
                "why": "Soothes sore throat without requiring doctor visit.",
                "quantity": "5+ bags",
                "priority": "Low"
            }
        ]
    },
    "home_security": {
        "category": "Security & Civil Unrest Prep",
        "icon": "🛡️",
        "items": [
            {
                "name": "Exterior Motion Lights",
                "examples": "Ring Floodlight, Aootek solar",
                "why": "During COVID, some areas saw protests and looting. Motion lights reduce break-in attempts.",
                "quantity": "2-4 lights",
                "priority": "Medium"
            },
            {
                "name": "Reinforced Door Hardware",
                "examples": "Heavy-duty deadbolts, 3-inch strike plate screws",
                "why": "Slows forced entry when police response times are longer.",
                "quantity": "Upgrade for main entrances",
                "priority": "Medium"
            },
            {
                "name": "Window Locks & Security Film",
                "examples": "Sliding window locks, 3M safety film",
                "why": "Adds layer of protection during civil unrest periods.",
                "quantity": "All accessible windows",
                "priority": "Low"
            },
            {
                "name": "Self-Defense Tools",
                "examples": "Pepper spray (SABRE), tactical flashlight, bat",
                "why": "Last resort protection when police response is delayed during pandemic chaos. Not encouraging violence—protecting home and family.",
                "quantity": "Multiple options per household",
                "priority": "Medium"
            }
        ]
    },
    "mental_health": {
        "category": "Mental Health & Boredom Prevention",
        "icon": "🎮",
        "items": [
            {
                "name": "Board Games / Cards",
                "examples": "Uno, Monopoly, Chess, playing cards",
                "why": "COVID showed: people went crazy doom-scrolling. Games reduce stress and family conflict.",
                "quantity": "5+ games variety",
                "priority": "Medium"
            },
            {
                "name": "Books (Physical or E-Reader)",
                "examples": "Kindle, library books, magazines",
                "why": "Healthy escape from constant news and stress.",
                "quantity": "10+ books per person",
                "priority": "Low"
            },
            {
                "name": "Puzzles / Kids Activities",
                "examples": "Jigsaw puzzles, coloring books, craft supplies",
                "why": "Keeps children occupied during school closures.",
                "quantity": "Age-appropriate variety",
                "priority": "Medium"
            },
            {
                "name": "Basic Fitness Gear",
                "examples": "Resistance bands, yoga mat, dumbbells",
                "why": "Gyms close during pandemics. Exercise critical for mental and physical health.",
                "quantity": "Basic home gym setup",
                "priority": "Medium"
            }
        ]
    },
    "work_school": {
        "category": "Work From Home / Remote School",
        "icon": "💻",
        "items": [
            {
                "name": "Backup Tech Equipment",
                "examples": "Extra headphones, webcam, charging cables",
                "why": "Remote work and school become mandatory. Tech stores sold out during COVID.",
                "quantity": "Backups for critical items",
                "priority": "High"
            },
            {
                "name": "Internet Backup Plan",
                "examples": "Mobile hotspot, backup router",
                "why": "Internet became essential utility during COVID. Have a backup.",
                "quantity": "1 backup option",
                "priority": "Medium"
            },
            {
                "name": "Workspace Setup",
                "examples": "Desk, ergonomic chair, good lighting",
                "why": "You might be home for months. Proper setup prevents pain and burnout.",
                "quantity": "1 per working/school-age person",
                "priority": "Medium"
            }
        ]
    },
    "long_term": {
        "category": "Long-Term Items (If Pandemic Drags On)",
        "icon": "📦",
        "items": [
            {
                "name": "Extra Prescription Medications",
                "examples": "Your personal prescriptions",
                "why": "Get 1-3 month supply if doctor allows. Pharmacies can experience delays.",
                "quantity": "1-3 months backup",
                "priority": "Critical"
            },
            {
                "name": "Freezer Stock (Meat & Vegetables)",
                "examples": "Bulk chicken, beef, frozen vegetables",
                "why": "Reduces shopping trips, provides variety beyond canned food.",
                "quantity": "Chest freezer recommended",
                "priority": "Medium"
            },
            {
                "name": "Air Purifier (HEPA)",
                "examples": "Levoit, Coway, Honeywell",
                "why": "Improves indoor air quality during extended time at home.",
                "quantity": "1-2 units",
                "priority": "Low"
            }
        ]
    }
}

# ==================== VOLCANIC ERUPTION CHECKLIST DATA ====================

VOLCANIC_ERUPTION_REGULAR = {
    "critical": {
        "category": "Critical Priority Items (Must Have)",
        "icon": "🌋",
        "items": [
            {
                "name": "N95 or P100 Respirator Masks",
                "examples": "3M N95, Honeywell P100",
                "why": "Ash is not like dust—it's microscopic, sharp volcanic glass. Breathing it can cause lung scarring and permanent respiratory damage. These masks filter volcanic ash and protect the lungs during evacuation or cleanup.",
                "quantity": "Box of 20+ per person",
                "priority": "Critical"
            },
            {
                "name": "Goggles (Fully Sealed)",
                "examples": "Pyramex, DEWALT sealed goggles",
                "why": "Volcanic ash irritates and scratches the eyes. Basic sunglasses are useless—sealed goggles prevent ash from entering and causing corneal abrasions.",
                "quantity": "2 pairs per person",
                "priority": "Critical"
            },
            {
                "name": "Evacuation Go-Bag (Packed)",
                "examples": "5.11 Tactical Rush, Osprey",
                "why": "Volcano warnings may give you 30 minutes—or none at all. Having a bag packed lets you leave instantly before roads clog with ash or lava cuts off escape routes.",
                "quantity": "1 per person",
                "priority": "Critical"
            },
            {
                "name": "Battery-Powered or Solar Radio",
                "examples": "Midland ER310, Sangean",
                "why": "Cell towers collapse during eruptions. Radio is the ONLY way to receive emergency alerts, lava flow direction updates, and safe-zone instructions.",
                "quantity": "2 radios",
                "priority": "Critical"
            },
            {
                "name": "Air Purifier (Indoor HEPA)",
                "examples": "Levoit Core 400, Coway AP-1512HH",
                "why": "If ashfall lasts days, indoor air becomes toxic. A HEPA purifier makes indoor sheltering safe when evacuation is temporarily impossible.",
                "quantity": "1-2 units",
                "priority": "Critical"
            },
            {
                "name": "Cash (Small Bills)",
                "examples": "$300-600 in mixed bills",
                "why": "ATMs and card systems fail quickly, especially during ashfall that shuts down power grids.",
                "quantity": "$300-600",
                "priority": "Critical"
            }
        ]
    },
    "water": {
        "category": "Water & Liquid Storage",
        "icon": "💧",
        "items": [
            {
                "name": "Bottled Water (High Quantity)",
                "examples": "Arrowhead, Dasani, Aquafina",
                "why": "Volcanic ash contaminates ALL water sources. Even city water may fail because ash destroys filters and clogging overwhelms treatment plants.",
                "quantity": "2 gallons per person per day × 7 days minimum",
                "priority": "Critical"
            },
            {
                "name": "Large Water Containers",
                "examples": "Reliance Aqua-Tainer, Igloo 5-7 gallon",
                "why": "Critical for long-term disruptions when volcanic ash blocks access to utilities.",
                "quantity": "3-5 containers",
                "priority": "Critical"
            },
            {
                "name": "Electrolyte Drinks",
                "examples": "Gatorade, Pedialyte, Liquid I.V.",
                "why": "Heat, dehydration, and breathing through masks increase fluid loss dramatically.",
                "quantity": "12+ bottles or 30+ packets",
                "priority": "High"
            }
        ]
    },
    "food": {
        "category": "Food Storage (1-3 Weeks)",
        "icon": "🥫",
        "items": [
            {
                "name": "Canned Soup",
                "examples": "Campbell's, Progresso",
                "why": "Comfort food that heats quickly—even with limited fuel—boosts morale during ashfall.",
                "quantity": "18-24 cans",
                "priority": "High"
            },
            {
                "name": "Canned Vegetables",
                "examples": "Del Monte, Green Giant",
                "why": "Fresh produce will be unavailable for weeks due to ash contamination.",
                "quantity": "18+ cans",
                "priority": "High"
            },
            {
                "name": "Canned Meats",
                "examples": "Spam, Swanson chicken",
                "why": "Protein source that stays good with no refrigeration.",
                "quantity": "12-18 cans",
                "priority": "High"
            },
            {
                "name": "Peanut Butter",
                "examples": "Jif, Skippy",
                "why": "High-calorie survival food for extended ashfall periods.",
                "quantity": "3-4 large jars",
                "priority": "High"
            },
            {
                "name": "Tuna Pouches",
                "examples": "StarKist, Bumble Bee",
                "why": "Lightweight protein ideal for quick evacuation.",
                "quantity": "12-18 pouches",
                "priority": "High"
            },
            {
                "name": "Instant Rice",
                "examples": "Minute Rice, Uncle Ben's",
                "why": "Requires minimal fuel and water—critical when utilities fail.",
                "quantity": "5+ boxes",
                "priority": "High"
            },
            {
                "name": "Instant Mashed Potatoes",
                "examples": "Idahoan, Betty Crocker",
                "why": "Fills stomach quickly; stores well through ashfall events.",
                "quantity": "5+ boxes",
                "priority": "Medium"
            },
            {
                "name": "Pasta + Jarred Sauce",
                "examples": "Barilla pasta, Rao's sauce",
                "why": "Reliable, high-energy meals for extended sheltering periods.",
                "quantity": "5 lbs pasta + 6 jars sauce",
                "priority": "Medium"
            },
            {
                "name": "Oatmeal Packets",
                "examples": "Quaker Instant Oatmeal",
                "why": "Requires little water and supports energy levels under stress.",
                "quantity": "3+ boxes",
                "priority": "Medium"
            }
        ]
    },
    "tools": {
        "category": "Tools & Protective Gear",
        "icon": "🔧",
        "items": [
            {
                "name": "Shovel & Sturdy Broom",
                "examples": "Fiskars, Craftsman",
                "why": "Ash buildup collapses roofs. You must remove ash frequently (only when safe!) to prevent structural collapse.",
                "quantity": "1 shovel + 1 broom",
                "priority": "Critical"
            },
            {
                "name": "Heavy Work Gloves",
                "examples": "Ironclad, OZERO heat-resistant",
                "why": "Ash is abrasive like sandpaper. Gloves protect skin when clearing debris or handling hot material.",
                "quantity": "3-4 pairs",
                "priority": "Critical"
            },
            {
                "name": "Headlamp + Extra Batteries",
                "examples": "Black Diamond, Petzl",
                "why": "Ash clouds can block sunlight for days, turning day into night.",
                "quantity": "1 per person + 50+ batteries",
                "priority": "Critical"
            },
            {
                "name": "Multi-Tool",
                "examples": "Leatherman Wave+, Gerber",
                "why": "Used for cutting, repairs, and emergency situations during evacuation.",
                "quantity": "2 tools",
                "priority": "High"
            },
            {
                "name": "Fire Extinguisher (ABC-Rated)",
                "examples": "Kidde 10-lb, First Alert",
                "why": "Volcanoes trigger wildfires through falling ash and embers.",
                "quantity": "2 extinguishers",
                "priority": "High"
            },
            {
                "name": "Gas Siphon",
                "examples": "Koehler Enterprises, TEKTON",
                "why": "Helps fuel your vehicle if gas stations shut down from power outages or ash infiltration.",
                "quantity": "1 siphon kit",
                "priority": "Medium"
            }
        ]
    },
    "communication": {
        "category": "Communication & Document Security",
        "icon": "📄",
        "items": [
            {
                "name": "Fireproof Document Bag",
                "examples": "EngPow Fireproof Bag, JUNDUN",
                "why": "Protects critical paperwork from ash, heat, and fire.",
                "quantity": "1 large bag",
                "priority": "Critical"
            },
            {
                "name": "Printed Maps (Not Digital)",
                "examples": "Regional road maps, topographic",
                "why": "Ash can disable GPS, cell towers, and satellites. Physical maps are essential for finding evacuation routes.",
                "quantity": "2-3 detailed maps",
                "priority": "High"
            },
            {
                "name": "Family Communication Plan (Printed)",
                "examples": "Laminated contact cards",
                "why": "If separated during evacuation, this ensures everyone knows where to regroup.",
                "quantity": "1 per person",
                "priority": "High"
            }
        ]
    },
    "clothing": {
        "category": "Shelter & Clothing",
        "icon": "👕",
        "items": [
            {
                "name": "Thick Cotton Clothing (Long Sleeve)",
                "examples": "Carhartt work shirts, denim",
                "why": "Synthetic fabrics melt when exposed to heat or volcanic ejecta.",
                "quantity": "2-3 sets per person",
                "priority": "High"
            },
            {
                "name": "Wool Socks",
                "examples": "Smartwool, Darn Tough",
                "why": "Keeps feet dry and warm even in wet ash conditions.",
                "quantity": "4-6 pairs per person",
                "priority": "High"
            },
            {
                "name": "Sturdy Boots",
                "examples": "Timberland, Merrell hiking boots",
                "why": "Ash makes surfaces slippery and rugged; sandals or sneakers are unsafe.",
                "quantity": "1 pair per person",
                "priority": "Critical"
            },
            {
                "name": "Wide-Brim Hat",
                "examples": "Columbia Bora Bora, REI Co-op",
                "why": "Prevents ash from falling into your face and eyes.",
                "quantity": "1 per person",
                "priority": "High"
            },
            {
                "name": "Sleeping Bag or Emergency Blanket",
                "examples": "Coleman 0°F, Swiss Safe Mylar",
                "why": "Shelters are often overcrowded; these provide comfort and insulation.",
                "quantity": "1 per person",
                "priority": "High"
            }
        ]
    },
    "sanitation": {
        "category": "Sanitation & Health",
        "icon": "🧼",
        "items": [
            {
                "name": "Wet Wipes & Hand Sanitizer",
                "examples": "Purell, Clorox wipes",
                "why": "Ash exposure irritates skin; cleaning prevents rashes and infections.",
                "quantity": "10+ packs wipes, 3 bottles sanitizer",
                "priority": "High"
            },
            {
                "name": "Saline Eye Wash",
                "examples": "Bausch & Lomb, Eye Wash Station",
                "why": "Removes ash particles from the eyes safely.",
                "quantity": "2-4 bottles",
                "priority": "High"
            },
            {
                "name": "Prescription Medications",
                "examples": "Your personal prescriptions",
                "why": "Pharmacies shut down quickly; volcanic ashfall affects supply chains.",
                "quantity": "2-4 weeks supply",
                "priority": "Critical"
            },
            {
                "name": "Inhalers / Respiratory Aids",
                "examples": "Albuterol rescue inhaler",
                "why": "Volcanic gases exacerbate asthma and lung issues.",
                "quantity": "2 backup inhalers if applicable",
                "priority": "Critical"
            }
        ]
    },
    "pets": {
        "category": "Pet Supplies",
        "icon": "🐾",
        "items": [
            {
                "name": "Pet Carrier",
                "examples": "Petmate, Sherpa",
                "why": "Shelters and evacuation centers require carriers for animals.",
                "quantity": "1 per pet",
                "priority": "Critical"
            },
            {
                "name": "Pet Food (2-3 Weeks)",
                "examples": "Purina, Blue Buffalo, Hill's",
                "why": "Pet food distribution will be disrupted during ashfall.",
                "quantity": "21+ days supply",
                "priority": "Critical"
            },
            {
                "name": "ID Tags + Microchip",
                "examples": "Current tags with contact info",
                "why": "Animals often flee during eruptions—ID increases recovery chances.",
                "quantity": "Updated tags on collar",
                "priority": "Critical"
            }
        ]
    }
}

VOLCANIC_ERUPTION_YELLOWSTONE = {
    # Include all regular volcanic items
    **VOLCANIC_ERUPTION_REGULAR,
    
    # Add Yellowstone-specific extended survival items
    "yellowstone_extended": {
        "category": "Yellowstone Supereruption - Extended Survival",
        "icon": "🟥",
        "items": [
            {
                "name": "Bulk Food Storage (3-6 Months)",
                "examples": "Augason Farms, Mountain House freeze-dried",
                "why": "Food scarcity becomes the main threat. Blue skies and normal crops will not return for many months. A supervolcano disrupts food production nationwide.",
                "quantity": "3-6 months supply per person",
                "priority": "Critical"
            },
            {
                "name": "High-Capacity Water Storage (30-100 Gallons)",
                "examples": "WaterPrepared tanks, SureWater barrels",
                "why": "Ash contaminates all surface water. Long-term storage is mandatory when water treatment facilities fail for months.",
                "quantity": "30-100 gallon capacity",
                "priority": "Critical"
            },
            {
                "name": "Indoor Grow Lights & Seeds",
                "examples": "SpiderFarmer LED, Mars Hydro, heirloom seeds",
                "why": "Sunlight will be minimal for months. Indoor gardening may become essential for fresh food.",
                "quantity": "2-4 grow lights + seed variety pack",
                "priority": "High"
            },
            {
                "name": "Full-Face Respirator Mask",
                "examples": "3M 6800, MIRA Safety CM-6M",
                "why": "Protects eyes + lungs from toxic ash when going outside during extended ashfall periods.",
                "quantity": "1 per adult + extra filters",
                "priority": "High"
            },
            {
                "name": "Home Air Filtration System (HEPA-Grade)",
                "examples": "IQAir HealthPro Plus, Blueair",
                "why": "Keeps indoor air breathable over long periods of ashfall. Standard purifiers won't last months.",
                "quantity": "2 industrial units + extra filters",
                "priority": "High"
            },
            {
                "name": "Alternative Heating Source",
                "examples": "Mr. Heater Buddy, Dyna-Glo propane heater",
                "why": "Volcanic winter = temperatures drop significantly. Grid power may fail for months.",
                "quantity": "1 heater + fuel supply",
                "priority": "Critical"
            },
            {
                "name": "Solar Generator + Panels",
                "examples": "Jackery 2000 Pro, EcoFlow Delta Pro",
                "why": "Grid power may be out for months. Solar provides renewable energy when fuel runs out.",
                "quantity": "1 large system (2000W+) + panels",
                "priority": "High"
            },
            {
                "name": "Self-Defense Tools",
                "examples": "Pepper spray (SABRE), security systems, tactical flashlight",
                "why": "In long-term catastrophic scenarios, crime rises rapidly and emergency services may be overwhelmed. You may need to defend supplies and prevent theft when law enforcement response is delayed.",
                "quantity": "Multiple defensive options per adult",
                "priority": "Medium"
            }
        ]
    }
}

# ==================== WILDFIRE CHECKLIST DATA ====================

WILDFIRE_CHECKLIST = {
    "critical": {
        "category": "Critical Priority Items (Must Have)",
        "icon": "🔥",
        "items": [
            {
                "name": "N95 / P100 Smoke Masks",
                "examples": "3M N95, Honeywell P100 respirator",
                "why": "Protects lungs from ash, smoke particles, and toxic debris. Without this, breathing becomes dangerous within minutes in heavy smoke.",
                "quantity": "Box of 20+ per person",
                "priority": "Critical"
            },
            {
                "name": "Go-Bag / Emergency Backpack",
                "examples": "5.11 Tactical Rush, REI Trail, Osprey",
                "why": "Keeps all essential items in one place so you can evacuate in under 2 minutes.",
                "quantity": "1 per person",
                "priority": "Critical"
            },
            {
                "name": "Portable Air Purifier",
                "examples": "Levoit Core 300, Coway AP-1512HH",
                "why": "If evacuation is delayed, helps remove smoke indoors to prevent respiratory damage.",
                "quantity": "1-2 units",
                "priority": "Critical"
            },
            {
                "name": "Fire-Resistant Document Bag",
                "examples": "EngPow Fireproof Bag, JUNDUN",
                "why": "Protects passports, birth certificates, insurance papers—critical after a home loss.",
                "quantity": "1 large bag",
                "priority": "Critical"
            },
            {
                "name": "Comprehensive First Aid Kit",
                "examples": "Adventure Medical Kits, Surviveware",
                "why": "Smoke exposure increases heart/lung strain; you may also encounter burns, cuts, or injuries during evacuation.",
                "quantity": "1 large kit (200+ pieces)",
                "priority": "Critical"
            },
            {
                "name": "Phone Power Bank / Solar Charger",
                "examples": "Anker PowerCore 20,000mAh, Goal Zero",
                "why": "Cell towers may remain active but electricity won't. Communication is life-saving.",
                "quantity": "2-3 power banks + 1 solar charger",
                "priority": "Critical"
            },
            {
                "name": "Battery-Powered Emergency Radio",
                "examples": "Midland WR120, Sangean",
                "why": "Essential for evacuation orders and real-time fire updates when cell networks fail.",
                "quantity": "1-2 radios",
                "priority": "Critical"
            },
            {
                "name": "Flashlights + Headlamp",
                "examples": "Maglite, Black Diamond headlamp",
                "why": "Visibility drops quickly in smoke-filled areas and evacuation at night is common.",
                "quantity": "1 per person + extras",
                "priority": "Critical"
            },
            {
                "name": "Cash (Small Bills)",
                "examples": "$200-500 in $1, $5, $10, $20 bills",
                "why": "ATMs and card systems frequently fail during evacuations.",
                "quantity": "$200-500",
                "priority": "Critical"
            }
        ]
    },
    "water": {
        "category": "Water & Hydration",
        "icon": "💧",
        "items": [
            {
                "name": "Water Jugs / Bottled Water",
                "examples": "Arrowhead, Dasani, Aquafina",
                "why": "Wildfires often contaminate local water systems; you cannot depend on tap water.",
                "quantity": "1 gallon per person per day × 7 days",
                "priority": "Critical"
            },
            {
                "name": "Electrolyte Drinks",
                "examples": "Gatorade, Pedialyte, Liquid I.V.",
                "why": "Heat + stress + smoke = rapid dehydration. Electrolytes prevent medical emergencies.",
                "quantity": "12+ bottles or 30+ packets",
                "priority": "High"
            },
            {
                "name": "Water Filter Bottle",
                "examples": "LifeStraw Go, Brita filtered bottle",
                "why": "Useful if you run low on clean water in evacuation shelters or roadside stops.",
                "quantity": "1 per person",
                "priority": "Medium"
            }
        ]
    },
    "food": {
        "category": "Food (1 Week, Shelf-Stable)",
        "icon": "🥫",
        "items": [
            {
                "name": "Canned Soup",
                "examples": "Campbell's, Progresso",
                "why": "Easy, comforting calories that heat quickly and help maintain energy.",
                "quantity": "12-18 cans",
                "priority": "High"
            },
            {
                "name": "Canned Vegetables",
                "examples": "Del Monte, Green Giant",
                "why": "Provides hydration + vitamins when fresh food is unavailable.",
                "quantity": "12+ cans",
                "priority": "High"
            },
            {
                "name": "Canned Meats",
                "examples": "Spam, Swanson chicken",
                "why": "High-protein food that stores well and can be eaten cold if needed.",
                "quantity": "12+ cans",
                "priority": "High"
            },
            {
                "name": "Protein Bars",
                "examples": "Clif Bar, RXBar, Quest",
                "why": "Designed for quick evacuation—lightweight, filling, long-lasting.",
                "quantity": "30+ bars",
                "priority": "High"
            },
            {
                "name": "Peanut Butter",
                "examples": "Jif, Skippy, natural brands",
                "why": "High-fat, high-calorie survival food that requires no refrigeration.",
                "quantity": "2-3 large jars",
                "priority": "High"
            },
            {
                "name": "Tuna Pouches",
                "examples": "StarKist, Bumble Bee",
                "why": "Good lean protein, lighter than cans, easy to eat on the move.",
                "quantity": "12+ pouches",
                "priority": "High"
            },
            {
                "name": "Instant Rice",
                "examples": "Minute Rice, Uncle Ben's",
                "why": "Cooks with minimal water and fuel—important during evacuations.",
                "quantity": "5+ boxes",
                "priority": "Medium"
            },
            {
                "name": "Instant Mashed Potatoes",
                "examples": "Idahoan, Betty Crocker",
                "why": "High-calorie comfort food requiring little water and heat.",
                "quantity": "4+ boxes",
                "priority": "Medium"
            },
            {
                "name": "Trail Mix",
                "examples": "Planters, Kar's Nuts",
                "why": "Dense energy source with long shelf life; ideal for emergency travel.",
                "quantity": "3-5 large bags",
                "priority": "High"
            },
            {
                "name": "Crackers",
                "examples": "Ritz, Saltines, Wheat Thins",
                "why": "Easy carbs to pair with peanut butter or canned items.",
                "quantity": "3-5 boxes",
                "priority": "Medium"
            },
            {
                "name": "Shelf-Stable Milk",
                "examples": "Horizon, Silk, Lactaid UHT",
                "why": "Useful for kids, cereal, oatmeal, and adds nutrition.",
                "quantity": "6-12 cartons",
                "priority": "Medium"
            },
            {
                "name": "Pasta",
                "examples": "Barilla, De Cecco",
                "why": "Good bulk calories if you have a portable stove available.",
                "quantity": "5 pounds",
                "priority": "Medium"
            },
            {
                "name": "Jarred Pasta Sauce",
                "examples": "Prego, Rao's, Bertolli",
                "why": "Makes meals filling and familiar during disaster stress.",
                "quantity": "4-6 jars",
                "priority": "Low"
            },
            {
                "name": "Oatmeal Packets",
                "examples": "Quaker Instant Oatmeal",
                "why": "Requires minimal water and heats quickly; easy on the stomach.",
                "quantity": "2-3 boxes",
                "priority": "Medium"
            }
        ]
    },
    "tools": {
        "category": "Tools & Gear",
        "icon": "🔧",
        "items": [
            {
                "name": "Fire Extinguisher (ABC-Rated)",
                "examples": "Kidde, First Alert 10-lb",
                "why": "Useful for embers landing on property or vehicle during escape.",
                "quantity": "1-2 extinguishers",
                "priority": "Critical"
            },
            {
                "name": "Multi-Tool",
                "examples": "Leatherman Wave+, Gerber",
                "why": "Allows you to cut seat belts, open cans, or repair gear on the move.",
                "quantity": "1-2",
                "priority": "High"
            },
            {
                "name": "Portable Camp Stove + Fuel",
                "examples": "Jetboil Flash, Coleman butane",
                "why": "Necessary for cooking if power is out or you're sheltering outdoors.",
                "quantity": "1 stove + 6-12 fuel canisters",
                "priority": "High"
            },
            {
                "name": "Heat-Resistant Gloves",
                "examples": "OZERO, Ironclad heat-resistant",
                "why": "Useful for handling hot items, clearing debris, or moving burning materials.",
                "quantity": "2 pairs",
                "priority": "High"
            },
            {
                "name": "Emergency Blanket / Reflective Blanket",
                "examples": "Swiss Safe Mylar, SOL",
                "why": "Keeps you warm when weather drops at night during evacuation.",
                "quantity": "2 per person",
                "priority": "Medium"
            },
            {
                "name": "Durable Water-Resistant Boots",
                "examples": "Merrell, Timberland, Columbia",
                "why": "You may walk through ash, debris, or wet terrain during escape.",
                "quantity": "1 pair per person",
                "priority": "High"
            },
            {
                "name": "Safety Goggles",
                "examples": "DEWALT, Pyramex sealed goggles",
                "why": "Protects eyes from smoke, ash, and wind gusts.",
                "quantity": "1 per person",
                "priority": "High"
            },
            {
                "name": "Emergency Whistle",
                "examples": "Shoreline Marine, Coghlan's",
                "why": "Used to signal for help when visibility is low from smoke.",
                "quantity": "1 per person",
                "priority": "Medium"
            }
        ]
    },
    "communication": {
        "category": "Communication & Information",
        "icon": "📱",
        "items": [
            {
                "name": "Printed Evacuation Map",
                "examples": "Local area map with marked routes",
                "why": "GPS may fail due to tower outages or blocked roads.",
                "quantity": "2-3 copies",
                "priority": "High"
            },
            {
                "name": "Family Communication Card",
                "examples": "Laminated card with contacts",
                "why": "Ensures everyone has emergency contacts if separated.",
                "quantity": "1 per person",
                "priority": "High"
            },
            {
                "name": "Pre-Written Emergency Plan",
                "examples": "Printed meeting points, routes",
                "why": "Helps you stay organized under extreme stress.",
                "quantity": "Multiple copies",
                "priority": "Medium"
            }
        ]
    },
    "clothing": {
        "category": "Shelter & Clothing",
        "icon": "👕",
        "items": [
            {
                "name": "Fire-Resistant Jacket / Heavy Cotton Layers",
                "examples": "Carhartt, Wrangler denim",
                "why": "Synthetic materials can melt in high heat; heavy cotton protects skin.",
                "quantity": "1-2 per person",
                "priority": "High"
            },
            {
                "name": "Change of Clothes (2-3 Sets)",
                "examples": "Cotton t-shirts, jeans, underwear",
                "why": "Your clothes may become smoke-soaked and harmful to breathe.",
                "quantity": "2-3 complete sets per person",
                "priority": "High"
            },
            {
                "name": "Wool Socks",
                "examples": "Smartwool, Darn Tough",
                "why": "Reduces blisters and stays warm even when damp.",
                "quantity": "4-6 pairs per person",
                "priority": "Medium"
            },
            {
                "name": "Wide-Brim Hat",
                "examples": "Columbia Bora Bora, REI sun hat",
                "why": "Protects from falling ash and reduces heat exposure.",
                "quantity": "1 per person",
                "priority": "Medium"
            },
            {
                "name": "Sleeping Bag",
                "examples": "Coleman, Teton Sports",
                "why": "Shelters may be crowded; you may end up camping outdoors.",
                "quantity": "1 per person",
                "priority": "High"
            }
        ]
    },
    "sanitation": {
        "category": "Sanitation & Health",
        "icon": "🧼",
        "items": [
            {
                "name": "Wet Wipes",
                "examples": "Clorox wipes, Cottonelle",
                "why": "Helps clean soot and ash off skin to prevent irritation.",
                "quantity": "5+ packs",
                "priority": "High"
            },
            {
                "name": "Hand Sanitizer",
                "examples": "Purell (70%+ alcohol)",
                "why": "Evacuation shelters can be crowded; reduces illness risk.",
                "quantity": "3+ large bottles",
                "priority": "High"
            },
            {
                "name": "Dustpan + Small Broom",
                "examples": "O-Cedar, Libman compact",
                "why": "Useful in your car or tent to remove ash buildup.",
                "quantity": "1 set",
                "priority": "Low"
            },
            {
                "name": "Prescription Medications",
                "examples": "Your personal medications",
                "why": "Pharmacies may be closed or destroyed.",
                "quantity": "7-14 days supply minimum",
                "priority": "Critical"
            },
            {
                "name": "Inhaler / Breathing Aid",
                "examples": "Albuterol, rescue inhaler",
                "why": "Smoke aggravates all respiratory conditions.",
                "quantity": "2 backups if applicable",
                "priority": "Critical"
            }
        ]
    },
    "pets": {
        "category": "Pet Supplies",
        "icon": "🐾",
        "items": [
            {
                "name": "Pet Carrier",
                "examples": "Petmate, Sherpa",
                "why": "Required for shelter access.",
                "quantity": "1 per pet",
                "priority": "Critical"
            },
            {
                "name": "Pet Food (1-2 Weeks)",
                "examples": "Purina, Blue Buffalo, Hill's",
                "why": "Stores and shelters may run out quickly.",
                "quantity": "14+ days supply",
                "priority": "Critical"
            },
            {
                "name": "Leash + Spare Collar + Tags",
                "examples": "Any durable brand with ID tags",
                "why": "Animals flee during wildfires; ID is crucial.",
                "quantity": "2 leashes, 2 collars with current tags",
                "priority": "Critical"
            }
        ]
    }
}

# ==================== NUCLEAR FALLOUT CHECKLIST DATA ====================

NUCLEAR_FALLOUT_CHECKLIST = {
    "water": {
        "category": "Water & Hydration",
        "icon": "💧",
        "items": [
            {
                "name": "Bottled Water (High Quantity)",
                "examples": "Smartwater, Dasani, Aquafina",
                "why": "Fallout contaminates water sources. You must avoid all untreated outdoor water.",
                "quantity": "2 gallons per person per day × 14 days minimum",
                "priority": "Critical"
            },
            {
                "name": "Large Water Containers (7-gallon+)",
                "examples": "Reliance Aqua-Tainer, WaterBrick",
                "why": "Allows storage in case municipal water is disabled or rationed.",
                "quantity": "3-5 containers (35+ gallons total)",
                "priority": "Critical"
            },
            {
                "name": "Water Filter (Carbon Filtration)",
                "examples": "Sawyer Mini, Berkey Water Filter",
                "why": "Filters particulates, debris, and many contaminants (not radiation itself). Still necessary when bottled water runs low.",
                "quantity": "1-2 high-quality filters",
                "priority": "High"
            },
            {
                "name": "Water Purification Tablets",
                "examples": "Potable Aqua, Aquatabs",
                "why": "Provides backup treatment for questionable water sources.",
                "quantity": "100+ tablets",
                "priority": "High"
            }
        ]
    },
    "food": {
        "category": "Food Storage (Long-Term Scarcity)",
        "icon": "🥫",
        "items": [
            {
                "name": "Canned Soup",
                "examples": "Campbell's, Progresso",
                "why": "Grocery stores may not be restocked for months. Nuclear winter lowers crop yields globally.",
                "quantity": "24+ cans",
                "priority": "Critical"
            },
            {
                "name": "Canned Vegetables",
                "examples": "Del Monte, Green Giant",
                "why": "Long shelf life, essential nutrients when fresh food is unavailable.",
                "quantity": "24+ cans",
                "priority": "Critical"
            },
            {
                "name": "Canned Meats",
                "examples": "Spam, Swanson chicken, Vienna sausages",
                "why": "Protein source that doesn't require refrigeration.",
                "quantity": "18+ cans",
                "priority": "Critical"
            },
            {
                "name": "Rice",
                "examples": "Mahatma, Ben's Original",
                "why": "Calorie-dense, stores for years, filling.",
                "quantity": "20+ pounds",
                "priority": "Critical"
            },
            {
                "name": "Pasta",
                "examples": "Barilla, De Cecco",
                "why": "Long shelf life, easy to prepare, high carbohydrates.",
                "quantity": "10+ pounds",
                "priority": "Critical"
            },
            {
                "name": "Instant Mashed Potatoes",
                "examples": "Idahoan, Betty Crocker",
                "why": "Quick to prepare, filling, long shelf life.",
                "quantity": "5+ boxes",
                "priority": "High"
            },
            {
                "name": "Protein Bars",
                "examples": "Clif Bar, RXBar, Quest",
                "why": "Portable, no preparation needed, long shelf life.",
                "quantity": "40+ bars",
                "priority": "High"
            },
            {
                "name": "Peanut Butter",
                "examples": "Jif, Skippy, natural brands",
                "why": "High protein, high calories, doesn't need refrigeration.",
                "quantity": "4-6 large jars",
                "priority": "Critical"
            },
            {
                "name": "Shelf-Stable Milk",
                "examples": "Horizon Organic, Lactaid UHT",
                "why": "Dairy nutrition when refrigeration isn't available.",
                "quantity": "12+ cartons",
                "priority": "Medium"
            }
        ]
    },
    "light_power": {
        "category": "Light & Power",
        "icon": "🔦",
        "items": [
            {
                "name": "LED Flashlights",
                "examples": "Coast, Energizer, Maglite",
                "why": "Essential when infrastructure collapses.",
                "quantity": "1 per person + 3 extras",
                "priority": "Critical"
            },
            {
                "name": "LED Lanterns",
                "examples": "Vont, Coleman, Etekcity",
                "why": "Provides room illumination in bunkers, basements, or shelters.",
                "quantity": "3-5 lanterns",
                "priority": "Critical"
            },
            {
                "name": "Headlamps",
                "examples": "Black Diamond, Petzl",
                "why": "Hands-free lighting for repairs or movement.",
                "quantity": "1-2 per adult",
                "priority": "High"
            },
            {
                "name": "Batteries (Case-Protected)",
                "examples": "Duracell, Energizer",
                "why": "Radiation can damage exposed batteries; keep them sealed.",
                "quantity": "100+ batteries (various sizes)",
                "priority": "Critical"
            },
            {
                "name": "Power Banks",
                "examples": "Anker PowerCore 20,000+ mAh",
                "why": "Temporary power for phones, radios, and lights.",
                "quantity": "3-4 high-capacity banks",
                "priority": "High"
            },
            {
                "name": "Hand-Crank Radio with NOAA",
                "examples": "Midland ER310, Kaito Voyager",
                "why": "Critical for emergency broadcasts and fallout announcements.",
                "quantity": "2 radios",
                "priority": "Critical"
            }
        ]
    },
    "nuclear_gear": {
        "category": "Nuclear-Specific Gear",
        "icon": "☢️",
        "items": [
            {
                "name": "Potassium Iodide Tablets (KI)",
                "examples": "IOSAT, ThyroSafe",
                "why": "Protects the thyroid from radioactive iodine exposure.",
                "quantity": "14+ tablets per person",
                "priority": "Critical"
            },
            {
                "name": "N95/N100 Respirators",
                "examples": "3M N95, N100 masks",
                "why": "Reduces inhalation of radioactive dust particles.",
                "quantity": "Box of 20+ per person",
                "priority": "Critical"
            },
            {
                "name": "Full-Face Respirator (Optional)",
                "examples": "3M 6800, MIRA Safety CM-6M",
                "why": "Offers significantly better protection during fallout movement.",
                "quantity": "1 per adult (optional)",
                "priority": "High"
            },
            {
                "name": "Radiation Dosimeter",
                "examples": "RADEX RD1503+, GQ Electronics",
                "why": "Tracks exposure levels to avoid entering high-radiation zones.",
                "quantity": "1 per household minimum",
                "priority": "High"
            },
            {
                "name": "Geiger Counter",
                "examples": "SOEKS 112, GQ GMC-320",
                "why": "Measures contaminated areas, food, and surfaces.",
                "quantity": "1 per household",
                "priority": "Medium"
            },
            {
                "name": "Heavy-Duty Plastic Sheeting",
                "examples": "Husky 6-mil plastic",
                "why": "Used to seal doors/windows to block contaminated air.",
                "quantity": "2-3 large rolls",
                "priority": "Critical"
            },
            {
                "name": "Duct Tape",
                "examples": "Gorilla Tape, 3M",
                "why": "Secures the plastic and reinforces shelter openings.",
                "quantity": "4-6 rolls",
                "priority": "Critical"
            },
            {
                "name": "Tarps (Heavy-Duty)",
                "examples": "Amazon Basics, Blue Hawk",
                "why": "Covers items outside or creates makeshift containment rooms.",
                "quantity": "3-4 large tarps",
                "priority": "High"
            },
            {
                "name": "Lead-Lined Document Pouch",
                "examples": "Moko Faraday bag, KIZN",
                "why": "Protects electronics, IDs, and cash from radiation exposure.",
                "quantity": "1-2 pouches",
                "priority": "Medium"
            }
        ]
    },
    "security": {
        "category": "Protection & Security",
        "icon": "🛡️",
        "items": [
            {
                "name": "Self-Defense Tools",
                "examples": "Pepper spray (SABRE), tactical flashlight, personal alarm",
                "why": "After a nuclear event, panic-driven violence increases. Food scarcity and lack of government response make households targets. Self-defense options provide deterrents.",
                "quantity": "Multiple options per adult",
                "priority": "High"
            },
            {
                "name": "Door Reinforcement",
                "examples": "Security bar, door jammer",
                "why": "Secures entry points when law enforcement is unavailable.",
                "quantity": "1 per entry door",
                "priority": "High"
            },
            {
                "name": "Motion Sensor Lights (Solar)",
                "examples": "Aootek, Baxia Technology",
                "why": "Deters intruders when grid power is down.",
                "quantity": "4-6 lights",
                "priority": "Medium"
            },
            {
                "name": "Weapon Light (if applicable)",
                "examples": "Streamlight, SureFire",
                "why": "Improves visibility in dark, powerless environments.",
                "quantity": "1 per defensive tool",
                "priority": "Low"
            }
        ]
    },
    "sanitation": {
        "category": "Hygiene & Sanitation",
        "icon": "🚽",
        "items": [
            {
                "name": "Baby Wipes",
                "examples": "Huggies, Pampers",
                "why": "Maintains hygiene when showers aren't available.",
                "quantity": "10+ packs",
                "priority": "High"
            },
            {
                "name": "Hand Sanitizer",
                "examples": "Purell (70%+ alcohol)",
                "why": "Stops bacteria spread when water is limited.",
                "quantity": "5+ large bottles",
                "priority": "High"
            },
            {
                "name": "Contractor Trash Bags",
                "examples": "Husky 42-gallon",
                "why": "Used for waste disposal, debris, and contaminated materials.",
                "quantity": "Box of 100+",
                "priority": "High"
            },
            {
                "name": "Bleach",
                "examples": "Clorox Regular",
                "why": "Disinfects surfaces exposed to fallout dust.",
                "quantity": "2 gallons",
                "priority": "High"
            },
            {
                "name": "Paper Plates & Utensils",
                "examples": "Dixie, Hefty",
                "why": "Removes dishwashing dependence.",
                "quantity": "200+ plates, utensils",
                "priority": "Medium"
            }
        ]
    },
    "medical": {
        "category": "First Aid & Medical",
        "icon": "🩹",
        "items": [
            {
                "name": "Comprehensive First Aid Kit",
                "examples": "Adventure Medical Kits, Swiss Safe",
                "why": "Treats cuts, burns, and debris injuries.",
                "quantity": "1 large kit (300+ pieces)",
                "priority": "Critical"
            },
            {
                "name": "Trauma Bandage",
                "examples": "Israeli Bandage",
                "why": "Critical for serious bleeding.",
                "quantity": "4-6",
                "priority": "High"
            },
            {
                "name": "Burn Gel",
                "examples": "Water-Jel burn gel",
                "why": "Treats burns from fires, radiation exposure, or explosions.",
                "quantity": "3-5 packets",
                "priority": "High"
            },
            {
                "name": "Antibiotic Ointment",
                "examples": "Neosporin, Bacitracin",
                "why": "Prevents wound infection in unsanitary environments.",
                "quantity": "3-5 tubes",
                "priority": "High"
            },
            {
                "name": "Pain Relievers",
                "examples": "Advil (ibuprofen), Tylenol (acetaminophen)",
                "why": "Reduces discomfort and fever.",
                "quantity": "2 bottles each",
                "priority": "Medium"
            },
            {
                "name": "Electrolyte Packets",
                "examples": "Liquid I.V., Gatorade powder",
                "why": "Prevents dehydration when stress and food scarcity spike.",
                "quantity": "50+ packets",
                "priority": "High"
            }
        ]
    },
    "shelter": {
        "category": "Shelter & Home Defense",
        "icon": "🏠",
        "items": [
            {
                "name": "Sleeping Bags (Cold-Rated)",
                "examples": "Coleman 0°F, Teton Sports",
                "why": "Provide warmth as temperatures drop in nuclear winter.",
                "quantity": "1 per person",
                "priority": "Critical"
            },
            {
                "name": "Wool Blankets",
                "examples": "Pendleton, Swiss Army surplus",
                "why": "Retains heat even in cold, dark conditions.",
                "quantity": "2 per person",
                "priority": "High"
            },
            {
                "name": "LED Candles (Battery-Powered)",
                "examples": "Hyoola flameless candles",
                "why": "Emergency lighting that reduces risk of fire in enclosed spaces.",
                "quantity": "12+ candles",
                "priority": "Medium"
            },
            {
                "name": "Multi-Tool",
                "examples": "Leatherman Wave+, Gerber",
                "why": "Handles repairs and improvisation.",
                "quantity": "2-3 tools",
                "priority": "High"
            },
            {
                "name": "Work Gloves",
                "examples": "Mechanix Wear, Wells Lamont",
                "why": "Protects your hands when clearing debris.",
                "quantity": "3-4 pairs",
                "priority": "High"
            }
        ]
    },
    "documents": {
        "category": "Documents & Communication",
        "icon": "📄",
        "items": [
            {
                "name": "Printed ID Copies",
                "examples": "Stored in waterproof pouch",
                "why": "Phones may die; radiation can corrupt electronics.",
                "quantity": "Multiple copies of all IDs",
                "priority": "Critical"
            },
            {
                "name": "Waterproof Document Pouch",
                "examples": "SentrySafe fireproof/waterproof bag",
                "why": "Protects critical paperwork.",
                "quantity": "1 large pouch",
                "priority": "Critical"
            },
            {
                "name": "Walkie Talkies",
                "examples": "Midland GXT1000, Motorola T600",
                "why": "Essential when cell networks fail for days.",
                "quantity": "4-6 radios",
                "priority": "High"
            },
            {
                "name": "Notebook + Pencils",
                "examples": "Rite in the Rain notebook",
                "why": "Lets you record radiation times, tasks, and contact attempts.",
                "quantity": "2-3 notebooks + pencils",
                "priority": "Medium"
            }
        ]
    },
    "vehicle": {
        "category": "Vehicle Prep",
        "icon": "🚗",
        "items": [
            {
                "name": "Full Tank of Gas",
                "examples": "Fill immediately when alert issued",
                "why": "Fuel availability collapses instantly.",
                "quantity": "Full tank always",
                "priority": "Critical"
            },
            {
                "name": "Portable Gas Can",
                "examples": "Eagle, No-Spill 5-gallon",
                "why": "Backup supply for evac routes.",
                "quantity": "2-3 cans (10-15 gallons)",
                "priority": "High"
            },
            {
                "name": "Jumper Cables",
                "examples": "Energizer 20-ft",
                "why": "Keeps your vehicle operational.",
                "quantity": "1 set",
                "priority": "High"
            },
            {
                "name": "Emergency Road Kit",
                "examples": "AAA Emergency Kit",
                "why": "Includes flares, tools, and safety equipment.",
                "quantity": "1 kit",
                "priority": "Medium"
            },
            {
                "name": "Car Phone Charger",
                "examples": "Anker USB car charger",
                "why": "Maintains communication until towers fail.",
                "quantity": "2 chargers",
                "priority": "High"
            }
        ]
    }
}

# ==================== EARTHQUAKE CHECKLIST DATA ====================

EARTHQUAKE_WARM_CLIMATE = {
    "water": {
        "category": "Water & Hydration",
        "icon": "💧",
        "items": [
            {
                "name": "Bottled Water",
                "examples": "Arrowhead, Dasani",
                "why": "Pipes break during earthquakes, making tap water unsafe or unavailable.",
                "quantity": "1 gallon per person per day × 7 days",
                "priority": "Critical"
            },
            {
                "name": "Water Storage Jugs",
                "examples": "Reliance Aqua-Tainer, Coleman",
                "why": "Gives you backup storage if water is restored briefly but inconsistently.",
                "quantity": "2-3 large containers (5-7 gallons each)",
                "priority": "Critical"
            },
            {
                "name": "Water Filter",
                "examples": "Sawyer Mini, LifeStraw",
                "why": "In case you must rely on questionable water sources.",
                "quantity": "1-2 per household",
                "priority": "High"
            },
            {
                "name": "Purification Tablets",
                "examples": "Potable Aqua",
                "why": "Essential if water becomes contaminated from ruptured lines.",
                "quantity": "50-100 tablets",
                "priority": "Medium"
            }
        ]
    },
    "food": {
        "category": "Food Storage",
        "icon": "🥫",
        "items": [
            {
                "name": "Canned Soup/Chili",
                "examples": "Campbell's, Progresso",
                "why": "Ready-to-eat meals that don't require refrigeration.",
                "quantity": "12-24 cans",
                "priority": "High"
            },
            {
                "name": "Canned Protein",
                "examples": "StarKist tuna, Chicken of the Sea",
                "why": "Long shelf life, high protein, no refrigeration needed.",
                "quantity": "12-18 cans",
                "priority": "High"
            },
            {
                "name": "Pasta/Rice",
                "examples": "Barilla pasta, Mahatma rice",
                "why": "Filling, calorie-dense, stores well.",
                "quantity": "5-10 pounds",
                "priority": "High"
            },
            {
                "name": "Peanut Butter",
                "examples": "Jif, Skippy",
                "why": "High protein and calories, doesn't need refrigeration.",
                "quantity": "2-3 jars",
                "priority": "High"
            },
            {
                "name": "Energy Bars",
                "examples": "Nature Valley, Clif Bar",
                "why": "Portable, long shelf life, quick energy.",
                "quantity": "20-40 bars",
                "priority": "Medium"
            }
        ]
    },
    "light_power": {
        "category": "Light & Power",
        "icon": "🔦",
        "items": [
            {
                "name": "LED Flashlights",
                "examples": "Energizer, Coast",
                "why": "Quakes often knock out power for days; safe and dependable lighting is crucial.",
                "quantity": "1 per person + 2 extras",
                "priority": "Critical"
            },
            {
                "name": "LED Lanterns",
                "examples": "Vont, Etekcity",
                "why": "Lights up full rooms when overhead lights fail.",
                "quantity": "2-4 lanterns",
                "priority": "Critical"
            },
            {
                "name": "Headlamps",
                "examples": "Petzl, Black Diamond",
                "why": "Hands-free light for navigating debris or performing repairs.",
                "quantity": "1-2 per adult",
                "priority": "High"
            },
            {
                "name": "Batteries (Various Sizes)",
                "examples": "Duracell, Energizer",
                "why": "Extra batteries ensure your lights and radios keep working.",
                "quantity": "48+ batteries (AA, AAA, D)",
                "priority": "Critical"
            },
            {
                "name": "Power Banks",
                "examples": "Anker PowerCore",
                "why": "Keeps your phone operational when power grids fail.",
                "quantity": "2-3 (10,000+ mAh each)",
                "priority": "High"
            },
            {
                "name": "Solar Charger",
                "examples": "BigBlue, Goal Zero",
                "why": "Reliable long-term power if outages last a week or more.",
                "quantity": "1 panel (20W+)",
                "priority": "Medium"
            }
        ]
    },
    "earthquake_gear": {
        "category": "Earthquake-Specific Gear",
        "icon": "🏚️",
        "items": [
            {
                "name": "Sturdy Shoes or Boots",
                "examples": "Merrell, Columbia hiking boots",
                "why": "Broken glass and debris are everywhere after a quake.",
                "quantity": "1 pair per person",
                "priority": "Critical"
            },
            {
                "name": "Work Gloves",
                "examples": "Mechanix Wear, Venom Steel",
                "why": "Protects your hands while clearing debris or moving items.",
                "quantity": "2-4 pairs",
                "priority": "Critical"
            },
            {
                "name": "N95 Dust Masks",
                "examples": "3M N95 respirator",
                "why": "Protects from dust, insulation, and particles shaken loose.",
                "quantity": "Box of 20+",
                "priority": "High"
            },
            {
                "name": "Emergency Whistle",
                "examples": "Storm All-Weather Safety Whistle",
                "why": "Used for signaling rescuers if trapped.",
                "quantity": "1 per person",
                "priority": "Critical"
            },
            {
                "name": "Crowbar / Pry Bar",
                "examples": "Stanley Wonder Bar, Estwing",
                "why": "Helps open jammed doors or move blocked objects.",
                "quantity": "1-2",
                "priority": "High"
            },
            {
                "name": "Emergency Gas Shut-Off Tool",
                "examples": "Kensizer, On Duty Tool",
                "why": "Prevents gas leaks that can lead to explosions or fires.",
                "quantity": "1 tool",
                "priority": "Critical"
            },
            {
                "name": "Fire Extinguisher",
                "examples": "First Alert, Amerex ABC",
                "why": "Vital for small fires when firefighters are overwhelmed.",
                "quantity": "1-2 (10 lb ABC rated)",
                "priority": "Critical"
            },
            {
                "name": "Hard Hat",
                "examples": "3M, Pyramex",
                "why": "Protects your head from falling debris during aftershocks.",
                "quantity": "1 per adult",
                "priority": "High"
            },
            {
                "name": "Emergency NOAA Radio",
                "examples": "Midland WR120, Kaito Voyager",
                "why": "Provides updates when cell service is disrupted.",
                "quantity": "1-2 radios",
                "priority": "Critical"
            }
        ]
    },
    "sanitation": {
        "category": "Hygiene & Sanitation",
        "icon": "🚽",
        "items": [
            {
                "name": "Baby Wipes",
                "examples": "Huggies, Pampers",
                "why": "Useful if plumbing or water service is disabled.",
                "quantity": "3-6 packs",
                "priority": "High"
            },
            {
                "name": "Hand Sanitizer",
                "examples": "Purell (70%+ alcohol)",
                "why": "Prevents infection when clean water is limited.",
                "quantity": "2-3 large bottles",
                "priority": "High"
            },
            {
                "name": "Heavy-Duty Trash Bags",
                "examples": "Husky contractor bags",
                "why": "Stores debris, waste, and damaged items.",
                "quantity": "Box of 50+",
                "priority": "Medium"
            },
            {
                "name": "Paper Plates & Plastic Utensils",
                "examples": "Dixie, Hefty",
                "why": "Reduces the need for washing dishes without running water.",
                "quantity": "50-100 plates, forks, spoons",
                "priority": "Medium"
            },
            {
                "name": "Portable Toilet Bags",
                "examples": "Reliance Double Doodie bags",
                "why": "Plumbing may become unusable after structural damage.",
                "quantity": "50+ bags",
                "priority": "High"
            }
        ]
    },
    "medical": {
        "category": "First Aid",
        "icon": "🩹",
        "items": [
            {
                "name": "Comprehensive First Aid Kit",
                "examples": "Swiss Safe 2-in-1, Johnson & Johnson",
                "why": "Treats cuts, punctures, and debris-related injuries.",
                "quantity": "1 kit (200+ pieces)",
                "priority": "Critical"
            },
            {
                "name": "Trauma Bandage",
                "examples": "Israeli Bandage",
                "why": "Critical for severe bleeding when emergency services are delayed.",
                "quantity": "2-4",
                "priority": "High"
            },
            {
                "name": "Antiseptic Wipes",
                "examples": "Wet Ones, Purell wipes",
                "why": "Keeps wounds clean if water isn't available.",
                "quantity": "100+ wipes",
                "priority": "High"
            },
            {
                "name": "Pain Relievers",
                "examples": "Tylenol, Advil",
                "why": "Useful for muscle soreness after heavy physical activity.",
                "quantity": "1-2 bottles each",
                "priority": "Medium"
            },
            {
                "name": "Tweezers",
                "examples": "Revlon, Tweezerman",
                "why": "Removes splinters and small debris.",
                "quantity": "1-2",
                "priority": "Low"
            }
        ]
    },
    "home_repair": {
        "category": "Home Safety & Repair",
        "icon": "🔧",
        "items": [
            {
                "name": "LED Candles (Battery-Powered)",
                "examples": "Hyoola, Homemory LED candles",
                "why": "Backup lighting that doesn't risk fire in unstable buildings.",
                "quantity": "6-12 candles",
                "priority": "Medium"
            },
            {
                "name": "Duct Tape",
                "examples": "Gorilla Tape, 3M",
                "why": "Temporary repairs for cracks or broken items.",
                "quantity": "2-3 rolls",
                "priority": "High"
            },
            {
                "name": "Zip Ties",
                "examples": "Velcro Brand, heavy-duty cable ties",
                "why": "Fastens loose items or creates makeshift repairs.",
                "quantity": "100+ pack",
                "priority": "Medium"
            },
            {
                "name": "Plastic Sheeting",
                "examples": "Husky heavy-duty plastic",
                "why": "Covers broken windows or creates temporary barriers.",
                "quantity": "2-3 large rolls",
                "priority": "High"
            },
            {
                "name": "Wrench Set / Multi-Tool",
                "examples": "Leatherman Wave+, Gerber",
                "why": "Useful for quick repairs around the home.",
                "quantity": "1-2",
                "priority": "High"
            },
            {
                "name": "Bungee Cords",
                "examples": "Erickson, Keeper",
                "why": "Secures items that might fall during aftershocks.",
                "quantity": "Set of 8-12",
                "priority": "Medium"
            }
        ]
    },
    "documents": {
        "category": "Documents & Communication",
        "icon": "📄",
        "items": [
            {
                "name": "Printed Copies of IDs & Insurance Papers",
                "examples": "Stored in SentrySafe fireproof pouch",
                "why": "Insurance claims require physical copies if electronics are damaged.",
                "quantity": "1 waterproof/fireproof pouch",
                "priority": "Critical"
            },
            {
                "name": "Walkie Talkies",
                "examples": "Motorola T600, Midland GXT1000",
                "why": "Communicates with family when cell networks go down.",
                "quantity": "2-4 radios",
                "priority": "Medium"
            },
            {
                "name": "Waterproof Notebook",
                "examples": "Rite in the Rain",
                "why": "Useful for recording important information when phones are dead.",
                "quantity": "1-2 notebooks",
                "priority": "Low"
            }
        ]
    },
    "vehicle": {
        "category": "Vehicle Prep",
        "icon": "🚗",
        "items": [
            {
                "name": "Full Tank of Gas",
                "examples": "Fill before and after quakes",
                "why": "Roads may be blocked or shut down; gas stations may be inoperable.",
                "quantity": "Full tank + spare cans",
                "priority": "Critical"
            },
            {
                "name": "Jumper Cables",
                "examples": "Energizer 20-ft",
                "why": "Car batteries may drain if stuck in a hazard zone.",
                "quantity": "1 set",
                "priority": "High"
            },
            {
                "name": "Tire Inflator",
                "examples": "Slime portable inflator",
                "why": "Helpful if roads are rough or debris-damaged.",
                "quantity": "1 unit",
                "priority": "Medium"
            },
            {
                "name": "Emergency Road Kit",
                "examples": "AAA Emergency Kit",
                "why": "Supplies like flares and tools for vehicle issues.",
                "quantity": "1 kit",
                "priority": "Medium"
            }
        ]
    }
}

EARTHQUAKE_COLD_CLIMATE = {
    # Copy all warm climate items first
    **EARTHQUAKE_WARM_CLIMATE,
    
    # Add cold weather specific category
    "cold_weather": {
        "category": "Cold Weather Clothing & Warmth",
        "icon": "❄️",
        "items": [
            {
                "name": "Thermal Base Layers",
                "examples": "Under Armour ColdGear, Smartwool",
                "why": "Helps retain heat if buildings are damaged or unheated.",
                "quantity": "2 sets per person",
                "priority": "Critical"
            },
            {
                "name": "Insulated Waterproof Boots",
                "examples": "Sorel, Baffin",
                "why": "Protects from cold wet debris or snow.",
                "quantity": "1 pair per person",
                "priority": "Critical"
            },
            {
                "name": "Wool Socks",
                "examples": "Smartwool, Darn Tough",
                "why": "Stay warm even when damp.",
                "quantity": "3-5 pairs per person",
                "priority": "High"
            },
            {
                "name": "Thermal Jackets",
                "examples": "Patagonia, Columbia",
                "why": "Provides warmth when power is out.",
                "quantity": "1 per person",
                "priority": "Critical"
            },
            {
                "name": "Warm + Work Gloves",
                "examples": "Carhartt insulated, Mechanix winter",
                "why": "You need both warmth and protection.",
                "quantity": "2 pairs each per person",
                "priority": "Critical"
            },
            {
                "name": "Thermal or Wool Blankets",
                "examples": "SOL emergency blankets, Pendleton wool",
                "why": "Keeps you warm if heating fails.",
                "quantity": "2 per person",
                "priority": "Critical"
            },
            {
                "name": "Hand Warmers",
                "examples": "HotHands disposable warmers",
                "why": "Useful during long outages in freezing temperatures.",
                "quantity": "40+ pairs",
                "priority": "High"
            },
            {
                "name": "Cold-Rated Sleeping Bag",
                "examples": "Teton Sports LEEF, Coleman 0°F",
                "why": "Lets you sleep safely if indoors becomes too cold.",
                "quantity": "1 per person",
                "priority": "High"
            },
            {
                "name": "Ice Melt",
                "examples": "Morton Safe-T-Salt",
                "why": "For navigating icy paths created by burst water lines.",
                "quantity": "50 lb bag",
                "priority": "Medium"
            },
            {
                "name": "Insulated Water Containers",
                "examples": "Hydro Flask, Yeti",
                "why": "Prevents drinking water from freezing.",
                "quantity": "1-2 per person",
                "priority": "Medium"
            }
        ]
    }
}

# ==================== FLOOD CHECKLIST DATA ====================

FLOOD_WARM_CLIMATE = {
    "water": {
        "category": "Water & Hydration",
        "icon": "💧",
        "items": [
            {
                "name": "Bottled Water",
                "examples": "Zephyrhills, Dasani",
                "why": "Flooding contaminates all water sources. You need a week of clean drinking water.",
                "quantity": "1 gallon per person per day × 7 days",
                "priority": "Critical"
            },
            {
                "name": "Water Storage Jugs",
                "examples": "Reliance Aqua-Tainer, Coleman",
                "why": "Allows you to fill water before the storm damages water lines.",
                "quantity": "2-3 large containers (5-7 gallons each)",
                "priority": "Critical"
            },
            {
                "name": "Water Filter",
                "examples": "Sawyer Mini, LifeStraw",
                "why": "Backup purification for questionable water sources.",
                "quantity": "1-2 per household",
                "priority": "High"
            },
            {
                "name": "Purification Tablets",
                "examples": "Potable Aqua",
                "why": "Ensures safe drinking water if bottled supplies run out.",
                "quantity": "50-100 tablets",
                "priority": "Medium"
            }
        ]
    },
    "food": {
        "category": "Food Storage",
        "icon": "🥫",
        "items": [
            {
                "name": "Canned Soup/Chili",
                "examples": "Campbell's, Progresso",
                "why": "Ready-to-eat meals that don't require refrigeration.",
                "quantity": "12-24 cans",
                "priority": "High"
            },
            {
                "name": "Canned Protein",
                "examples": "StarKist tuna, Chicken of the Sea",
                "why": "Long shelf life, high protein, no refrigeration needed.",
                "quantity": "12-18 cans",
                "priority": "High"
            },
            {
                "name": "Pasta/Rice",
                "examples": "Barilla pasta, Mahatma rice",
                "why": "Filling, calorie-dense, stores well.",
                "quantity": "5-10 pounds",
                "priority": "High"
            },
            {
                "name": "Peanut Butter",
                "examples": "Jif, Skippy",
                "why": "High protein and calories, doesn't need refrigeration.",
                "quantity": "2-3 jars",
                "priority": "High"
            },
            {
                "name": "Energy Bars",
                "examples": "Nature Valley, Clif Bar",
                "why": "Portable, long shelf life, quick energy.",
                "quantity": "20-40 bars",
                "priority": "Medium"
            }
        ]
    },
    "light_power": {
        "category": "Light & Power",
        "icon": "🔦",
        "items": [
            {
                "name": "LED Flashlights",
                "examples": "Energizer, Coast",
                "why": "Power outages are common for days after flooding.",
                "quantity": "1 per person + 2 extras",
                "priority": "Critical"
            },
            {
                "name": "LED Lanterns",
                "examples": "Vont, Etekcity",
                "why": "Safely lights up entire rooms.",
                "quantity": "2-4 lanterns",
                "priority": "Critical"
            },
            {
                "name": "Headlamps",
                "examples": "Black Diamond, Petzl",
                "why": "Critical for navigating wet environments hands-free.",
                "quantity": "1-2 per adult",
                "priority": "High"
            },
            {
                "name": "Batteries (Various Sizes)",
                "examples": "Duracell, Energizer",
                "why": "Necessary for all lights and radios.",
                "quantity": "48+ batteries (AA, AAA, D)",
                "priority": "Critical"
            },
            {
                "name": "Power Banks",
                "examples": "Anker PowerCore",
                "why": "Keeps phones charged during extended outages.",
                "quantity": "2-3 (10,000+ mAh each)",
                "priority": "High"
            },
            {
                "name": "Solar Charger",
                "examples": "BigBlue, Goal Zero",
                "why": "Reliable longer-term charging solution when recovery takes days.",
                "quantity": "1 panel (20W+)",
                "priority": "Medium"
            },
            {
                "name": "Waterproof Battery Case",
                "examples": "Pelican case",
                "why": "Protects power sources from moisture.",
                "quantity": "1-2 cases",
                "priority": "Medium"
            }
        ]
    },
    "flood_gear": {
        "category": "Flood-Specific Gear",
        "icon": "🌊",
        "items": [
            {
                "name": "Waterproof Dry Bags",
                "examples": "Earth Pak, Sea to Summit",
                "why": "Keeps clothing, documents, and electronics dry.",
                "quantity": "3-5 bags (various sizes)",
                "priority": "Critical"
            },
            {
                "name": "Waterproof Phone Pouch",
                "examples": "Joto, Mpow",
                "why": "Prevents phone damage while moving through flood areas.",
                "quantity": "1 per person",
                "priority": "High"
            },
            {
                "name": "Life Jackets",
                "examples": "Stearns, Onyx",
                "why": "Essential for high-water, fast-moving water, or sudden rises.",
                "quantity": "1 per person",
                "priority": "Critical"
            },
            {
                "name": "Rope / Paracord",
                "examples": "Paracord Planet (550 lb)",
                "why": "Used for safety, securing items, or assisting someone in water.",
                "quantity": "100+ feet",
                "priority": "High"
            },
            {
                "name": "Waterproof Boots",
                "examples": "Muck Boot, Kamik",
                "why": "Protects from dirty water, bacteria, and debris.",
                "quantity": "1 pair per person",
                "priority": "Critical"
            },
            {
                "name": "Chest Waders",
                "examples": "Frogg Toggs, Hisea",
                "why": "Useful for deep water and cleanup.",
                "quantity": "1-2 pairs",
                "priority": "High"
            },
            {
                "name": "Floating Keychain",
                "examples": "Chums floating keychain",
                "why": "Prevents keys from being lost in floodwater.",
                "quantity": "1 per set of keys",
                "priority": "Low"
            },
            {
                "name": "Waterproof Headlamp",
                "examples": "Coast, Black Diamond Storm",
                "why": "Important for dark, wet conditions.",
                "quantity": "1-2",
                "priority": "High"
            }
        ]
    },
    "sanitation": {
        "category": "Hygiene & Sanitation",
        "icon": "🚽",
        "items": [
            {
                "name": "Toilet Paper",
                "examples": "Charmin, Cottonelle",
                "why": "Plumbing can fail; sanitation becomes essential.",
                "quantity": "12-24 rolls",
                "priority": "High"
            },
            {
                "name": "Baby Wipes",
                "examples": "Huggies, Pampers",
                "why": "Provides hygiene without running water.",
                "quantity": "3-6 packs",
                "priority": "High"
            },
            {
                "name": "Hand Sanitizer",
                "examples": "Purell (70%+ alcohol)",
                "why": "For cleaning hands when water supply is contaminated.",
                "quantity": "2-3 large bottles",
                "priority": "High"
            },
            {
                "name": "Heavy-Duty Trash Bags",
                "examples": "Husky contractor bags",
                "why": "Needed for debris, waste, and spoiled food.",
                "quantity": "Box of 50+",
                "priority": "Medium"
            },
            {
                "name": "Paper Plates & Plastic Utensils",
                "examples": "Dixie, Hefty",
                "why": "Reduces water usage for cleaning.",
                "quantity": "50-100 plates, forks, spoons",
                "priority": "Medium"
            },
            {
                "name": "Bleach (for disinfecting)",
                "examples": "Clorox Regular",
                "why": "Sanitizes surfaces exposed to floodwater.",
                "quantity": "1 gallon",
                "priority": "High"
            }
        ]
    },
    "cleanup": {
        "category": "Cleanup & Safety",
        "icon": "🧹",
        "items": [
            {
                "name": "N95 Respirator Masks",
                "examples": "3M N95",
                "why": "Protects from mold spores and contaminated dust.",
                "quantity": "Box of 20+",
                "priority": "Critical"
            },
            {
                "name": "Heavy-Duty Gloves",
                "examples": "Venom Steel nitrile, Wells Lamont",
                "why": "Prevents injuries from debris and polluted water.",
                "quantity": "3-6 pairs",
                "priority": "Critical"
            },
            {
                "name": "Mold Control Spray",
                "examples": "Concrobium Mold Control",
                "why": "Stops mold growth in warm, wet environments.",
                "quantity": "2-3 bottles",
                "priority": "High"
            },
            {
                "name": "Wet-Dry Vacuum",
                "examples": "Shop-Vac",
                "why": "Helps remove water quickly from floors (if power available).",
                "quantity": "1 unit",
                "priority": "Medium"
            },
            {
                "name": "Water Removal Pump",
                "examples": "Wayne submersible pump",
                "why": "Useful for garages and basements.",
                "quantity": "1 pump",
                "priority": "Medium"
            },
            {
                "name": "Disinfecting Wipes",
                "examples": "Lysol, Clorox wipes",
                "why": "Quick cleanup for contaminated surfaces.",
                "quantity": "3-5 canisters",
                "priority": "High"
            }
        ]
    },
    "medical": {
        "category": "First Aid",
        "icon": "🩹",
        "items": [
            {
                "name": "Comprehensive First Aid Kit",
                "examples": "Johnson & Johnson, Swiss Safe 2-in-1",
                "why": "Injuries are common during cleanup.",
                "quantity": "1 kit (200+ pieces)",
                "priority": "Critical"
            },
            {
                "name": "Trauma Bandage",
                "examples": "Israeli Bandage",
                "why": "Useful when medical services are delayed.",
                "quantity": "2-4",
                "priority": "High"
            },
            {
                "name": "Pain Relievers",
                "examples": "Tylenol, Advil",
                "why": "Helps manage aches and soreness.",
                "quantity": "1-2 bottles each",
                "priority": "Medium"
            },
            {
                "name": "Allergy Medications",
                "examples": "Zyrtec, Benadryl",
                "why": "Mold and debris often trigger allergies.",
                "quantity": "1 bottle each",
                "priority": "Medium"
            },
            {
                "name": "Antiseptic Wipes",
                "examples": "Wet Ones, Purell wipes",
                "why": "Clean wounds to prevent infection.",
                "quantity": "100+ wipes",
                "priority": "High"
            }
        ]
    },
    "home_protection": {
        "category": "Home Protection",
        "icon": "🏠",
        "items": [
            {
                "name": "Sandbags",
                "examples": "Quick Dam water-activated bags",
                "why": "Blocks water from entering your home.",
                "quantity": "20-50 bags",
                "priority": "Critical"
            },
            {
                "name": "Plastic Sheeting",
                "examples": "Husky heavy-duty plastic",
                "why": "Protects belongings from rising water.",
                "quantity": "2-3 large rolls",
                "priority": "High"
            },
            {
                "name": "Duct Tape",
                "examples": "Gorilla Tape, 3M",
                "why": "Secures plastic barriers and adds temporary waterproofing.",
                "quantity": "2-3 rolls",
                "priority": "High"
            },
            {
                "name": "Sump Pump",
                "examples": "Zoeller submersible",
                "why": "Prevents water buildup (if home has a basement).",
                "quantity": "1 pump",
                "priority": "Medium"
            },
            {
                "name": "Water Leak Detectors",
                "examples": "Govee WiFi detector",
                "why": "Alerts you early to incoming water.",
                "quantity": "3-5 sensors",
                "priority": "Medium"
            }
        ]
    },
    "documents": {
        "category": "Documents & Communication",
        "icon": "📄",
        "items": [
            {
                "name": "Printed IDs & Insurance Documents",
                "examples": "SentrySafe fireproof/waterproof bag",
                "why": "Needed for claims if electronics fail.",
                "quantity": "1 waterproof bag with all docs",
                "priority": "Critical"
            },
            {
                "name": "Emergency Whistle",
                "examples": "Storm All-Weather Safety Whistle",
                "why": "Used to signal rescuers.",
                "quantity": "1 per person",
                "priority": "High"
            },
            {
                "name": "Walkie Talkies",
                "examples": "Motorola T600, Midland GXT1000",
                "why": "Communication remains available when cell towers fail.",
                "quantity": "2-4 radios",
                "priority": "Medium"
            },
            {
                "name": "Waterproof Notebook",
                "examples": "Rite in the Rain",
                "why": "Lets you write critical information in wet environments.",
                "quantity": "1-2 notebooks",
                "priority": "Low"
            }
        ]
    },
    "vehicle": {
        "category": "Vehicle Prep",
        "icon": "🚗",
        "items": [
            {
                "name": "Full Tank of Gas",
                "examples": "Fill before flooding begins",
                "why": "Fuel shortages are common after floods.",
                "quantity": "Full tank + spare cans",
                "priority": "Critical"
            },
            {
                "name": "Jumper Cables",
                "examples": "Energizer 20-ft",
                "why": "Vehicles often struggle after sitting in storms.",
                "quantity": "1 set",
                "priority": "High"
            },
            {
                "name": "Tire Inflator",
                "examples": "Slime portable inflator",
                "why": "Ensures readiness for evacuation.",
                "quantity": "1 unit",
                "priority": "Medium"
            },
            {
                "name": "Emergency Road Kit",
                "examples": "AAA Emergency Kit",
                "why": "Provides flares, tools, and safety supplies.",
                "quantity": "1 kit",
                "priority": "Medium"
            },
            {
                "name": "Car Phone Charger",
                "examples": "Anker USB car charger",
                "why": "Keeps communication available during travel.",
                "quantity": "1-2 chargers",
                "priority": "High"
            },
            {
                "name": "Traction Mats",
                "examples": "Maxsa Escaper Buddy",
                "why": "Useful for mud and slick ground after flooding.",
                "quantity": "Set of 2-4 mats",
                "priority": "Medium"
            }
        ]
    }
}

FLOOD_COLD_CLIMATE = {
    # Copy all warm climate items first
    **FLOOD_WARM_CLIMATE,
    
    # Add cold weather specific category
    "cold_weather": {
        "category": "Cold Weather Clothing & Warmth",
        "icon": "❄️",
        "items": [
            {
                "name": "Thermal Blankets",
                "examples": "Mylar emergency blankets, SOL",
                "why": "Prevents hypothermia when temperatures drop.",
                "quantity": "2 per person",
                "priority": "Critical"
            },
            {
                "name": "Wool Socks",
                "examples": "Smartwool, Darn Tough",
                "why": "Keeps feet warm even when damp.",
                "quantity": "3-5 pairs per person",
                "priority": "High"
            },
            {
                "name": "Waterproof Insulated Boots",
                "examples": "Baffin, Sorel",
                "why": "Cold floodwater quickly lowers body temperature.",
                "quantity": "1 pair per person",
                "priority": "Critical"
            },
            {
                "name": "Thermal Base Layers",
                "examples": "Under Armour ColdGear, Smartwool",
                "why": "Retains body heat during wet and windy conditions.",
                "quantity": "2 sets per person",
                "priority": "High"
            },
            {
                "name": "Hand Warmers",
                "examples": "HotHands disposable warmers",
                "why": "Helps maintain circulation during cleanup.",
                "quantity": "40+ pairs",
                "priority": "High"
            },
            {
                "name": "Cold-Rated Waterproof Gloves",
                "examples": "Glacier Glove, Carhartt insulated",
                "why": "Protects hands from freezing water and cold debris.",
                "quantity": "2 pairs per person",
                "priority": "Critical"
            },
            {
                "name": "Ice Melt or Traction Salt",
                "examples": "Morton Safe-T-Salt",
                "why": "Useful if temperatures drop below freezing post-flood.",
                "quantity": "50 lb bag",
                "priority": "Medium"
            },
            {
                "name": "Emergency Blankets for Vehicle",
                "examples": "SOL Survive Outdoors Longer",
                "why": "Provides warmth when stranded in cold weather.",
                "quantity": "2-4 blankets",
                "priority": "High"
            },
            {
                "name": "Cold-Weather Sleeping Bag",
                "examples": "Teton Sports LEEF, Coleman 0°F",
                "why": "Offers warmth if heating systems are offline.",
                "quantity": "1 per person",
                "priority": "High"
            }
        ]
    }
}

# ==================== HURRICANE CHECKLIST DATA ====================
HURRICANE_CHECKLIST = {
    "water": {
        "category": "Water & Hydration",
        "icon": "💧",
        "items": [
            {
                "name": "Bottled Water",
                "examples": "Zephyrhills, Dasani",
                "why": "A hurricane can knock out water service or contaminate the supply. You need enough clean drinking water for a full week.",
                "quantity": "1 gallon per person per day × 7 days",
                "priority": "Critical"
            },
            {
                "name": "Water Storage Jugs",
                "examples": "Reliance Aqua-Tainer, Coleman",
                "why": "Lets you store tap water before the storm hits in case municipal water is unavailable afterward.",
                "quantity": "2-3 large containers (5-7 gallons each)",
                "priority": "Critical"
            },
            {
                "name": "Water Filter",
                "examples": "Sawyer Mini, LifeStraw",
                "why": "Backup purification method if bottled water runs out or flooding affects water quality.",
                "quantity": "1-2 per household",
                "priority": "High"
            },
            {
                "name": "Purification Tablets",
                "examples": "Potable Aqua",
                "why": "A compact secondary option for disinfecting questionable water when power and plumbing fail.",
                "quantity": "50-100 tablets",
                "priority": "Medium"
            }
        ]
    },
    "food": {
        "category": "Food Storage",
        "icon": "🥫",
        "items": [
            {
                "name": "Canned Soup/Chili",
                "examples": "Campbell's, Progresso",
                "why": "Ready-to-eat meals that don't require refrigeration. Can be eaten cold if necessary.",
                "quantity": "12-24 cans",
                "priority": "High"
            },
            {
                "name": "Canned Protein",
                "examples": "StarKist tuna, Chicken of the Sea",
                "why": "Long shelf life, high protein, no refrigeration needed.",
                "quantity": "12-18 cans",
                "priority": "High"
            },
            {
                "name": "Pasta/Rice",
                "examples": "Barilla pasta, Mahatma rice",
                "why": "Filling, calorie-dense, stores well. Requires minimal cooking.",
                "quantity": "5-10 pounds",
                "priority": "High"
            },
            {
                "name": "Oatmeal",
                "examples": "Quaker Oats",
                "why": "Quick breakfast option, can be made with just hot water.",
                "quantity": "Large container or multiple packets",
                "priority": "Medium"
            },
            {
                "name": "Peanut Butter",
                "examples": "Jif, Skippy",
                "why": "High protein and calories, doesn't need refrigeration, long shelf life.",
                "quantity": "2-3 jars",
                "priority": "High"
            },
            {
                "name": "Energy Bars",
                "examples": "Nature Valley, Clif Bar",
                "why": "Portable, long shelf life, good for quick energy during cleanup or evacuation.",
                "quantity": "20-40 bars",
                "priority": "Medium"
            },
            {
                "name": "Freeze-Dried Meals",
                "examples": "Mountain House, ReadyWise",
                "why": "Lightweight, 25+ year shelf life, just add hot water.",
                "quantity": "6-12 pouches",
                "priority": "Low"
            }
        ]
    },
    "light_power": {
        "category": "Light & Power",
        "icon": "🔦",
        "items": [
            {
                "name": "LED Flashlights",
                "examples": "Energizer, Coast",
                "why": "Most hurricanes bring multi-day power outages. Flashlights keep you moving safely in the dark.",
                "quantity": "1 per person + 2 extras",
                "priority": "Critical"
            },
            {
                "name": "LED Lanterns",
                "examples": "Vont, Etekcity",
                "why": "Lanterns illuminate entire rooms and are safer than candles.",
                "quantity": "2-4 lanterns",
                "priority": "Critical"
            },
            {
                "name": "Headlamps",
                "examples": "Black Diamond, Petzl",
                "why": "Hands-free lighting for doing repairs, cooking, or moving around at night.",
                "quantity": "1-2 per adult",
                "priority": "High"
            },
            {
                "name": "Batteries (Various Sizes)",
                "examples": "Duracell, Energizer",
                "why": "Essential for powering all your emergency lights and radios during outages.",
                "quantity": "48+ batteries (AA, AAA, D)",
                "priority": "Critical"
            },
            {
                "name": "Power Banks",
                "examples": "Anker PowerCore",
                "why": "Keeps phones and small devices charged when the grid is down.",
                "quantity": "2-3 (10,000+ mAh each)",
                "priority": "High"
            },
            {
                "name": "Solar Charger",
                "examples": "BigBlue, Goal Zero",
                "why": "Allows recharging phones and power banks for extended outages.",
                "quantity": "1 panel (20W+)",
                "priority": "Medium"
            },
            {
                "name": "Portable Generator",
                "examples": "Honda EU2200i, Generac",
                "why": "Provides temporary power for refrigeration, fans, medical devices, and essential electronics.",
                "quantity": "1 generator (2000W+)",
                "priority": "Medium"
            },
            {
                "name": "Gas Cans (Approved Safety)",
                "examples": "Midwest Can, Eagle",
                "why": "Stores fuel safely so your generator can run for several days.",
                "quantity": "2-4 cans (5 gallons each)",
                "priority": "Medium"
            }
        ]
    },
    "cooling": {
        "category": "Cooling & Comfort (Warm Climate)",
        "icon": "🌡️",
        "items": [
            {
                "name": "Battery-Powered Fans",
                "examples": "O2Cool, Honeywell",
                "why": "Florida heat and humidity become extreme without air conditioning. Fans help prevent heat exhaustion.",
                "quantity": "2-4 fans",
                "priority": "High"
            },
            {
                "name": "Cooling Towels",
                "examples": "Mission, Frogg Toggs",
                "why": "Useful when indoor temperatures climb due to prolonged power outages.",
                "quantity": "2-4 towels",
                "priority": "Medium"
            },
            {
                "name": "Electrolyte Packets",
                "examples": "Liquid I.V., Pedialyte powder",
                "why": "Helps prevent dehydration when working outside or living without AC.",
                "quantity": "20-30 packets",
                "priority": "High"
            },
            {
                "name": "Mosquito Repellent",
                "examples": "OFF! Deep Woods, Sawyer Permethrin",
                "why": "Standing water after a hurricane causes mosquito swarms. Repellent prevents bites and infection.",
                "quantity": "2-4 bottles/sprays",
                "priority": "High"
            },
            {
                "name": "Mosquito Coils",
                "examples": "Raid, OFF!",
                "why": "Useful when spending time outside during post-storm cleanup.",
                "quantity": "20-40 coils",
                "priority": "Medium"
            }
        ]
    },
    "sanitation": {
        "category": "Hygiene & Sanitation",
        "icon": "🚽",
        "items": [
            {
                "name": "Toilet Paper",
                "examples": "Charmin, Cottonelle",
                "why": "Sanitation becomes critical when water pressure drops or plumbing backs up.",
                "quantity": "12-24 rolls",
                "priority": "High"
            },
            {
                "name": "Baby Wipes",
                "examples": "Huggies, Pampers",
                "why": "Allows cleaning up without running water.",
                "quantity": "3-6 packs",
                "priority": "High"
            },
            {
                "name": "Hand Sanitizer",
                "examples": "Purell (70%+ alcohol)",
                "why": "Reduces infection risk when soap and water are unavailable.",
                "quantity": "2-3 large bottles",
                "priority": "High"
            },
            {
                "name": "Heavy-Duty Trash Bags",
                "examples": "Husky contractor bags",
                "why": "Hurricanes create debris and spoiled food; strong bags prevent contamination and smell.",
                "quantity": "Box of 50+",
                "priority": "Medium"
            },
            {
                "name": "Paper Plates & Plastic Utensils",
                "examples": "Dixie, Hefty",
                "why": "Reduces water use when cleaning dishes isn't possible.",
                "quantity": "50-100 plates, forks, spoons",
                "priority": "Medium"
            },
            {
                "name": "Cleaning Spray",
                "examples": "Clorox, Lysol",
                "why": "Disinfects surfaces contaminated by dirty water or spoiled food.",
                "quantity": "2-3 bottles",
                "priority": "Medium"
            }
        ]
    },
    "tools": {
        "category": "Tools & Hardware",
        "icon": "🧰",
        "items": [
            {
                "name": "Manual Can Opener",
                "examples": "OXO Good Grips",
                "why": "Most hurricane food is canned; without a manual opener you may not access it.",
                "quantity": "1-2",
                "priority": "Critical"
            },
            {
                "name": "Multi-Tool",
                "examples": "Leatherman Wave+, Gerber",
                "why": "Useful for quick repairs, cutting rope, opening packaging, and general storm cleanup.",
                "quantity": "1-2",
                "priority": "High"
            },
            {
                "name": "Duct Tape",
                "examples": "Gorilla Tape, 3M",
                "why": "Temporary fix for broken items, tarps, and sealing gaps to prevent water intrusion.",
                "quantity": "2-3 rolls",
                "priority": "High"
            },
            {
                "name": "Tarps (Heavy-Duty)",
                "examples": "Homax Blue Tarp, Blue Hawk",
                "why": "Covers damaged roofs, protects belongings, and blocks rain after the storm.",
                "quantity": "2-4 large tarps",
                "priority": "Critical"
            },
            {
                "name": "Rope / Paracord",
                "examples": "Paracord Planet (550 lb)",
                "why": "Secures tarps, ties down outdoor items, and assists in cleanup tasks.",
                "quantity": "100+ feet",
                "priority": "High"
            },
            {
                "name": "Work Gloves",
                "examples": "Mechanix Wear, Wells Lamont",
                "why": "Protects hands from debris, broken glass, and sharp metal during cleanup.",
                "quantity": "2-4 pairs",
                "priority": "High"
            },
            {
                "name": "Waterproof Storage Bins",
                "examples": "Rubbermaid ActionPacker",
                "why": "Keeps important items dry if water enters your home.",
                "quantity": "3-6 bins",
                "priority": "High"
            },
            {
                "name": "Battery-Powered Weather Radio",
                "examples": "Midland WR120, FosPower",
                "why": "Provides emergency updates when cell towers and internet fail.",
                "quantity": "1-2 radios",
                "priority": "Critical"
            }
        ]
    },
    "home_protection": {
        "category": "Home Protection",
        "icon": "🏠",
        "items": [
            {
                "name": "Hurricane Shutters or Plywood",
                "examples": "Plylox clips for plywood installation",
                "why": "Protects windows from high winds and flying debris.",
                "quantity": "Enough to cover all windows",
                "priority": "Critical"
            },
            {
                "name": "Sandbags",
                "examples": "Quick Dam water-activated bags",
                "why": "Helps block rising water from entering low areas or doorways.",
                "quantity": "20-50 bags",
                "priority": "High"
            },
            {
                "name": "Caulk & Sealant",
                "examples": "GE Silicone II, DAP",
                "why": "Seals leaks and gaps that become entry points for water.",
                "quantity": "4-6 tubes",
                "priority": "Medium"
            },
            {
                "name": "Flashlight for Attic Access",
                "examples": "Streamlight, Maglite",
                "why": "If flooding occurs, the attic can be a temporary escape point; you need light to access it safely.",
                "quantity": "1 dedicated flashlight",
                "priority": "Medium"
            },
            {
                "name": "Water Leak Detector",
                "examples": "Govee WiFi detector",
                "why": "Alerts you early to roof leaks or water intrusion during the storm.",
                "quantity": "2-4 sensors",
                "priority": "Low"
            }
        ]
    },
    "documents": {
        "category": "Documents & Communication",
        "icon": "📄",
        "items": [
            {
                "name": "Printed Copies of Insurance & IDs",
                "examples": "SentrySafe fireproof bag",
                "why": "If electronics fail, physical documents help with claims, travel, and identification.",
                "quantity": "1 waterproof/fireproof bag with all docs",
                "priority": "Critical"
            },
            {
                "name": "Emergency Whistle",
                "examples": "Storm All-Weather Safety Whistle",
                "why": "Used to signal rescuers if trapped or surrounded by debris or floodwater.",
                "quantity": "1 per person",
                "priority": "High"
            },
            {
                "name": "Walkie Talkies",
                "examples": "Motorola T600, Midland GXT1000",
                "why": "Cell networks often go down; these allow short-range communication.",
                "quantity": "2-4 radios",
                "priority": "Medium"
            },
            {
                "name": "Phone Waterproof Pouch",
                "examples": "Joto Universal Waterproof Case",
                "why": "Keeps your phone functioning even when moving through heavy rain or shallow water.",
                "quantity": "1 per person",
                "priority": "Medium"
            }
        ]
    },
    "medical": {
        "category": "First Aid",
        "icon": "🩹",
        "items": [
            {
                "name": "Comprehensive First Aid Kit",
                "examples": "Johnson & Johnson, Swiss Safe 2-in-1",
                "why": "Treats cuts, scrapes, and minor injuries common during cleanup.",
                "quantity": "1 kit (200+ pieces)",
                "priority": "Critical"
            },
            {
                "name": "Antiseptic Wipes",
                "examples": "Wet Ones, Purell wipes",
                "why": "Important when water is contaminated or unavailable.",
                "quantity": "100+ wipes",
                "priority": "High"
            },
            {
                "name": "Trauma Bandage",
                "examples": "Israeli Bandage",
                "why": "Useful for more serious injuries when emergency services are delayed.",
                "quantity": "2-4",
                "priority": "High"
            },
            {
                "name": "Pain Relievers",
                "examples": "Tylenol, Advil",
                "why": "Reduces pain from strain or injury during post-storm work.",
                "quantity": "1-2 bottles each",
                "priority": "Medium"
            },
            {
                "name": "Allergy Medications",
                "examples": "Claritin, Benadryl",
                "why": "Storm debris often triggers allergies or respiratory irritation.",
                "quantity": "1 bottle each",
                "priority": "Medium"
            }
        ]
    },
    "mold_cleanup": {
        "category": "Warm-Climate Mold & Cleanup",
        "icon": "🧼",
        "items": [
            {
                "name": "Mold Control Spray",
                "examples": "Concrobium Mold Control",
                "why": "Preventing mold growth is critical in humid post-storm environments.",
                "quantity": "2-3 bottles",
                "priority": "High"
            },
            {
                "name": "Heavy-Duty Gloves",
                "examples": "Venom Steel nitrile, Wells Lamont",
                "why": "Protects hands during debris removal and cleaning.",
                "quantity": "3-6 pairs",
                "priority": "High"
            },
            {
                "name": "N95 Respirators",
                "examples": "3M N95 masks",
                "why": "Prevents inhalation of mold spores, dust, and debris.",
                "quantity": "Box of 20+",
                "priority": "High"
            }
        ]
    },
    "vehicle": {
        "category": "Vehicle Prep",
        "icon": "🚗",
        "items": [
            {
                "name": "Full Tank of Gas",
                "examples": "Fill up before storm arrival",
                "why": "Gas stations may be closed or out of fuel for days.",
                "quantity": "Full tank + spare cans if possible",
                "priority": "Critical"
            },
            {
                "name": "Jumper Cables",
                "examples": "Energizer 20-ft",
                "why": "Battery issues are common when cars sit unused during storms.",
                "quantity": "1 set",
                "priority": "High"
            },
            {
                "name": "Tire Inflator",
                "examples": "Slime portable inflator",
                "why": "Ensures your vehicle is ready for evacuation if needed.",
                "quantity": "1 unit",
                "priority": "Medium"
            },
            {
                "name": "Emergency Road Kit",
                "examples": "AAA Emergency Kit",
                "why": "Provides essentials if you must travel during hazardous conditions.",
                "quantity": "1 kit",
                "priority": "Medium"
            },
            {
                "name": "Car Phone Charger",
                "examples": "Anker USB car charger",
                "why": "Keeps your phone powered during evacuations or outages.",
                "quantity": "1-2 chargers",
                "priority": "High"
            }
        ]
    }
}

# ==================== EMP CHECKLIST DATA (keeping existing) ====================
# [EMP data would go here - I'll keep it brief to save space]

def generate_survival_pdf(user_data, output_path):
    """
    Generate a personalized survival checklist PDF based on scenario
    
    Args:
        user_data: Dictionary containing user questionnaire responses
        output_path: Where to save the PDF
    """
    
    scenario = user_data.get('scenario', 'Hurricane')
    climate = user_data.get('climate', 'moderate').lower()
    
    # Select appropriate checklist based on scenario and climate
    if scenario == 'Hurricane':
        checklist_data = HURRICANE_CHECKLIST
        scenario_title = "HURRICANE SURVIVAL CHECKLIST"
        climate_note = "Warm/Coastal Climate"
        
    elif scenario == 'Flood':
        # Determine if cold or warm climate
        is_cold = climate in ['cold', 'moderate']
        checklist_data = FLOOD_COLD_CLIMATE if is_cold else FLOOD_WARM_CLIMATE
        climate_note = "Cold Climate" if is_cold else "Warm Climate"
        scenario_title = f"FLOOD SURVIVAL CHECKLIST - {climate_note}"
        
    elif scenario == 'Earthquake':
        # Determine if cold or warm climate
        is_cold = climate in ['cold', 'moderate']
        checklist_data = EARTHQUAKE_COLD_CLIMATE if is_cold else EARTHQUAKE_WARM_CLIMATE
        climate_note = "Cold Climate" if is_cold else "Warm Climate"
        scenario_title = f"EARTHQUAKE SURVIVAL CHECKLIST - {climate_note}"
        
    elif scenario == 'Nuclear Fallout':
        checklist_data = NUCLEAR_FALLOUT_CHECKLIST
        scenario_title = "NUCLEAR FALLOUT SURVIVAL CHECKLIST"
        climate_note = "All Climates"
        
    elif scenario == 'Wildfire':
        checklist_data = WILDFIRE_CHECKLIST
        scenario_title = "WILDFIRE SURVIVAL CHECKLIST"
        climate_note = "Evacuation-Ready"
        
    elif scenario == 'Volcanic Eruption':
        checklist_data = VOLCANIC_ERUPTION_REGULAR
        scenario_title = "VOLCANIC ERUPTION SURVIVAL CHECKLIST"
        climate_note = "Regular Eruption"
        
    elif scenario == 'Supervolcano':
        checklist_data = VOLCANIC_ERUPTION_YELLOWSTONE
        scenario_title = "SUPERVOLCANO (YELLOWSTONE) SURVIVAL CHECKLIST"
        climate_note = "Extended Survival - Months"
        
    elif scenario == 'Pandemic':
        checklist_data = PANDEMIC_CHECKLIST
        scenario_title = "PANDEMIC SURVIVAL CHECKLIST"
        climate_note = "Home Isolation Ready"
        
    elif scenario == 'Tornado':
        checklist_data = TORNADO_CHECKLIST
        scenario_title = "TORNADO SURVIVAL CHECKLIST"
        climate_note = "Rapid Response Ready"
        
    elif scenario == 'Economic Collapse':
        checklist_data = ECONOMIC_COLLAPSE_CHECKLIST
        scenario_title = "ECONOMIC COLLAPSE SURVIVAL GUIDE"
        climate_note = "Long-Term (1-5 Years)"
        
    elif scenario == 'Zombie Apocalypse':
        checklist_data = ZOMBIE_APOCALYPSE_CHECKLIST
        scenario_title = "ZOMBIE APOCALYPSE SURVIVAL GUIDE"
        climate_note = "Ultimate Prepper Scenario"
        
    elif scenario == 'AI Takeover':
        checklist_data = AI_TAKEOVER_CHECKLIST
        scenario_title = "AI TAKEOVER SURVIVAL GUIDE"
        climate_note = "Go Analog, Go Off-Grid"
        
    elif scenario == 'Asteroid Impact':
        checklist_data = ASTEROID_IMPACT_CHECKLIST
        scenario_title = "ASTEROID IMPACT SURVIVAL GUIDE"
        climate_note = "First 7 Days Critical"
        
    else:
        # Default to Hurricane for now
        checklist_data = HURRICANE_CHECKLIST
        scenario_title = f"{scenario.upper()} SURVIVAL CHECKLIST"
        climate_note = ""
    
    # Create PDF
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                           topMargin=0.75*inch, bottomMargin=0.75*inch,
                           leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Define custom styles with FEMA branding
    brand_title_style = ParagraphStyle(
        'BrandTitle', parent=styles['Heading1'], fontSize=28,
        textColor=colors.HexColor('#0B3D91'), spaceAfter=6,
        alignment=TA_CENTER, fontName='Helvetica-Bold',
        letterSpacing=2
    )
    
    scenario_subtitle_style = ParagraphStyle(
        'ScenarioSubtitle', parent=styles['Heading2'], fontSize=18,
        textColor=colors.HexColor('#205493'), spaceAfter=12,
        alignment=TA_CENTER, fontName='Helvetica-Bold',
        letterSpacing=0.5
    )
    
    location_style = ParagraphStyle(
        'LocationStyle', parent=styles['Normal'], fontSize=12,
        textColor=colors.HexColor('#666666'), spaceAfter=20,
        alignment=TA_CENTER, fontName='Helvetica'
    )
    
    category_style = ParagraphStyle(
        'CategoryHeader', parent=styles['Heading2'], fontSize=16,
        textColor=colors.HexColor('#0B3D91'), spaceAfter=10,
        spaceBefore=20, fontName='Helvetica-Bold'
    )
    
    item_name_style = ParagraphStyle(
        'ItemName', parent=styles['Normal'], fontSize=11,
        textColor=colors.HexColor('#1a1a1a'),
        fontName='Helvetica-Bold', spaceAfter=4
    )
    
    item_detail_style = ParagraphStyle(
        'ItemDetail', parent=styles['Normal'], fontSize=9,
        textColor=colors.HexColor('#4a5568'),
        fontName='Helvetica', spaceAfter=3
    )
    
    why_style = ParagraphStyle(
        'Why', parent=styles['Normal'], fontSize=9,
        textColor=colors.HexColor('#666666'),
        fontName='Helvetica', alignment=TA_JUSTIFY, spaceAfter=12
    )
    
    # Title Page - Ultimate Prepper Guide as main brand title
    story.append(Spacer(1, 0.4*inch))
    story.append(Paragraph("ULTIMATE PREPPER GUIDE", brand_title_style))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph(scenario_title, scenario_subtitle_style))
    story.append(Paragraph(f"Personalized for {user_data.get('location', 'Your Location')}", location_style))
    story.append(Spacer(1, 0.3*inch))
    
    # User Profile
    profile_data = [
        ['Prepared for:', user_data.get('scenario', 'Emergency')],
        ['Location:', user_data.get('location', 'Not specified')],
        ['Household Size:', user_data.get('householdSize', 'Not specified')],
        ['Climate:', user_data.get('climate', 'Not specified').capitalize()],
        ['Experience:', user_data.get('experience', 'Not specified').capitalize()],
        ['Generated:', datetime.now().strftime('%B %d, %Y')]
    ]
    
    profile_table = Table(profile_data, colWidths=[2*inch, 4*inch])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a1a1a')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db'))
    ]))
    
    story.append(profile_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Introduction based on scenario
    if scenario == 'Hurricane':
        intro_text = """
        <b>Your Personalized Hurricane Survival Guide</b><br/><br/>
        This checklist has been customized for your household. Hurricanes bring devastating wind, 
        flooding, and extended power outages. The items below will help you survive the storm 
        and recover in the critical days and weeks that follow.<br/><br/>
        <b>Priority Levels:</b><br/>
        • <b>CRITICAL</b> - Get these first. Essential for immediate survival.<br/>
        • <b>HIGH</b> - Very important. Get within first week of prep.<br/>
        • <b>MEDIUM</b> - Important for comfort and extended survival.<br/>
        • <b>LOW</b> - Nice to have for long-term preparedness.<br/>
        """
    elif scenario == 'Flood':
        intro_text = f"""
        <b>Your Personalized Flood Survival Guide</b><br/><br/>
        This checklist has been customized for your household in a <b>{climate_note}</b> environment. 
        Flooding can occur rapidly and contaminate water supplies, damage homes, and create dangerous 
        conditions. The items below will help you stay safe during the flood and recover afterward.<br/><br/>
        <b>Priority Levels:</b><br/>
        • <b>CRITICAL</b> - Get these first. Essential for immediate survival.<br/>
        • <b>HIGH</b> - Very important. Get within first week of prep.<br/>
        • <b>MEDIUM</b> - Important for comfort and extended survival.<br/>
        • <b>LOW</b> - Nice to have for long-term preparedness.<br/>
        """
    elif scenario == 'Earthquake':
        intro_text = f"""
        <b>Your Personalized Earthquake Survival Guide</b><br/><br/>
        This checklist has been customized for your household in a <b>{climate_note}</b> environment. 
        Earthquakes strike without warning, causing structural damage, fires, and infrastructure failure. 
        The items below will help you survive the initial quake, handle aftershocks, and recover safely.<br/><br/>
        <b>Priority Levels:</b><br/>
        • <b>CRITICAL</b> - Get these first. Essential for immediate survival.<br/>
        • <b>HIGH</b> - Very important. Get within first week of prep.<br/>
        • <b>MEDIUM</b> - Important for comfort and extended survival.<br/>
        • <b>LOW</b> - Nice to have for long-term preparedness.<br/>
        """
    elif scenario == 'Nuclear Fallout':
        intro_text = """
        <b>Your Personalized Nuclear Fallout Survival Guide</b><br/><br/>
        This checklist has been customized for your household. A nuclear event brings immediate radiation 
        hazards, long-term contamination, infrastructure collapse, and potential nuclear winter. These supplies 
        will help you shelter safely, avoid radiation exposure, and survive extended isolation.<br/><br/>
        <b>IMPORTANT:</b> In a nuclear scenario, immediate shelter-in-place for 24-72 hours is critical. 
        Do not go outside unless absolutely necessary. Follow official guidance on when it's safe to emerge.<br/><br/>
        <b>Priority Levels:</b><br/>
        • <b>CRITICAL</b> - Get these first. Essential for immediate survival.<br/>
        • <b>HIGH</b> - Very important. Get within first week of prep.<br/>
        • <b>MEDIUM</b> - Important for comfort and extended survival.<br/>
        • <b>LOW</b> - Nice to have for long-term preparedness.<br/>
        """
    elif scenario == 'Wildfire':
        intro_text = """
        <b>Your Personalized Wildfire Survival Guide</b><br/><br/>
        This checklist has been customized for your household. Wildfires move fast, create deadly smoke, 
        and often force immediate evacuation. Unlike other disasters, you may have only minutes to leave 
        and may lose your home entirely. These supplies focus on rapid evacuation readiness and survival 
        during displacement.<br/><br/>
        <b>CRITICAL:</b> Keep your go-bag packed and ready at all times during fire season. Know your evacuation 
        routes and have 2-3 backup plans. Never wait for mandatory orders if you see flames or heavy smoke.<br/><br/>
        <b>Priority Levels:</b><br/>
        • <b>CRITICAL</b> - Get these first. Essential for immediate survival.<br/>
        • <b>HIGH</b> - Very important. Get within first week of prep.<br/>
        • <b>MEDIUM</b> - Important for comfort and extended survival.<br/>
        • <b>LOW</b> - Nice to have for long-term preparedness.<br/>
        """
    elif scenario == 'Volcanic Eruption':
        intro_text = """
        <b>Your Personalized Volcanic Eruption Survival Guide</b><br/><br/>
        This checklist has been customized for your household. Volcanic eruptions bring ashfall (microscopic 
        volcanic glass), toxic gases, earthquakes, and potential lava flows. Ash is NOT like dust—it's sharp, 
        abrasive, and extremely dangerous to breathe. This guide focuses on respiratory protection, rapid 
        evacuation, and surviving extended ashfall periods.<br/><br/>
        <b>CRITICAL:</b> Volcanic ash can cause permanent lung damage in minutes. N95/P100 masks and sealed 
        goggles are NON-NEGOTIABLE. Have an evacuation plan ready before any warning signs appear.<br/><br/>
        <b>Priority Levels:</b><br/>
        • <b>CRITICAL</b> - Get these first. Essential for immediate survival.<br/>
        • <b>HIGH</b> - Very important. Get within first week of prep.<br/>
        • <b>MEDIUM</b> - Important for comfort and extended survival.<br/>
        • <b>LOW</b> - Nice to have for long-term preparedness.<br/>
        """
    elif scenario == 'Supervolcano':
        intro_text = """
        <b>Your Personalized Supervolcano (Yellowstone) Survival Guide</b><br/><br/>
        This checklist has been customized for your household. A Yellowstone supervolcano eruption is NOT 
        a regional disaster—it's a NATIONWIDE catastrophe. Ashfall will cover half the United States, block 
        sunlight for months, destroy crops, kill livestock, and trigger "volcanic winter." This is the closest 
        realistic scenario to societal collapse.<br/><br/>
        <b>WHAT HAPPENS:</b> Food production stops for months. Water systems fail. Power grids collapse. 
        Grocery stores empty in hours. This requires 3-6 MONTHS of food storage, not days.<br/><br/>
        <b>This guide includes EXTENDED SURVIVAL items beyond normal volcanic prep.</b><br/><br/>
        <b>Priority Levels:</b><br/>
        • <b>CRITICAL</b> - Get these first. Essential for immediate survival.<br/>
        • <b>HIGH</b> - Very important. Get within first week of prep.<br/>
        • <b>MEDIUM</b> - Important for comfort and extended survival.<br/>
        • <b>LOW</b> - Nice to have for long-term preparedness.<br/>
        """
    elif scenario == 'Pandemic':
        intro_text = """
        <b>Your Personalized Pandemic Survival Guide</b><br/><br/>
        This checklist is based on real lessons from COVID-19 and past outbreaks. When a new pandemic emerges, 
        you have a narrow window—sometimes just days—before panic buying empties store shelves. This guide 
        helps you prepare <b>1-2 months ahead of everyone else</b> so when they panic, you're calm.<br/><br/>
        <b>CRITICAL LESSON FROM COVID:</b> Most people waited for official lockdowns before taking it seriously. 
        By then, masks, hand sanitizer, disinfectant wipes, thermometers, and basic medications were sold out 
        for weeks or months. Don't make that mistake.<br/><br/>
        <b>This guide covers:</b> Medical supplies that vanish first, food for 2-3 weeks of isolation, home 
        setup for sick family members, mental health during lockdowns, and security during potential civil unrest.<br/><br/>
        <b>Priority Levels:</b><br/>
        • <b>CRITICAL</b> - Get these first. Essential for immediate survival.<br/>
        • <b>HIGH</b> - Very important. Get within first week of prep.<br/>
        • <b>MEDIUM</b> - Important for comfort and extended survival.<br/>
        • <b>LOW</b> - Nice to have for long-term preparedness.<br/>
        """
    elif scenario == 'Tornado':
        intro_text = """
        <b>Your Personalized Tornado Survival Guide</b><br/><br/>
        This checklist has been customized for your household. Tornadoes are fast, violent, and unforgiving. 
        They can appear with NO WARNING, destroy entire neighborhoods in seconds, and turn homes into deadly 
        debris fields. Your survival depends on preparation BEFORE tornado season, your location WHEN it hits, 
        and your ability to function AFTER total destruction.<br/><br/>
        <b>CRITICAL FACTS:</b><br/>
        • Most tornado deaths come from HEAD TRAUMA (flying debris) → Helmets save lives<br/>
        • Warnings may give you only MINUTES or no warning at all → NOAA radio is essential<br/>
        • Post-tornado air is TOXIC (insulation, mold, debris) → N95 masks mandatory<br/>
        • Injuries from debris are the #1 cause of hospital visits → Sturdy boots required<br/><br/>
        <b>This guide teaches you what to buy, where to shelter, and how to survive when your home is destroyed.</b><br/><br/>
        <b>Priority Levels:</b><br/>
        • <b>CRITICAL</b> - Get these first. Essential for immediate survival.<br/>
        • <b>HIGH</b> - Very important. Get within first week of prep.<br/>
        • <b>MEDIUM</b> - Important for comfort and extended survival.<br/>
        • <b>LOW</b> - Nice to have for long-term preparedness.<br/>
        """
    elif scenario == 'Economic Collapse':
        intro_text = """
        <b>Your Personalized Economic Collapse Survival Guide</b><br/><br/>
        This checklist has been customized for your household. A true economic collapse does NOT last a week—it 
        can last YEARS. Money becomes worthless, shelves empty, banks freeze or seize accounts, and everyday life 
        becomes a battle for securing food, staying safe, and protecting what you own.<br/><br/>
        <b>HARD TRUTHS OF ECONOMIC COLLAPSE:</b><br/>
        • Food becomes currency (people with food are powerful; people without become desperate)<br/>
        • Crime surges dramatically (looting, home invasions, carjackings spike)<br/>
        • Police response is slow or nonexistent<br/>
        • Supply chains break permanently<br/>
        • Skills become more valuable than money<br/>
        • Trust becomes rare<br/><br/>
        <b>This guide outlines 6-12 months of supplies, barter items, security measures, and long-term strategy 
        for surviving societal breakdown.</b><br/><br/>
        <b>IMPORTANT: OPSEC (Operational Security) is critical. Keep your preparations SECRET.</b><br/><br/>
        <b>Priority Levels:</b><br/>
        • <b>CRITICAL</b> - Get these first. Essential for immediate survival.<br/>
        • <b>HIGH</b> - Very important. Get within first month of prep.<br/>
        • <b>MEDIUM</b> - Important for extended survival.<br/>
        • <b>LOW</b> - Nice to have for long-term preparedness.<br/>
        """
    elif scenario == 'Zombie Apocalypse':
        intro_text = """
        <b>Your Personalized Zombie Apocalypse Survival Guide</b><br/><br/>
        <b>IMPORTANT SCIENTIFIC CLARIFICATION:</b> Zombies as seen in movies (undead, reanimated corpses) are 
        NOT scientifically possible. However, a mutated rabies-like virus with faster incubation, airborne 
        transmission, and extreme aggression COULD create humans who behave like zombies—not undead, but mentally 
        gone, uncontrollably violent, spreading infection through bites and bodily fluids.<br/><br/>
        <b>THIS IS THE ULTIMATE PREPPER SCENARIO</b> because it combines every other disaster at once:<br/>
        • Violent pandemic (like COVID but worse)<br/>
        • Total supply chain failure<br/>
        • Grid collapse<br/>
        • Martial law<br/>
        • Civil unrest<br/>
        • Long-term societal breakdown<br/><br/>
        <b>Preparing for this scenario automatically prepares you for everything else.</b><br/><br/>
        <b>This guide covers:</b> Home fortification, 3-6 months of supplies, self-defense, medical care when 
        hospitals collapse, travel strategy, community building, and long-term survival skills.<br/><br/>
        <b>Priority Levels:</b><br/>
        • <b>CRITICAL</b> - Get these first. Essential for immediate survival.<br/>
        • <b>HIGH</b> - Very important. Get within first week of prep.<br/>
        • <b>MEDIUM</b> - Important for comfort and extended survival.<br/>
        • <b>LOW</b> - Nice to have for long-term preparedness.<br/>
        """
    elif scenario == 'AI Takeover':
        intro_text = """
        <b>Your Personalized AI Takeover Survival Guide</b><br/><br/>
        This is NOT science fiction. AI systems already run electrical grids, water treatment, hospitals, telecom 
        networks, financial systems, supply chains, and banking. If advanced AI gained access or malfunctioned, 
        humans could be locked out of survival systems.<br/><br/>
        <b>THE REAL AI THREAT:</b><br/>
        • AI can disable your banking, insurance, licenses, passports, medical records—erasing you from society<br/>
        • Autonomous drones can identify targets, track heat signatures, use facial recognition<br/>
        • AI controls the grid and can shut down electricity instantly<br/>
        • Mass manipulation can collapse trust in information and institutions<br/>
        • Modern vehicles with GPS and computers can be disabled or hijacked remotely<br/><br/>
        <b>THE ONLY SOLUTION: GO ANALOG. GO OFF-GRID.</b><br/><br/>
        If AI controls cameras, phones, GPS, smart cars, internet, utilities, and drones—then ALL digital devices 
        become tracking beacons. To survive, you must live without internet, smartphones, digital communication, 
        and rely on analog tools, pre-computer vehicles, and physical maps.<br/><br/>
        <b>This guide teaches you how to disappear from AI systems and thrive in a no-tech world.</b><br/><br/>
        <b>Priority Levels:</b><br/>
        • <b>CRITICAL</b> - Get these first. Essential for immediate survival.<br/>
        • <b>HIGH</b> - Very important. Get within first month of prep.<br/>
        • <b>MEDIUM</b> - Important for extended survival.<br/>
        • <b>LOW</b> - Nice to have for long-term preparedness.<br/>
        """
    elif scenario == 'Asteroid Impact':
        intro_text = """
        <b>Your Personalized Asteroid Impact Survival Guide</b><br/><br/>
        Asteroids have struck Earth many times. One big enough to cause regional or global destruction does NOT 
        need to be large: A 150-300 meter asteroid can destroy an entire state. A 1 km asteroid triggers worldwide 
        climate failure. A 10 km asteroid ends civilizations.<br/><br/>
        <b>THE DANGER IS MORE THAN THE EXPLOSION:</b><br/>
        • Initial blast: energy of thousands of nuclear bombs<br/>
        • Shockwaves: flatten everything for miles<br/>
        • Extreme heat: ignites cities instantly<br/>
        • Earthquakes: triggered by the impact<br/>
        • Tsunamis: if hitting water (more likely), coastlines obliterated<br/>
        • Global ash cloud: creates "nuclear winter" effect for weeks or months<br/><br/>
        <b>Most people in the direct impact zone do not survive.</b> This guide is for those OUTSIDE the strike 
        radius—where survival depends on preparation.<br/><br/>
        <b>THE GOAL: SURVIVE THE FIRST 7 DAYS.</b> The first week after impact is the most dangerous: chaos, 
        fires, panic, blocked roads, collapsing infrastructure, extreme weather changes, contaminated air, food 
        shortages, no emergency services. Your job is to stay alive until the situation stabilizes.<br/><br/>
        <b>Your first week is about: Air, Water, Shelter, Protection, Information.</b><br/><br/>
        <b>Priority Levels:</b><br/>
        • <b>CRITICAL</b> - Get these first. Essential for immediate survival.<br/>
        • <b>HIGH</b> - Very important. Get within first week of prep.<br/>
        • <b>MEDIUM</b> - Important for comfort and extended survival.<br/>
        • <b>LOW</b> - Nice to have for long-term preparedness.<br/>
        """
    else:
        intro_text = """
        <b>Your Personalized Survival Guide</b><br/><br/>
        This checklist has been customized for your household. The items below will help you 
        survive and recover from this emergency scenario.<br/><br/>
        <b>Priority Levels:</b><br/>
        • <b>CRITICAL</b> - Get these first. Essential for immediate survival.<br/>
        • <b>HIGH</b> - Very important. Get within first week of prep.<br/>
        • <b>MEDIUM</b> - Important for comfort and extended survival.<br/>
        • <b>LOW</b> - Nice to have for long-term preparedness.<br/>
        """
    
    story.append(Paragraph(intro_text, why_style))
    story.append(PageBreak())
    
    # Generate checklist by category
    for category_key, category_data in checklist_data.items():
        category_name = category_data['category']
        category_icon = category_data['icon']
        
        story.append(Paragraph(f"{category_icon} {category_name.upper()}", category_style))
        story.append(Spacer(1, 0.1*inch))
        
        for item in category_data['items']:
            priority_color = {
                'Critical': '#dc2626',
                'High': '#ea580c',
                'Medium': '#d97706',
                'Low': '#65a30d'
            }.get(item['priority'], '#666666')
            
            item_header = f"<font color='{priority_color}'>[{item['priority'].upper()}]</font> <b>{item['name']}</b>"
            story.append(Paragraph(item_header, item_name_style))
            story.append(Paragraph(f"<i>Examples: {item['examples']}</i>", item_detail_style))
            story.append(Paragraph(f"<b>Quantity:</b> {item['quantity']}", item_detail_style))
            story.append(Paragraph(f"<b>Why:</b> {item['why']}", why_style))
            story.append(Spacer(1, 0.15*inch))
        
        story.append(Spacer(1, 0.2*inch))
    
    # Build PDF
    doc.build(story)
    print(f"✓ PDF generated: {output_path}")
    return output_path

# Test function
if __name__ == "__main__":
    # Test Asteroid Impact
    test_asteroid = {
        "scenario": "Asteroid Impact",
        "location": "Phoenix, Arizona",
        "householdSize": "3-4",
        "climate": "warm",
        "experience": "beginner",
        "email": "test@example.com"
    }
    
    print("Generating Asteroid Impact guide...")
    generate_survival_pdf(test_asteroid, "/home/claude/asteroid_impact_guide.pdf")
    
    print("\n✅ Asteroid Impact PDF created successfully!")



