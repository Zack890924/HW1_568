from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import F, Q, Sum, Value
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy


from .models import Ride, RideShare
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .forms import RideRequestForm, DriverSearchForm, SearchRideShareForm, RideShareForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import DriverRequiredMixin, OwnerRequiredMixin

from django.db.models.functions import Coalesce
# Create your views here.
class OpenRideListView(ListView):
    model = Ride
    template_name = 'rides/ride_list.html'
    context_object_name = 'rides_list'
    paginate_by = 5
    ordering = ['-created_at']

    def get_queryset(self):
        # 初步筛选状态为 OPEN 或 CLOSED 的 Ride (之后改为只显示OPEN)
        qs = super().get_queryset().filter(
            Q(status=Ride.Status.OPEN) | Q(status=Ride.Status.CLOSED)
        )
        # 使用 annotate 计算每个 Ride 的总乘客数：
        # 总乘客数 = owner_passengers + (所有 ride_share 中的 passenger 数量之和)
        # 使用 Coalesce 处理没有 ride_share 时 Sum 返回 None 的情况
        # ride_share__passenger表示访问 Ride 对象相关联的所有 RideShare 对象中的 passenger 字段
        qs = qs.annotate(
            total_people=F('owner_passengers') + Coalesce(Sum('ride_share__passenger'), Value(0))
        )
        # 过滤条件：如果 Ride 有司机，则要求 total_people <= driver__maxPassengers；
        # 如果 Ride 没有司机，则暂时保留（后续根据当前用户类型再决定是否排除）
        qs = qs.filter(
            Q(driver__isnull=True) | Q(total_people__lte=F('driver__maxPassengers'))
        )
        # 根据当前用户的 is_driver 字段进行进一步过滤：
        # 如果当前用户不是司机，则排除掉没有司机接单的 Ride（driver 为 NULL 的记录）
        if not self.request.user.userprofile.is_driver:
            qs = qs.filter(driver__isnull=False)

        # 获取 GET 请求中的搜索参数
        destination = self.request.GET.get('destination', '').strip()
        if destination:
            qs = qs.filter(destination__icontains=destination)

        # 到达时间区间搜索
        arrival_time_start = self.request.GET.get('arrival_time_start', '').strip()
        arrival_time_end = self.request.GET.get('arrival_time_end', '').strip()

        # datetime-local格式 'YYYY-MM-DDTHH:MM'
        if arrival_time_start:
            try:
                start_datetime = datetime.strptime(arrival_time_start, '%Y-%m-%dT%H:%M')
                qs = qs.filter(scheduled_datetime__gte=start_datetime)
            except ValueError:
                pass

        if arrival_time_end:
            try:
                end_datetime = datetime.strptime(arrival_time_end, '%Y-%m-%dT%H:%M')
                qs = qs.filter(scheduled_datetime__lte=end_datetime)
            except ValueError:
                pass

        # 乘客数量搜索：剩余座位大于或等于用户输入的数量
        passengers = self.request.GET.get('passengers', '').strip()
        if passengers:
            try:
                passengers = int(passengers)
                qs = qs.annotate(
                    available_seats=F('driver__maxPassengers') - F('total_people')
                ).filter(available_seats__gte=passengers)
            except ValueError:
                pass

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 将搜索参数传递到模板，用于回显搜索条件
        context['destination'] = self.request.GET.get('destination', '')
        context['arrival_time_start'] = self.request.GET.get('arrival_time_start', '')
        context['arrival_time_end'] = self.request.GET.get('arrival_time_end', '')
        context['passengers'] = self.request.GET.get('passengers', '')
        return context



class MyRidesView(ListView):
    model = Ride
    template_name = 'rides/my_rides_list.html'
    context_object_name = 'rides_list'
    paginate_by = 5
    ordering = ['-scheduled_datetime']

    def get_queryset(self):
        user = self.request.user

        user_profile = user.userprofile


        owned = Ride.objects.filter(owner=user_profile).exclude(status=Ride.Status.COMPLETED)


        sharer_rides = RideShare.objects.filter(sharer=user_profile).select_related('ride')
        sharer = Ride.objects.filter(id__in=sharer_rides.values('ride_id')).exclude(status=Ride.Status.COMPLETED)

        driven = Ride.objects.none()
        if hasattr(user, 'driverprofile'):
            driven = Ride.objects.filter(driver=user.driverprofile).exclude(status=Ride.Status.COMPLETED)

        return owned.union(sharer, driven)




class RideDetailView(DetailView):
    model = Ride
    template_name = 'rides/ride_detail.html'
    context_object_name = 'ride'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user_profile = self.request.user.userprofile
            context['has_joined'] = self.object.ride_share.filter(sharer=user_profile).exists()
        else:
            context['has_joined'] = False

        return context





# owner create ride
class RideCreateView(LoginRequiredMixin, CreateView):
    model = Ride
    form_class = RideRequestForm
    template_name = 'rides/ride_create.html'
    # success_url = reverse_lazy('rides:my_ride_list')
    success_url = reverse_lazy('home')

    # logic for form created successfully
    def form_valid(self, form):
        form.instance.owner = self.request.user.userprofile
        if form.cleaned_data.get('can_shared'):
            form.instance.status = Ride.Status.OPEN
        else:
            form.instance.status = Ride.Status.CLOSED
        return super().form_valid(form)


class RideEditView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Ride
    form_class = RideRequestForm
    template_name = 'rides/rides_edit.html'
    success_url = reverse_lazy('rides:my_ride_list')
    def form_valid(self, form):
        if form.instance.status != Ride.Status.OPEN:
            messages.error(self.request, "Cannot edit this form")
            # TODO direct location needs to be improve
            return redirect('rides:ride-list')
        return super().form_valid(form)


# Sharer search for ride
@login_required()
def ride_search(request):
    form = SearchRideShareForm(request.GET or None)
    rides = []

    if form.is_valid():
        destination = form.cleaned_data['destination']
        earliest_dt = form.cleaned_data['earliest_date']
        latest_dt = form.cleaned_data['latest_date']
        passengers_size = form.cleaned_data['passengers_size'] or 1


        rides = (Ride.objects.filter(status = 'OPEN', can_shared = True)
                 .annotate(available_seats=F('driver__capacity') - 1 - F('owner_passengers')))


        if destination:
            rides = rides.filter(destination__icontains=destination)

        if earliest_dt:
            rides = rides.filter(scheduled_datetime__gte=earliest_dt)
        if latest_dt:
            rides = rides.filter(scheduled_datetime__lte=latest_dt)

        rides = rides.filter(available_seats__gte=passengers_size)



        rides = rides.order_by('-created_at')
    return render(request, 'rides/ride_search.html', {'rides': rides, 'form': form})


@login_required()
def ride_join(request, pk):
    ride = get_object_or_404(Ride, pk=pk, status='OPEN', can_shared=True)
    if request.method == 'POST':
        form = RideShareForm(request.POST)
        if form.is_valid():
            ride_share = form.save(commit=False)
            ride_share.ride = ride
            ride_share.sharer = request.user.userprofile
            try:
                ride_share.save()
                messages.success(request, 'You have joined the ride successfully')
            except IntegrityError:
                messages.error(request, 'You have already joined the ride')
            return redirect('rides:my-ride-list')
    else:
        form = RideShareForm()
    return render(request, 'rides/ride_join.html', {'form': form, 'ride': ride})

@login_required()
def driver_search_ride(request):
    driver_profile = getattr(request.user, 'driverprofile', None)
    if driver_profile is None:
        messages.error(request, 'You are not a driver')
        return redirect('rides:ride-list')
    form = DriverSearchForm(request.GET or None)
    valid_rides = []
    if form.is_valid():
        destination = form.cleaned_data['destination']


        rides = Ride.objects.filter(status = 'OPEN', can_shared = True)
        if destination:
            rides = rides.filter(destination__icontains=destination)
            for ride in rides:
                if ride.vehicle_type_request and driver_profile.vehicle_type != ride.vehicle_type_request:
                    continue
                if ride.total_amount_people() > driver_profile.capacity:
                    continue
                # TODO Special request
                valid_rides.append(ride)
    return render(request,
                  'rides/driver_search.html',
                  {'rides': valid_rides, 'form': form}
                  )


def send_email_for_ride(ride):
    subject = f"Your ride {ride.id} has been claimed"
    email_messages = f'''
        Dear {ride.owner.name}, your ride to {ride.destination} has been claimed by a driver!
        Ride detail: 
            - Date: {ride.date}
            - Time: {ride.time}
            - Destination: {ride.destination}
            - Vehicle type: {ride.vehicle_type}
            - Driver: {ride.driver.name}
    '''
    recipients = [ride.owner.userprofile.email]
    for ride_share in ride.ride_share.all():
        recipients.append(ride_share.sharer.userprofile.email)

    send_mail(subject, email_messages, settings.DEFAULT_FROM_EMAIL, recipients)


@login_required()
def driver_claim_ride(request, pk):
    driver_profile = getattr(request.user, 'driverprofile', None)
    if driver_profile is None:
        messages.error(request, 'You are not a driver')
        return redirect('rides:ride-list')
    ride = get_object_or_404(Ride, pk=pk, status='OPEN')
    # double check
    if ride.total_amount_people() > driver_profile.capacity:
        messages.error(request, 'Passengers size exceed total capacity')
        return redirect('rides:ride-list')

    ride.driver = request.user.driverprofile
    ride.status = 'CONFIRMED'
    ride.save()


    send_email_for_ride(ride)
    messages.success(request, f"You have successfully claimed ride #{ride.id}!")
    return redirect('rides:ride-list')


@login_required()
def driver_complete_ride(request, pk):
    ride = get_object_or_404(Ride, pk=pk, status='CONFIRMED', driver = request.user.driverprofile)
    if request.method == 'POST':
        ride.status = 'COMPLETED'
        ride.save()
        messages.success(request, f"You have successfully completed ride #{ride.id}!")
        return redirect('rides:ride-list')
    return render(request, 'rides/driver_complete.html', {'ride': ride})



