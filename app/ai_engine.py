"""AI Engine - Workout & Diet Logic (Rule-based MVP, upgradeable to ML)"""
import json
from datetime import date, timedelta


# ══════════════════════════════════════════════
#  WORKOUT AI
# ══════════════════════════════════════════════

WORKOUT_TEMPLATES = {
    "lose_weight": {
        "beginner": [
            {"day": "Monday",    "focus": "Full Body Cardio", "exercises": [
                {"name": "Jumping Jacks", "sets": 3, "reps": "30", "rest": 30, "cal_per_min": 8, "muscle": "cardio"},
                {"name": "Bodyweight Squats", "sets": 3, "reps": "15", "rest": 45, "cal_per_min": 5, "muscle": "legs"},
                {"name": "Push-ups (Knee)", "sets": 3, "reps": "10", "rest": 45, "cal_per_min": 4, "muscle": "chest"},
                {"name": "Plank Hold", "sets": 3, "reps": "20s", "rest": 30, "cal_per_min": 3, "muscle": "core"},
                {"name": "Mountain Climbers", "sets": 3, "reps": "20", "rest": 30, "cal_per_min": 9, "muscle": "cardio"},
            ]},
            {"day": "Tuesday",   "focus": "Rest / Light Walk", "exercises": []},
            {"day": "Wednesday", "focus": "Lower Body + Core", "exercises": [
                {"name": "Lunges", "sets": 3, "reps": "12 each", "rest": 45, "cal_per_min": 5, "muscle": "legs"},
                {"name": "Glute Bridges", "sets": 3, "reps": "15", "rest": 30, "cal_per_min": 4, "muscle": "legs"},
                {"name": "Crunches", "sets": 3, "reps": "20", "rest": 30, "cal_per_min": 3, "muscle": "core"},
                {"name": "Leg Raises", "sets": 3, "reps": "15", "rest": 30, "cal_per_min": 3, "muscle": "core"},
            ]},
            {"day": "Thursday",  "focus": "Rest", "exercises": []},
            {"day": "Friday",    "focus": "Upper Body + Cardio", "exercises": [
                {"name": "Push-ups", "sets": 3, "reps": "10", "rest": 45, "cal_per_min": 4, "muscle": "chest"},
                {"name": "Dumbbell Rows", "sets": 3, "reps": "12", "rest": 45, "cal_per_min": 4, "muscle": "back"},
                {"name": "Shoulder Press", "sets": 3, "reps": "12", "rest": 45, "cal_per_min": 4, "muscle": "shoulders"},
                {"name": "Burpees", "sets": 3, "reps": "10", "rest": 45, "cal_per_min": 10, "muscle": "cardio"},
            ]},
            {"day": "Saturday",  "focus": "HIIT Cardio", "exercises": [
                {"name": "High Knees", "sets": 4, "reps": "30s", "rest": 20, "cal_per_min": 9, "muscle": "cardio"},
                {"name": "Jump Squats", "sets": 3, "reps": "15", "rest": 30, "cal_per_min": 8, "muscle": "legs"},
                {"name": "Burpees", "sets": 3, "reps": "10", "rest": 30, "cal_per_min": 10, "muscle": "cardio"},
            ]},
            {"day": "Sunday",    "focus": "Active Recovery", "exercises": []},
        ],
        "intermediate": [
            {"day": "Monday",    "focus": "Chest + Cardio", "exercises": [
                {"name": "Bench Press", "sets": 4, "reps": "12", "rest": 60, "cal_per_min": 5, "muscle": "chest"},
                {"name": "Incline Dumbbell Press", "sets": 3, "reps": "12", "rest": 60, "cal_per_min": 5, "muscle": "chest"},
                {"name": "Cable Flyes", "sets": 3, "reps": "15", "rest": 45, "cal_per_min": 4, "muscle": "chest"},
                {"name": "Treadmill HIIT", "sets": 1, "reps": "20 min", "rest": 0, "cal_per_min": 11, "muscle": "cardio"},
            ]},
            {"day": "Tuesday",   "focus": "Back + Biceps", "exercises": [
                {"name": "Pull-ups", "sets": 4, "reps": "8", "rest": 60, "cal_per_min": 5, "muscle": "back"},
                {"name": "Barbell Row", "sets": 4, "reps": "10", "rest": 60, "cal_per_min": 5, "muscle": "back"},
                {"name": "Lat Pulldown", "sets": 3, "reps": "12", "rest": 45, "cal_per_min": 4, "muscle": "back"},
                {"name": "Barbell Curl", "sets": 3, "reps": "12", "rest": 45, "cal_per_min": 4, "muscle": "arms"},
            ]},
            {"day": "Wednesday", "focus": "Rest / Yoga", "exercises": []},
            {"day": "Thursday",  "focus": "Legs", "exercises": [
                {"name": "Barbell Squats", "sets": 4, "reps": "10", "rest": 90, "cal_per_min": 6, "muscle": "legs"},
                {"name": "Romanian Deadlift", "sets": 3, "reps": "12", "rest": 60, "cal_per_min": 5, "muscle": "legs"},
                {"name": "Leg Press", "sets": 3, "reps": "15", "rest": 60, "cal_per_min": 5, "muscle": "legs"},
                {"name": "Calf Raises", "sets": 4, "reps": "20", "rest": 30, "cal_per_min": 3, "muscle": "legs"},
            ]},
            {"day": "Friday",    "focus": "Shoulders + Triceps", "exercises": [
                {"name": "Overhead Press", "sets": 4, "reps": "10", "rest": 60, "cal_per_min": 5, "muscle": "shoulders"},
                {"name": "Lateral Raises", "sets": 3, "reps": "15", "rest": 45, "cal_per_min": 4, "muscle": "shoulders"},
                {"name": "Skull Crushers", "sets": 3, "reps": "12", "rest": 45, "cal_per_min": 4, "muscle": "arms"},
                {"name": "Tricep Dips", "sets": 3, "reps": "15", "rest": 45, "cal_per_min": 4, "muscle": "arms"},
            ]},
            {"day": "Saturday",  "focus": "Full Body HIIT", "exercises": [
                {"name": "Kettlebell Swings", "sets": 4, "reps": "20", "rest": 30, "cal_per_min": 10, "muscle": "cardio"},
                {"name": "Box Jumps", "sets": 4, "reps": "10", "rest": 45, "cal_per_min": 9, "muscle": "legs"},
                {"name": "Battle Ropes", "sets": 4, "reps": "30s", "rest": 30, "cal_per_min": 11, "muscle": "cardio"},
            ]},
            {"day": "Sunday",    "focus": "Rest", "exercises": []},
        ],
    },
    "gain_muscle": {
        "beginner": [
            {"day": "Monday",    "focus": "Push (Chest/Shoulders/Triceps)", "exercises": [
                {"name": "Push-ups", "sets": 4, "reps": "12", "rest": 60, "cal_per_min": 4, "muscle": "chest"},
                {"name": "Dumbbell Press", "sets": 3, "reps": "10", "rest": 60, "cal_per_min": 4, "muscle": "chest"},
                {"name": "Shoulder Press", "sets": 3, "reps": "10", "rest": 60, "cal_per_min": 4, "muscle": "shoulders"},
                {"name": "Tricep Extensions", "sets": 3, "reps": "12", "rest": 45, "cal_per_min": 3, "muscle": "arms"},
            ]},
            {"day": "Tuesday",   "focus": "Pull (Back/Biceps)", "exercises": [
                {"name": "Dumbbell Row", "sets": 4, "reps": "10", "rest": 60, "cal_per_min": 4, "muscle": "back"},
                {"name": "Lat Pulldown", "sets": 3, "reps": "12", "rest": 60, "cal_per_min": 4, "muscle": "back"},
                {"name": "Bicep Curls", "sets": 3, "reps": "12", "rest": 45, "cal_per_min": 3, "muscle": "arms"},
                {"name": "Hammer Curls", "sets": 3, "reps": "12", "rest": 45, "cal_per_min": 3, "muscle": "arms"},
            ]},
            {"day": "Wednesday", "focus": "Legs + Core", "exercises": [
                {"name": "Barbell Squats", "sets": 4, "reps": "10", "rest": 90, "cal_per_min": 6, "muscle": "legs"},
                {"name": "Leg Press", "sets": 3, "reps": "12", "rest": 60, "cal_per_min": 5, "muscle": "legs"},
                {"name": "Plank", "sets": 3, "reps": "45s", "rest": 30, "cal_per_min": 3, "muscle": "core"},
                {"name": "Russian Twists", "sets": 3, "reps": "20", "rest": 30, "cal_per_min": 3, "muscle": "core"},
            ]},
            {"day": "Thursday",  "focus": "Rest", "exercises": []},
            {"day": "Friday",    "focus": "Push (Heavy)", "exercises": [
                {"name": "Bench Press", "sets": 4, "reps": "8", "rest": 90, "cal_per_min": 5, "muscle": "chest"},
                {"name": "Incline Press", "sets": 3, "reps": "10", "rest": 60, "cal_per_min": 5, "muscle": "chest"},
                {"name": "Arnold Press", "sets": 3, "reps": "10", "rest": 60, "cal_per_min": 4, "muscle": "shoulders"},
            ]},
            {"day": "Saturday",  "focus": "Pull (Heavy)", "exercises": [
                {"name": "Deadlifts", "sets": 4, "reps": "6", "rest": 120, "cal_per_min": 6, "muscle": "back"},
                {"name": "Pull-ups", "sets": 4, "reps": "8", "rest": 60, "cal_per_min": 5, "muscle": "back"},
                {"name": "Seated Cable Row", "sets": 3, "reps": "12", "rest": 60, "cal_per_min": 4, "muscle": "back"},
            ]},
            {"day": "Sunday",    "focus": "Active Recovery", "exercises": []},
        ],
    },
    "maintain": {
        "beginner": [
            {"day": "Monday",    "focus": "Full Body Strength", "exercises": [
                {"name": "Bodyweight Squats", "sets": 3, "reps": "15", "rest": 45, "cal_per_min": 5, "muscle": "legs"},
                {"name": "Push-ups", "sets": 3, "reps": "12", "rest": 45, "cal_per_min": 4, "muscle": "chest"},
                {"name": "Plank", "sets": 3, "reps": "30s", "rest": 30, "cal_per_min": 3, "muscle": "core"},
                {"name": "Jumping Jacks", "sets": 3, "reps": "30", "rest": 30, "cal_per_min": 8, "muscle": "cardio"},
            ]},
            {"day": "Tuesday",   "focus": "Yoga / Stretching", "exercises": []},
            {"day": "Wednesday", "focus": "Cardio", "exercises": [
                {"name": "Brisk Walk / Jog", "sets": 1, "reps": "30 min", "rest": 0, "cal_per_min": 6, "muscle": "cardio"},
                {"name": "Cycling", "sets": 1, "reps": "20 min", "rest": 0, "cal_per_min": 8, "muscle": "cardio"},
            ]},
            {"day": "Thursday",  "focus": "Rest", "exercises": []},
            {"day": "Friday",    "focus": "Full Body", "exercises": [
                {"name": "Lunges", "sets": 3, "reps": "12", "rest": 45, "cal_per_min": 5, "muscle": "legs"},
                {"name": "Dumbbell Press", "sets": 3, "reps": "12", "rest": 45, "cal_per_min": 4, "muscle": "chest"},
                {"name": "Dumbbell Row", "sets": 3, "reps": "12", "rest": 45, "cal_per_min": 4, "muscle": "back"},
            ]},
            {"day": "Saturday",  "focus": "Light Cardio", "exercises": [
                {"name": "Cycling or Swimming", "sets": 1, "reps": "40 min", "rest": 0, "cal_per_min": 7, "muscle": "cardio"},
            ]},
            {"day": "Sunday",    "focus": "Rest", "exercises": []},
        ],
    },
}


def generate_workout_plan(goal, level, weight_kg=70):
    """Return weekly workout plan based on user goal and fitness level."""
    goal_key = goal if goal in WORKOUT_TEMPLATES else "maintain"
    level_key = level if level in WORKOUT_TEMPLATES.get(goal_key, {}) else "beginner"
    plan = WORKOUT_TEMPLATES.get(goal_key, {}).get(level_key, WORKOUT_TEMPLATES["maintain"]["beginner"])
    return plan


def get_today_workout(goal, level):
    """Return today's workout specifically."""
    plan = generate_workout_plan(goal, level)
    day_name = date.today().strftime("%A")
    for day in plan:
        if day["day"] == day_name:
            return day
    return {"day": day_name, "focus": "Rest", "exercises": []}


def calculate_calories_burned(exercises, weight_kg=70):
    """Estimate calories burned from a list of exercises."""
    total = 0
    for ex in exercises:
        # Rough estimate: cal_per_min * estimated_duration
        reps_str = str(ex.get("reps", "10"))
        if "min" in reps_str:
            mins = float(reps_str.replace(" min", "").strip())
        elif "s" in reps_str and not reps_str.replace("s", "").replace(" ", "").isdigit():
            mins = 1
        else:
            try:
                reps = int(reps_str.split()[0])
                mins = (reps * 3) / 60  # ~3 sec per rep
            except:
                mins = 1
        sets = ex.get("sets", 3)
        cpm = ex.get("cal_per_min", 5)
        total += sets * mins * cpm * (weight_kg / 70)
    return round(total)


# ══════════════════════════════════════════════
#  DIET AI - Indian Budget Meals
# ══════════════════════════════════════════════

INDIAN_FOOD_DB = {
    # name: {cal, protein, carbs, fat, cost_inr, serving_g, category}
    "Roti (1 piece)":           {"cal": 71,  "protein": 2.5, "carbs": 15, "fat": 0.4, "cost": 2,   "g": 30,  "cat": "grain"},
    "Brown Rice (1 cup)":       {"cal": 216, "protein": 5,   "carbs": 45, "fat": 1.8, "cost": 8,   "g": 195, "cat": "grain"},
    "White Rice (1 cup)":       {"cal": 204, "protein": 4.2, "carbs": 44, "fat": 0.4, "cost": 5,   "g": 195, "cat": "grain"},
    "Dal Tadka (1 bowl)":       {"cal": 180, "protein": 11,  "carbs": 28, "fat": 4,   "cost": 20,  "g": 200, "cat": "protein"},
    "Paneer Bhurji (100g)":     {"cal": 265, "protein": 18,  "carbs": 6,  "fat": 19,  "cost": 35,  "g": 100, "cat": "protein"},
    "Chicken Breast (100g)":    {"cal": 165, "protein": 31,  "carbs": 0,  "fat": 3.6, "cost": 40,  "g": 100, "cat": "protein"},
    "Egg (1 boiled)":           {"cal": 78,  "protein": 6,   "carbs": 0.6,"fat": 5,   "cost": 7,   "g": 50,  "cat": "protein"},
    "Banana (1 medium)":        {"cal": 89,  "protein": 1.1, "carbs": 23, "fat": 0.3, "cost": 8,   "g": 118, "cat": "fruit"},
    "Apple (1 medium)":         {"cal": 95,  "protein": 0.5, "carbs": 25, "fat": 0.3, "cost": 15,  "g": 182, "cat": "fruit"},
    "Oats (50g dry)":           {"cal": 190, "protein": 6.5, "carbs": 34, "fat": 3.5, "cost": 12,  "g": 50,  "cat": "grain"},
    "Curd (1 cup)":             {"cal": 150, "protein": 8,   "carbs": 11, "fat": 8,   "cost": 15,  "g": 245, "cat": "dairy"},
    "Sprouts (1 cup)":          {"cal": 86,  "protein": 8,   "carbs": 17, "fat": 0.4, "cost": 10,  "g": 104, "cat": "protein"},
    "Rajma Chawal (1 plate)":   {"cal": 350, "protein": 14,  "carbs": 62, "fat": 4,   "cost": 30,  "g": 300, "cat": "meal"},
    "Poha (1 plate)":           {"cal": 250, "protein": 4,   "carbs": 48, "fat": 5,   "cost": 15,  "g": 200, "cat": "meal"},
    "Idli (2 pieces)":          {"cal": 140, "protein": 4,   "carbs": 30, "fat": 0.5, "cost": 15,  "g": 120, "cat": "meal"},
    "Sambar (1 bowl)":          {"cal": 100, "protein": 5,   "carbs": 15, "fat": 2,   "cost": 10,  "g": 200, "cat": "protein"},
    "Peanut Butter (2 tbsp)":   {"cal": 188, "protein": 8,   "carbs": 6,  "fat": 16,  "cost": 20,  "g": 32,  "cat": "fat"},
    "Almonds (10 pieces)":      {"cal": 70,  "protein": 2.6, "carbs": 2.5,"fat": 6,   "cost": 15,  "g": 12,  "cat": "fat"},
    "Milk (1 glass 250ml)":     {"cal": 150, "protein": 8,   "carbs": 12, "fat": 8,   "cost": 12,  "g": 250, "cat": "dairy"},
    "Vegetable Sabzi (1 bowl)": {"cal": 120, "protein": 3,   "carbs": 18, "fat": 4,   "cost": 25,  "g": 200, "cat": "vegetable"},
    "Amul Paneer (100g)":       {"cal": 265, "protein": 18,  "carbs": 6,  "fat": 20,  "cost": 50,  "g": 100, "cat": "protein"},
    "Chana Masala (1 bowl)":    {"cal": 210, "protein": 12,  "carbs": 35, "fat": 4,   "cost": 25,  "g": 200, "cat": "protein"},
    "Soya Chunks (50g dry)":    {"cal": 175, "protein": 25,  "carbs": 15, "fat": 0.5, "cost": 10,  "g": 50,  "cat": "protein"},
    "Bread (2 slices)":         {"cal": 140, "protein": 4,   "carbs": 28, "fat": 1.5, "cost": 8,   "g": 60,  "cat": "grain"},
    "Sweet Potato (100g)":      {"cal": 86,  "protein": 1.6, "carbs": 20, "fat": 0.1, "cost": 8,   "g": 100, "cat": "vegetable"},
}


MEAL_PLANS = {
    "lose_weight": {
        "1500": {
            "breakfast": [
                {"items": ["Oats (50g dry)", "Banana (1 medium)", "Milk (1 glass 250ml)"], "note": "High-fiber, filling breakfast"},
            ],
            "lunch": [
                {"items": ["Brown Rice (1 cup)", "Dal Tadka (1 bowl)", "Vegetable Sabzi (1 bowl)", "Curd (1 cup)"], "note": "Balanced macro lunch"},
            ],
            "snack": [
                {"items": ["Apple (1 medium)", "Almonds (10 pieces)"], "note": "Low-calorie snack"},
            ],
            "dinner": [
                {"items": ["Roti (1 piece)", "Roti (1 piece)", "Dal Tadka (1 bowl)", "Vegetable Sabzi (1 bowl)"], "note": "Light dinner"},
            ],
        },
    },
    "gain_muscle": {
        "2500": {
            "breakfast": [
                {"items": ["Oats (50g dry)", "Egg (1 boiled)", "Egg (1 boiled)", "Egg (1 boiled)", "Banana (1 medium)", "Milk (1 glass 250ml)"], "note": "Protein-rich morning fuel"},
            ],
            "lunch": [
                {"items": ["White Rice (1 cup)", "Chicken Breast (100g)", "Dal Tadka (1 bowl)", "Vegetable Sabzi (1 bowl)"], "note": "High protein, high carb"},
            ],
            "snack": [
                {"items": ["Peanut Butter (2 tbsp)", "Bread (2 slices)", "Banana (1 medium)"], "note": "Pre/Post workout snack"},
            ],
            "dinner": [
                {"items": ["Roti (1 piece)", "Roti (1 piece)", "Roti (1 piece)", "Paneer Bhurji (100g)", "Curd (1 cup)"], "note": "Protein-heavy dinner"},
            ],
        },
    },
    "maintain": {
        "2000": {
            "breakfast": [
                {"items": ["Poha (1 plate)", "Egg (1 boiled)", "Egg (1 boiled)", "Milk (1 glass 250ml)"], "note": "Easy balanced breakfast"},
            ],
            "lunch": [
                {"items": ["Rajma Chawal (1 plate)", "Curd (1 cup)", "Vegetable Sabzi (1 bowl)"], "note": "Classic Indian balanced meal"},
            ],
            "snack": [
                {"items": ["Sprouts (1 cup)", "Apple (1 medium)"], "note": "Nutritious snack"},
            ],
            "dinner": [
                {"items": ["Roti (1 piece)", "Roti (1 piece)", "Dal Tadka (1 bowl)", "Vegetable Sabzi (1 bowl)"], "note": "Light dinner"},
            ],
        },
    },
}


def generate_diet_plan(goal, tdee, budget_inr=150, is_veg=True):
    """Generate a daily diet plan with nutritional and cost info."""
    goal_key = goal if goal in MEAL_PLANS else "maintain"
    cal_key = list(MEAL_PLANS[goal_key].keys())[0]
    plan = MEAL_PLANS[goal_key][cal_key]

    meals_list = []
    total_cals = 0
    total_protein = 0
    total_cost = 0

    for meal_type, options in plan.items():
        meal = options[0]  # MVP: pick first option
        items_detail = []
        meal_cals = 0
        meal_protein = 0
        meal_cost = 0

        for item_name in meal["items"]:
            # Skip non-veg if user is veg
            if is_veg and any(nv in item_name for nv in ["Chicken", "Fish", "Mutton"]):
                item_name = "Soya Chunks (50g dry)"
            if item_name in INDIAN_FOOD_DB:
                fd = INDIAN_FOOD_DB[item_name]
                items_detail.append({
                    "name": item_name,
                    "calories": fd["cal"],
                    "protein": fd["protein"],
                    "carbs": fd["carbs"],
                    "fat": fd["fat"],
                    "cost": fd["cost"],
                })
                meal_cals += fd["cal"]
                meal_protein += fd["protein"]
                meal_cost += fd["cost"]
        meals_list.append({
            "type": meal_type,
            "name": meal["note"],
            "description": " · ".join([i["name"] for i in items_detail]),
            "calories": round(meal_cals),
            "protein": f"{round(meal_protein, 1)}g",
        })

        total_cals += meal_cals
        total_protein += meal_protein
        total_cost += meal_cost

    return {
        "budget": {
            "spent": round(total_cost),
            "target": budget_inr
        },
        "macros": {
            "calories": tdee,
            "protein": f"{round(tdee * 0.3 / 4)}g",  # 30% protein
            "carbs": f"{round(tdee * 0.4 / 4)}g",    # 40% carbs
            "fats": f"{round(tdee * 0.3 / 9)}g"      # 30% fats
        },
        "meals": meals_list
    }


# ══════════════════════════════════════════════
#  CHATBOT AI - Rule-Based Fitness Advisor
# ══════════════════════════════════════════════

CHATBOT_RESPONSES = {
    "protein": "💪 For muscle gain, aim for **1.6–2.2g of protein per kg** of body weight daily. Great Indian sources: paneer, dal, soya chunks, eggs, chicken, sprouts, and Greek yogurt.",
    "weight loss": "🔥 For weight loss: create a **300-500 calorie deficit** daily. Focus on more vegetables, dal, and whole grains. Avoid sugary drinks and refined flour (maida).",
    "chest": "🏋️ Best chest exercises: **Bench Press, Push-ups, Incline Press, Cable Flyes, Dips**. Train chest 1-2x/week with 3-4 sets of 8-15 reps.",
    "back": "💪 Best back exercises: **Deadlift, Pull-ups, Barbell Row, Lat Pulldown, Cable Row**. A strong back prevents injury and improves posture.",
    "legs": "🦵 Don't skip leg day! Key exercises: **Squats, Deadlifts, Leg Press, Lunges, Calf Raises**. Legs = your biggest muscle group = most calorie burn.",
    "cardio": "❤️ For fat loss: **20-30 min HIIT** 3x/week is more effective than long slow cardio. Try: 30s sprint, 30s rest, repeat 10-15 times.",
    "diet": "🥗 Best Indian diet tips: Eat **roti + dal + sabzi** as base. Add protein (paneer/egg/chicken). Avoid rice at night. Drink 3-4L water daily.",
    "supplement": "💊 Beginner supplements (optional): **Whey Protein** (if low on food protein), **Creatine** (5g/day for strength), **Vitamin D3** (most Indians are deficient). Always prefer food first!",
    "sleep": "😴 Sleep is when you grow! Aim for **7-9 hours** of quality sleep. Poor sleep raises cortisol, kills gains, and increases fat storage.",
    "water": "💧 Drink **3-4 liters** of water daily. More if you workout intensely. Signs of dehydration: fatigue, headache, dark urine.",
    "rest": "🛌 Rest days are NOT wasted days. Muscles grow **during recovery, not during workout**. Take 1-2 rest days per week.",
    "bmi": "📊 BMI categories: Underweight < 18.5, Normal 18.5-24.9, Overweight 25-29.9, Obese ≥ 30. However, BMI doesn't account for muscle mass — use it as a guide only.",
    "beginner": "🌟 Beginner tips: Start with **bodyweight exercises** first. Focus on form over weight. Workout 3x/week. Track your food. Sleep well. Results come in 8-12 weeks with consistency!",
    "creatine": "⚗️ **Creatine monohydrate** is the most researched supplement. 5g/day. No loading phase needed. Safe for long-term use. Improves strength and muscle volume slightly.",
    "motivation": "🚀 Remember: **Consistency beats perfection**. A 70% effort workout done regularly beats the perfect workout done once. Show up every day, results are guaranteed!",
    "fat": "🔥 You **cannot spot-reduce fat**. Fat is lost all over the body through overall calorie deficit. Combine cardio + strength training for best fat loss results.",
}


def chatbot_response(user_message):
    """Return a relevant fitness tip based on keyword matching."""
    msg_lower = user_message.lower()
    for keyword, response in CHATBOT_RESPONSES.items():
        if keyword in msg_lower:
            return response
    # Default response
    return (
        "🤖 I can help with questions about: **protein, weight loss, chest, back, legs, cardio, "
        "diet, supplements, sleep, water, rest days, BMI, creatine, fat loss, motivation**. "
        "What would you like to know?"
    )
