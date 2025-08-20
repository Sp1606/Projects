import datetime
import time

def time_audit():
    """
    Tracks how you currently spend your wasted hour.
    """
    print("Let's track your current wasted hour for 3 days to understand your habits.")
    audit_data = []

    for day in range(1, 4):
        print(f"\n--- Day {day} ---")
        start_time = input("What time did your wasted hour START today? (HH:MM format): ")
        end_time = input("What time did your wasted hour END today? (HH:MM format): ")

        try:
            start_datetime = datetime.datetime.strptime(start_time, "%H:%M")
            end_datetime = datetime.datetime.strptime(end_time, "%H:%M")
            duration = end_datetime - start_datetime
            duration_minutes = duration.total_seconds() / 60

            if duration_minutes > 60 * 1.5 or duration_minutes < 30: # Reasonable time range
                print("Invalid time range.  Please enter a time range close to an hour.")
                continue # Skip to the next day

        except ValueError:
            print("Invalid time format. Please use HH:MM format.")
            continue # Skip to the next day

        activity = input("What activities did you do during this wasted hour? (Be specific): ")
        audit_data.append({
            "day": day,
            "start_time": start_time,
            "end_time": end_time,
            "activity": activity
        })

    print("\n--- Time Audit Summary ---")
    for item in audit_data:
        print(f"Day {item['day']}: {item['start_time']} - {item['end_time']} - {item['activity']}")

    return audit_data


def identify_monetizable_skills(audit_data):
    """
    Identifies potential skills to monetize based on the time audit.
    """
    print("\n--- Identifying Monetizable Skills ---")
    print("Based on your time audit and interests, consider these options:")

    # These are just example suggestions - you need to customize this.
    suggestions = [
        "Freelance writing/editing (content mill, blog posts)",
        "Online tutoring (specific subject you're good at)",
        "Social media management (for small businesses)",
        "Virtual assistant tasks (data entry, scheduling)",
        "Creating and selling digital products (eBooks, templates)",
        "Affiliate marketing (promote products related to your interests)",
        "Online surveys and micro-tasks (low pay but easy)",
        "Learning a new skill (e.g., coding) and freelancing"
    ]

    for i, suggestion in enumerate(suggestions):
        print(f"{i+1}. {suggestion}")

    skill_choice = input("Which skill are you most interested in exploring? (Enter number): ")

    try:
        skill_index = int(skill_choice) - 1
        chosen_skill = suggestions[skill_index]
        print(f"Great! You've chosen: {chosen_skill}")
        return chosen_skill
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a number from the list.")
        return None


def skill_development(chosen_skill):
    """
    Provides guidance on how to develop the chosen skill.
    """
    print(f"\n--- Skill Development for {chosen_skill} ---")

    # Customize this section based on the chosen skill.  These are EXAMPLES!
    if "writing" in chosen_skill.lower():
        print("1. Take an online writing course (e.g., on Coursera, Udemy, Skillshare).")
        print("2. Practice writing daily (even for just 30 minutes).")
        print("3. Build a portfolio of your best writing samples.")
        print("4. Create a profile on freelance platforms like Upwork or Fiverr.")
    elif "tutoring" in chosen_skill.lower():
        print("1. Identify your subject expertise and target audience.")
        print("2. Create a profile on online tutoring platforms (e.g., TutorMe, Chegg Tutors).")
        print("3. Develop engaging lesson plans and teaching materials.")
        print("4. Market your tutoring services to students.")
    elif "social media" in chosen_skill.lower():
        print("1. Take a social media marketing course (e.g., HubSpot Academy).")
        print("2. Practice managing social media accounts for friends or family.")
        print("3. Build a portfolio of your work.")
        print("4. Offer your services to local businesses.")
    else:
        print("I need more information to provide specific skill development guidance.")


def action_plan(chosen_skill):
    """
    Creates a concrete action plan to start earning.
    """
    print("\n--- Action Plan to Earn $500/Month ---")

    # Customize this based on the chosen skill
    if "writing" in chosen_skill.lower():
        print("1. Set a goal of earning $16.67 per day ($500 / 30 days).")
        print("2. Identify writing platforms that pay well (e.g., ProBlogger Job Board).")
        print("3. Pitch your writing services to potential clients.")
        print("4. Track your earnings daily and adjust your strategy as needed.")

    elif "tutoring" in chosen_skill.lower():
        print("1. Determine your hourly rate (research competitive rates).")
        print("2. Set a goal of tutoring a certain number of hours per week (e.g., 5-10 hours).")
        print("3. Market your tutoring services through online platforms and local schools.")
        print("4. Track your earnings and student progress.")

    elif "social media" in chosen_skill.lower():
        print("1. Research average rates for social media management services in your area.")
        print("2. Create a proposal for a potential client outlining the benefits of your services.")
        print("3. Offer packages that fit different budgets.")
        print("4. Network with local businesses and attend industry events.")

    else:
        print("I need more information to provide a specific action plan.")


def time_reallocation():
    """
    Helps you reallocate your wasted hour.
    """
    print("\n--- Reallocating Your Wasted Hour ---")
    print("Now that you have a plan, it's time to replace your wasted activities with income-generating activities.")
    print("For example, instead of scrolling social media, you'll be writing articles or tutoring students.")
    print("This requires discipline and commitment.  Set reminders and track your progress.")
    print("Consider using time blocking techniques to schedule your hour effectively.")


def track_progress():
    """
    Tracks progress and provides encouragement.
    """
    print("\n--- Tracking Your Progress ---")
    print("It's important to track your progress to stay motivated.")
    print("Keep a log of your earnings and the time you spend working.")
    print("Celebrate your successes and learn from your setbacks.")
    print("Don't give up!  With consistent effort, you can achieve your goal of earning $500/month.")


def main():
    """
    Main function to execute the program.
    """
    print("Welcome to the 1-Hour to $500/Month System!")

    audit_data = time_audit()
    if not audit_data:
        return  # Exit if audit failed

    chosen_skill = identify_monetizable_skills(audit_data)
    if not chosen_skill:
        return # Exit if no skill chosen

    skill_development(chosen_skill)
    action_plan(chosen_skill)
    time_reallocation()
    track_progress()

    print("\nGood luck!  Remember, consistency and dedication are key to success.")


if __name__ == "__main__":
    main()