from .models import User
from .config import *

def r01_no_matches(email_matches, phone_number_matches, email, phone_number):
    """If both email_matches and phone_number_matches are empty, add a new primary record to our db"""
    
    if not len(email_matches) and not len(phone_number_matches):
        user = User(email=email, phoneNumber=phone_number, linkPrecedence=User.LinkPrecedenceChoices.primary)
        user.save()
        return {'status': SUCCESS, 'data': user}
    return {'status': FAILED, 'data': None}



RECON_RULES = [r01_no_matches]

def populate_data(matched_user, primary_contact_id, emails, phone_numbers, secondary_contact_ids):
    emails.append(matched_user.email)
    if matched_user.phoneNumber:
        phone_numbers.append(matched_user.phoneNumber)
    if matched_user.linkPrecedence == User.LinkPrecedenceChoices.primary:
        primary_contact_id = matched_user.id
    else:
        secondary_contact_ids.append(matched_user.id)
    return primary_contact_id, emails, phone_numbers, secondary_contact_ids

def recon_main(email, phone_number):
    # Get entries that match with the email
    email_matches = User.objects.filter(email=email)
    # Get entries that match with the phone_number
    phone_number_matches = User.objects.filter(phoneNumber=phone_number)
    for rule in RECON_RULES:
        res = rule(email_matches, phone_number_matches, email, phone_number)
        if res['status'] == SUCCESS:
            break
    
    # Get new entries as primary might have changed
    email_matches = User.objects.filter(email=email)
    phone_number_matches = User.objects.filter(phoneNumber=phone_number)
    primary_contact_id = None
    emails = []
    phone_numbers = []
    secondary_contact_ids = []
    
    for email_match in email_matches:
        primary_contact_id, emails, phone_numbers, secondary_contact_ids = populate_data(email_match, primary_contact_id, emails, phone_numbers, secondary_contact_ids)
    for phone_number_match in phone_number_matches:
        primary_contact_id, emails, phone_numbers, secondary_contact_ids = populate_data(phone_number_match, primary_contact_id, emails, phone_numbers, secondary_contact_ids)
    
    return 	{
		"contact":{
			"primaryContatctId": primary_contact_id,
			"emails": list(set(emails)),
			"phoneNumbers": list(set(phone_numbers)),
			"secondaryContactIds": list(set(secondary_contact_ids))
		}
	}