import json


# ==============================================================
# 1. Define the Case Base (Past Student Interventions)
# ==============================================================
case_base = [
    {
        "id": "CASE_101",
        "problem": {
            "topic": "Algebra",
            "error_type": "Formula Misuse",
            "error_frequency": 3,
            "skill_level": "Beginner"
        },
        "solution": {
            "feedback": "Review the quadratic formula components step-by-step.",
            "recommended_lesson": "Algebra Fundamentals: Video Walkthrough 2.1",
            "practice_difficulty": "Easy",
            "recommended_practice_problems": 3
        }
    },
    {
        "id": "CASE_102",
        "problem": {
            "topic": "Calculus",
            "error_type": "Sign Error",
            "error_frequency": 2,
            "skill_level": "Intermediate"
        },
        "solution": {
            "feedback": "Pay close attention when applying the chain rule to negative exponents.",
            "recommended_lesson": "Derivatives: Signs & Negative Exponent Drill",
            "practice_difficulty": "Medium",
            "recommended_practice_problems": 4
        }
    },
    {
        "id": "CASE_103",
        "problem": {
            "topic": "Algebra",
            "error_type": "Formula Misuse",
            "error_frequency": 5,
            "skill_level": "Intermediate"
        },
        "solution": {
            "feedback": "Double check parenthetical distribution before substituting values into the formula.",
            "recommended_lesson": "Algebra: Common Formula Pitfalls & Practice Modules",
            "practice_difficulty": "Medium",
            "recommended_practice_problems": 5
        }
    },
    {
        "id": "CASE_104",
        "problem": {
            "topic": "Geometry",
            "error_type": "Conceptual Misunderstanding",
            "error_frequency": 4,
            "skill_level": "Beginner"
        },
        "solution": {
            "feedback": "Focus on the geometric definitions of angles before applying the theorems.",
            "recommended_lesson": "Geometry Foundations: Interactive Angle Visualizer",
            "practice_difficulty": "Easy",
            "recommended_practice_problems": 3
        }
    }
]




# ==============================================================
# 2. Similarity Assessment (Weighted Scoring)
# ==============================================================
def calculate_similarity(query_problem, case_problem):
    """
    Computes a weighted similarity score (0.0 to 1.0):
    - Topic match: 35% weight
    - Error Type match: 35% weight
    - Skill Level match: 15% weight
    - Error Frequency proximity: 15% weight (max difference span: 5)
    """
    topic_score = 1.0 if query_problem["topic"].strip().lower() == case_problem["topic"].lower() else 0.0
    error_score = 1.0 if query_problem["error_type"].strip().lower() == case_problem["error_type"].lower() else 0.0
    skill_score = 1.0 if query_problem["skill_level"].strip().lower() == case_problem["skill_level"].lower() else 0.0
   
    freq_diff = abs(query_problem["error_frequency"] - case_problem["error_frequency"])
    freq_score = max(0.0, 1.0 - (freq_diff / 5.0))


    total_similarity = (
        (topic_score * 0.35) +
        (error_score * 0.35) +
        (skill_score * 0.15) +
        (freq_score * 0.15)
    )
    return round(total_similarity, 3)


def retrieve_best_case(new_problem, cases):
    ranked_cases = []
    for case in cases:
        score = calculate_similarity(new_problem, case["problem"])
        ranked_cases.append((case, score))


    # Sort descending by similarity score
    ranked_cases.sort(key=lambda x: x[1], reverse=True)
    return ranked_cases[0], ranked_cases




# ==============================================================
# 3. Adapt the Solution
# ==============================================================
def adapt_solution(retrieved_case, new_problem, student_name="Student"):
    base_solution = retrieved_case["solution"]
    adapted = dict(base_solution)


    # Personalize feedback message
    adapted["feedback"] = f"Hi {student_name}, we noticed {new_problem['error_frequency']} instances of '{new_problem['error_type']}' in {new_problem['topic']}. {base_solution['feedback']}"


    # Scale problem count and adapt difficulty
    if new_problem["error_frequency"] >= 4:
        adapted["recommended_practice_problems"] = max(base_solution["recommended_practice_problems"], 6)
        adapted["practice_difficulty"] = "Guided Step-by-Step"
    else:
        adapted["recommended_practice_problems"] = max(3, new_problem["error_frequency"] + 1)
        adapted["practice_difficulty"] = new_problem["skill_level"].capitalize()


    adapted["recommended_lesson"] = f"[Adapted for {new_problem['skill_level'].capitalize()}] {base_solution['recommended_lesson']}"
    return adapted




# ==============================================================
# 4. Retain Stage (Learning)
# ==============================================================
def retain_case(cases, new_problem, final_solution):
    new_id = f"CASE_{101 + len(cases)}"
    new_case_entry = {
        "id": new_id,
        "problem": new_problem,
        "solution": final_solution
    }
    cases.append(new_case_entry)
    return new_case_entry




# ==============================================================
# 5. Interactive Execution
# ==============================================================
if __name__ == "__main__":
    print("=" * 65)
    print("      INTELLIGENT TUTORING SYSTEM (ITS) — STUDENT INPUT")
    print("=" * 65)


    # Interactive User Inputs
    student_name = input("Enter student name: ").strip() or "Student"
   
    print("\nAvailable Topics: Algebra, Calculus, Geometry")
    topic = input("Enter topic: ").strip().capitalize()
   
    print("\nCommon Errors: Formula Misuse, Sign Error, Conceptual Misunderstanding")
    error_type = input("Enter error type: ").strip().title()
   
    while True:
        try:
            error_frequency = int(input("Enter error frequency (number of occurrences): ").strip())
            if error_frequency > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter an integer.")


    print("\nSkill Levels: Beginner, Intermediate, Advanced")
    skill_level = input("Enter skill level: ").strip().capitalize()


    new_student_case = {
        "topic": topic,
        "error_type": error_type,
        "error_frequency": error_frequency,
        "skill_level": skill_level
    }


    # Step A: Problem Description Display
    print("\n" + "=" * 65)
    print("[1] NEW PROBLEM SUBMISSION:")
    print(f"Student Name    : {student_name}")
    print(f"Topic           : {new_student_case['topic']}")
    print(f"Detected Error  : {new_student_case['error_type']}")
    print(f"Error Frequency : {new_student_case['error_frequency']} times")
    print(f"Skill Level     : {new_student_case['skill_level']}")


    # Step B: Retrieval & Similarity Assessment
    (best_case, top_score), all_ranked = retrieve_best_case(new_student_case, case_base)


    print("\n[2] SIMILARITY RANKING OF PAST CASES:")
    for rank, (case, score) in enumerate(all_ranked, 1):
        print(f"  {rank}. {case['id']} | Topic: {case['problem']['topic']:<8} | Error: {case['problem']['error_type']:<26} | Similarity: {score * 100:.1f}%")


    print(f"\n✔ Most Relevant Past Case Retrieved: {best_case['id']} (Match: {top_score * 100:.1f}%)")
    print("   Problem Profile:", json.dumps(best_case["problem"]))
    print("   Original Solution:", json.dumps(best_case["solution"]))


    # Step C: Adaptation
    adapted_solution = adapt_solution(best_case, new_student_case, student_name=student_name)


    print("\n[3] ADAPTED FINAL SOLUTION (PERSONALIZED INTERVENTION):")
    print(f"  - Tailored Feedback   : {adapted_solution['feedback']}")
    print(f"  - Assigned Lesson     : {adapted_solution['recommended_lesson']}")
    print(f"  - Target Difficulty   : {adapted_solution['practice_difficulty']}")
    print(f"  - Practice Problems   : {adapted_solution['recommended_practice_problems']} problems")


    # Step D: Retain (Learning)
    saved_case = retain_case(case_base, new_student_case, adapted_solution)
    print(f"\n[4] LEARNING (RETAIN STAGE):")
    print(f"✔ New case saved successfully as '{saved_case['id']}'!")


    # Step E: Updated Case Base Overview
    print(f"\n[5] UPDATED CASE BASE (Total Records: {len(case_base)}):")
    for case in case_base:
        print(f"  * {case['id']}: [{case['problem']['topic']}] {case['problem']['error_type']} | Skill: {case['problem']['skill_level']} -> Lesson: {case['solution']['recommended_lesson']}")
    print("=" * 65)
