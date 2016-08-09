from core.views import monthly_occupant_report
from core.models import *
from django.contrib.auth.models import User

def monthly_occupant_report_console(location_slug, year, month):
	(occupants, messages) = monthly_occupant_report(location_slug, year, month)
	print "occupancy report for %s %s" % (month, year)
	print "name, email, total_nights, total_value, total_comped, owing, reference_ids"
	print "Residents"
	for v in occupants['residents'].values():
		print "%s, %s, %d" % (v['name'], v['email'], v['total_nights'])
	print "Guests"
	for v in occupants['guests'].values():
		print "%s, %s, %d, %d, %d, %s, %s" % (v['name'], v['email'], v['total_nights'], v['total_value'], v['total_comped'], ' '.join(map(str, v['owing'])), ' '.join(map(str, v['ids'])))
	print "Subscriptions"
	for v in occupants['members'].values():
		print "%s, %s, %d, %d, %d, %s, %s" % (v['name'], v['email'], v['total_nights'], v['total_value'], v['total_comped'], ' '.join(map(str, v['owing'])), ' '.join(map(str, v['ids'])))

	for message in messages:
		print message


def people_with_reservations_longer_than(min_length):
	# JKS this should probably be a manager method Reservation.objects.length(...)
	users = []
	reservations = Reservation.objects.all()
	for r in reservations:
		length = r.nights_between(r.arrive, r.depart)
		if length >= min_length:
			users.append(r.user)
	# make sure the returned list has only unique users
	return list(set(users))

def repeat_guests(num_stays, location=None):
	users = []
	all_users = User.objects.all()
	for u in all_users:
		if location:
			at_loc = u.reservations.filter(location = location).filter(status='confirmed')
			if len(at_loc) >= num_stays:
				users.append(u)
		else:
			if u.reservations.filter(status='confirmed').count() >= num_stays:
				users.append(u)
	return users




