from datetime import datetime, timedelta
from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from .models import User, Leave, Holiday

def add_leave_with_calculation(user, leave_type, start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    requested_days = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:
            if not Holiday.objects.filter(date=current_date).exists():
                requested_days += 1
        current_date += timedelta(days=1)

    remaining_leave_days = getattr(user, f"{leave_type}_leave_days")

    if requested_days > remaining_leave_days:
        extra_days = requested_days - remaining_leave_days
        return Response({
            "message": f"Not enough leave days. You are requesting {extra_days} extra days. Please connect with HR.",
            "extra_days": extra_days
        }, status=status.HTTP_400_BAD_REQUEST)

    setattr(user, f"{leave_type}_leave_days", F(f"{leave_type}_leave_days") - requested_days)
    user.save()

    Leave.objects.create(user=user, leave_type=leave_type, start_date=start_date, end_date=end_date)

    return Response({"message": "Leave added successfully"}, status=status.HTTP_201_CREATED)
