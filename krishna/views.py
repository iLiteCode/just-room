from django.shortcuts import render ,redirect
from django.http import HttpResponse , HttpResponseRedirect
from .models import Hotels,Rooms,Reservation
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.all()  # This works with your custom model
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Rooms, Hotels
from .forms import RoomForm

from datetime import datetime



def Check_list(request):
    # Get all hotels for the location filter
    hotels = Hotels.objects.all()

    # Filter rooms based on query parameters
    rooms = Rooms.objects.filter(status='1')  # Only 'available' rooms
    location = request.GET.get('location')
    if location:
        rooms = rooms.filter(hotel__location=location)

    # Check for amenities (filters)
    if 'ac' in request.GET:
        rooms = rooms.filter(ac=True)
    if 'fan' in request.GET:
        rooms = rooms.filter(fan=True)
    if 'wifi' in request.GET:
        rooms = rooms.filter(wifi=True)
    if 'parking' in request.GET:
        rooms = rooms.filter(parking=True)
    if 'heater' in request.GET:
        rooms = rooms.filter(heater=True)
    if 'food_facility' in request.GET:
        rooms = rooms.filter(food_facility=True)

    # Filter based on other POST values
    if request.method == 'POST':
        location = request.POST.get('search_location')
        if location:
            rooms = rooms.filter(hotel__location=location)

        check_in = request.POST.get('cin')
        check_out = request.POST.get('cout')
        capacity = request.POST.get('capacity')

        if check_in and check_out:
            # Logic to exclude booked rooms in the selected date range
            booked_rooms = []
            for reservation in Reservation.objects.all():
                if (str(reservation.check_in) < str(check_in) and str(reservation.check_out) < str(check_out)) or \
                   (str(reservation.check_in) > str(check_in) and str(reservation.check_out) > str(check_out)):
                    pass
                else:
                    booked_rooms.append(reservation.room.id)

            rooms = rooms.exclude(id__in=booked_rooms)
        
        if capacity:
            rooms = rooms.filter(capacity__gte=int(capacity))

    context = {
        'rooms': rooms,
        'hotels': hotels,
    }
    return render(request, 'index.html', context)

#homepage
def homepage(request):
    all_location = Hotels.objects.values_list('location','id').distinct().order_by()
    if request.method =="POST":
        try:
            print(request.POST)
            hotel = Hotels.objects.all().get(id=int(request.POST['search_location']))
            rr = []
            
            #for finding the reserved rooms on this time period for excluding from the query set
            for each_reservation in Reservation.objects.all():
                if str(each_reservation.check_in) < str(request.POST['cin']) and str(each_reservation.check_out) < str(request.POST['cout']):
                    pass
                elif str(each_reservation.check_in) > str(request.POST['cin']) and str(each_reservation.check_out) > str(request.POST['cout']):
                    pass
                else:
                    rr.append(each_reservation.room.id)
                
            room = Rooms.objects.all().filter(hotel=hotel,capacity__gte = int(request.POST['capacity'])).exclude(id__in=rr)
            if len(room) == 0:
                messages.warning(request,"Sorry No Rooms Are Available on this time period")
            data = {'rooms':room,'all_location':all_location,'flag':True}
            response = render(request,'index.html',data)
        except Exception as e:
            messages.error(request,e)
            response = render(request,'index.html',{'all_location':all_location})


    else:
        
        
        data = {'all_location':all_location}
        response = render(request,'index.html',data)
    return HttpResponse(response)

#about
def aboutpage(request):
    return HttpResponse(render(request,'about.html'))

#contact page
def contactpage(request):
    return HttpResponse(render(request,'contact.html'))


#staff panel page
@login_required(login_url='/staff')
def panel(request):
    
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    
    rooms = Rooms.objects.all()
    total_rooms = len(rooms)
    available_rooms = len(Rooms.objects.all().filter(status='1'))
    unavailable_rooms = len(Rooms.objects.all().filter(status='2'))
    reserved = len(Reservation.objects.all())

    hotel = Hotels.objects.values_list('location','id').distinct().order_by()

    response = render(request,'staff/panel.html',{'location':hotel,'reserved':reserved,'rooms':rooms,'total_rooms':total_rooms,'available':available_rooms,'unavailable':unavailable_rooms})
    return HttpResponse(response)


@login_required(login_url='/staff')
def edit_room(request):
    if not request.user.is_staff:
        return HttpResponse('Access Denied')  # Staff-only access

    if request.method == 'POST':
        room_id = request.POST.get('roomid')
        
        if not room_id:
            messages.error(request, "Room ID is missing.")
            return redirect('staffpanel')  # Redirect if room ID is missing

        try:
            room = get_object_or_404(Rooms, id=room_id)
            form = RoomForm(request.POST, request.FILES, instance=room)

            if form.is_valid():
                form.save()  # Save the updated room to the database
                messages.success(request, "Room details updated successfully.")
                return redirect('staffpanel')  # Redirect to staff panel after success
            else:
                messages.error(request, "Form validation failed. Please correct the errors below.")
                return render(request, 'staff/editroom.html', {'form': form, 'room': room})  # Ensure return response

        except Rooms.DoesNotExist:
            messages.error(request, "Room not found.")
            return redirect('staffpanel')  # Redirect if room does not exist
        except Exception as e:
            messages.error(request, f"Error updating room: {e}")
            return render(request, 'staff/editroom.html', {'form': form, 'room': room})  # Ensure return response

    else:
        room_id = request.GET.get('roomid')

        if not room_id:
            messages.error(request, "Room ID is missing.")
            return redirect('staffpanel')  # Redirect if room ID is missing

        try:
            room = get_object_or_404(Rooms, id=room_id)
            form = RoomForm(instance=room)  # Pre-populate the form with the existing room data
            hotels = Hotels.objects.all()  # Get all hotels for the select options

            return render(request, 'staff/editroom.html', {'form': form, 'hotels': hotels, 'room': room})

        except Rooms.DoesNotExist:
            messages.error(request, "Room not found.")
            return redirect('staffpanel')  # Redirect if room does not exist

@login_required(login_url='/staff')
def add_new_room(request):
    if not request.user.is_staff:
        return HttpResponse('Access Denied')  # Staff-only access

    if request.method == "POST" and request.FILES:
        try:
            # Fetch the hotel based on the provided hotel ID
            hotel = Hotels.objects.get(id=int(request.POST['hotel']))

            # Parse check-in and check-out times if provided
            check_in_time = request.POST.get('check_in_time')
            check_out_time = request.POST.get('check_out_time')

            # Create a new room object
            new_room = Rooms(
                room_number=request.POST.get('room_number'),
                room_type=request.POST.get('roomtype'),
                capacity=int(request.POST.get('capacity', 0)),
                size=int(request.POST.get('size', 0)),
                price=float(request.POST.get('price', 0.0)),
                discount=float(request.POST.get('discount', 0.0)),
                status=request.POST.get('status'),
                hotel=hotel,
                description=request.POST.get('description'),
                heading=request.POST.get('heading'),
                food_facility=bool(request.POST.get('food_facility', False)),
                parking=bool(request.POST.get('parking', False)),
                check_in_time=check_in_time if check_in_time else None,
                check_out_time=check_out_time if check_out_time else None,
            )

            # Add images if provided
            if 'image1' in request.FILES:
                new_room.image1 = request.FILES['image1']
            if 'image2' in request.FILES:
                new_room.image2 = request.FILES['image2']
            if 'image3' in request.FILES:
                new_room.image3 = request.FILES['image3']

            # Validate and save the new room
            new_room.full_clean()
            new_room.save()

            messages.success(request, "New Room Added Successfully")
        except Exception as e:
            messages.error(request, f"Error adding room: {e}")
            return redirect('staffpanel')

    return redirect('staffpanel')




#booking room page
@login_required(login_url='/user')
def book_room_page(request):
    room = Rooms.objects.all().get(id=int(request.GET['roomid']))
    return HttpResponse(render(request,'user/bookroom.html',{'room':room}))


from datetime import datetime  # import datetime class

#For booking the room
@login_required(login_url='/user')
def book_room(request):
    
    if request.method == "POST":

        room_id = request.POST['room_id']
        
        room = Rooms.objects.all().get(id=room_id)
        #for finding the reserved rooms on this time period for excluding from the query set
        for each_reservation in Reservation.objects.all().filter(room=room):
            if str(each_reservation.check_in) < str(request.POST['check_in']) and str(each_reservation.check_out) < str(request.POST['check_out']):
                pass
            elif str(each_reservation.check_in) > str(request.POST['check_in']) and str(each_reservation.check_out) > str(request.POST['check_out']):
                pass
            else:
                messages.warning(request,"Sorry This Room is unavailable for Booking")
                return redirect("homepage")
            
        current_user = request.user
        total_person = int(request.POST['person'])
        booking_id = str(room_id) + str(datetime.now())  # using datetime.now() after import

        reservation = Reservation()
        room_object = Rooms.objects.all().get(id=room_id)
        room_object.status = '2'
        
        user_object = User.objects.all().get(username=current_user)

        reservation.guest = user_object
        reservation.room = room_object
        person = total_person
        reservation.check_in = request.POST['check_in']
        reservation.check_out = request.POST['check_out']

        reservation.save()

        messages.success(request,"Congratulations! Booking Successfull")

        return redirect("homepage")
    else:
        return HttpResponse('Access Denied')


def handler404(request):
    return render(request, '404.html', status=404)

from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from .models import Rooms, Reservation
from django.contrib import messages

@login_required(login_url='/staff')
def view_room(request):
    # Get room ID from the GET parameter 'roomid'
    room_id = request.GET.get('roomid')

    # Check if room ID exists, if not raise 404
    if not room_id:
        messages.error(request, "Room ID is required.")
        return HttpResponse(render(request, 'staff/viewroom.html', {'error': 'Room ID is required.'}))

    try:
        # Fetch the room using the room_id
        room = Rooms.objects.get(id=room_id)
    except Rooms.DoesNotExist:
        # Room does not exist
        raise Http404("Room not found")

    # Get all reservations for the specific room
    reservations = Reservation.objects.filter(room=room)

    # Get the current date for comparing bookings
    current_date = datetime.now().date()

    # Annotate each reservation with status: past, current, or future
    for reservation in reservations:
        if reservation.check_out < current_date:
            reservation.status = 'past'
        elif reservation.check_in <= current_date and reservation.check_out >= current_date:
            reservation.status = 'current'
        else:
            reservation.status = 'future'

    # Render the view with room and reservation details
    return HttpResponse(render(request, 'staff/viewroom.html', {
        'room': room,
        'reservations': reservations,
        'current_date': current_date  # Pass current date for date comparison
    }))



@login_required(login_url='/user')
def user_bookings(request):
    if request.user.is_authenticated == False:
        return redirect('userloginpage')
    
    user = User.objects.get(id=request.user.id)
    bookings = Reservation.objects.filter(guest=user)

    # Get the current date
    current_date = datetime.now().date()

    if not bookings:
        messages.warning(request, "No Bookings Found")

    return render(request, 'user/mybookings.html', {'bookings': bookings, 'current_date': current_date})

@login_required(login_url='/staff')
def add_new_location(request):
    if request.method == "POST" and request.user.is_staff:
        owner = request.POST['new_owner']
        location = request.POST['new_city']
        state = request.POST['new_state']
        country = request.POST['new_country']
        
        hotels = Hotels.objects.all().filter(location = location , state = state)
        if hotels:
            messages.warning(request,"Sorry City at this Location already exist")
            return redirect("staffpanel")
        else:
            new_hotel = Hotels()
            new_hotel.owner = owner
            new_hotel.location = location
            new_hotel.state = state
            new_hotel.country = country
            new_hotel.save()
            messages.success(request,"New Location Has been Added Successfully")
            return redirect("staffpanel")

    else:
        return HttpResponse("Not Allowed")
    
#for showing all bookings to staff

@login_required(login_url='/staff')
def all_bookings(request):

    bookings = Reservation.objects.all()

    # Get the current date
    current_date = datetime.now().date()


    if not bookings:
        messages.warning(request, "No Bookings Found")

    # Render the page with bookings and the current date
    return render(request, 'staff/allbookings.html', {
        'bookings': bookings,
        'current_date': current_date 
    })
























        