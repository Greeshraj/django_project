from datetime import datetime

def calculate_attendance_stats(joining_date, attendance_records):
    # Calculate total days from now to joining date
    today = datetime.now().date()
    total_days = (today - joining_date).days

    # Count total number of attendance records
    total_attendance = len(attendance_records)
    total_absent = total_days- total_attendance
    return total_days, total_attendance,total_absent
