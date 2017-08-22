import requests
import json
from collections import OrderedDict
from datetime import datetime
from functools import wraps


class CAKEApi(object):
    def __init__(
            self, admin_domain=None, api_key=None, secure=True,
            json_response=False):

        if admin_domain is None:
            raise TypeError('Missing Argument: admin_domain')
        self.admin_domain = admin_domain
        self.api_key = api_key
        self.protocol = 'https' if secure else 'http'
        self.json_response = json_response


    def __api_call(self, url, params, force_json=False):
        if self.api_key is None:
            raise TypeError('No API key has been set. You must initialize a '
                'CAKEApi object with an api_key or use the set_api_key() '
                'method on an existing CAKEApi object')
        elif self.json_response or force_json:
            request = requests.post(url, json=params, stream=True)
            raw_response = request.text
            json_response = json.loads(raw_response)
            try:
                _ = json_response['d']
                return raw_response
            except:
                request = requests.post(url, data=params, stream=True)
                raw_response = request.text
                return raw_response
            
        else:
            request = requests.post(url, data=params, stream=True)
            response = request.text
            return response


    def __required_params(required_list):
        def actual_decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                for item in required_list:
                    if item not in kwargs:
                        raise TypeError('Missing argument: {}'.format(item))
                else:
                    return f(*args, **kwargs)
            return wrapper
        return actual_decorator


    def __must_have_one(param_list):
        def actual_decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                if not any(i in kwargs for i in param_list):
                    raise TypeError('Please provide one of the following: '
                        '{}'. format(', '.join(param_list)))
                else:
                    return f(*args, **kwargs)
            return wrapper
        return actual_decorator


    def __if_one_then_all(param_list):
        def actual_decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                for param in param_list:
                    if (param in kwargs and not
                            all(param in kwargs for param in param_list)):
                        raise TypeError('If providing one of the following '
                            'please provide all: {}'.format(
                            ', '.join(param_list)))
                else:
                    return f(*args, **kwargs)
            return wrapper
        return actual_decorator


    @__required_params(['username', 'password'])
    def set_api_key(self, username=None, password=None):
        
        api_url = '{}://{}/api/1/get.asmx/GetAPIKey'.format(self.protocol,
            self.admin_domain)
        
        parameters = OrderedDict()
        parameters['username'] = username
        parameters['password'] = password
        
        try:
            request = requests.post(api_url, json=parameters, stream=True)
            response = json.loads(request.text)
            if response['d'] == '':
                self.api_key = None
            else:
                self.api_key = response['d'] 
        except:
            self.api_key = None


#-----------------------------ACCOUNTING------------------------------#


    @__required_params(
        ['billing_period_start_date', 'billing_period_end_date'])
    def export_advertiser_bills(
            self, billing_period_start_date, 
            billing_period_end_date, billing_cycle='all'):

        api_url = ('{}://{}/api/1/accounting.asmx/ExportAdvertiserBills'
            .format(self.protocol, self.admin_domain))

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['billing_cycle'] = billing_cycle
        parameters['billing_period_start_date'] = (
            str(billing_period_start_date))
        parameters['billing_period_end_date'] = str(billing_period_end_date)

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(
        ['billing_period_start_date', 'billing_period_end_date'])
    def export_affiliate_bills(
            self, billing_period_start_date, billing_period_end_date,
            billing_cycle='all', paid_only='FALSE', payment_type_id='0'):
        
        api_url = ('{}://{}/api/1/accounting.asmx/ExportAffiliateBills'
            .format(self.protocol, self.admin_domain))

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['billing_cycle'] = billing_cycle
        parameters['billing_period_start_date'] = (
            str(billing_period_start_date))
        parameters['billing_period_end_date'] = str(billing_period_end_date)
        parameters['paid_only'] = paid_only
        parameters['payment_type_id'] = payment_type_id

        return self.__api_call(url=api_url, params=parameters)


#------------------------------ADDEDIT--------------------------------#


    @__required_params(['advertiser_name'])
    def add_advertiser(
        self, advertiser_name, third_party_name='', account_status_id='1',
        online_signup='FALSE', signup_ip_address='', website='',
        billing_cycle_id='3', account_manager_id='0', address_street='',
        address_street2='', address_city='', address_state='',
        address_zip_code='', address_country='', notes='', tags=''):

        api_url = '{}://{}/api/1/addedit.asmx/Advertiser'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['advertiser_id'] = 0
        parameters['advertiser_name'] = advertiser_name
        parameters['third_party_name'] = third_party_name
        parameters['account_status_id'] = account_status_id
        parameters['online_signup'] = online_signup
        parameters['signup_ip_address'] = signup_ip_address
        parameters['website'] = website
        parameters['billing_cycle_id'] = billing_cycle_id
        parameters['account_manager_id'] = account_manager_id
        parameters['address_street'] = address_street
        parameters['address_street2'] = address_street2
        parameters['address_city'] = address_city
        parameters['address_state'] = address_state
        parameters['address_zip_code'] = address_zip_code
        parameters['address_country'] = address_country
        parameters['notes'] = notes
        parameters['tags'] = tags

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['affiliate_name'])
    def add_affiliate(
            self, affiliate_name, third_party_name='', account_status_id='1',
            inactive_reason_id='0', affiliate_tier_id='0',
            account_manager_id='0', hide_offers='FALSE', website='',
            tax_class='', ssn_tax_id='', vat_tax_required='FALSE',
            swift_iban='', payment_to='0', payment_fee='-1',
            payment_min_threshold='-1', currency_id='0',
            payment_setting_id='1', billing_cycle_id='3', payment_type_id='1',
            payment_type_info='', address_street='', address_street2='',
            address_city='', address_state='', address_zip_code='',
            address_country='', media_type_ids='', price_format_ids='',
            vertical_category_ids='', country_codes='', tags='',
            pixel_html='', postback_url='', postback_delay_ms='-1',
            fire_global_pixel='TRUE', date_added='', online_signup='FALSE',
            signup_ip_address='', referral_affiliate_id='0', referral_notes='',
            terms_and_conditions_agreed='TRUE', notes=''):
                
        api_url = '{}://{}/api/2/addedit.asmx/Affiliate'.format(
            self.protocol, self.admin_domain)
        
        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['affiliate_id'] = 0
        parameters['affiliate_name'] = affiliate_name
        parameters['third_party_name'] = third_party_name
        parameters['account_status_id'] = account_status_id
        parameters['inactive_reason_id'] = inactive_reason_id
        parameters['affiliate_tier_id'] = affiliate_tier_id
        parameters['account_manager_id'] = account_manager_id
        parameters['hide_offers'] = hide_offers
        parameters['website'] = website
        parameters['tax_class'] = tax_class
        parameters['ssn_tax_id'] = ssn_tax_id
        parameters['vat_tax_required'] = vat_tax_required
        parameters['swift_iban'] = swift_iban
        parameters['payment_to'] = payment_to
        parameters['payment_fee'] = payment_fee
        parameters['payment_min_threshold'] = payment_min_threshold
        parameters['currency_id'] = currency_id
        parameters['payment_setting_id'] = payment_setting_id
        parameters['billing_cycle_id'] = billing_cycle_id
        parameters['payment_type_id'] = payment_type_id
        parameters['payment_type_info'] = payment_type_info
        parameters['address_street'] = address_street
        parameters['address_street2'] = address_street2
        parameters['address_city'] = address_city
        parameters['address_state'] = address_state
        parameters['address_zip_code'] = address_zip_code
        parameters['address_country'] = address_country
        parameters['media_type_ids'] = media_type_ids
        parameters['price_format_ids'] = price_format_ids
        parameters['vertical_category_ids'] = vertical_category_ids
        parameters['country_codes'] = country_codes
        parameters['tags'] = tags
        parameters['pixel_html'] = pixel_html
        parameters['postback_url'] = postback_url
        parameters['postback_delay_ms'] = postback_delay_ms
        parameters['fire_global_pixel'] = fire_global_pixel
        parameters['date_added'] = (str(datetime.now()) if
            date_added == '' else date_added)
        parameters['online_signup'] = online_signup
        parameters['signup_ip_address'] = signup_ip_address
        parameters['referral_affiliate_id'] = referral_affiliate_id
        parameters['referral_notes'] = referral_notes
        parameters['terms_and_conditions_agreed'] = (
            terms_and_conditions_agreed)
        parameters['notes'] = notes
        
        return self.__api_call(url=api_url, params=parameters)


    @__required_params(
        ['affiliate_id', 'blacklist_reason_id', 'redirect_type'])
    @__must_have_one(['advertiser_id', 'offer_id'])
    def add_blacklist(
        self, affiliate_id, blacklist_reason_id, redirect_type, sub_id='',
        advertiser_id='0', offer_id='0', blacklist_date=datetime.now()):

        api_url = '{}://{}/api/1/addedit.asmx/Blacklist'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['blacklist_id'] = 0
        parameters['affiliate_id'] = affiliate_id
        parameters['sub_id'] = sub_id
        parameters['advertiser_id'] = advertiser_id
        parameters['offer_id'] = offer_id
        parameters['blacklist_reason_id'] = blacklist_reason_id
        parameters['redirect_type'] = redirect_type
        parameters['blacklist_date'] = str(blacklist_date)
        parameters['blacklist_date_modification_type'] = 'change'

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['buyer_name', 'account_manager_id'])
    @__if_one_then_all(['credit_type', 'credit_limit'])
    def add_buyer(
        self, buyer_name, account_manager_id, account_status_id='1',
        address_street='', address_street2='', address_city='',
        address_state='', address_zip_code='', address_country='', website='',
        billing_cycle_id='3', credit_type='unlimited', credit_limit='-1'):

        api_url = '{}://{}/api/1/addedit.asmx/Buyer'.format(self.protocol,
            self.admin_domain)
        
        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['buyer_id'] = 0
        parameters['buyer_name'] = buyer_name
        parameters['account_status_id'] = account_status_id
        parameters['account_manager_id'] = account_manager_id
        parameters['address_street'] = address_street
        parameters['address_street2'] = address_street2
        parameters['address_city'] = address_city
        parameters['address_state'] = address_state
        parameters['address_zip_code'] = address_zip_code
        parameters['address_country'] = address_country
        parameters['website'] = website
        parameters['billing_cycle_id'] = billing_cycle_id
        parameters['credit_type'] = credit_type
        parameters['credit_limit'] = credit_limit

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['buyer_id', 'vertical_id', 'buyer_contract_name'])
    def add_buyer_contract(
        self, buyer_id, vertical_id, buyer_contract_name,
        account_status_id='1', offer_id='0', replace_returns='off',
        replacements_non_returnable='off', max_return_age_days='30',
        buy_upsells='off', vintage_leads='off', min_lead_age_minutes='0',
        max_lead_age_minutes='7200', posting_wait_seconds='0',
        default_confirmation_page_link='', max_post_errors='10',
        send_alert_only='off', rank='0', email_template_id='0',
        portal_template_id='0'):

        api_url = '{}://{}/api/1/addedit.asmx/BuyerContract'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['buyer_contract_id'] = 0
        parameters['buyer_id'] = buyer_id
        parameters['vertical_id'] = vertical_id
        parameters['buyer_contract_name'] = buyer_contract_name
        parameters['account_status_id'] = account_status_id
        parameters['offer_id'] = offer_id
        parameters['replace_returns'] = replace_returns
        parameters['replacements_non_returnable'] = replacements_non_returnable
        parameters['max_return_age_days'] = max_return_age_days
        parameters['buy_upsells'] = buy_upsells
        parameters['vintage_leads'] = vintage_leads
        parameters['min_lead_age_minutes'] = min_lead_age_minutes
        parameters['max_lead_age_minutes'] = max_lead_age_minutes
        parameters['posting_wait_seconds'] = posting_wait_seconds
        parameters['default_confirmation_page_link'] = default_confirmation_page_link
        parameters['max_post_errors'] = max_post_errors
        parameters['send_alert_only'] = send_alert_only
        parameters['rank'] = rank
        parameters['email_template_id'] = email_template_id
        parameters['portal_template_id'] = portal_template_id

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['affiliate_id', 'media_type_id', 'payout'])
    @__must_have_one(['offer_id', 'offer_contract_id'])
    def add_campaign(
            self, affiliate_id, media_type_id, payout, offer_id='0',
            offer_contract_id='0', third_party_name='', account_status_id='1',
            display_link_type_id='1', expiration_date='',
            currency_id='0', paid='on', static_suppression='-1',
            paid_redirects='on', paid_upsells='on', review='off',
            auto_disposition_delay_hours='-1', redirect_offer_contract_id='0',
            redirect_404='off', clear_session_on_conversion='off',
            postback_url='', postback_delay_ms='-1',
            unique_key_hash_type='none', pixel_html='', test_link='',
            redirect_domain=''):

        if (not str(affiliate_id).isdigit() or int(affiliate_id) < 1 or 
                int(affiliate_id) > 999999999):
            raise ValueError(('affiliate_id must be an integer between 1 '
                'and 999999999'))
        if (not offer_id is None and not str(offer_id).isdigit() or
            int(offer_id) < 1 or int(offer_id) > 999999999):
            raise ValueError(('offer_id must be an integer between 1 and '
                '999999999'))
        if (not offer_contract_id is None and
            not str(offer_contract_id).isdigit()):
            raise ValueError(('offer_contract_id must be an integer between '
                '1 and 999999999'))
        if media_type_id is None:
            raise TypeError(("Missing Argument: media_type_id. Use "
                "get(item='MediaTypes') for available IDs"))
        if not str(media_type_id).isdigit() or int(media_type_id) < 1:
            raise ValueError(("media_type_id must be an integer greater than "
                "0. Use get(item='MediaTypes') for available IDs"))
        
        api_url = '{}://{}/api/3/addedit.asmx/Campaign'.format(self.protocol,
            self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['campaign_id'] = 0
        parameters['affiliate_id'] = affiliate_id
        parameters['offer_id'] = 0 if offer_id is None else offer_id
        parameters['offer_contract_id'] = (0 if offer_contract_id is None else
            offer_contract_id)
        parameters['media_type_id'] = media_type_id
        parameters['third_party_name'] = third_party_name
        parameters['account_status_id'] = account_status_id
        parameters['display_link_type_id'] = display_link_type_id
        parameters['expiration_date'] = ('2067-10-20 13:31:59.7' if
            expiration_date == '' else str(expiration_date))
        parameters['expiration_date_modification_type'] = ('do_not_change' if
            parameters['expiration_date'] == '2067-10-20 13:31:59.7' else 
            'change')
        parameters['currency_id'] = currency_id
        parameters['use_offer_contract_payout'] = 'no_change'  #doesn't do anything when creating campaign
        parameters['payout'] = payout
        parameters['payout_update_option'] = 'change'
        parameters['paid'] = paid
        parameters['static_suppression'] = static_suppression
        parameters['paid_redirects'] = paid_redirects
        parameters['paid_upsells'] = paid_upsells
        parameters['review'] = review
        parameters['auto_disposition_delay_hours'] = (
            auto_disposition_delay_hours)
        parameters['redirect_offer_contract_id'] = redirect_offer_contract_id
        parameters['redirect_404'] = redirect_404
        parameters['clear_session_on_conversion'] = (
            clear_session_on_conversion)
        parameters['postback_url'] = postback_url
        parameters['postback_delay_ms'] = postback_delay_ms
        parameters['unique_key_hash_type'] = unique_key_hash_type
        parameters['pixel_html'] = pixel_html
        parameters['test_link'] = test_link
        parameters['redirect_domain'] = redirect_domain

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['creative_id', 'creative_file_import_url'])
    def add_creative_files(
            self, creative_id, creative_file_import_url,
            is_preview_file='FALSE', replace_all_files='FALSE'):
        
        api_url = '{}://{}/api/1/addedit.asmx/CreativeFiles'.format(
            self.protocol, self.admin_domain)
        
        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['creative_id'] = creative_id
        parameters['creative_file_id'] = 0
        parameters['creative_file_import_url'] = creative_file_import_url
        parameters['is_preview_file'] = is_preview_file
        parameters['replace_all_files'] = replace_all_files

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(
        ['advertiser_id', 'vertical_id', 'offer_name', 'offer_status_id',
        'offer_type_id', 'last_touch', 'price_format_id', 'payout',
        'received', 'offer_link'])
    @__if_one_then_all(['tags', 'tags_modification_type'])
    @__if_one_then_all(
        ['allowed_media_type_ids', 'allowed_media_type_modification_type'])
    def add_offer(
            self, advertiser_id, vertical_id, offer_name, offer_status_id,
            offer_type_id, last_touch, price_format_id, payout, received,
            offer_link, third_party_name='', hidden='off',
            currency_id='0', ssl='on', click_cookie_days='30',
            impression_cookie_days='30', auto_disposition_type='none',
            auto_disposition_delay_hours='-1', redirect_offer_contract_id='0',
            redirect_404='off', redirect_domain='',
            conversions_from_whitelist_only='off',
            track_search_terms_from_non_supported_search_engines='off',
            enable_view_thru_conversions='off', click_trumps_impression='off',
            disable_click_deduplication='off',
            session_regeneration_seconds='-1',
            session_regeneration_type_id='0',
            enable_transaction_id_deduplication='off', cookie_domain='',
            postbacks_only='off', pixel_html='', postback_url='',
            postback_url_ms_delay='-1', fire_global_pixel='on',
            fire_pixel_on_non_paid_conversions='off', static_suppression='-1',
            conversion_cap_behavior='0', conversion_behavior_on_redirect='0',
            expiration_date='', offer_contract_name='',
            offer_contract_hidden='off', received_percentage='off',
            thankyou_link='', preview_link='', thumbnail_file_import_url='',
            offer_description='', restrictions='',
            advertiser_extended_terms='', testing_instructions='',
            tags_modification_type='do_not_change', tags='',
            allow_affiliates_to_create_creatives='off', unsubscribe_link='',
            from_lines='', subject_lines='',
            allowed_media_type_modification_type='do_not_change',
            allowed_media_type_ids=''):
        
        api_url = '{}://{}/api/5/addedit.asmx/Offer'.format(
            self.protocol, self.admin_domain)
        
        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['offer_id'] = 0
        parameters['advertiser_id'] = advertiser_id
        parameters['vertical_id'] = vertical_id
        parameters['offer_name'] = offer_name
        parameters['third_party_name'] = third_party_name
        parameters['hidden'] = hidden
        parameters['offer_status_id'] = offer_status_id
        parameters['offer_type_id'] = offer_type_id
        parameters['currency_id'] = currency_id
        parameters['ssl'] = ssl
        parameters['click_cookie_days'] = click_cookie_days
        parameters['impression_cookie_days'] = impression_cookie_days
        parameters['auto_disposition_type'] = auto_disposition_type
        parameters['auto_disposition_delay_hours'] = (
            auto_disposition_delay_hours)
        parameters['redirect_offer_contract_id'] = redirect_offer_contract_id
        parameters['redirect_404'] = redirect_404
        parameters['redirect_domain'] = redirect_domain
        parameters['conversions_from_whitelist_only'] = (
            conversions_from_whitelist_only)
        parameters['track_search_terms_from_non_supported_search_engines'] = (
            track_search_terms_from_non_supported_search_engines)
        parameters['enable_view_thru_conversions'] = (
            enable_view_thru_conversions)
        parameters['click_trumps_impression'] = click_trumps_impression
        parameters['disable_click_deduplication'] = (
            disable_click_deduplication)
        parameters['last_touch'] = last_touch
        parameters['session_regeneration_seconds'] = (
            session_regeneration_seconds)
        parameters['session_regeneration_type_id'] = (
            session_regeneration_type_id)
        parameters['enable_transaction_id_deduplication'] = (
            enable_transaction_id_deduplication)
        parameters['cookie_domain'] = cookie_domain
        parameters['postbacks_only'] = postbacks_only
        parameters['pixel_html'] = pixel_html
        parameters['postback_url'] = postback_url
        parameters['postback_url_ms_delay'] = postback_url_ms_delay
        parameters['fire_global_pixel'] = fire_global_pixel
        parameters['fire_pixel_on_non_paid_conversions'] = (
            fire_pixel_on_non_paid_conversions)
        parameters['static_suppression'] = static_suppression
        parameters['conversion_cap_behavior'] = conversion_cap_behavior
        parameters['conversion_behavior_on_redirect'] = (
            conversion_behavior_on_redirect)
        parameters['expiration_date'] = ('2067-10-20 13:31:59.7' if
            expiration_date == '' else str(expiration_date))
        parameters['expiration_date_modification_type'] = ('do_not_change' if
            parameters['expiration_date'] == '2067-10-20 13:31:59.7' else 'change')
        parameters['offer_contract_name'] = offer_contract_name
        parameters['offer_contract_hidden'] = offer_contract_hidden
        parameters['price_format_id'] = price_format_id
        parameters['payout_modification_type'] = 'change'
        parameters['payout'] = payout
        parameters['received_modification_type'] = 'change'
        parameters['received'] = received
        parameters['received_percentage'] = received_percentage
        parameters['offer_link'] = offer_link
        parameters['thankyou_link'] = thankyou_link
        parameters['preview_link'] = preview_link
        parameters['thumbnail_file_import_url'] = thumbnail_file_import_url
        parameters['offer_description'] = offer_description
        parameters['restrictions'] = restrictions
        parameters['advertiser_extended_terms'] = advertiser_extended_terms
        parameters['testing_instructions'] = testing_instructions
        parameters['tags_modification_type'] = tags_modification_type
        parameters['tags'] = tags
        parameters['allow_affiliates_to_create_creatives'] = (
            allow_affiliates_to_create_creatives)
        parameters['unsubscribe_link'] = unsubscribe_link
        parameters['from_lines'] = from_lines
        parameters['subject_lines'] = subject_lines
        parameters['allowed_media_type_modification_type'] = (
            allowed_media_type_modification_type)
        parameters['allowed_media_type_ids'] = allowed_media_type_ids
        
        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['advertiser_id'])
    def edit_advertiser(
        self, advertiser_id, advertiser_name='', third_party_name='',
        account_status_id='0', website='', billing_cycle_id='0',
        account_manager_id='0', address_street='', address_street2='',
        address_city='', address_state='', address_zip_code='',
        address_country='', notes='', tags=''):

        advertiser_export = self.export_advertisers(
            advertiser_id=advertiser_id, force_json=True)
        export_response = json.loads(advertiser_export)
        if export_response['d']['row_count'] == 0:
            current_notes = ''
        else:
            current_notes = (export_response['d']['advertisers'][0]
                ['notes'])

        api_url = '{}://{}/api/1/addedit.asmx/Advertiser'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['advertiser_id'] = advertiser_id
        parameters['advertiser_name'] = advertiser_name
        parameters['third_party_name'] = third_party_name
        parameters['account_status_id'] = account_status_id
        parameters['online_signup'] = 'FALSE'  #can't change on edit
        parameters['signup_ip_address'] = ''  #can't change on edit
        parameters['website'] = website
        parameters['billing_cycle_id'] = billing_cycle_id
        parameters['account_manager_id'] = account_manager_id
        parameters['address_street'] = address_street
        parameters['address_street2'] = address_street2
        parameters['address_city'] = address_city
        parameters['address_state'] = address_state
        parameters['address_zip_code'] = address_zip_code
        parameters['address_country'] = address_country
        parameters['notes'] = (current_notes if notes == '' else
            current_notes + '\n' + notes)
        parameters['tags'] = tags

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['affiliate_id'])
    def edit_affiliate(
            self, affiliate_id, affiliate_name='', third_party_name='',
            account_status_id='0', inactive_reason_id='0',
            affiliate_tier_id='0', account_manager_id='0', hide_offers='',
            website='', tax_class='', ssn_tax_id='', vat_tax_required='',
            swift_iban='', payment_to='', payment_fee='-1',
            payment_min_threshold='-1', currency_id='0',
            payment_setting_id='1', billing_cycle_id='3', payment_type_id='1',
            payment_type_info='', address_street='', address_street2='',
            address_city='', address_state='', address_zip_code='',
            address_country='', media_type_ids='', price_format_ids='',
            vertical_category_ids='', country_codes='', tags='',
            pixel_html='', postback_url='', postback_delay_ms='-1',
            fire_global_pixel='', referral_affiliate_id='0',
            referral_notes='', notes=''):
        
        affiliate_export = self.export_affiliates(
            affiliate_id=affiliate_id, force_json=True)
        export_response = json.loads(affiliate_export)
        if export_response['d']['row_count'] == 0:
            current_hide_offers = 'FALSE'
            current_vat_required = 'FALSE'
            current_payment_to = 0
            current_fire_global = 'FALSE'
            current_notes = ''
        else:
            current_hide_offers = (export_response['d']['affiliates'][0]
                ['hide_offers'])
            current_vat_required = (export_response['d']['affiliates'][0]
                ['pay_vat'])
            current_payment_to = (export_response['d']['affiliates'][0]
                ['payment_to'])
            if current_payment_to == 'Company':
                current_payment_to = 0
            else:
                current_payment_to = 1
            current_fire_global = (export_response['d']['affiliates'][0]
                ['fire_global_pixel'])
            current_notes = export_response['d']['affiliates'][0]['notes']
        
        api_url = '{}://{}/api/2/addedit.asmx/Affiliate'.format(
            self.protocol, self.admin_domain)
        
        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['affiliate_id'] = affiliate_id
        parameters['affiliate_name'] = affiliate_name
        parameters['third_party_name'] = third_party_name
        parameters['account_status_id'] = account_status_id
        parameters['inactive_reason_id'] = inactive_reason_id
        parameters['affiliate_tier_id'] = affiliate_tier_id
        parameters['account_manager_id'] = account_manager_id
        parameters['hide_offers'] = (current_hide_offers if hide_offers
            == '' else hide_offers)
        parameters['website'] = website
        parameters['tax_class'] = tax_class
        parameters['ssn_tax_id'] = ssn_tax_id
        parameters['vat_tax_required'] = (current_vat_required if
            vat_tax_required == '' else vat_tax_required)
        parameters['swift_iban'] = swift_iban
        parameters['payment_to'] = (current_payment_to if payment_to == ''
            else payment_to)
        parameters['payment_fee'] = payment_fee
        parameters['payment_min_threshold'] = payment_min_threshold
        parameters['currency_id'] = currency_id
        parameters['payment_setting_id'] = payment_setting_id
        parameters['billing_cycle_id'] = billing_cycle_id
        parameters['payment_type_id'] = payment_type_id
        parameters['payment_type_info'] = payment_type_info
        parameters['address_street'] = address_street
        parameters['address_street2'] = address_street2
        parameters['address_city'] = address_city
        parameters['address_state'] = address_state
        parameters['address_zip_code'] = address_zip_code
        parameters['address_country'] = address_country
        parameters['media_type_ids'] = media_type_ids
        parameters['price_format_ids'] = price_format_ids
        parameters['vertical_category_ids'] = vertical_category_ids
        parameters['country_codes'] = country_codes
        parameters['tags'] = tags
        parameters['pixel_html'] = pixel_html
        parameters['postback_url'] = postback_url
        parameters['postback_delay_ms'] = postback_delay_ms
        parameters['fire_global_pixel'] = (current_fire_global if
            fire_global_pixel == '' else fire_global_pixel)
        parameters['date_added'] = '2017-1-1'  #can't change on edit
        parameters['online_signup'] = 'FALSE'  #can't change on edit
        parameters['signup_ip_address'] = ''
        parameters['referral_affiliate_id'] = referral_affiliate_id
        parameters['referral_notes'] = referral_notes
        parameters['terms_and_conditions_agreed'] = 'FALSE'  #can't change on edit
        parameters['notes'] = (current_notes if notes == '' else
            current_notes + '\n' + notes)
        
        return self.__api_call(url=api_url, params=parameters)


    #Can't seem to edit an existing blacklist. Use remove_blacklist() and then add a new one

    # @__required_params(['blacklist_id'])
    # def edit_blacklist(
    #     self, blacklist_id=None, affiliate_id='0', sub_id='',
    #     advertiser_id='0', offer_id='0', blacklist_reason_id='0',
    #     redirect_type=None, blacklist_date='2067-10-20 13:31:59.7',
    #     blacklist_date_modification_type='do_not_change'):

    #     blacklist_export = self.export_blacklists(
    #         affiliate_id=affiliate_id, force_json=True)
    #     export_response = json.loads(blacklist_export)
    #     if export_response['d']['row_count'] == 0:
    #         raise ValueError('Invalid blacklist_id')
    #     current_affiliate_id = (export_response['d']['blacklists'][0]
    #         ['affiliate']['affiliate_id'])
    #     current_advertiser_id = (export_response['d']['blacklists'][0]
    #         ['advertiser']['advertiser_id'])
    #     current_offer_id = (0 if export_response['d']['blacklists'][0]
    #         ['offer'] is None else export_response['d']['blacklists'][0]
    #         ['offer']['offer_id'])
    #     current_reason_id = (export_response['d']['blacklists'][0]
    #         ['blacklist_reason']['blacklist_reason_id'])
    #     current_redirect_type = (export_response['d']['blacklists'][0]
    #         ['blacklist_type']['blacklist_type_name'])

    #     current_redirect_type = current_redirect_type.replace(
    #         '404', 'redirect_404')
    #     print current_redirect_type

    #     api_url = '{}://{}/api/1/addedit.asmx/Blacklist'.format(
    #         self.protocol, self.admin_domain)

    #     parameters = OrderedDict()
    #     parameters['api_key'] = self.api_key
    #     parameters['blacklist_id'] = 0
    #     parameters['affiliate_id'] = (current_affiliate_id if
    #         str(affiliate_id) == '0' else affiliate_id)
    #     parameters['sub_id'] = sub_id
    #     parameters['advertiser_id'] = (current_advertiser_id if
    #         str(advertiser_id) == '0' else advertiser_id)
    #     parameters['offer_id'] = (current_offer_id if
    #         str(offer_id) == '0' else offer_id)
    #     parameters['blacklist_reason_id'] = (current_reason_id if
    #         str(blacklist_reason_id) == '0' else blacklist_reason_id)
    #     parameters['redirect_type'] = (current_redirect_type if
    #         redirect_type is None else redirect_type)
    #     parameters['blacklist_date'] = str(blacklist_date)
    #     parameters['blacklist_date_modification_type'] = ('do_not_change' if
    #         blacklist_date == '2067-10-20 13:31:59.7' else 'change')

    #     return self.__api_call(url=api_url, params=parameters)


    @__required_params(['buyer_id'])
    def edit_buyer(
        self, buyer_id, buyer_name='', account_status_id='0',
        account_manager_id='0', address_street='', address_street2='',
        address_city='', address_state='', address_zip_code='',
        address_country='', website='', billing_cycle_id='0',
        credit_type='no_change', credit_limit='-1'):

        api_url = '{}://{}/api/1/addedit.asmx/Buyer'.format(self.protocol,
            self.admin_domain)
        
        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['buyer_id'] = buyer_id
        parameters['buyer_name'] = buyer_name
        parameters['account_status_id'] = account_status_id
        parameters['account_manager_id'] = account_manager_id
        parameters['address_street'] = address_street
        parameters['address_street2'] = address_street2
        parameters['address_city'] = address_city
        parameters['address_state'] = address_state
        parameters['address_zip_code'] = address_zip_code
        parameters['address_country'] = address_country
        parameters['website'] = website
        parameters['billing_cycle_id'] = billing_cycle_id
        parameters['credit_type'] = credit_type
        parameters['credit_limit'] = credit_limit

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['buyer_contract_id'])
    def edit_buyer_contract(
        self, buyer_contract_id, buyer_contract_name='',
        account_status_id='0', offer_id='0', replace_returns='no_change',
        replacements_non_returnable='no_change', max_return_age_days='-1',
        buy_upsells='no_change', vintage_leads='no_change',
        min_lead_age_minutes='-1', max_lead_age_minutes='-1',
        posting_wait_seconds='-1', default_confirmation_page_link='',
        max_post_errors='-1', send_alert_only='no_change', rank='-1',
        email_template_id='0', portal_template_id='0'):

        api_url = '{}://{}/api/1/addedit.asmx/BuyerContract'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['buyer_contract_id'] = buyer_contract_id
        parameters['buyer_id'] = 0
        parameters['vertical_id'] = 0
        parameters['buyer_contract_name'] = buyer_contract_name
        parameters['account_status_id'] = account_status_id
        parameters['offer_id'] = offer_id
        parameters['replace_returns'] = replace_returns
        parameters['replacements_non_returnable'] = replacements_non_returnable
        parameters['max_return_age_days'] = max_return_age_days
        parameters['buy_upsells'] = buy_upsells
        parameters['vintage_leads'] = vintage_leads
        parameters['min_lead_age_minutes'] = min_lead_age_minutes
        parameters['max_lead_age_minutes'] = max_lead_age_minutes
        parameters['posting_wait_seconds'] = posting_wait_seconds
        parameters['default_confirmation_page_link'] = default_confirmation_page_link
        parameters['max_post_errors'] = max_post_errors
        parameters['send_alert_only'] = send_alert_only
        parameters['rank'] = rank
        parameters['email_template_id'] = email_template_id
        parameters['portal_template_id'] = portal_template_id

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['campaign_id'])
    def edit_campaign(
            self, campaign_id, offer_contract_id='0', media_type_id='0',
            third_party_name='', account_status_id='0',
            display_link_type_id='0', expiration_date='',
            use_offer_contract_payout='no_change', payout='',
            paid='no_change', static_suppression='-1',
            paid_redirects='no_change', paid_upsells='no_change',
            review='no_change', auto_disposition_delay_hours='-1',
            redirect_offer_contract_id='0', redirect_404='no_change',
            clear_session_on_conversion='no_change', postback_url='',
            postback_delay_ms='-1', unique_key_hash_type='', pixel_html='',
            test_link='', redirect_domain=''):

        if (not str(campaign_id).isdigit() or int(campaign_id) < 1 or
            int(campaign_id) > 999999999):
            raise ValueError(('campaign_id must be an integer between 1 and '
                '999999999'))

        campaign_export = self.export_campaigns(
            campaign_id=campaign_id, force_json=True)
        export_response = json.loads(campaign_export)
        if export_response['d']['row_count'] == 0:
            current_hash = 'none'
        else:
            if export_response['d']['campaigns'][0]['pixel_info'] is None:
                current_hash = 'none'
            else:
                current_hash = (export_response['d']['campaigns'][0]
                    ['pixel_info']['hash_type']['hash_type_name'].lower()
                    .replace(' ', '_'))

        api_url = '{}://{}/api/3/addedit.asmx/Campaign'.format(self.protocol,
            self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['campaign_id'] = campaign_id
        parameters['affiliate_id'] = 0
        parameters['offer_id'] = 0
        parameters['offer_contract_id'] = offer_contract_id
        parameters['media_type_id'] = media_type_id
        parameters['third_party_name'] = third_party_name
        parameters['account_status_id'] = account_status_id
        parameters['display_link_type_id'] = display_link_type_id
        parameters['expiration_date'] = ('2067-10-20 13:31:59.7' if
            expiration_date == '' else str(expiration_date))
        parameters['expiration_date_modification_type'] = ('do_not_change' if
            expiration_date == '2067-10-20 13:31:59.7' else 'change')
        parameters['currency_id'] = 0
        parameters['payout'] = 9999.1234 if payout == '' else payout
        parameters['use_offer_contract_payout'] = (
            'off' if parameters['payout'] != 9999.1234 else 
            use_offer_contract_payout)
        parameters['payout_update_option'] = ('change' if
            parameters['payout'] != 9999.1234 or 
            use_offer_contract_payout != 'no_change' else 'do_not_change')
        parameters['paid'] = paid
        parameters['static_suppression'] = static_suppression
        parameters['paid_redirects'] = paid_redirects
        parameters['paid_upsells'] = paid_upsells
        parameters['review'] = review
        parameters['auto_disposition_delay_hours'] = (
            auto_disposition_delay_hours)
        parameters['redirect_offer_contract_id'] = redirect_offer_contract_id
        parameters['redirect_404'] = redirect_404
        parameters['clear_session_on_conversion'] = (
            clear_session_on_conversion)
        parameters['postback_url'] = postback_url
        parameters['postback_delay_ms'] = postback_delay_ms
        parameters['unique_key_hash_type'] = (current_hash if
            unique_key_hash_type == '' else unique_key_hash_type)
        parameters['pixel_html'] = pixel_html
        parameters['test_link'] = test_link
        parameters['redirect_domain'] = redirect_domain
    
        return self.__api_call(url=api_url, params=parameters)


    @__required_params(
        ['creative_id', 'creative_file_id', 'creative_file_import_url'])
    def edit_creative_files(
            self, creative_id, creative_file_id, creative_file_import_url,
            is_preview_file='FALSE', replace_all_files='FALSE'):
        
        api_url = '{}://{}/api/1/addedit.asmx/CreativeFiles'.format(
            self.protocol, self.admin_domain)
        
        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['creative_id'] = creative_id
        parameters['creative_file_id'] = creative_file_id
        parameters['creative_file_import_url'] = creative_file_import_url
        parameters['is_preview_file'] = is_preview_file
        parameters['replace_all_files'] = replace_all_files

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['offer_id'])
    @__if_one_then_all(['tags', 'tags_modification_type'])
    @__if_one_then_all(
        ['allowed_media_type_ids', 'allowed_media_type_modification_type'])
    def edit_offer(
            self, offer_id, offer_name='', vertical_id='0', third_party_name='',
            hidden='no_change', offer_status_id='0', ssl='no_change',
            click_cookie_days='-1', impression_cookie_days='-1',
            auto_disposition_type='no_change',
            auto_disposition_delay_hours='-1', redirect_offer_contract_id='0',
            redirect_404='no_change', redirect_domain='',
            conversions_from_whitelist_only='no_change',
            track_search_terms_from_non_supported_search_engines='no_change',
            enable_view_thru_conversions='no_change', 
            click_trumps_impression='no_change', 
            disable_click_deduplication='no_change', last_touch='no_change',
            session_regeneration_seconds='-1',
            session_regeneration_type_id='0',
            enable_transaction_id_deduplication='no_change', cookie_domain='',
            postbacks_only='no_change', pixel_html='', postback_url='',
            postback_url_ms_delay='-1', fire_global_pixel='no_change',
            fire_pixel_on_non_paid_conversions='no_change',
            static_suppression='-1', conversion_cap_behavior='-1',
            conversion_behavior_on_redirect='-1',
            expiration_date='', offer_contract_name='',
            offer_contract_hidden='no_change', payout='', received='',
            received_percentage='no_change', offer_link='', thankyou_link='',
            preview_link='', thumbnail_file_import_url='',
            offer_description='', restrictions='',
            advertiser_extended_terms='', testing_instructions='',
            tags_modification_type='do_not_change', tags='',
            allow_affiliates_to_create_creatives='no_change',
            unsubscribe_link='', from_lines='', subject_lines='',
            allowed_media_type_modification_type='do_not_change',
            allowed_media_type_ids=''):
        
        api_url = '{}://{}/api/5/addedit.asmx/Offer'.format(self.protocol,
            self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['offer_id'] = offer_id
        parameters['advertiser_id'] = 0
        parameters['vertical_id'] = vertical_id
        parameters['offer_name'] = offer_name
        parameters['third_party_name'] = third_party_name
        parameters['hidden'] = hidden
        parameters['offer_status_id'] = offer_status_id
        parameters['offer_type_id'] = 0
        parameters['currency_id'] = 0
        parameters['ssl'] = ssl
        parameters['click_cookie_days'] = click_cookie_days
        parameters['impression_cookie_days'] = impression_cookie_days
        parameters['auto_disposition_type'] = auto_disposition_type
        parameters['auto_disposition_delay_hours'] = (
            auto_disposition_delay_hours)
        parameters['redirect_offer_contract_id'] = redirect_offer_contract_id
        parameters['redirect_404'] = redirect_404
        parameters['redirect_domain'] = redirect_domain
        parameters['conversions_from_whitelist_only'] = (
            conversions_from_whitelist_only)
        parameters['track_search_terms_from_non_supported_search_engines'] = (
            track_search_terms_from_non_supported_search_engines)
        parameters['enable_view_thru_conversions'] = (
            enable_view_thru_conversions)
        parameters['click_trumps_impression'] = click_trumps_impression
        parameters['disable_click_deduplication'] = (
            disable_click_deduplication)
        parameters['last_touch'] = last_touch
        parameters['session_regeneration_seconds'] = (
            session_regeneration_seconds)
        parameters['session_regeneration_type_id'] = (
            session_regeneration_type_id)
        parameters['enable_transaction_id_deduplication'] = (
            enable_transaction_id_deduplication)
        parameters['cookie_domain'] = cookie_domain
        parameters['postbacks_only'] = postbacks_only
        parameters['pixel_html'] = pixel_html
        parameters['postback_url'] = postback_url
        parameters['postback_url_ms_delay'] = postback_url_ms_delay
        parameters['fire_global_pixel'] = fire_global_pixel
        parameters['fire_pixel_on_non_paid_conversions'] = (
            fire_pixel_on_non_paid_conversions)
        parameters['static_suppression'] = static_suppression
        parameters['conversion_cap_behavior'] = conversion_cap_behavior
        parameters['conversion_behavior_on_redirect'] = (
            conversion_behavior_on_redirect)
        parameters['expiration_date'] = ('2067-10-20 13:31:59.7' if
            expiration_date == '' else str(expiration_date))
        parameters['expiration_date_modification_type'] = ('do_not_change' if
            parameters['expiration_date'] == '2067-10-20 13:31:59.7' else
            'change')
        parameters['offer_contract_name'] = offer_contract_name
        parameters['offer_contract_hidden'] = offer_contract_hidden
        parameters['price_format_id'] = 0
        parameters['payout'] = 9999.1234 if payout == '' else payout
        parameters['payout_modification_type'] = ('do_not_change' if
            parameters['payout'] == 9999.1234 else 'change')
        parameters['received'] = 9999.1234 if received == '' else received
        parameters['received_modification_type'] = ('do_not_change' if
            parameters['received'] == 9999.1234 else 'change')
        parameters['received_percentage'] = received_percentage
        parameters['offer_link'] = offer_link
        parameters['thankyou_link'] = thankyou_link
        parameters['preview_link'] = preview_link
        parameters['thumbnail_file_import_url'] = thumbnail_file_import_url
        parameters['offer_description'] = offer_description
        parameters['restrictions'] = restrictions
        parameters['advertiser_extended_terms'] = advertiser_extended_terms
        parameters['testing_instructions'] = testing_instructions
        parameters['tags_modification_type'] = tags_modification_type
        parameters['tags'] = tags
        parameters['allow_affiliates_to_create_creatives'] = (
            allow_affiliates_to_create_creatives)
        parameters['unsubscribe_link'] = unsubscribe_link
        parameters['from_lines'] = from_lines
        parameters['subject_lines'] = subject_lines
        parameters['allowed_media_type_modification_type'] = (
            allowed_media_type_modification_type)
        parameters['allowed_media_type_ids'] = allowed_media_type_ids

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['blacklist_id'])
    def remove_blacklist(self, blacklist_id):

        api_url = '{}://{}/api/1/addedit.asmx/RemoveBlacklist'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self. api_key
        parameters['blacklist_id'] = blacklist_id

        return self.__api_call(url=api_url, params=parameters)


#-------------------------------EXPORT--------------------------------#


    def export_advertisers(
            self, advertiser_id='0', advertiser_name='',
            account_manager_id='0', tag_id='0', start_at_row='0',
            row_limit='0', sort_field='advertiser_id',
            sort_descending='FALSE', **kwargs):
        
        api_url = '{}://{}/api/6/export.asmx/Advertisers'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['advertiser_id'] = advertiser_id
        parameters['advertiser_name'] = advertiser_name
        parameters['account_manager_id'] = account_manager_id
        parameters['tag_id'] = tag_id
        parameters['start_at_row'] = start_at_row
        parameters['row_limit'] = row_limit
        parameters['sort_field'] = sort_field
        parameters['sort_descending'] = sort_descending

        force_json = kwargs['force_json'] if 'force_json' in kwargs else False

        return self.__api_call(
            url=api_url, params=parameters, force_json=force_json)


    def export_affiliates(
            self, affiliate_id='0', affiliate_name='', account_manager_id='0',
            tag_id='0', start_at_row='0', row_limit='0',
            sort_field='affiliate_id', sort_descending='FALSE', **kwargs):

        api_url = '{}://{}/api/5/export.asmx/Affiliates'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['affiliate_id'] = affiliate_id
        parameters['affiliate_name'] = affiliate_name
        parameters['account_manager_id'] = account_manager_id
        parameters['tag_id'] = tag_id
        parameters['start_at_row'] = start_at_row
        parameters['row_limit'] = row_limit
        parameters['sort_field'] = sort_field
        parameters['sort_descending'] = sort_descending
         
        force_json = kwargs['force_json'] if 'force_json' in kwargs else False

        return self.__api_call(
            url=api_url, params=parameters, force_json=force_json)


    def export_blacklists(
            self, affiliate_id='0', sub_id='',
            advertiser_id='0', offer_id='0', **kwargs):

        api_url = '{}://{}/api/1/export.asmx/Blacklists'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['affiliate_id'] = affiliate_id
        parameters['sub_id'] = sub_id
        parameters['advertiser_id'] = advertiser_id
        parameters['offer_id'] = offer_id

        force_json = kwargs['force_json'] if 'force_json' in kwargs else False

        return self.__api_call(
            url=api_url, params=parameters, force_json=force_json)


    def export_buyer_contracts(
            self, buyer_contract_id='0', buyer_id='0',
            vertical_id='0', buyer_contract_status_id='0'):

        api_url = '{}://{}/api/4/export.asmx/BuyerContracts'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['buyer_contract_id'] = buyer_contract_id
        parameters['buyer_id'] = buyer_id
        parameters['vertical_id'] = vertical_id
        parameters['buyer_contract_status_id'] = buyer_contract_status_id

        return self.__api_call(url=api_url, params=parameters)


    def export_buyers(self, buyer_id='0', account_status_id='0'):

        api_url = '{}://{}/api/2/export.asmx/Buyers'.format(self.protocol,
            self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['buyer_id'] = buyer_id
        parameters['account_status_id'] = account_status_id

        return self.__api_call(url=api_url, params=parameters)


    def export_campaigns(
            self, campaign_id='0', offer_id='0', affiliate_id='0',
            account_status_id='0', media_type_id='0', start_at_row='0',
            row_limit='0', sort_field='campaign_id', sort_descending='FALSE',
            **kwargs):

        api_url = '{}://{}/api/7/export.asmx/Campaigns'.format(self.protocol,
            self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['campaign_id'] = campaign_id
        parameters['offer_id'] = offer_id
        parameters['affiliate_id'] = affiliate_id
        parameters['account_status_id'] = account_status_id
        parameters['media_type_id'] = media_type_id
        parameters['start_at_row'] = start_at_row
        parameters['row_limit'] = row_limit
        parameters['sort_field'] = sort_field
        parameters['sort_descending'] = sort_descending
        
        force_json = kwargs['force_json'] if 'force_json' in kwargs else False

        return self.__api_call(
            url=api_url, params=parameters, force_json=force_json)


    @__required_params(['offer_id'])
    def export_creatives(
            self, offer_id, creative_id='0', creative_name='',
            creative_type_id='0', creative_status_id='0', start_at_row='0',
            row_limit='0', sort_field='creative_id', sort_descending='FALSE'):

        api_url = '{}://{}/api/3/export.asmx/Creatives'.format(self.protocol,
            self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['creative_id'] = creative_id
        parameters['creative_name'] = creative_name
        parameters['offer_id'] = offer_id
        parameters['creative_type_id'] = creative_type_id
        parameters['creative_status_id'] = creative_status_id
        parameters['start_at_row'] = start_at_row
        parameters['row_limit'] = row_limit
        parameters['sort_field'] = sort_field
        parameters['sort_descending'] = sort_descending

        return self.__api_call(url=api_url, params=parameters)


    def export_offers(
            self, offer_id='0', offer_name='', advertiser_id='0',
            vertical_id='0', offer_type_id='0', media_type_id='0',
            offer_status_id='0', tag_id='0', start_at_row='0', row_limit='0',
            sort_field='offer_id', sort_descending='FALSE'):

        api_url = '{}://{}/api/6/export.asmx/Offers'.format(self.protocol,
            self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['offer_id'] = offer_id
        parameters['offer_name'] = offer_name
        parameters['advertiser_id'] = advertiser_id
        parameters['vertical_id'] = vertical_id
        parameters['offer_type_id'] = offer_type_id
        parameters['media_type_id'] = media_type_id
        parameters['offer_status_id'] = offer_status_id
        parameters['tag_id'] = tag_id
        parameters['start_at_row'] = start_at_row
        parameters['row_limit'] = row_limit
        parameters['sort_field'] = sort_field
        parameters['sort_descending'] = sort_descending

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def export_pixel_log_requests(
        self, start_date, end_date, advertiser_id='0', offer_id='0', 
        converted_only='FALSE', start_at_row='0', row_limit='0',
        sort_descending='FALSE'):

        api_url = '{}://{}/api/1/export.asmx/PixelLogRequests'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['advertiser_id'] = advertiser_id
        parameters['offer_id'] = offer_id
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['converted_only'] = converted_only
        parameters['start_at_row'] = start_at_row
        parameters['row_limit'] = row_limit
        parameters['sort_descending'] = sort_descending

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['rule_id'])
    def export_rule_targets(self, rule_id):

        api_url = '{}://{}/api/3/export.asmx/RuleTargets'.format(
            self.protocol, self.admin_domain) 

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['rule_id'] = rule_id

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def export_schedules(
            self, start_date, end_date, buyer_id='0', status_id='0',
            vertical_id='0', priority_only='FALSE', active_only='FALSE'):

        api_url = '{}://{}/api/2/export.asmx/Schedules'.format(
            self.protocol, self.admin_domain) 

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['buyer_id'] = buyer_id
        parameters['status_id'] = status_id
        parameters['vertical_id'] = vertical_id
        parameters['priority_only'] = priority_only
        parameters['active_only'] = active_only

        return self.__api_call(url=api_url, params=parameters)


#--------------------------------GET----------------------------------#


    def get(self, item=None, **kwargs):
        if item is None:
            raise TypeError(('Missing argument: item. For a list of valid '
                'items please see http://{}/api/1/get.asmx'
                .format(self.admin_domain)))
        elif item not in [
                'AccountStatuses', 'Advertisers', 'AffiliateTags',
                'AffiliateTiers', 'BillingCycles', 'BlacklistReasons',
                'CapIntervals', 'CapTypes', 'Countries', 'Currencies',
                'CustomQueueStatuses', 'Departments', 'EmailTemplates',
                'ExchangeRates', 'FilterTypes', 'GetAPIKey',
                'InactiveReasons', 'Languages', 'LeadInfo', 'LeadTierGroups',
                'LinkDisplayTypes', 'MediaTypes', 'OfferStatuses',
                'OfferTypes', 'PaymentSettings', 'PaymentTypes',
                'PriceFormats', 'ResponseDispositions', 'Roles',
                'ScheduleTypes', 'SessionRegenerationTypes', 'SharedRules',
                'TrackingDomains', 'Verticals']:
            raise ValueError(('Invalid item: {}. For a list of valid items '
                'please see http://{}/api/1/get.asmx'.format(item,
                    self.admin_domain)))
            
        api_url = '{}://{}/api/1/get.asmx/{}'.format(self.protocol,
            self.admin_domain, item)
        
        parameters = {key: kwargs[key] for key in kwargs}
        parameters['api_key'] = self.api_key
        
        return self.__api_call(url=api_url, params=parameters)


#------------------------------REPORTS--------------------------------#


    @__required_params(['start_date', 'end_date'])
    def brand_advertiser_summary(
            self, start_date, end_date, brand_advertiser_id='0',
            brand_advertiser_manager_id='0', brand_advertiser_tag_id='0',
            event_id='0', event_type='all'):

        api_url = '{}://{}/api/3/reports.asmx/BrandAdvertiserSummary'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['brand_advertiser_id'] = brand_advertiser_id
        parameters['brand_advertiser_manager_id'] = (
            brand_advertiser_manager_id)
        parameters['brand_advertiser_tag_id'] = brand_advertiser_tag_id
        parameters['event_id'] = event_id
        parameters['event_type'] = event_type

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def campaign_summary(
            self, start_date, end_date, campaign_id='0',
            source_affiliate_id='0', subid_id='', site_offer_id='0',
            source_affiliate_tag_id='0', site_offer_tag_id='0',
            source_affiliate_manager_id='0', brand_advertiser_manager_id='0',
            event_id='0', event_type='all'):

        api_url = '{}://{}/api/5/reports.asmx/CampaignSummary'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['campaign_id'] = campaign_id
        parameters['source_affiliate_id'] = source_affiliate_id
        parameters['subid_id'] = subid_id
        parameters['site_offer_id'] = site_offer_id
        parameters['source_affiliate_tag_id'] = source_affiliate_tag_id
        parameters['site_offer_tag_id'] = site_offer_tag_id
        parameters['source_affiliate_manager_id'] = source_affiliate_manager_id
        parameters['brand_advertiser_manager_id'] = brand_advertiser_manager_id
        parameters['event_id'] = event_id
        parameters['event_type'] = event_type

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def clicks(
            self, start_date, end_date, affiliate_id='0', advertiser_id='0',
            offer_id='0', campaign_id='0', creative_id='0',
            price_format_id='0', include_duplicates='FALSE',
            include_tests='FALSE', start_at_row='0', row_limit='0'):

        api_url = '{}://{}/api/12/reports.asmx/Clicks'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['affiliate_id'] = affiliate_id
        parameters['advertiser_id'] = advertiser_id
        parameters['offer_id'] = offer_id
        parameters['campaign_id'] = campaign_id
        parameters['creative_id'] = creative_id
        parameters['price_format_id'] = price_format_id
        parameters['include_duplicates'] = include_duplicates
        parameters['include_tests'] = include_tests
        parameters['start_at_row'] = start_at_row
        parameters['row_limit'] = row_limit

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['changes_since'])
    def conversion_changes(
            self, changes_since, include_new_conversions='FALSE',
            affiliate_id='0', advertiser_id='0', offer_id='0',
            campaign_id='0', creative_id='0', include_tests='FALSE',
            start_at_row='0', row_limit='0', sort_field='conversion_id',
            sort_descending='FALSE'):

        api_url = '{}://{}/api/10/reports.asmx/ConversionChanges'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['changes_since'] = str(changes_since)
        parameters['include_new_conversions'] = include_new_conversions
        parameters['affiliate_id'] = affiliate_id
        parameters['advertiser_id'] = advertiser_id
        parameters['offer_id'] = offer_id
        parameters['campaign_id'] = campaign_id
        parameters['creative_id'] = creative_id
        parameters['include_tests'] = include_tests
        parameters['start_at_row'] = start_at_row
        parameters['row_limit'] = row_limit
        parameters['sort_field'] = sort_field
        parameters['sort_descending'] = sort_descending

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def conversions(
            self, start_date, end_date, event_type='all', event_id='0',
            source_affiliate_id='0', brand_advertiser_id='0', channel_id='0',
            site_offer_id='0', site_offer_contract_id='0',
            source_affiliate_tag_id='0', brand_advertiser_tag_id='0',
            site_offer_tag_id='0', campaign_id='0', creative_id='0',
            price_format_id='0', source_type='all',
            payment_percentage_filter='both', disposition_type='all',
            disposition_id='0', source_affiliate_billing_status='all',
            brand_advertiser_billing_status='all', test_filter='non_tests',
            start_at_row='0', row_limit='0',
            sort_field='event_conversion_date', sort_descending='FALSE'):

        api_url = '{}://{}/api/17/reports.asmx/EventConversions'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['event_type'] = event_type
        parameters['event_id'] = event_id
        parameters['source_affiliate_id'] = source_affiliate_id
        parameters['brand_advertiser_id'] = brand_advertiser_id
        parameters['channel_id'] = channel_id
        parameters['site_offer_id'] = site_offer_id
        parameters['site_offer_contract_id'] = site_offer_contract_id
        parameters['source_affiliate_tag_id'] = source_affiliate_tag_id
        parameters['brand_advertiser_tag_id'] = brand_advertiser_tag_id
        parameters['site_offer_tag_id'] = site_offer_tag_id
        parameters['campaign_id'] = campaign_id
        parameters['creative_id'] = creative_id
        parameters['price_format_id'] = price_format_id
        parameters['source_type'] = source_type
        parameters['payment_percentage_filter'] = payment_percentage_filter
        parameters['disposition_type'] = disposition_type
        parameters['disposition_id'] = disposition_id
        parameters['source_affiliate_billing_status'] = (
            source_affiliate_billing_status)
        parameters['brand_advertiser_billing_status'] = (
            brand_advertiser_billing_status)
        parameters['test_filter'] = test_filter
        parameters['start_at_row'] = start_at_row
        parameters['row_limit'] = row_limit
        parameters['sort_field'] = sort_field
        parameters['sort_descending'] = sort_descending

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    @__must_have_one(['site_offer_id', 'campaign_id'])
    def creative_summary(
            self, start_date, end_date, site_offer_id='0', campaign_id='0',
            event_id='0', event_type='all'):

        api_url = '{}://{}/api/3/reports.asmx/CreativeSummary'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['site_offer_id'] = (0 if site_offer_id is None else
            site_offer_id)
        parameters['campaign_id'] = (0 if campaign_id is None else
            campaign_id)
        parameters['event_id'] = event_id
        parameters['event_type'] = event_type

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def daily_summary(
            self, start_date, end_date, source_affiliate_id='0',
            brand_advertiser_id='0', site_offer_id='0', vertical_id='0',
            campaign_id='0', creative_id='0', account_manager_id='0',
            include_tests='FALSE'):

        api_url = '{}://{}/api/2/reports.asmx/DailySummaryExport'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['source_affiliate_id'] = source_affiliate_id
        parameters['brand_advertiser_id'] = brand_advertiser_id
        parameters['site_offer_id'] = site_offer_id
        parameters['vertical_id'] = vertical_id
        parameters['campaign_id'] = campaign_id
        parameters['creative_id'] = creative_id
        parameters['account_manager_id'] = account_manager_id
        parameters['include_tests'] = include_tests

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def leads_by_buyer(
            self, start_date, end_date, vertical_id='0', buyer_id='0',
            buyer_contract_id='0', status_id='0', sub_status_id='0',
            start_at_row='0', row_limit='0', sort_field='transaction_date',
            sort_descending='FALSE'):

        api_url = '{}://{}/api/4/reports.asmx/LeadsByBuyer'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['vertical_id'] = vertical_id
        parameters['buyer_id'] = buyer_id
        parameters['buyer_contract_id'] = buyer_contract_id
        parameters['status_id'] = status_id
        parameters['sub_status_id'] = sub_status_id
        parameters['start_at_row'] = start_at_row
        parameters['row_limit'] = row_limit
        parameters['sort_field'] = sort_field
        parameters['sort_descending'] = sort_descending

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def leads_by_affiliate(
            self, start_date, end_date, affiliate_id='0', contact_id='0'):

        api_url = '{}://{}/api/1/reports.asmx/LeadsByAffiliateExport'.format(
            self.protocol, self.admin_domain) 

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['affiliate_id'] = affiliate_id
        parameters['contact_id'] = contact_id

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def lite_clicks_advertiser_summary(
            self, start_date, end_date, advertiser_id='0',
            advertiser_manager_id='0', advertiser_tag_id='0', event_id='0',
            revenue_filter='conversions_and_events'):

        api_url = ('{}://{}/api/1/reports_lite_clicks.asmx/AdvertiserSummary'
            .format(self.protocol, self.admin_domain))

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['advertiser_id'] = advertiser_id
        parameters['advertiser_manager_id'] = advertiser_manager_id
        parameters['advertiser_tag_id'] = advertiser_tag_id
        parameters['event_id'] = event_id
        parameters['revenue_filter'] = revenue_filter

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def lite_clicks_affiliate_summary(
            self, start_date, end_date, affiliate_id='0',
            affiliate_manager_id='0', affiliate_tag_id='0', offer_tag_id='0',
            event_id='0', revenue_filter='conversions_and_events'):

        api_url = ('{}://{}/api/1/reports_lite_clicks.asmx/AffiliateSummary'
            .format(self.protocol, self.admin_domain))

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['affiliate_id'] = affiliate_id
        parameters['affiliate_manager_id'] = affiliate_manager_id
        parameters['affiliate_tag_id'] = affiliate_tag_id
        parameters['offer_tag_id'] = offer_tag_id
        parameters['event_id'] = event_id
        parameters['revenue_filter'] = revenue_filter

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def lite_clicks_campaign_summary(
            self, start_date, end_date, affiliate_id='0', subaffiliate_id='',
            affiliate_tag_id='0', offer_id='0', offer_tag_id='0',
            campaign_id='0', event_id='0',
            revenue_filter='conversions_and_events'):
        
        api_url = ('{}://{}/api/2/reports_lite_clicks.asmx/CampaignSummary'
            .format(self.protocol, self.admin_domain))
        
        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['affiliate_id'] = affiliate_id
        parameters['subaffiliate_id'] = subaffiliate_id
        parameters['affiliate_tag_id'] = affiliate_tag_id
        parameters['offer_id'] = offer_id
        parameters['offer_tag_id'] = offer_tag_id
        parameters['campaign_id'] = campaign_id
        parameters['event_id'] = event_id
        parameters['revenue_filter'] = revenue_filter
        
        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def lite_clicks_daily_summary(
            self, start_date, end_date, affiliate_id='0', advertiser_id='0',
            offer_id='0', vertical_id='0', campaign_id='0', creative_id='0',
            account_manager_id='0', include_tests='FALSE'):

        api_url = ('{}://{}/api/1/reports_lite_clicks.asmx/DailySummaryExport'
            .format(self.protocol, self.admin_domain))

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['affiliate_id'] = affiliate_id
        parameters['advertiser_id'] = advertiser_id
        parameters['offer_id'] = offer_id
        parameters['vertical_id'] = vertical_id
        parameters['campaign_id'] = campaign_id
        parameters['creative_id'] = creative_id
        parameters['account_manager_id'] = account_manager_id
        parameters['include_tests'] = include_tests

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def lite_clicks_offer_summary(
            self, start_date, end_date, advertiser_id='0',
            advertiser_manager_id='0', offer_id='0', offer_tag_id='0',
            affiliate_tag_id='0', event_id='0',
            revenue_filter='conversions_and_events'):

        api_url = ('{}://{}/api/1/reports_lite_clicks.asmx/OfferSummary'
            .format(self.protocol, self.admin_domain))

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['advertiser_id'] = advertiser_id
        parameters['advertiser_manager_id'] = advertiser_manager_id
        parameters['offer_id'] = offer_id
        parameters['offer_tag_id'] = offer_tag_id
        parameters['affiliate_tag_id'] = affiliate_tag_id
        parameters['event_id'] = event_id
        parameters['revenue_filter'] = revenue_filter

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date', 'source_affiliate_id'])
    def lite_clicks_sub_id_summary(
            self, start_date, end_date, source_affiliate_id, site_offer_id='0',
            campaign_id='0', sub_id='NULL', event_id='0',
            revenue_filter='conversions_and_events'):

        api_url = ('{}://{}/api/2/reports_lite_clicks.asmx/SubIDSummary'
            .format(self.protocol, self.admin_domain))

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['source_affiliate_id'] = source_affiliate_id
        parameters['site_offer_id'] = site_offer_id
        parameters['campaign_id'] = campaign_id
        parameters['sub_id'] = sub_id
        parameters['event_id'] = event_id
        parameters['revenue_filter'] = revenue_filter

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def login_export(self, start_date, end_date, role_id='0'):

        api_url = '{}://{}/api/1/reports.asmx/LoginExport'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['role_id'] = role_id

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def order_details(
        self, start_date, end_date, affiliate_id='0', conversion_id='0',
        order_id='', start_at_row='0', row_limit='0', sort_field='order_id',
        sort_descending='FALSE'):

        api_url = '{}://{}/api/1/reports.asmx/OrderDetails'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['affiliate_id'] = affiliate_id
        parameters['conversion_id'] = conversion_id
        parameters['order_id'] = order_id
        parameters['start_at_row'] = start_at_row
        parameters['row_limit'] = row_limit
        parameters['sort_field'] = sort_field
        parameters['sort_descending'] = sort_descending

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def site_offer_summary(
            self, start_date, end_date, brand_advertiser_id='0',
            brand_advertiser_manager_id='0', site_offer_id='0',
            site_offer_tag_id='0', source_affiliate_tag_id='0', event_id='0',
            event_type='all'):

        api_url = '{}://{}/api/4/reports.asmx/SiteOfferSummary'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['brand_advertiser_id'] = brand_advertiser_id
        parameters['brand_advertiser_manager_id'] = (
            brand_advertiser_manager_id)
        parameters['site_offer_id'] = site_offer_id
        parameters['site_offer_tag_id'] = site_offer_tag_id
        parameters['source_affiliate_tag_id'] = source_affiliate_tag_id
        parameters['event_id'] = event_id
        parameters['event_type'] = event_type

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date'])
    def source_affiliate_summary(
            self, start_date, end_date, source_affiliate_id='0',
            source_affiliate_manager_id='0', source_affiliate_tag_id='0',
            site_offer_tag_id='0', event_id='0', event_type='all'):

        api_url = '{}://{}/api/3/reports.asmx/SourceAffiliateSummary'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['source_affiliate_id'] = source_affiliate_id
        parameters['source_affiliate_manager_id'] = (
            source_affiliate_manager_id)
        parameters['source_affiliate_tag_id'] = source_affiliate_tag_id
        parameters['site_offer_tag_id'] = site_offer_tag_id
        parameters['event_id'] = event_id
        parameters['event_type'] = event_type

        return self.__api_call(url=api_url, params=parameters)


    @__required_params(['start_date', 'end_date', 'source_affiliate_id'])
    def sub_id_summary(
            self, start_date, end_date, source_affiliate_id, site_offer_id='0',
            event_id='0', revenue_filter='conversions_and_events'):

        api_url = '{}://{}/api/1/reports.asmx/SubIDSummary'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)
        parameters['source_affiliate_id'] = source_affiliate_id
        parameters['site_offer_id'] = site_offer_id
        parameters['event_id'] = event_id
        parameters['revenue_filter'] = revenue_filter

        return self.__api_call(url=api_url, params=parameters)



    @__required_params(['start_date', 'end_date'])
    def traffic_export(self, start_date, end_date):

        api_url = '{}://{}/api/1/reports.asmx/TrafficExport'.format(
            self.protocol, self.admin_domain)

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['start_date'] = str(start_date)
        parameters['end_date'] = str(end_date)

        return self.__api_call(url=api_url, params=parameters)


#------------------------------TRACK--------------------------------#


    @__required_params(['offer_id'])
    @__must_have_one(['conversion_id', 'request_session_id', 'transaction_id'])
    @__if_one_then_all(('payout', 'add_to_existing_payout'))
    @__if_one_then_all(('received', 'received_option'))
    def update_conversion(
            self, offer_id, conversion_id='0', request_session_id='0',
            transaction_id='', payout='', add_to_existing_payout='TRUE',
            received='', received_option='no_change',
            disposition_type='no_change', disposition_id='0',
            update_revshare_payout='FALSE',
            effective_date_option='conversion_date', custom_date='',
            note_to_append='', disallow_on_billing_status='ignore'):

        if (effective_date_option == 'custom' and
                custom_date == ''):
            raise TypeError('Missing argument: custom_date')

        api_url = '{}://{}/api/4/track.asmx/UpdateConversion'.format(
            self.protocol, self.admin_domain) 

        parameters = OrderedDict()
        parameters['api_key'] = self.api_key
        parameters['offer_id'] = offer_id
        parameters['conversion_id'] = conversion_id
        parameters['request_session_id'] = request_session_id
        parameters['transaction_id'] = transaction_id
        parameters['payout'] = 0 if payout == '' else payout
        parameters['add_to_existing_payout'] = add_to_existing_payout
        parameters['received'] = 0 if received == '' else received
        parameters['received_option'] = received_option
        parameters['disposition_type'] = disposition_type
        parameters['disposition_id'] = disposition_id
        parameters['update_revshare_payout'] = update_revshare_payout
        parameters['effective_date_option'] = effective_date_option
        parameters['custom_date'] = ('2067-10-20 13:31:59.7' if
            custom_date == '' else str(custom_date))
        parameters['note_to_append'] = note_to_append
        parameters['disallow_on_billing_status'] = disallow_on_billing_status

        return self.__api_call(url=api_url, params=parameters)




