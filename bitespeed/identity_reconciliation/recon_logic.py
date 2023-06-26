from .models import User
from .config import *

def r01_no_matches(email_matches, phone_number_matches, email, phone_number):
    """If both email_matches and phone_number_matches are empty, add a new primary record to our db"""
    print(f"Running rule: r01_no_matches")
    if not len(email_matches) and not len(phone_number_matches):
        user = User(email=email, phoneNumber=phone_number, linkPrecedence=User.LinkPrecedenceChoices.primary)
        user.save()
        return {'status': SUCCESS, 'data': user}
    return {'status': FAILED, 'data': None}

def r02_full_match(email_matches, phone_number_matches, email, phone_number):
    # if we find a record where both phoneNumber and email match, return success to break loop
    print(f"Running rule: r02_full_match")
    for matched_user in email_matches:
        if matched_user.email == email and matched_user.phoneNumber == phone_number:
            return {'status': SUCCESS, 'data': matched_user}
    for matched_user in phone_number_matches:
        if matched_user.email == email and matched_user.phoneNumber == phone_number:
            return {'status': SUCCESS, 'data': matched_user}
        
    return {'status': FAILED, 'data': None}

def r03_multiple_primaries(email_matches, phone_number_matches, email, phone_number):
    # This rule caters to "Can primary contacts turn into secondary?"
    #  i.e., if a primary was found in email_matches and phone_number_matches
    print(f"Running rule: r03_multiple_primaries")
    primary_user = None
    rule_state = FAILED
    for matched_user in email_matches:
        if matched_user.linkPrecedence == User.LinkPrecedenceChoices.primary:
            primary_user = matched_user
    for matched_user in phone_number_matches:
        # if a primary user was found in email_matches and another primary user was found in phone_number_matches, break loop
        if primary_user and matched_user.linkPrecedence == User.LinkPrecedenceChoices.primary:
            rule_state = SUCCESS
            break
    # determine which user becomes primary and which one secondary
    if rule_state == SUCCESS:
        # check which user was created earlier and set data primary accordingly 
        if primary_user.createdAt < matched_user.createdAt:
            matched_user.linkedId = primary_user
            matched_user.linkPrecedence = User.LinkPrecedenceChoices.secondary
            matched_user.save()
        else:
            primary_user.linkedId = matched_user
            primary_user.linkPrecedence = User.LinkPrecedenceChoices.secondary
            primary_user.save()
    return {'status': rule_state, 'data': primary_user}

def r04_partial_match(email_matches, phone_number_matches, email, phone_number):
    """If either email_matches or phone_number_matches is not empty, check if new information is available add an entry to DB as a secondary referring to the primary"""
    print(f"Running rule: r04_partial_match")
    
    for matched_user in email_matches:
        if matched_user.linkPrecedence == User.LinkPrecedenceChoices.primary and matched_user.email == email and matched_user.phoneNumber != phone_number:
            primary_user = matched_user
    for matched_user in phone_number_matches:
        if matched_user.linkPrecedence == User.LinkPrecedenceChoices.primary and matched_user.email != email and matched_user.phoneNumber == phone_number:
            primary_user = matched_user
    
    if not len(email_matches) or not len(phone_number_matches):
        user = User(email=email, phoneNumber=phone_number, linkPrecedence=User.LinkPrecedenceChoices.secondary, linkedId=primary_user)
        user.save()
        return {'status': SUCCESS, 'data': user}
    return {'status': FAILED, 'data': primary_user}



RECON_RULES = [r01_no_matches, r02_full_match, r03_multiple_primaries, r04_partial_match]

def recon_main(email, phone_number):
    # Get entries that match with the email
    email_matches = User.objects.filter(email=email)
    # Get entries that match with the phone_number
    phone_number_matches = User.objects.filter(phoneNumber=phone_number)
    ref_user = None
    for rule in RECON_RULES:
        res = rule(email_matches, phone_number_matches, email, phone_number)
        if res['status'] == SUCCESS:
            ref_user = res['data']
            break
    # Get new entries as primary might have changed
    if ref_user.linkPrecedence == User.LinkPrecedenceChoices.primary:
        matches = User.objects.filter(id=ref_user.id) | User.objects.filter(linkedId = ref_user.id)
    else:
        matches = User.objects.filter(id=ref_user.linkedId.id) | User.objects.filter(linkedId = ref_user.linkedId.id)
    primary_contact_id = None
    emails = []
    phone_numbers = []
    secondary_contact_ids = []
    
    for matched_user in matches:
        emails.append(matched_user.email)
        if matched_user.phoneNumber:
            phone_numbers.append(matched_user.phoneNumber)
        if matched_user.linkPrecedence == User.LinkPrecedenceChoices.primary:
            primary_contact_id = matched_user.id
        else:
            secondary_contact_ids.append(matched_user.id)
    
    return 	{
		"contact":{
			"primaryContatctId": primary_contact_id,
			"emails": list(set(emails)),
			"phoneNumbers": list(set(phone_numbers)),
			"secondaryContactIds": list(set(secondary_contact_ids))
		}
	}