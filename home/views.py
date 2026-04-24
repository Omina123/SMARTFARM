
from django.contrib.auth.decorators import login_required
from .models import Field, Crop
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import *
from .models import *
from django.contrib import messages

def home(request):
    return render(request, 'index.html')

def dashboard(request):
    # Determine the queryset based on role
    if request.user.user_type == '1': # Admin
        fields = Field.objects.all()
        template = 'admin_dashboard.html'
    else: # Field Agent
        fields = Field.objects.filter(agent=request.user)
        template = 'agent_dashboard.html'

    # Summary Statistics (Status Breakdown)
    total_fields = fields.count()
    active = sum(1 for f in fields if f.computed_status == 'Active')
    at_risk = sum(1 for f in fields if f.computed_status == 'At Risk')
    completed = sum(1 for f in fields if f.computed_status == 'Completed')

    context = {
        'fields': fields,
        'total': total_fields,
        'active': active,
        'at_risk': at_risk,
        'completed': completed,
    }
    
    return render(request, template, context)



# Access Control: Only Admins can manage/create fields
def is_admin(user):
    return user.user_type == '1'

@user_passes_test(is_admin)
def create_field(request):
    if request.method == 'POST':
        form = FieldCreationForm(request.POST)
        if form.is_valid():
            # 1. Create the Crop instance
            new_crop = Crop.objects.create(
                name=form.cleaned_data['crop_name'],
                variety=form.cleaned_data['variety'],
                planting_date=form.cleaned_data['planting_date'],
                expected_harvest_date=form.cleaned_data['expected_harvest_date'],
                acreage=form.cleaned_data['acreage']
            )
            
            # 2. Create the Field and link the crop
            field = form.save(commit=False)
            field.crop = new_crop
            field.save()
            
            return redirect('dashboard')
    else:
        form = FieldCreationForm()
    
    return render(request, 'manage_field.html', {'form': form, 'title': 'Create New Field'})


@login_required
def update_field(request, field_id):
    field = get_object_or_404(Field, id=field_id)

    # Access Control: Only the assigned Agent or an Admin can perform updates
    is_assigned_agent = (field.agent == request.user)
    is_admin = (request.user.user_type == '1')

    if not (is_assigned_agent or is_admin):
        messages.error(request, "Access Denied: You are not assigned to this field.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = FieldUpdateForm(request.POST, instance=field)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updates for {field.name} saved successfully.")
            return redirect('dashboard')
    else:
        form = FieldUpdateForm(instance=field)

    context = {
        'form': form,
        'field': field,
        'title': 'Field Observation Update'
    }
    return render(request, 'pdate_field.html', context)
